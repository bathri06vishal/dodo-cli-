from __future__ import annotations

import json

from typer.testing import CliRunner

from dodo.cli import app


runner = CliRunner()


def test_import_generate_validate_export(tmp_path, monkeypatch):
    project = tmp_path / "demo"
    result = runner.invoke(app, ["init", str(project)])
    assert result.exit_code == 0

    log = tmp_path / "log.json"
    log.write_text(
        json.dumps(
            [
                {"timestamp": 0.0, "topic": "/camera/image", "payload": {"frame": 1}},
                {"timestamp": 0.0, "topic": "/imu", "payload": {"value": [0, 0, 9.8]}},
                {"timestamp": 0.0, "topic": "/cmd_vel", "payload": {"action": [0.1, 0.0]}},
                {"timestamp": 1.0, "topic": "/camera/image", "payload": {"frame": 2}},
                {"timestamp": 1.0, "topic": "/imu", "payload": {"value": [0, 0, 9.7]}},
                {"timestamp": 1.0, "topic": "/cmd_vel", "payload": {"action": [0.2, 0.0]}},
            ]
        )
    )

    monkeypatch.chdir(project)

    result = runner.invoke(app, ["import", str(log)])
    assert result.exit_code == 0

    result = runner.invoke(app, ["generate-metadata"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 0

    metadata = json.loads((project / "dataset" / "metadata" / "metadata.json").read_text())
    assert metadata["dataset_name"] == "demo"
    assert metadata["number_of_frames"] == 2
    assert metadata["task"] == "navigation"
    assert metadata["frames"][0]["camera"].startswith("data/images/")
    assert metadata["frames"][0]["imu"] == [0, 0, 9.8]
    assert metadata["frames"][0]["action"] == [0.1, 0.0]

    export_path = tmp_path / "exported"
    result = runner.invoke(app, ["export", str(export_path)])
    assert result.exit_code == 0
    assert (export_path / "metadata" / "metadata.json").exists()
