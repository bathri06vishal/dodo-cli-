#!/usr/bin/env python3
"""
Create a sample JSON dataset with intentional duplicates for testing DODO filter functionality.
"""

import json
import numpy as np
from datetime import datetime, timedelta

def create_dataset_with_duplicates():
    """Create a dataset with some duplicate messages."""
    
    messages = []
    start_time = datetime.now().timestamp()
    
    # Create some unique messages first
    for i in range(10):
        current_time = start_time + i * 0.1
        
        # Unique IMU message
        imu_msg = {
            "timestamp": current_time,
            "topic": "/imu",
            "type": "sensor_msgs/Imu",
            "data": {
                "linear_acceleration": {"x": 0.1 * i, "y": 0.0, "z": 9.8},
                "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.1 * i}
            }
        }
        messages.append(imu_msg)
        
        # Unique odometry message
        odom_msg = {
            "timestamp": current_time,
            "topic": "/odom",
            "type": "nav_msgs/Odometry",
            "data": {
                "pose": {
                    "position": {"x": 0.1 * i, "y": 0.0, "z": 0.0},
                    "orientation": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0}
                },
                "twist": {
                    "linear": {"x": 0.1, "y": 0.0, "z": 0.0},
                    "angular": {"x": 0.0, "y": 0.0, "z": 0.05}
                }
            }
        }
        messages.append(odom_msg)
    
    # Now add some duplicates
    # Duplicate IMU message (same timestamp and data)
    duplicate_imu = {
        "timestamp": start_time + 0.3,  # Same as message 3
        "topic": "/imu",
        "type": "sensor_msgs/Imu",
        "data": {
            "linear_acceleration": {"x": 0.3, "y": 0.0, "z": 9.8},  # Same as message 3
            "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.3}
        }
    }
    messages.append(duplicate_imu)
    
    # Another duplicate IMU message
    duplicate_imu2 = {
        "timestamp": start_time + 0.3,  # Same timestamp
        "topic": "/imu",
        "type": "sensor_msgs/Imu",
        "data": {
            "linear_acceleration": {"x": 0.3, "y": 0.0, "z": 9.8},  # Same data
            "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.3}
        }
    }
    messages.append(duplicate_imu2)
    
    # Duplicate odometry message
    duplicate_odom = {
        "timestamp": start_time + 0.5,  # Same as message 5
        "topic": "/odom",
        "type": "nav_msgs/Odometry",
        "data": {
            "pose": {
                "position": {"x": 0.5, "y": 0.0, "z": 0.0},  # Same as message 5
                "orientation": {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0}
            },
            "twist": {
                "linear": {"x": 0.1, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.05}
            }
        }
    }
    messages.append(duplicate_odom)
    
    # Add some more unique messages
    for i in range(10, 15):
        current_time = start_time + i * 0.1
        
        imu_msg = {
            "timestamp": current_time,
            "topic": "/imu",
            "type": "sensor_msgs/Imu",
            "data": {
                "linear_acceleration": {"x": 0.1 * i, "y": 0.0, "z": 9.8},
                "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.1 * i}
            }
        }
        messages.append(imu_msg)
    
    # Sort messages by timestamp
    messages.sort(key=lambda x: x['timestamp'])
    
    # Create dataset file
    dataset = {
        "metadata": {
            "name": "dataset_with_duplicates",
            "description": "Dataset with intentional duplicates for testing filter functionality",
            "duration": 1.5,
            "sensors": ["imu", "odom"],
            "total_messages": len(messages)
        },
        "messages": messages
    }
    
    output_file = '/home/user/test_dodo/dataset_with_duplicates.json'
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Created dataset with duplicates: {output_file}")
    print(f"Total messages: {len(messages)}")
    print(f"Expected duplicates: 3 (2 IMU, 1 odom)")
    print(f"Expected unique messages: {len(messages) - 3}")
    
    return output_file

if __name__ == "__main__":
    create_dataset_with_duplicates()
