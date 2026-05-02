# Installation Guide

## 📦 Installation Methods

### Method 1: PyPI Installation (Recommended)

```bash
# Basic installation
pip install dodo-robotics

# With ROS bag support
pip install dodo-robotics[ros]

# Development installation
pip install dodo-robotics[dev]
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/dodo-robotics/Dodo_CLI.V1.0.git
cd Dodo_CLI.V1.0

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]
```

### Method 3: From Source

```bash
# Download source code
wget https://github.com/dodo-robotics/Dodo_CLI.V1.0/archive/refs/tags/v1.0.0.tar.gz
tar -xzf v1.0.0.tar.gz
cd Dodo_CLI.V1.0-1.0.0

# Install
pip install .
```

## 🔧 Requirements

- Python 3.10 or higher
- pip (Python package manager)

### Optional Dependencies

- **ROS Support**: `rosbags>=0.10.0`
- **Development**: `pytest>=8.0.0`, `black>=23.0.0`, `flake8>=6.0.0`, `mypy>=1.0.0`

## ✅ Verification

After installation, verify that DODO CLI is working:

```bash
# Check installation
dodo --help

# Show welcome screen
dodo

# Check version
dodo --version
```

## 🚀 Quick Start

1. **Create Account**
   ```bash
   dodo register --username your-username
   ```

2. **Login**
   ```bash
   dodo login --username your-username
   ```

3. **Create Project**
   ```bash
   dodo init my_dataset
   ```

4. **Import Data**
   ```bash
   dodo import data.bag --project my_dataset
   ```

5. **Generate Metadata**
   ```bash
   dodo generate-metadata --project my_dataset
   ```

6. **Export Dataset**
   ```bash
   dodo export ./output --project my_dataset
   ```

## 🐛 Troubleshooting

### Common Issues

#### 1. Command Not Found
```bash
# If 'dodo' command is not found, try:
python -m dodo.cli

# Or reinstall:
pip uninstall dodo-robotics
pip install dodo-robotics
```

#### 2. Permission Denied
```bash
# Use user installation:
pip install --user dodo-robotics

# Or use sudo (not recommended):
sudo pip install dodo-robotics
```

#### 3. Python Version Incompatible
```bash
# Check Python version:
python --version

# If < 3.10, upgrade Python or use conda:
conda create -n dodo python=3.10
conda activate dodo
pip install dodo-robotics
```

#### 4. ROS Bag Issues
```bash
# Install ROS support:
pip install dodo-robotics[ros]

# Or install manually:
pip install rosbags>=0.10.0
```

### Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/dodo-robotics/Dodo_CLI.V1.0/issues)
- **Email**: support@dodo-robotics.com
- **Discord**: [Community Server](https://discord.gg/dodo-robotics)

## 🔄 Updates

To update to the latest version:

```bash
pip install --upgrade dodo-robotics
```

## 🗑️ Uninstallation

To uninstall DODO CLI:

```bash
pip uninstall dodo-robotics
```

## 📁 Installation Locations

### System Installation
- **Linux/macOS**: `/usr/local/bin/dodo`
- **Windows**: `C:\PythonXX\Scripts\dodo.exe`

### User Installation
- **Linux/macOS**: `~/.local/bin/dodo`
- **Windows**: `%APPDATA%\Python\PythonXX\Scripts\dodo.exe`

### Development Installation
- **Virtual Environment**: `venv/bin/dodo` or `venv\Scripts\dodo.exe`

## 🔐 Permissions

DODO CLI may require the following permissions:

- **Read**: Access to robotics data files
- **Write**: Create projects and export datasets
- **Network**: For authentication and updates

## 🌐 Offline Usage

DODO CLI works offline after installation, except for:
- Initial authentication
- Version updates
- Cloud features (future)

---

**Need help? Contact us at support@dodo-robotics.com** 📧
