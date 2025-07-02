"""Image processing utilities for converting and resizing images."""

import os
import logging
from glob import glob
from pathlib import Path
from typing import List, Union, Tuple, Optional
from io import BytesIO

from PIL import Image
import streamlit as st

from .config import (
    SUPPORTED_EXTENSIONS,
    OUTPUT_DIRECTORY,
    JPEG_QUALITY,
    RESIZE_ALGORITHM,
)

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles image conversion and resizing operations."""

    def __init__(self, output_dir: str = OUTPUT_DIRECTORY) -> None:
        """Initialize the ImageProcessor.
        
        Args:
            output_dir: Directory to save processed images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def find_images(self, directory: str = ".") -> List[str]:
        """Find all supported image files in a directory.
        
        Args:
            directory: Directory path to search for images
            
        Returns:
            List of image file paths
        """
        files = []
        dir_path = Path(directory)
        
        for ext in SUPPORTED_EXTENSIONS:
            pattern = f"*.{ext}"
            files.extend(glob(str(dir_path / pattern)))
            # Also search for uppercase extensions
            files.extend(glob(str(dir_path / pattern.upper())))
        
        logger.info(f"Found {len(files)} image files in {directory}")
        return files

    def _calculate_new_dimensions(
        self, width: int, height: int, max_resolution: int
    ) -> Tuple[int, int]:
        """Calculate new dimensions while maintaining aspect ratio.
        
        Args:
            width: Original width
            height: Original height
            max_resolution: Maximum dimension allowed
            
        Returns:
            Tuple of (new_width, new_height)
        """
        if width > height:
            new_width = min(width, max_resolution)
            new_height = int(height * (new_width / width))
        else:
            new_height = min(height, max_resolution)
            new_width = int(width * (new_height / height))
        
        return new_width, new_height

    def _prepare_image_for_format(self, img: Image.Image, output_format: str) -> Image.Image:
        """Prepare image for specific output format.
        
        Args:
            img: PIL Image object
            output_format: Target format (jpg, png, etc.)
            
        Returns:
            Processed PIL Image object
        """
        if output_format.lower() == "jpg" and img.mode in ("RGBA", "P"):
            # Convert to RGB for JPEG format
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            return background
        
        return img

    def convert_image(
        self,
        file_input: Union[str, st.runtime.uploaded_file_manager.UploadedFile],
        output_format: str,
        max_resolution: Optional[int] = None,
        enable_resizing: bool = True,
    ) -> bool:
        """Convert and optionally resize an image.
        
        Args:
            file_input: File path string or uploaded file object
            output_format: Target format (jpg, png, etc.)
            max_resolution: Maximum dimension for resizing
            enable_resizing: Whether to resize the image
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Determine file name and open image
            if isinstance(file_input, str):
                base_name = Path(file_input).stem
                img = Image.open(file_input)
            else:
                base_name = Path(file_input.name).stem
                img = Image.open(file_input)

            # Prepare image for output format
            img = self._prepare_image_for_format(img, output_format)

            # Resize if enabled
            if enable_resizing and max_resolution:
                width, height = img.size
                new_width, new_height = self._calculate_new_dimensions(
                    width, height, max_resolution
                )
                
                # Only resize if the image is larger than max_resolution
                if new_width < width or new_height < height:
                    resample = getattr(Image.Resampling, RESIZE_ALGORITHM, Image.Resampling.LANCZOS)
                    img = img.resize((new_width, new_height), resample)
                    output_filename = f"{base_name}_{max_resolution}.{output_format}"
                else:
                    output_filename = f"{base_name}.{output_format}"
            else:
                output_filename = f"{base_name}.{output_format}"

            # Save the image
            output_path = self.output_dir / output_filename
            save_kwargs = {}
            
            if output_format.lower() in ["jpg", "jpeg"]:
                save_kwargs["quality"] = JPEG_QUALITY
                save_kwargs["optimize"] = True
            
            img.save(output_path, **save_kwargs)
            logger.info(f"Successfully converted: {base_name} -> {output_filename}")
            return True

        except Exception as e:
            error_name = getattr(file_input, 'name', str(file_input))
            logger.error(f"Error converting {error_name}: {str(e)}")
            return False

    def process_batch(
        self,
        files: List[Union[str, st.runtime.uploaded_file_manager.UploadedFile]],
        output_format: str,
        max_resolution: Optional[int] = None,
        enable_resizing: bool = True,
        progress_callback: Optional[callable] = None,
    ) -> Tuple[int, int]:
        """Process a batch of images.
        
        Args:
            files: List of file paths or uploaded file objects
            output_format: Target format
            max_resolution: Maximum dimension for resizing
            enable_resizing: Whether to resize images
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (converted_count, failed_count)
        """
        total_files = len(files)
        converted_count = 0
        failed_count = 0

        for i, file_input in enumerate(files):
            success = self.convert_image(
                file_input, output_format, max_resolution, enable_resizing
            )
            
            if success:
                converted_count += 1
            else:
                failed_count += 1

            # Call progress callback if provided
            if progress_callback:
                progress = (i + 1) / total_files
                progress_callback(progress, i + 1, total_files)

        logger.info(
            f"Batch processing complete: {converted_count} converted, {failed_count} failed"
        )
        return converted_count, failed_count