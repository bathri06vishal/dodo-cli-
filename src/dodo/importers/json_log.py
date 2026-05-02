from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dodo.models import ImportedMessage
from dodo.sensor_detection import infer_modality


def read_json_log(path: Path) -> list[ImportedMessage]:
    text = path.read_text().strip()
    if not text:
        return []

    if path.suffix.lower() == ".jsonl":
        records = [json.loads(line) for line in text.splitlines() if line.strip()]
    else:
        parsed = json.loads(text)
        records = parsed.get("messages", parsed) if isinstance(parsed, dict) else parsed

    return [_record_to_message(record) for record in records]


def _record_to_message(record: dict[str, Any]) -> ImportedMessage:
    timestamp = record.get("timestamp", record.get("time", record.get("t")))
    topic = record.get("topic", record.get("sensor", "unknown"))
    payload = record.get("payload", record.get("data", {}))
    modality = record.get("modality") or record.get("type") or infer_modality(topic)

    if timestamp is None:
        raise ValueError(f"Missing timestamp in record: {record}")
    if not isinstance(payload, dict):
        payload = {"value": payload}

    return ImportedMessage(
        timestamp=float(timestamp),
        topic=str(topic),
        modality=modality if modality in {"camera", "imu", "lidar", "action"} else "unknown",
        payload=payload,
    )

