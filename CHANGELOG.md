# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-02

### Added
- 🎉 Initial release of DODO CLI
- 🤖 Multimodal robotics dataset creation
- 📦 Support for ROS bags, JSON, and JSONL formats
- ⚡ Automatic sensor data synchronization and alignment
- 🔐 User authentication and API key management
- 📊 Comprehensive metadata generation
- 🧹 Duplicate detection and filtering
- ✅ Dataset validation
- 📤 Structured dataset export
- 🎥 Camera, IMU, LiDAR, and action data support
- 📖 Complete documentation and examples
- 🧪 Comprehensive test suite
- 🏗️ Professional project structure

### Features
- **CLI Interface**: Beautiful command-line interface with Typer
- **Temporal Alignment**: Nearest-neighbor sensor data synchronization
- **Security**: Built-in user management and authentication
- **Metadata**: Rich dataset metadata for ML workflows
- **Validation**: Dataset integrity and structure validation
- **Export**: Multiple export formats for ML pipelines
- **Filtering**: Smart duplicate detection and removal
- **Project Management**: Complete project lifecycle management

### Supported Formats
- ROS bags (.bag)
- JSON logs (.json)
- JSONL logs (.jsonl)
- Mock data generation

### Sensor Modalities
- Camera frames with file paths
- IMU data (linear acceleration, angular velocity)
- LiDAR point clouds
- Robot action commands

### Documentation
- Comprehensive README with examples
- API documentation
- Contributing guidelines
- License information
- Changelog

### Development
- Pydantic models for data validation
- Type hints throughout
- Comprehensive test coverage
- Development tools configuration
- CI/CD ready structure

## [Unreleased]

### Planned
- Web interface for dataset management
- Cloud storage integration
- Advanced filtering algorithms
- Real-time data streaming support
- Additional sensor modalities
- Performance optimizations
- Plugin system for custom importers

---

## Version History

- **1.0.0** - Initial public release
- Future versions will follow semantic versioning
