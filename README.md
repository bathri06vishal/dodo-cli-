# 🤖 DODO CLI - Multimodal Robotics Dataset Creator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/dodo-robotics.svg)](https://badge.fury.io/py/dodo-robotics)

> **Transform raw robotics logs into structured, ML-ready multimodal datasets**

DODO CLI is a powerful command-line tool that converts robotics sensor data (ROS bags, JSON logs) into synchronized, machine learning-ready datasets. Perfect for computer vision, robotics, and multimodal AI applications.

## ✨ Features

- 🎥 **Multimodal Support**: Camera, IMU, LiDAR, and action data synchronization
- 📦 **Multiple Formats**: ROS bags, JSON, JSONL, and mock data support
- ⚡ **Temporal Alignment**: Automatic sensor data synchronization using nearest-neighbor matching
- 🔐 **Security**: Built-in user authentication and API key management
- 📊 **Metadata Generation**: Comprehensive dataset metadata for ML workflows
- 🧹 **Data Cleaning**: Duplicate detection and filtering capabilities
- ✅ **Validation**: Dataset integrity and structure validation
- 📤 **Export**: Structured dataset export for ML pipelines

## 🚀 Quick Start

### Installation

```bash
# Clone from GitHub
git clone https://github.com/bathri06vishal/dodo-cli-.git
cd dodo-cli-

# Install in development mode
pip install -e .

# Or install from PyPI (when published)
pip install dodo-robotics

# With ROS bag support
pip install dodo-robotics[ros]

# For development
pip install dodo-robotics[dev]
```

### Basic Usage

```bash
# Create a new account
dodo register --username your-username

# Login
dodo login --username your-username

# Initialize a new dataset project
dodo init my_robot_dataset

# Import robotics data
dodo import robot_data.bag --project my_robot_dataset

# Generate synchronized metadata
dodo generate-metadata --project my_robot_dataset

# Export ML-ready dataset
dodo export ./output_dataset --project my_robot_dataset
```

## CLI in Action

### Welcome Screen
The DODO CLI features a beautiful animated welcome screen with comprehensive command listings:

![DODO CLI Demo](https://github.com/bathri06vishal/dodo-cli-/raw/main/screenshots/dodo-welcome.png)

### Project Management
Easily list and manage your robotics datasets:

```bash
$ dodo list
Found 2 DODO project(s):

📁 test_robot_dataset
   Path: /home/user/test_dodo/test_robot_dataset
   Task: navigation
   Version: 0.1.0

📁 tmp_dataset2
   Path: /home/user/test_dodo/tmp_dataset2
   Task: inspection
   Version: 0.1.0
```

### Quick Commands Reference
All commands are accessible from the welcome screen:
- `init` - Create new project
- `list` - List all projects  
- `delete` - Delete project
- `register` - Create user account
- `login` - Login to DODO
- `import` - Import robot logs
- `generate-metadata` - Create aligned frames
- `filter` - Remove duplicates
- `validate` - Validate dataset
- `export` - Export dataset
- `logout` - Logout from session

## Documentation

### Project Structure

```
my_robot_dataset/
├── dodo.json              # Project configuration
├── .dodo/                 # Imported messages
├── dataset/
│   ├── metadata/
│   │   ├── metadata.json  # Aligned frames and metadata
│   │   ├── sensors.json   # Sensor information
│   │   └── episodes.json  # Episode timing
│   ├── raw/               # Raw imported data
│   └── processed/         # Processed frames
└── exports/               # Exported datasets
```

### Supported Data Formats

| Format | Description | Example |
|--------|-------------|---------|
| **ROS Bags** | `.bag` files from ROS1/ROS2 | `dodo import data.bag` |
| **JSON Logs** | Structured JSON logs | `dodo import log.json` |
| **JSONL Logs** | Line-delimited JSON | `dodo import log.jsonl` |
| **Mock Data** | Generated test data | `dodo import mock.log` |

### Sensor Modalities

- **🎥 Camera**: Image frames with file paths
- **📡 IMU**: Linear acceleration and angular velocity
- **🔍 LiDAR**: Point cloud data
- **🎮 Actions**: Robot control commands

### Command Reference

#### Project Management
```bash
dodo init <project_name>           # Create new project
dodo list                          # List all projects
dodo delete <project_name>         # Delete project
```

#### Data Operations
```bash
dodo import <file> --project <name>     # Import robotics data
dodo generate-metadata --project <name> # Create aligned frames
dodo filter <type> --project <name>     # Remove duplicates
dodo validate --project <name>          # Validate dataset
dodo export <path> --project <name>    # Export dataset
```

#### User Management
```bash
dodo register --username <name>    # Create account
dodo login --username <name>       # Login
dodo logout                         # Logout
dodo whoami                         # Show current user
```

## 🔧 Configuration

### Project Configuration (`dodo.json`)

```json
{
  "dataset_name": "my_robot_dataset",
  "task": "navigation",
  "dataset_dir": "dataset",
  "version": "1.0.0"
}
```

### Supported Tasks

- `navigation` - Autonomous navigation
- `manipulation` - Robotic arm control
- `perception` - Computer vision tasks
- `localization` - Position estimation
- `custom` - User-defined tasks

## 📊 Metadata Structure

### Aligned Frame Example

```json
{
  "timestamp": 1234567890.123,
  "camera": "/path/to/image.jpg",
  "imu": {
    "linear_acceleration": [0.1, 0.2, 9.8],
    "angular_velocity": [0.01, -0.02, 0.00]
  },
  "lidar": "/path/to/pointcloud.pcd",
  "action": [0.5, -0.3, 0.0]
}
```

### Sensor Information

```json
{
  "name": "camera_front",
  "modality": "camera",
  "topic": "/camera/front/image_raw",
  "frequency_hz": 30.0,
  "message_count": 900
}
```

## 🧪 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dodo-robotics/Dodo_CLI.V1.0.git
cd Dodo_CLI.V1.0

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/
```

### Project Structure

```
src/dodo/
├── __init__.py
├── cli.py              # Main CLI interface
├── metadata.py         # Metadata generation
├── alignment.py        # Sensor data alignment
├── models.py           # Pydantic models
├── config.py           # Configuration management
├── project.py          # Project utilities
├── security.py         # Authentication
├── validation.py       # Dataset validation
├── filter.py           # Data filtering
├── exporter.py         # Dataset export
├── importers/          # Data importers
├── sensor_detection.py # Sensor type detection
└── alignment.py        # Temporal alignment
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Dodo Robotics

Dodo Robotics is dedicated to advancing robotics and AI through open-source tools and datasets. Our mission is to make robotics data accessible and useful for the global AI community.

🌐 **Website**: [https://dodo-robotics.com](https://dodo-robotics.com)

## 📞 Support

- 📧 Email: support@dodo-robotics.com
- 💬 Discord: [Join our community](https://discord.gg/dodo-robotics)
- 🐛 Issues: [GitHub Issues](https://github.com/dodo-robotics/Dodo_CLI.V1.0/issues)

## 🙏 Acknowledgments

- ROS community for the robotics messaging framework
- Typer for the beautiful CLI framework
- Pydantic for data validation
- All our contributors and users!

---

**⭐ If you find DODO CLI useful, please give us a star on GitHub!**
