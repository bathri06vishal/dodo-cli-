from __future__ import annotations

from pathlib import Path
from typing import Any

from dodo.models import ImportedMessage
from dodo.sensor_detection import infer_modality


def read_rosbag(path: Path) -> list[ImportedMessage]:
    try:
        from rosbags.highlevel import AnyReader
    except ImportError as exc:
        raise RuntimeError(
            "ROS bag import requires the optional `rosbags` dependency. "
            "Install with `pip install 'dodo-robotics[ros]'`."
        ) from exc

    messages: list[ImportedMessage] = []
    with AnyReader([path]) as reader:
        connections = list(reader.connections)
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            message = reader.deserialize(rawdata, connection.msgtype)
            seconds = timestamp / 1_000_000_000
            messages.append(
                ImportedMessage(
                    timestamp=seconds,
                    topic=connection.topic,
                    modality=infer_modality(connection.topic, connection.msgtype),
                    payload=_message_to_payload(message),
                )
            )
    return messages


def _message_to_payload(message: Any) -> dict[str, Any]:
    if hasattr(message, "__dict__"):
        return {key: _jsonable(value) for key, value in vars(message).items() if not key.startswith("_")}
    return {"value": _jsonable(message)}


def _jsonable(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return {"byte_count": len(value)}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "tolist"):
        return value.tolist()
    if hasattr(value, "__dict__"):
        return {key: _jsonable(item) for key, item in vars(value).items() if not key.startswith("_")}
    return str(value)

