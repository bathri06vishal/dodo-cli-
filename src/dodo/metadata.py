from __future__ import annotations

from pathlib import Path

from dodo.alignment import align_messages
from dodo.config import DodoConfig
from dodo.models import Episode, ImportedMessage, Metadata, SensorInfo
from dodo.project import read_json, write_json
from dodo.sensor_detection import sensor_name


def generate_metadata(project_root: Path, config: DodoConfig) -> Metadata:
    messages = _load_imported_messages(project_root)
    frames = align_messages(messages)
    sensors = _sensors(messages)
    timestamps = [message.timestamp for message in messages]
    start = min(timestamps) if timestamps else 0.0
    end = max(timestamps) if timestamps else 0.0
    duration = max(end - start, 0.0)

    metadata = Metadata(
        dataset_name=config.dataset_name,
        sensors_used=[sensor.name for sensor in sensors],
        fps=_fps(frames),
        frequency={sensor.name: sensor.frequency_hz for sensor in sensors},
        duration=duration,
        number_of_frames=len(frames),
        task=config.task,
        frames=frames,
    )
    episode = Episode(
        id="episode_0000",
        start_time=start,
        end_time=end,
        duration=duration,
        number_of_frames=len(frames),
    )

    metadata_root = project_root / config.dataset_dir / "metadata"
    write_json(metadata_root / "metadata.json", metadata.model_dump(mode="json"))
    write_json(metadata_root / "sensors.json", [sensor.model_dump(mode="json") for sensor in sensors])
    write_json(metadata_root / "episodes.json", [episode.model_dump(mode="json")])
    return metadata


def _load_imported_messages(project_root: Path) -> list[ImportedMessage]:
    dodo_root = project_root / ".dodo"
    messages: list[ImportedMessage] = []
    for path in sorted(dodo_root.glob("*.messages.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                messages.append(ImportedMessage.model_validate_json(line))
    return sorted(messages, key=lambda message: message.timestamp)


def _sensors(messages: list[ImportedMessage]) -> list[SensorInfo]:
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
                modality=topic_messages[0].modality,
                topic=topic,
                frequency_hz=frequency,
                message_count=len(topic_messages),
            )
        )
    return sensors


def _fps(frames: list) -> float | None:
    if len(frames) < 2:
        return None
    duration = frames[-1].timestamp - frames[0].timestamp
    if duration <= 0:
        return None
    return (len(frames) - 1) / duration


def metadata_exists(project_root: Path, config: DodoConfig) -> bool:
    metadata_root = project_root / config.dataset_dir / "metadata"
    return all((metadata_root / name).exists() for name in ["metadata.json", "sensors.json", "episodes.json"])


def read_metadata(project_root: Path, config: DodoConfig) -> dict:
    return read_json(project_root / config.dataset_dir / "metadata" / "metadata.json")

