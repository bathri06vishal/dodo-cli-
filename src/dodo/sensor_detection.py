from __future__ import annotations

import re

from dodo.models import Modality


def infer_modality(topic: str, msgtype: str | None = None) -> Modality:
    value = f"{topic} {msgtype or ''}".lower()
    if any(token in value for token in ["image", "camera", "compressedimage"]):
        return "camera"
    if "imu" in value:
        return "imu"
    if any(token in value for token in ["lidar", "laser", "pointcloud", "scan"]):
        return "lidar"
    if any(token in value for token in ["cmd_vel", "action", "command", "twist", "control"]):
        return "action"
    return "unknown"


def sensor_name(topic: str) -> str:
    name = topic.strip("/").replace("/", "_") or "unknown"
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", name)
    return name.lower()

