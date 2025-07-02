# 🖼️ Image Converter and Resizer

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional, user-friendly Streamlit application for converting and resizing images with support for multiple formats including HEIC. Built with a clean architecture, comprehensive error handling, and modern Python best practices.

## ✨ Features

- **Multi-format Support**: Convert between JPG, PNG, GIF, TIFF, BMP, and HEIC formats
- **Smart Resizing**: Resize images while maintaining aspect ratio
- **Flexible Input**: Process images from local directory or via drag-and-drop upload
- **Batch Processing**: Handle multiple images simultaneously with progress tracking
- **Quality Control**: Optimized output with configurable quality settings
- **Real-time Logging**: Detailed processing logs with timestamps
- **Modern UI**: Clean, responsive interface with emoji icons and helpful tooltips

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Poetry (recommended) or pip

### Installation

#### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/jbone3311/image-converter-resizer.git
cd image-converter-resizer

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the application
streamlit run src/main.py
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/jbone3311/image-converter-resizer.git
cd image-converter-resizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/main.py
```

## 📖 Usage

1. **Launch the Application**
   ```bash
   streamlit run src/main.py
   ```

2. **Configure Settings** (via sidebar)
   - Select output format (JPG, PNG, GIF, TIFF, BMP)
   - Enable/disable resizing
   - Choose maximum resolution (256px to 4096px)

3. **Choose Input Source**
   - **Current Directory**: Process all images in the current folder
   - **File Upload**: Drag and drop or select specific files

4. **Process Images**
   - Click "🚀 Start Processing"
   - Monitor progress with the built-in progress bar
   - View results and check logs for details

5. **Access Output**
   - Converted images are saved in the `OUTPUT/` directory
   - Files are automatically named with format and resolution suffixes

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
src/
├── __init__.py          # Package initialization
├── main.py              # Streamlit UI and main application logic
├── image_processor.py   # Core image processing functionality
└── config.py            # Configuration constants and settings
```

### Key Components

- **`ImageProcessor`**: Handles all image conversion and resizing operations
- **`StreamlitLogHandler`**: Custom logging handler for real-time log display
- **Configuration Management**: Centralized settings in `config.py`
- **Type Safety**: Full type hints throughout the codebase

## 🔧 Configuration

The application can be configured by modifying `src/config.py`:

```python
# Supported formats
OUTPUT_FORMATS = ["jpg", "png", "gif", "tiff", "bmp"]

# Resolution options
RESOLUTION_OPTIONS = [256, 512, 1024, 2048, 4096]

# Quality settings
JPEG_QUALITY = 95
```

## 🧪 Development

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality

## 📋 Requirements

### Core Dependencies
- `streamlit ^1.38.0` - Web application framework
- `pillow ^10.4.0` - Image processing library
- `glob2 ^0.7` - Advanced file globbing

### Development Dependencies
- `pytest ^7.4.0` - Testing framework
- `black ^23.0.0` - Code formatter
- `isort ^5.12.0` - Import sorter
- `flake8 ^6.0.0` - Linter
- `mypy ^1.5.0` - Type checker

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`poetry run pytest && poetry run black src/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the excellent web app framework
- **Pillow** - For robust image processing capabilities
- **Python Community** - For the amazing ecosystem of tools and libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/jbone3311/image-converter-resizer/issues) page
2. Create a new issue with detailed information
3. Include error logs and steps to reproduce

---

**Made with ❤️ by jBone**
