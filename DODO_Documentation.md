# DODO: Multimodal Dataset Creation Tool

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Commands](#commands)
5. [Security Features](#security-features)
6. [Data Formats](#data-formats)
7. [Examples](#examples)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

## Overview

DODO is a powerful command-line tool that transforms raw robotics logs into structured, ML-ready multimodal datasets. It automatically aligns sensor data (camera, IMU, lidar, actions) into synchronized frames and generates comprehensive metadata for computer vision, robotics, and multimodal AI training.

### Key Features
- **Multimodal Data Processing**: Handle camera, IMU, lidar, and action data
- **Automatic Alignment**: Synchronize sensor data across different frequencies
- **Duplicate Removal**: Filter out redundant data with advanced algorithms
- **Security**: Enterprise-grade authentication and encryption
- **Multiple Formats**: Support for rosbag, JSON, JSONL, and mock logs
- **Validation**: Built-in dataset integrity checking

## Installation

### Prerequisites
- Python 3.8 or higher
- Required dependencies: typer, click, pydantic, cryptography, numpy

### Install from Source
```bash
git clone <repository-url>
cd dodo
pip install -e .
```

### Dependencies
```bash
pip install typer click pydantic cryptography numpy
```

## Quick Start

### 1. Create User Account
```bash
dodo register --username myuser --email user@example.com
```

### 2. Login
```bash
dodo login --username myuser
```

### 3. Create Project
```bash
dodo init my_dataset --task navigation
```

### 4. Import Data
```bash
dodo import robot_data.bag --project my_dataset
```

### 5. Generate Metadata
```bash
dodo generate-metadata --project my_dataset
```

### 6. Filter Duplicates
```bash
dodo filter frames --project my_dataset
dodo filter messages --project my_dataset
```

### 7. Export Dataset
```bash
dodo export output/ --project my_dataset
```

## Commands

### Project Management

#### `init`
Create a new DODO project.
```bash
dodo init <project_name> [--task TASK] [--version VERSION]
```
- `project_name`: Name of the DODO dataset project
- `--task, -t`: Dataset task label (default: navigation)
- `--version`: Project version (default: 0.1.0)

#### `list`
List all DODO projects.
```bash
dodo list [--path PATH]
```
- `--path, -p`: Path to search for DODO projects (default: current directory)

#### `delete`
Delete a DODO project.
```bash
dodo delete <project_name> [--force]
```
- `project_name`: Name of the DODO project to delete
- `--force, -f`: Force deletion without confirmation

### Data Operations

#### `import`
Import robot logs into a DODO project.
```bash
dodo import <file_path> [--project PROJECT]
```
- `file_path`: Path to rosbag, JSON, JSONL, or mock log
- `--project, -p`: DODO project root

#### `generate-metadata`
Generate aligned frame metadata.
```bash
dodo generate-metadata [--project PROJECT]
```
- `--project, -p`: DODO project root

#### `filter`
Remove duplicate data from dataset (requires authentication).
```bash
dodo filter <filter_type> [--project PROJECT]
```
- `filter_type`: 'frames' or 'messages'
- `--project, -p`: DODO project root

#### `export`
Export dataset to structured format.
```bash
dodo export <output_path> [--project PROJECT] [--overwrite]
```
- `output_path`: Destination path for the structured dataset
- `--project, -p`: DODO project root
- `--overwrite, -f`: Overwrite existing output directory

### Data Inspection

#### `show-metadata`
Display DODO dataset metadata.
```bash
dodo show-metadata [--project PROJECT]
```
- `--project, -p`: DODO project root

#### `validate`
Validate dataset integrity.
```bash
dodo validate [--project PROJECT]
```
- `--project, -p`: DODO project root

### Security Commands

#### `register`
Create a new user account.
```bash
dodo register --username USERNAME [--email EMAIL]
```
- `--username, -u`: Username for new account
- `--email, -e`: Email address (optional)

#### `login`
Login to DODO with authentication.
```bash
dodo login --username USERNAME [--password PASSWORD]
```
- `--username, -u`: Username for login
- `--password, -p`: Password (will prompt if not provided)

#### `logout`
Logout from current DODO session.
```bash
dodo logout
```

#### `whoami`
Show current logged in user.
```bash
dodo whoami
```

#### `change-password`
Change user password.
```bash
dodo change-password [--username USERNAME]
```
- `--username, -u`: Username (defaults to current user)

## Security Features

### Authentication System
- **User Registration**: Secure account creation with password validation
- **Session Management**: Time-limited sessions (1 hour expiration)
- **API Keys**: Unique secure API keys for each user
- **Password Security**: PBKDF2 key derivation with 100,000 iterations

### Encryption
- **Data Encryption**: AES-256 encryption for sensitive data
- **Secure Storage**: Encrypted credential storage
- **HMAC Protection**: Timing attack prevention
- **Salt Management**: Unique salts for password hashing

### Access Control
- **Command Protection**: Sensitive operations require authentication
- **Session Validation**: Automatic session expiration
- **API Key Verification**: Secure API access control

## Data Formats

### Input Formats
- **ROSBAG**: Robot Operating System bag files
- **JSON**: Structured JSON logs
- **JSONL**: JSON Lines format
- **Mock Logs**: Synthetic test data

### Output Formats
- **Aligned Frames**: Synchronized multimodal data
- **Metadata**: Comprehensive dataset information
- **Structured Export**: ML-ready format

### Sensor Types
- **Camera**: Image data (compressed/raw)
- **IMU**: Inertial measurement unit data
- **Lidar**: Point cloud data
- **Action**: Robot command/control data
- **Odometry**: Position and orientation data

## Examples

### Basic Workflow
```bash
# 1. Register and login
dodo register --username researcher --email lab@university.edu
dodo login --username researcher

# 2. Create project
dodo init robot_navigation --task navigation

# 3. Import real data
dodo import turtlebot_data.bag --project robot_navigation

# 4. Process and clean data
dodo generate-metadata --project robot_navigation
dodo filter frames --project robot_navigation
dodo filter messages --project robot_navigation

# 5. Validate and export
dodo validate --project robot_navigation
dodo export clean_dataset/ --project robot_navigation --overwrite
```

### Advanced Filtering
```bash
# Remove duplicate frames (keeps unique synchronized data)
dodo filter frames --project my_dataset

# Remove duplicate messages (cleans raw sensor data)
dodo filter messages --project my_dataset
```

### Data Inspection
```bash
# View dataset overview
dodo show-metadata --project my_dataset

# Check data integrity
dodo validate --project my_dataset
```

## API Reference

### Security Manager
The security system provides the following APIs:

#### Authentication
```python
from dodo.security import security_manager

# Create user
security_manager.create_user(username, password, email)

# Authenticate
user_data = security_manager.authenticate(username, password)

# Get current user
current_user = security_manager.get_current_user()

# Logout
security_manager.logout()
```

#### Encryption
```python
# Encrypt data
encrypted = security_manager.encrypt_data(data, password)

# Decrypt data
decrypted = security_manager.decrypt_data(encrypted, password)
```

#### API Key Management
```python
# Get API key
api_key = security_manager.get_user_api_key(username)

# Verify API key
username = security_manager.verify_api_key(api_key)
```

### Data Models
```python
from dodo.models import AlignedFrame, ImportedMessage, Metadata

# Aligned frame structure
frame = AlignedFrame(
    timestamp=1234567890.0,
    camera="path/to/image.jpg",
    imu={"linear_acceleration": [0.1, 0.0, 9.8]},
    action=[0.2, 0.0]
)

# Message structure
message = ImportedMessage(
    timestamp=1234567890.0,
    topic="/imu",
    modality="imu",
    payload={"data": "sensor_data"}
)
```

## Troubleshooting

### Common Issues

#### Authentication Errors
**Problem**: "Authentication required" error
**Solution**: Run `dodo login` with valid credentials

#### Session Expired
**Problem**: Commands fail after inactivity
**Solution**: Run `dodo login` again to refresh session

#### Import Failures
**Problem**: Cannot import rosbag files
**Solution**: Ensure ROS dependencies are installed and file is valid

#### Memory Issues
**Problem**: Large datasets cause memory errors
**Solution**: Process data in chunks or increase system memory

#### Permission Errors
**Problem**: Cannot write to project directories
**Solution**: Check file permissions and run with appropriate user

### Debug Mode
Enable verbose logging:
```bash
export DODO_DEBUG=1
dodo <command>
```

### Configuration Files
- User data: `~/.dodo/`
- Users database: `~/.dodo/users.json`
- Session data: `~/.dodo/session.json`
- Project config: `<project>/dodo.json`

### Getting Help
```bash
# Show all commands
dodo --help

# Show command help
dodo <command> --help

# Show current user
dodo whoami
```

## Best Practices

### Security
1. Use strong passwords (8+ characters, mixed case, numbers, symbols)
2. Never share API keys
3. Logout when finished working
4. Change passwords regularly
5. Use different passwords for different services

### Data Management
1. Validate datasets before processing
2. Filter duplicates to reduce noise
3. Export with descriptive names
4. Keep original raw data as backup
5. Document data sources and processing steps

### Performance
1. Process large datasets in batches
2. Use SSD storage for faster I/O
3. Monitor system resources during processing
4. Clean temporary files regularly

## Version History

### Current Version: 1.0.0
- Initial release with core functionality
- Security features implemented
- Multi-format data support
- Advanced filtering capabilities

### Planned Features
- Web-based interface
- Cloud storage integration
- Advanced data visualization
- Machine learning pipeline integration
- Real-time data streaming support

## Support

For issues, questions, or contributions:
- Documentation: Available in this guide
- Commands: Use `dodo --help` for quick reference
- Security: Contact system administrator for account issues

---

*This documentation covers all DODO features as of version 1.0.0. For the latest updates, check the official repository.*
