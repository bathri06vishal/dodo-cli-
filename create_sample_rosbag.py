#!/usr/bin/env python3
"""
Create a sample rosbag file for testing DODO with realistic robotics data.
This simulates a TurtleBot3 navigation scenario with multiple sensors.
"""

import rosbag
import rospy
from sensor_msgs.msg import Imu, LaserScan, CompressedImage
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import numpy as np
import os

def create_sample_rosbag():
    """Create a sample rosbag with realistic robotics data."""
    
    # Create rosbag file
    bag_path = '/home/user/test_dodo/sample_robot_data.bag'
    
    with rosbag.Bag(bag_path, 'w') as bag:
        # Simulate 10 seconds of data at 10Hz
        duration = 10.0  # seconds
        rate = 10.0  # Hz
        total_steps = int(duration * rate)
        
        start_time = rospy.Time.from_sec(1234567890)  # Fixed timestamp
        
        for i in range(total_steps):
            current_time = rospy.Time.from_sec(start_time.to_sec() + i / rate)
            
            # 1. IMU Data (10 Hz)
            imu_msg = Imu()
            imu_msg.header.stamp = current_time
            imu_msg.header.frame_id = "imu_link"
            
            # Simulate robot motion with some noise
            t = i / rate
            imu_msg.linear_acceleration.x = 0.1 * np.sin(0.5 * t) + np.random.normal(0, 0.01)
            imu_msg.linear_acceleration.y = 0.05 * np.cos(0.3 * t) + np.random.normal(0, 0.01)
            imu_msg.linear_acceleration.z = 9.8 + np.random.normal(0, 0.02)
            
            imu_msg.angular_velocity.x = np.random.normal(0, 0.01)
            imu_msg.angular_velocity.y = np.random.normal(0, 0.01)
            imu_msg.angular_velocity.z = 0.1 * np.sin(0.2 * t) + np.random.normal(0, 0.005)
            
            bag.write('/imu', imu_msg, current_time)
            
            # 2. Odometry Data (10 Hz)
            odom_msg = Odometry()
            odom_msg.header.stamp = current_time
            odom_msg.header.frame_id = "odom"
            odom_msg.child_frame_id = "base_link"
            
            # Simulate robot movement
            odom_msg.pose.pose.position.x = 0.1 * t
            odom_msg.pose.pose.position.y = 0.05 * np.sin(0.5 * t)
            odom_msg.pose.pose.orientation.w = 1.0
            
            odom_msg.twist.twist.linear.x = 0.1 + 0.02 * np.sin(0.5 * t)
            odom_msg.twist.twist.angular.z = 0.05 * np.sin(0.2 * t)
            
            bag.write('/odom', odom_msg, current_time)
            
            # 3. Laser Scan Data (5 Hz)
            if i % 2 == 0:  # Every other frame
                scan_msg = LaserScan()
                scan_msg.header.stamp = current_time
                scan_msg.header.frame_id = "laser"
                scan_msg.angle_min = -np.pi
                scan_msg.angle_max = np.pi
                scan_msg.angle_increment = 2 * np.pi / 360
                scan_msg.range_min = 0.1
                scan_msg.range_max = 10.0
                
                # Simulate laser scan with some obstacles
                ranges = []
                for angle in np.linspace(-np.pi, np.pi, 360):
                    # Add some random obstacles
                    if abs(angle - np.pi/4) < 0.1:
                        ranges.append(2.0 + np.random.normal(0, 0.1))
                    elif abs(angle + np.pi/3) < 0.1:
                        ranges.append(3.5 + np.random.normal(0, 0.1))
                    else:
                        ranges.append(5.0 + np.random.normal(0, 0.2))
                
                scan_msg.ranges = ranges
                bag.write('/scan', scan_msg, current_time)
            
            # 4. Camera Data (2 Hz)
            if i % 5 == 0:  # Every 5th frame
                img_msg = CompressedImage()
                img_msg.header.stamp = current_time
                img_msg.header.frame_id = "camera_link"
                img_msg.format = "jpeg"
                
                # Simulate compressed image data
                img_msg.data = b'fake_jpeg_data_' + str(i).encode()
                bag.write('/camera/image/compressed', img_msg, current_time)
            
            # 5. Command Velocity (10 Hz)
            cmd_msg = Twist()
            cmd_msg.linear.x = 0.1 + 0.02 * np.sin(0.5 * t)
            cmd_msg.angular.z = 0.05 * np.sin(0.2 * t)
            
            bag.write('/cmd_vel', cmd_msg, current_time)
    
    print(f"Created sample rosbag: {bag_path}")
    print(f"Duration: {duration}s, Rate: {rate}Hz, Total messages: {total_steps * 4}")
    
    # Show bag info
    os.system(f"rosbag info {bag_path}")

if __name__ == "__main__":
    try:
        create_sample_rosbag()
    except Exception as e:
        print(f"Error creating rosbag: {e}")
        print("Creating a simple mock JSON dataset instead...")
        
        # Fallback: Create a simple JSON dataset
        import json
        from datetime import datetime, timedelta
        
        mock_data = {
            "messages": []
        }
        
        start_time = datetime.now()
        for i in range(100):
            timestamp = (start_time + timedelta(seconds=i*0.1)).timestamp()
            
            mock_data["messages"].append({
                "timestamp": timestamp,
                "topic": "/imu",
                "type": "sensor_msgs/Imu",
                "data": {
                    "linear_acceleration": [0.1, 0.0, 9.8],
                    "angular_velocity": [0.0, 0.0, 0.1]
                }
            })
            
            mock_data["messages"].append({
                "timestamp": timestamp,
                "topic": "/odom",
                "type": "nav_msgs/Odometry", 
                "data": {
                    "position": [i*0.1, 0.0, 0.0],
                    "linear_velocity": [0.1, 0.0, 0.0]
                }
            })
        
        with open('/home/user/test_dodo/sample_robot_data.json', 'w') as f:
            json.dump(mock_data, f, indent=2)
        
        print("Created mock JSON dataset: sample_robot_data.json")
