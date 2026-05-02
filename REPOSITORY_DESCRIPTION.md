# 🤖 DODO CLI - Repository Description

## 📝 Repository Description

**Primary Description:**
```
DODO CLI - Transform raw robotics logs into structured, ML-ready multimodal datasets
```

**Extended Description:**
```
🚀 Powerful command-line tool for converting robotics sensor data (ROS bags, JSON logs) into synchronized, machine learning-ready datasets. Perfect for computer vision, robotics, and multimodal AI applications.

🎥 Multimodal Support: Camera, IMU, LiDAR, and action data synchronization
📦 Multiple Formats: ROS bags, JSON, JSONL, and mock data support  
⚡ Temporal Alignment: Automatic sensor data synchronization
🔐 Security: Built-in user authentication and API key management
📊 Metadata Generation: Comprehensive dataset metadata for ML workflows
🧹 Data Cleaning: Duplicate detection and filtering capabilities
✅ Validation: Dataset integrity and structure validation
📤 Export: Structured dataset export for ML pipelines
```

## 🏷️ Repository Topics/Tags

```
robotics, machine-learning, dataset, multimodal, ros, computer-vision, cli, python, pydantic, typer, sensor-data, data-processing, artificial-intelligence, automation, data-science, robotics-datasets, ml-datasets, computer-vision-datasets
```

## 🌟 Repository Features

### Core Features
- **🤖 Multimodal Dataset Creation**: Transform raw robotics logs into ML-ready datasets
- **⚡ Temporal Alignment**: Automatic sensor data synchronization using nearest-neighbor matching
- **📦 Multiple Format Support**: ROS bags, JSON, JSONL, and mock data
- **🔐 User Authentication**: Built-in security with API key management
- **📊 Rich Metadata**: Comprehensive dataset metadata for ML workflows

### Technical Features
- **🎥 Camera Support**: Image frames with file paths
- **📡 IMU Processing**: Linear acceleration and angular velocity
- **🔍 LiDAR Integration**: Point cloud data handling
- **🎮 Action Commands**: Robot control command processing
- **🧹 Data Cleaning**: Smart duplicate detection and removal
- **✅ Validation**: Dataset integrity and structure validation
- **📤 Export Options**: Multiple export formats for ML pipelines

## 📋 README Summary

### Quick Start
```bash
pip install dodo-robotics
dodo register --username your-username
dodo login --username your-username
dodo init my_robot_dataset
dodo import robot_data.bag --project my_robot_dataset
dodo generate-metadata --project my_robot_dataset
dodo export ./output_dataset --project my_robot_dataset
```

### Key Commands
- **Project Management**: `init`, `list`, `delete`
- **Data Operations**: `import`, `generate-metadata`, `filter`, `validate`, `export`
- **User Management**: `register`, `login`, `logout`, `whoami`

## 🎯 Use Cases

### Computer Vision
- **Object Detection**: Synchronized camera and sensor data
- **Scene Understanding**: Multimodal context for better perception
- **Visual Odometry**: Camera-IMU fusion for navigation

### Robotics
- **SLAM**: Simultaneous localization and mapping datasets
- **Navigation**: Sensor fusion for autonomous navigation
- **Manipulation**: Robotic arm control with visual feedback

### Machine Learning
- **Multimodal Learning**: Combined sensor data for better models
- **Time Series Analysis**: Synchronized temporal sensor streams
- **Reinforcement Learning**: Action-reward datasets with sensory context

## 🏗️ Technical Architecture

### Data Pipeline
1. **Import**: Load robotics data from various formats
2. **Alignment**: Temporal synchronization of sensor modalities
3. **Processing**: Data cleaning and validation
4. **Export**: Structured ML-ready datasets

### Supported Modalities
- **Camera**: RGB/Depth images with timestamps
- **IMU**: 6-DOF motion data (acceleration + angular velocity)
- **LiDAR**: Point cloud data with spatial information
- **Actions**: Robot control commands and trajectories

## 🔧 Installation

```bash
# Basic installation
pip install dodo-robotics

# With ROS support
pip install dodo-robotics[ros]

# Development installation
pip install dodo-robotics[dev]
```

## 📊 Project Statistics

- **Language**: Python 3.10+
- **Lines of Code**: 58,000+
- **Files**: 94+
- **Dependencies**: Typer, Pydantic, Questionary
- **License**: MIT (Open Source)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/bathri06vishal/dodocil.git
cd dodocil
pip install -e .[dev]
pytest tests/
```

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🏢 About

Created by **bathri06vishal** for the robotics and AI community.

**Mission**: Make robotics data accessible and useful for machine learning applications.

---

## 🚀 Why Choose DODO CLI?

✅ **Easy to Use**: Beautiful CLI with helpful commands
✅ **Professional**: Production-ready with comprehensive documentation  
✅ **Flexible**: Supports multiple robotics data formats
✅ **Reliable**: Built-in validation and error handling
✅ **Open Source**: MIT license for commercial and academic use
✅ **Active**: Continuously maintained and improved

**Perfect for**: Robotics researchers, ML engineers, data scientists, and open source contributors!
