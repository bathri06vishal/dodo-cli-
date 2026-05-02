from __future__ import annotations

from pathlib import Path

from dodo.config import DodoConfig
from dodo.models import Metadata, SensorInfo, ValidationReport
from dodo.project import load_config


def validate_dataset(project_root: Path) -> ValidationReport:
    errors: list[str] = []
    config = load_config(project_root)
    dataset_root = project_root / config.dataset_dir
    metadata_root = dataset_root / "metadata"

    for directory in ["data/images", "data/imu", "data/lidar", "metadata"]:
        if not (dataset_root / directory).exists():
            errors.append(f"Missing directory: {dataset_root / directory}")

    metadata = _load_metadata(metadata_root / "metadata.json", errors)
    sensors = _load_sensors(metadata_root / "sensors.json", errors)
    if not (metadata_root / "episodes.json").exists():
        errors.append(f"Missing file: {metadata_root / 'episodes.json'}")

    if metadata:
        if metadata.number_of_frames != len(metadata.frames):
            errors.append("metadata.json number_of_frames does not match frames length")
        for index, frame in enumerate(metadata.frames):
            if frame.camera and not (dataset_root / frame.camera).exists():
                errors.append(f"Frame {index} references missing camera file: {frame.camera}")
            if isinstance(frame.lidar, str) and not (dataset_root / frame.lidar).exists():
                errors.append(f"Frame {index} references missing lidar file: {frame.lidar}")
        if sensors and sorted(metadata.sensors_used) != sorted(sensor.name for sensor in sensors):
            errors.append("metadata.json sensors_used does not match sensors.json")

    return ValidationReport(valid=not errors, errors=errors)


def _load_metadata(path: Path, errors: list[str]) -> Metadata | None:
    if not path.exists():
        errors.append(f"Missing file: {path}")
        return None
    try:
        return Metadata.model_validate_json(path.read_text())
    except Exception as exc:
        errors.append(f"Invalid metadata.json: {exc}")
        return None


def _load_sensors(path: Path, errors: list[str]) -> list[SensorInfo]:
    if not path.exists():
        errors.append(f"Missing file: {path}")
        return []
    try:
        data = path.read_text()
        return [SensorInfo.model_validate(item) for item in __import__("json").loads(data)]
    except Exception as exc:
        errors.append(f"Invalid sensors.json: {exc}")
        return []

