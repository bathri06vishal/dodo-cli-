from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class SensorTopic(BaseModel):
    name: str
    modality: str
    topic: str
    frequency_hz: float | None = None


class DodoConfig(BaseModel):
    dataset_name: str
    task: str = "navigation"
    version: str = "0.1.0"
    raw_dir: str = "raw"
    dataset_dir: str = "dataset"
    sensors: list[SensorTopic] = Field(default_factory=list)

    @property
    def dataset_path_name(self) -> Path:
        return Path(self.dataset_dir)

