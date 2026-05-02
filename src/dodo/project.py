from __future__ import annotations

import json
from pathlib import Path

from dodo.config import DodoConfig

CONFIG_FILE = "dodo.json"


def create_project(root: Path, task: str) -> None:
    # Check if directory already exists
    if root.exists():
        # Check if it's already a DODO project
        if (root / CONFIG_FILE).exists():
            raise FileExistsError(f"Directory '{root.name}' is already a DODO project.")
        else:
            raise FileExistsError(f"Directory '{root.name}' already exists but is not a DODO project.")
    
    root.mkdir(parents=True)
    for directory in [
        root / "raw",
        root / "dataset" / "data" / "images",
        root / "dataset" / "data" / "imu",
        root / "dataset" / "data" / "lidar",
        root / "dataset" / "data" / "actions",
        root / "dataset" / "metadata",
        root / ".dodo",
    ]:
        directory.mkdir(parents=True)

    config = DodoConfig(dataset_name=root.name, task=task)
    write_json(root / CONFIG_FILE, config.model_dump())
    write_json(root / ".dodo" / "manifest.json", {"imports": []})


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / CONFIG_FILE).exists():
            return candidate
    raise FileNotFoundError("No DODO project found. Run `dodo init <project_name>` first.")


def load_config(root: Path) -> DodoConfig:
    config_path = root / CONFIG_FILE
    if not config_path.exists():
        raise FileNotFoundError(f"Missing DODO config: {config_path}")
    return DodoConfig.model_validate_json(config_path.read_text())


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")

