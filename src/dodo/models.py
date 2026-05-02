from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Modality = Literal["camera", "imu", "lidar", "action", "unknown"]


class SensorInfo(BaseModel):
    name: str
    modality: Modality
    topic: str
    frequency_hz: float | None = None
    message_count: int = 0


class ImportedMessage(BaseModel):
    timestamp: float
    topic: str
    modality: Modality
    payload: dict[str, Any] = Field(default_factory=dict)
    file_path: str | None = None


class ImportSummary(BaseModel):
    source: str
    total_messages: int
    sensors: list[SensorInfo]
    start_time: float | None = None
    end_time: float | None = None


class AlignedFrame(BaseModel):
    timestamp: float
    camera: str | None = None
    imu: list[float] | dict[str, Any] | None = None
    lidar: str | list[float] | dict[str, Any] | None = None
    action: list[float] | dict[str, Any] | None = None


class Metadata(BaseModel):
    dataset_name: str
    sensors_used: list[str]
    fps: float | None = None
    frequency: dict[str, float | None] = Field(default_factory=dict)
    duration: float
    number_of_frames: int
    task: str
    frames: list[AlignedFrame] = Field(default_factory=list)


class Episode(BaseModel):
    id: str
    start_time: float
    end_time: float
    duration: float
    number_of_frames: int


class ValidationReport(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)

