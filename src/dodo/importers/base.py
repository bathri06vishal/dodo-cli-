from __future__ import annotations

import json
import shutil
from pathlib import Path

from dodo.config import DodoConfig
from dodo.importers.json_log import read_json_log
from dodo.importers.rosbag import read_rosbag
from dodo.models import ImportedMessage, ImportSummary, SensorInfo
from dodo.project import read_json, write_json
from dodo.sensor_detection import infer_modality, sensor_name


def import_log(source: Path, project_root: Path, config: DodoConfig) -> ImportSummary:
    if not source.exists():
        raise FileNotFoundError(f"Log file does not exist: {source}")

    raw_target = project_root / config.raw_dir / source.name
    if source.resolve() != raw_target.resolve():
        shutil.copy2(source, raw_target)

    messages = _read_messages(source)
    dataset_root = project_root / config.dataset_dir
    extracted = [_extract_message(message, dataset_root, index) for index, message in enumerate(messages)]
    _write_import(project_root, source, extracted)
    summary = _summarize(source, extracted)
    _update_manifest(project_root, source, summary)
    return summary


def _read_messages(source: Path) -> list[ImportedMessage]:
    suffix = source.suffix.lower()
    if suffix in {".json", ".jsonl", ".mock"}:
        return read_json_log(source)
    return read_rosbag(source)


def _extract_message(message: ImportedMessage, dataset_root: Path, index: int) -> ImportedMessage:
    modality = message.modality if message.modality != "unknown" else infer_modality(message.topic)
    name = sensor_name(message.topic)
    payload = dict(message.payload)
    file_path = message.file_path

    if modality == "camera":
        image_name = payload.get("file") or payload.get("path") or f"{name}_{index:08d}.json"
        path = dataset_root / "data" / "images" / Path(str(image_name)).name
        if "bytes" in payload:
            path.write_bytes(bytes(payload["bytes"]))
        else:
            write_json(path, payload)
        file_path = str(path.relative_to(dataset_root))
    elif modality == "imu":
        path = dataset_root / "data" / "imu" / f"{name}_{index:08d}.json"
        write_json(path, payload)
        file_path = str(path.relative_to(dataset_root))
    elif modality == "lidar":
        path = dataset_root / "data" / "lidar" / f"{name}_{index:08d}.json"
        write_json(path, payload)
        file_path = str(path.relative_to(dataset_root))
    elif modality == "action":
        path = dataset_root / "data" / "actions" / f"{name}_{index:08d}.json"
        write_json(path, payload)
        file_path = str(path.relative_to(dataset_root))

    return ImportedMessage(
        timestamp=message.timestamp,
        topic=message.topic,
        modality=modality,
        payload=payload,
        file_path=file_path,
    )


def _write_import(project_root: Path, source: Path, messages: list[ImportedMessage]) -> None:
    import_path = project_root / ".dodo" / f"{source.stem}.messages.jsonl"
    import_path.parent.mkdir(parents=True, exist_ok=True)
    import_path.write_text("\n".join(message.model_dump_json() for message in messages) + "\n")


def _summarize(source: Path, messages: list[ImportedMessage]) -> ImportSummary:
    by_topic: dict[str, list[ImportedMessage]] = {}
    for message in messages:
        by_topic.setdefault(message.topic, []).append(message)

    sensors = []
    for topic, topic_messages in sorted(by_topic.items()):
        start = min(message.timestamp for message in topic_messages)
        end = max(message.timestamp for message in topic_messages)
        duration = max(end - start, 0.0)
        frequency = (len(topic_messages) - 1) / duration if duration > 0 and len(topic_messages) > 1 else None
        sensors.append(
            SensorInfo(
                name=sensor_name(topic),
                topic=topic,
                modality=topic_messages[0].modality,
                frequency_hz=frequency,
                message_count=len(topic_messages),
            )
        )

    timestamps = [message.timestamp for message in messages]
    return ImportSummary(
        source=str(source),
        total_messages=len(messages),
        sensors=sensors,
        start_time=min(timestamps) if timestamps else None,
        end_time=max(timestamps) if timestamps else None,
    )


def _update_manifest(project_root: Path, source: Path, summary: ImportSummary) -> None:
    manifest_path = project_root / ".dodo" / "manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {"imports": []}
    imports = [entry for entry in manifest.get("imports", []) if entry.get("source") != str(source)]
    imports.append(summary.model_dump())
    manifest["imports"] = imports
    write_json(manifest_path, manifest)

