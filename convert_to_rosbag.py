#!/usr/bin/env python3
"""
Convert JSON log to rosbag format for DODO import
"""

import json
import numpy as np
from pathlib import Path
try:
    from rosbags.rosbag1 import Writer
    from rosbags.serde import serialize
    from std_msgs.msg import Header
    from sensor_msgs.msg import Imu, Image
    from geometry_msgs.msg import Twist, Vector3
    from rcl_interfaces.msg import Log
except ImportError as e:
    print(f"Error: {e}")
    print("Install rosbags: pip install rosbags")
    exit(1)

def json_to_rosbag(json_file: str, output_bag: str):
    """Convert JSON log to rosbag format"""
    
    # Read JSON log
    with open(json_file, 'r') as f:
        messages = json.load(f)
    
    # Create rosbag writer
    with Writer(output_bag) as writer:
        # Create connections for each topic
        connections = {}
        
        for i, msg_data in enumerate(messages):
            timestamp = int(msg_data['timestamp'] * 1e9)  # Convert to nanoseconds
            topic = msg_data['topic']
            payload = msg_data['payload']
            
            # Create ROS message based on topic
            if topic == "/rosout":
                msg = Log()
                msg.stamp.sec = int(msg_data['timestamp'])
                msg.stamp.nanosec = int((msg_data['timestamp'] % 1) * 1e9)
                msg.level = Log.INFO
                msg.name = "dodo_converter"
                msg.msg = payload.get('msg', 'converted from JSON')
                msg.file = ""
                msg.function = ""
                msg.line = 0
                
            elif topic == "/camera/image":
                msg = Image()
                msg.header.stamp.sec = int(msg_data['timestamp'])
                msg.header.stamp.nanosec = int((msg_data['timestamp'] % 1) * 1e9)
                msg.header.frame_id = payload.get('frame_id', 'camera_link')
                msg.width = payload.get('width', 640)
                msg.height = payload.get('height', 480)
                msg.encoding = payload.get('encoding', 'rgb8')
                msg.is_bigendian = 0
                msg.step = msg.width * 3  # 3 bytes per pixel for rgb8
                # Create dummy image data
                msg.data = bytes([255, 0, 0] * (msg.width * msg.height))  # Red image
                
            elif topic == "/imu":
                msg = Imu()
                msg.header.stamp.sec = int(msg_data['timestamp'])
                msg.header.stamp.nanosec = int((msg_data['timestamp'] % 1) * 1e9)
                msg.header.frame_id = payload.get('frame_id', 'imu_link')
                
                # Linear acceleration
                if 'linear_acceleration' in payload:
                    la = payload['linear_acceleration']
                    msg.linear_acceleration.x = la[0]
                    msg.linear_acceleration.y = la[1] 
                    msg.linear_acceleration.z = la[2]
                
                # Angular velocity
                if 'angular_velocity' in payload:
                    av = payload['angular_velocity']
                    msg.angular_velocity.x = av[0]
                    msg.angular_velocity.y = av[1]
                    msg.angular_velocity.z = av[2]
                    
            elif topic == "/cmd_vel":
                msg = Twist()
                if 'linear' in payload:
                    lin = payload['linear']
                    msg.linear.x = lin[0] if len(lin) > 0 else 0.0
                    msg.linear.y = lin[1] if len(lin) > 1 else 0.0
                    msg.linear.z = lin[2] if len(lin) > 2 else 0.0
                if 'angular' in payload:
                    ang = payload['angular']
                    msg.angular.x = ang[0] if len(ang) > 0 else 0.0
                    msg.angular.y = ang[1] if len(ang) > 1 else 0.0
                    msg.angular.z = ang[2] if len(ang) > 2 else 0.0
            else:
                continue  # Skip unknown topics
            
            # Create connection if not exists
            if topic not in connections:
                connections[topic] = writer.add_connection(
                    topic, 
                    msg.__class__,
                    msg.__class__.__msgtype__
                )
            
            # Write message
            writer.write(connections[topic], timestamp, serialize(msg, msg.__class__))
    
    print(f"Successfully converted {len(messages)} messages to {output_bag}")

if __name__ == "__main__":
    json_to_rosbag("simple_log.json", "simple_log.bag")
