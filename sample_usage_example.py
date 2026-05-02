#!/usr/bin/env python3
"""
Example of how to use the exported DODO dataset for ML training
"""

import json
import numpy as np
from pathlib import Path

class DodoDatasetLoader:
    """Load and use DODO exported dataset for machine learning"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.metadata = self.load_metadata()
        self.frames = self.metadata['frames']
        
    def load_metadata(self):
        """Load dataset metadata"""
        with open(self.dataset_path / 'metadata' / 'metadata.json', 'r') as f:
            return json.load(f)
    
    def get_frame_data(self, frame_idx: int):
        """Get data for a specific frame"""
        if frame_idx >= len(self.frames):
            raise IndexError(f"Frame {frame_idx} not found. Dataset has {len(self.frames)} frames.")
        
        frame = self.frames[frame_idx]
        data = {}
        
        # Load camera data
        if frame.get('camera'):
            camera_path = self.dataset_path / frame['camera']
            with open(camera_path, 'r') as f:
                data['camera'] = json.load(f)
        
        # Load IMU data (already in metadata)
        if frame.get('imu'):
            data['imu'] = frame['imu']
        
        # Load action data (already in metadata)
        if frame.get('action'):
            data['action'] = frame['action']
        
        return data
    
    def get_sensor_data_sequence(self, sensor_type: str):
        """Get all data for a specific sensor type across all frames"""
        sequence = []
        for frame in self.frames:
            if sensor_type in frame and frame[sensor_type] is not None:
                sequence.append(frame[sensor_type])
        return sequence
    
    def create_training_sequences(self):
        """Create training sequences for different ML tasks"""
        
        # Navigation task: predict action from sensor data
        X = []  # Input features (IMU + Camera)
        y = []  # Target actions
        
        for frame in self.frames:
            # Input features
            features = {}
            
            # IMU features
            if frame.get('imu'):
                imu_data = frame['imu']
                features['imu_acc'] = np.array(imu_data['linear_acceleration'])
                features['imu_gyro'] = np.array(imu_data['angular_velocity'])
            
            # Camera features (simplified - using metadata)
            if frame.get('camera'):
                camera_path = self.dataset_path / frame['camera']
                with open(camera_path, 'r') as f:
                    camera_meta = json.load(f)
                features['camera_size'] = [camera_meta['width'], camera_meta['height']]
            
            X.append(features)
            
            # Target action
            if frame.get('action'):
                y.append(np.array(frame['action']['linear']))
        
        return X, y
    
    def print_dataset_summary(self):
        """Print summary of the dataset"""
        print(f"Dataset: {self.metadata['dataset_name']}")
        print(f"Task: {self.metadata['task']}")
        print(f"Frames: {self.metadata['number_of_frames']}")
        print(f"Duration: {self.metadata['duration']}s")
        print(f"FPS: {self.metadata['fps']}")
        print(f"Sensors: {', '.join(self.metadata['sensors_used'])}")
        print()
        
        print("Frame details:")
        for i, frame in enumerate(self.frames):
            print(f"Frame {i+1}: {frame['timestamp']}s")
            if frame.get('camera'):
                print(f"  Camera: {frame['camera']}")
            if frame.get('imu'):
                print(f"  IMU: acc={frame['imu']['linear_acceleration']}")
            if frame.get('action'):
                print(f"  Action: linear={frame['action']['linear']}")

# Example usage
if __name__ == "__main__":
    # Load the exported dataset
    dataset = DodoDatasetLoader("exported1_dataset")
    
    # Print dataset summary
    dataset.print_dataset_summary()
    
    # Get data for specific frame
    print("\nFrame 1 data:")
    frame_data = dataset.get_frame_data(0)
    print(json.dumps(frame_data, indent=2))
    
    # Create training sequences
    print("\nTraining sequences:")
    X, y = dataset.create_training_sequences()
    print(f"Input features: {len(X)} sequences")
    print(f"Target actions: {len(y)} sequences")
    
    # Example: Simple action prediction
    print("\nSample training data:")
    for i, (features, action) in enumerate(zip(X, y)):
        print(f"Frame {i+1}:")
        print(f"  IMU acceleration: {features['imu_acc']}")
        print(f"  Target action: {action}")
