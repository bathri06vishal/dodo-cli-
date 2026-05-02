from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dodo.config import DodoConfig
from dodo.models import AlignedFrame, ImportedMessage, Metadata
from dodo.project import read_json, write_json


def remove_duplicate_frames(project_root: Path, config: DodoConfig) -> dict[str, Any]:
    """Remove duplicate frames from the dataset based on timestamp and content."""
    metadata_root = project_root / config.dataset_dir / "metadata"
    
    # Load existing metadata
    metadata_file = metadata_root / "metadata.json"
    if not metadata_file.exists():
        raise FileNotFoundError(f"No metadata found at {metadata_file}. Run 'dodo generate-metadata' first.")
    
    metadata_dict = read_json(metadata_file)
    metadata = Metadata.model_validate(metadata_dict)
    
    # Remove duplicate frames
    original_count = len(metadata.frames)
    unique_frames = _remove_duplicate_frames(metadata.frames)
    filtered_count = len(unique_frames)
    
    # Update metadata with filtered frames
    metadata.frames = unique_frames
    metadata.number_of_frames = filtered_count
    
    # Recalculate duration and FPS
    if unique_frames:
        timestamps = [frame.timestamp for frame in unique_frames]
        metadata.duration = max(timestamps) - min(timestamps)
        if len(unique_frames) > 1:
            duration = unique_frames[-1].timestamp - unique_frames[0].timestamp
            metadata.fps = (len(unique_frames) - 1) / duration if duration > 0 else None
    
    # Save filtered metadata
    write_json(metadata_file, metadata.model_dump(mode="json"))
    
    # Update episodes
    episodes_file = metadata_root / "episodes.json"
    if episodes_file.exists():
        episodes = read_json(episodes_file)
        if episodes:
            episodes[0]["number_of_frames"] = filtered_count
            episodes[0]["duration"] = metadata.duration
            write_json(episodes_file, episodes)
    
    return {
        "original_frames": original_count,
        "filtered_frames": filtered_count,
        "removed_frames": original_count - filtered_count,
        "duration": metadata.duration
    }


def remove_duplicate_messages(project_root: Path, config: DodoConfig) -> dict[str, Any]:
    """Remove duplicate messages from the imported data."""
    dodo_root = project_root / ".dodo"
    
    # Load all messages
    all_messages = []
    for path in sorted(dodo_root.glob("*.messages.jsonl")):
        messages = []
        for line in path.read_text().splitlines():
            if line.strip():
                messages.append(ImportedMessage.model_validate_json(line))
        all_messages.extend(messages)
    
    original_count = len(all_messages)
    
    # Remove duplicates based on timestamp, topic, and payload hash
    unique_messages = _remove_duplicate_messages(all_messages)
    filtered_count = len(unique_messages)
    
    # Save filtered messages back to files
    _save_filtered_messages(project_root, unique_messages)
    
    return {
        "original_messages": original_count,
        "filtered_messages": filtered_count,
        "removed_messages": original_count - filtered_count
    }


def _remove_duplicate_frames(frames: list[AlignedFrame]) -> list[AlignedFrame]:
    """Remove duplicate frames based on timestamp and content."""
    seen = set()
    unique_frames = []
    
    for frame in frames:
        # Create a hashable representation of the frame
        frame_key = (
            round(frame.timestamp, 6),  # Round timestamp to avoid floating point precision issues
            frame.camera,
            _hash_dict(frame.imu) if frame.imu else None,
            _hash_dict(frame.lidar) if frame.lidar else None,
            _hash_dict(frame.action) if frame.action else None
        )
        
        if frame_key not in seen:
            seen.add(frame_key)
            unique_frames.append(frame)
    
    return unique_frames


def _remove_duplicate_messages(messages: list[ImportedMessage]) -> list[ImportedMessage]:
    """Remove duplicate messages based on timestamp, topic, and payload."""
    seen = set()
    unique_messages = []
    
    for message in messages:
        # Create a hashable representation of the message
        message_key = (
            round(message.timestamp, 6),  # Round timestamp to avoid floating point precision issues
            message.topic,
            _hash_dict(message.payload) if message.payload else None
        )
        
        if message_key not in seen:
            seen.add(message_key)
            unique_messages.append(message)
    
    return unique_messages


def _hash_dict(obj: Any) -> str:
    """Create a hashable string representation of a dictionary or list."""
    if isinstance(obj, dict):
        # Sort keys to ensure consistent ordering
        return json.dumps({k: _hash_dict(v) for k, v in sorted(obj.items())}, sort_keys=True)
    elif isinstance(obj, list):
        return json.dumps([_hash_dict(item) for item in obj])
    else:
        return str(obj)


def _save_filtered_messages(project_root: Path, messages: list[ImportedMessage]) -> None:
    """Save filtered messages back to the .dodo directory."""
    dodo_root = project_root / ".dodo"
    
    # Group messages by source file (based on existing file structure)
    # For simplicity, we'll save all messages to a single file
    output_file = dodo_root / "filtered.messages.jsonl"
    
    with open(output_file, 'w') as f:
        for message in sorted(messages, key=lambda m: m.timestamp):
            f.write(message.model_dump_json() + '\n')
    
    # Remove old message files
    for old_file in dodo_root.glob("*.messages.jsonl"):
        if old_file != output_file:
            old_file.unlink()
