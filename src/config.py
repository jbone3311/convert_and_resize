"""Configuration constants for the Image Converter and Resizer application."""

from typing import List

# Application Configuration
APP_TITLE = "Image Converter and Resizer"
APP_AUTHOR = "jBone"
OUTPUT_DIRECTORY = "OUTPUT"

# Supported image formats
SUPPORTED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "tiff", "bmp", "heic"]
OUTPUT_FORMATS: List[str] = ["jpg", "png", "gif", "tiff", "bmp"]

# Resolution options
RESOLUTION_OPTIONS: List[int] = [256, 512, 1024, 2048, 4096]
DEFAULT_RESOLUTION_INDEX = 1  # 512px

# Image processing settings
JPEG_QUALITY = 95
RESIZE_ALGORITHM = "LANCZOS"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"