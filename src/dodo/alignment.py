from __future__ import annotations

from dodo.models import AlignedFrame, ImportedMessage


def align_messages(messages: list[ImportedMessage]) -> list[AlignedFrame]:
    cameras = sorted([message for message in messages if message.modality == "camera"], key=lambda item: item.timestamp)
    base = cameras or sorted(messages, key=lambda item: item.timestamp)
    imu = sorted([message for message in messages if message.modality == "imu"], key=lambda item: item.timestamp)
    lidar = sorted([message for message in messages if message.modality == "lidar"], key=lambda item: item.timestamp)
    actions = sorted([message for message in messages if message.modality == "action"], key=lambda item: item.timestamp)

    frames = []
    for message in base:
        nearest_imu = nearest(message.timestamp, imu)
        nearest_lidar = nearest(message.timestamp, lidar)
        nearest_action = nearest(message.timestamp, actions)
        camera_path = message.file_path if message.modality == "camera" else nearest(message.timestamp, cameras).file_path if cameras else None

        frames.append(
            AlignedFrame(
                timestamp=message.timestamp,
                camera=camera_path,
                imu=_payload_or_path(nearest_imu),
                lidar=_payload_or_path(nearest_lidar),
                action=_payload_or_path(nearest_action),
            )
        )
    return frames


def nearest(timestamp: float, messages: list[ImportedMessage]) -> ImportedMessage | None:
    if not messages:
        return None
    return min(messages, key=lambda message: abs(message.timestamp - timestamp))


def _payload_or_path(message: ImportedMessage | None) -> object | None:
    if message is None:
        return None
    if message.modality in {"camera", "lidar"} and message.file_path:
        return message.file_path
    value = message.payload.get("value")
    if value is not None:
        return value
    if message.modality == "imu":
        linear_acceleration = message.payload.get("linear_acceleration")
        angular_velocity = message.payload.get("angular_velocity")
        if linear_acceleration is not None or angular_velocity is not None:
            return {
                "linear_acceleration": linear_acceleration,
                "angular_velocity": angular_velocity,
            }
    if message.modality == "action":
        action = message.payload.get("action") or message.payload.get("command")
        if action is not None:
            return action
    return message.payload

