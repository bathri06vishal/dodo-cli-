#!/usr/bin/env python3
"""
Create a sample JSON dataset for testing DODO with realistic robotics data.
This simulates a TurtleBot3 navigation scenario with multiple sensors.
"""

import json
import numpy as np
from datetime import datetime, timedelta

def create_sample_json_dataset():
    """Create a sample JSON dataset with realistic robotics data."""
    
    # Simulate 10 seconds of data at 10Hz
    duration = 10.0  # seconds
    rate = 10.0  # Hz
    total_steps = int(duration * rate)
    
    messages = []
    start_time = datetime.now().timestamp()
    
    for i in range(total_steps):
        current_time = start_time + i / rate
        t = i / rate
        
        # 1. IMU Data (10 Hz)
        imu_msg = {
            "timestamp": current_time,
            "topic": "/imu",
            "type": "sensor_msgs/Imu",
            "data": {
                "linear_acceleration": {
                    "x": 0.1 * np.sin(0.5 * t) + np.random.normal(0, 0.01),
                    "y": 0.05 * np.cos(0.3 * t) + np.random.normal(0, 0.01),
                    "z": 9.8 + np.random.normal(0, 0.02)
                },
                "angular_velocity": {
                    "x": np.random.normal(0, 0.01),
                    "y": np.random.normal(0, 0.01),
                    "z": 0.1 * np.sin(0.2 * t) + np.random.normal(0, 0.005)
                }
            }
        }
        messages.append(imu_msg)
        
        # 2. Odometry Data (10 Hz)
        odom_msg = {
            "timestamp": current_time,
            "topic": "/odom",
            "type": "nav_msgs/Odometry",
            "data": {
                "pose": {
                    "position": {
                        "x": 0.1 * t,
                        "y": 0.05 * np.sin(0.5 * t),
                        "z": 0.0
                    },
                    "orientation": {
                        "w": 1.0,
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.0
                    }
                },
                "twist": {
                    "linear": {
                        "x": 0.1 + 0.02 * np.sin(0.5 * t),
                        "y": 0.0,
                        "z": 0.0
                    },
                    "angular": {
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.05 * np.sin(0.2 * t)
                    }
                }
            }
        }
        messages.append(odom_msg)
        
        # 3. Laser Scan Data (5 Hz)
        if i % 2 == 0:  # Every other frame
            ranges = []
            for angle in np.linspace(-np.pi, np.pi, 360):
                # Add some random obstacles
                if abs(angle - np.pi/4) < 0.1:
                    ranges.append(2.0 + np.random.normal(0, 0.1))
                elif abs(angle + np.pi/3) < 0.1:
                    ranges.append(3.5 + np.random.normal(0, 0.1))
                else:
                    ranges.append(5.0 + np.random.normal(0, 0.2))
            
            scan_msg = {
                "timestamp": current_time,
                "topic": "/scan",
                "type": "sensor_msgs/LaserScan",
                "data": {
                    "angle_min": -np.pi,
                    "angle_max": np.pi,
                    "angle_increment": 2 * np.pi / 360,
                    "range_min": 0.1,
                    "range_max": 10.0,
                    "ranges": ranges
                }
            }
            messages.append(scan_msg)
        
        # 4. Camera Data (2 Hz)
        if i % 5 == 0:  # Every 5th frame
            img_msg = {
                "timestamp": current_time,
                "topic": "/camera/image/compressed",
                "type": "sensor_msgs/CompressedImage",
                "data": {
                    "format": "jpeg",
                    "data": f"fake_jpeg_data_{i}"
                }
            }
            messages.append(img_msg)
        
        # 5. Command Velocity (10 Hz)
        cmd_msg = {
            "timestamp": current_time,
            "topic": "/cmd_vel",
            "type": "geometry_msgs/Twist",
            "data": {
                "linear": {
                    "x": 0.1 + 0.02 * np.sin(0.5 * t),
                    "y": 0.0,
                    "z": 0.0
                },
                "angular": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.05 * np.sin(0.2 * t)
                }
            }
        }
        messages.append(cmd_msg)
    
    # Sort messages by timestamp
    messages.sort(key=lambda x: x['timestamp'])
    
    # Create dataset file
    dataset = {
        "metadata": {
            "name": "sample_robot_dataset",
            "description": "Sample TurtleBot3 navigation dataset for testing DODO",
            "duration": duration,
            "sensors": ["imu", "odom", "scan", "camera", "cmd_vel"],
            "total_messages": len(messages)
        },
        "messages": messages
    }
    
    output_file = '/home/user/test_dodo/sample_robot_data.json'
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Created sample JSON dataset: {output_file}")
    print(f"Duration: {duration}s, Rate: {rate}Hz, Total messages: {len(messages)}")
    print(f"Sensors: IMU, Odometry, Laser Scan, Camera, Command Velocity")
    
    return output_file

if __name__ == "__main__":
    create_sample_json_dataset()
