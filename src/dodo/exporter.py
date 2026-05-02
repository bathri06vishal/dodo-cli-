from __future__ import annotations

import shutil
from pathlib import Path

from dodo.project import load_config
from dodo.validation import validate_dataset


def export_dataset(project_root: Path, output_path: Path, overwrite: bool = False) -> Path:
    config = load_config(project_root)
    dataset_root = project_root / config.dataset_dir
    report = validate_dataset(project_root)
    if not report.valid:
        raise ValueError("Cannot export invalid dataset: " + "; ".join(report.errors))

    if output_path.exists():
        if not overwrite:
            raise FileExistsError(f"Output path already exists: {output_path}")
        shutil.rmtree(output_path)

    shutil.copytree(dataset_root, output_path)
    return output_path

