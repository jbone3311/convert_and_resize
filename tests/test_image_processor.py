"""Tests for the ImageProcessor class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from PIL import Image
import tempfile
import os

from src.image_processor import ImageProcessor


class TestImageProcessor:
    """Test cases for ImageProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.processor = ImageProcessor(output_dir=self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_output_directory(self):
        """Test that initialization creates the output directory."""
        assert self.processor.output_dir.exists()
        assert self.processor.output_dir.is_dir()

    @patch('src.image_processor.glob')
    def test_find_images_returns_supported_files(self, mock_glob):
        """Test that find_images returns files with supported extensions."""
        mock_glob.return_value = ['test.jpg', 'test.png', 'test.gif']
        
        files = self.processor.find_images('/test/directory')
        
        assert len(files) == 3
        assert 'test.jpg' in files
        assert 'test.png' in files
        assert 'test.gif' in files

    def test_calculate_new_dimensions_landscape(self):
        """Test dimension calculation for landscape images."""
        new_width, new_height = self.processor._calculate_new_dimensions(
            1920, 1080, 1024
        )
        
        assert new_width == 1024
        assert new_height == 576  # Maintains aspect ratio

    def test_calculate_new_dimensions_portrait(self):
        """Test dimension calculation for portrait images."""
        new_width, new_height = self.processor._calculate_new_dimensions(
            1080, 1920, 1024
        )
        
        assert new_width == 576  # Maintains aspect ratio
        assert new_height == 1024

    def test_calculate_new_dimensions_no_resize_needed(self):
        """Test dimension calculation when image is smaller than max."""
        new_width, new_height = self.processor._calculate_new_dimensions(
            512, 384, 1024
        )
        
        assert new_width == 512
        assert new_height == 384

    @patch('src.image_processor.Image')
    def test_prepare_image_for_jpg_format(self, mock_image):
        """Test image preparation for JPEG format."""
        # Create a mock RGBA image
        mock_img = Mock()
        mock_img.mode = 'RGBA'
        mock_img.size = (100, 100)
        mock_img.split.return_value = [Mock(), Mock(), Mock(), Mock()]
        
        # Mock the new RGB background image
        mock_background = Mock()
        mock_image.new.return_value = mock_background
        
        result = self.processor._prepare_image_for_format(mock_img, 'jpg')
        
        # Should create a new RGB background
        mock_image.new.assert_called_once_with('RGB', (100, 100), (255, 255, 255))
        # Should paste the original image onto the background
        mock_background.paste.assert_called_once()

    def test_prepare_image_for_png_format(self):
        """Test image preparation for PNG format (no changes needed)."""
        mock_img = Mock()
        mock_img.mode = 'RGBA'
        
        result = self.processor._prepare_image_for_format(mock_img, 'png')
        
        assert result is mock_img  # Should return the original image unchanged

    @patch('src.image_processor.Image')
    def test_convert_image_success(self, mock_image):
        """Test successful image conversion."""
        # Create a mock image
        mock_img = Mock()
        mock_img.mode = 'RGB'
        mock_img.size = (1920, 1080)
        mock_image.open.return_value = mock_img
        
        # Test conversion
        success = self.processor.convert_image(
            '/test/image.jpg', 'png', 1024, True
        )
        
        assert success is True
        mock_img.save.assert_called_once()

    @patch('src.image_processor.Image')
    def test_convert_image_failure(self, mock_image):
        """Test image conversion failure handling."""
        # Make Image.open raise an exception
        mock_image.open.side_effect = Exception("File not found")
        
        success = self.processor.convert_image(
            '/test/nonexistent.jpg', 'png', 1024, True
        )
        
        assert success is False

    @patch.object(ImageProcessor, 'convert_image')
    def test_process_batch_success(self, mock_convert):
        """Test batch processing with successful conversions."""
        mock_convert.return_value = True
        files = ['image1.jpg', 'image2.png', 'image3.gif']
        
        converted, failed = self.processor.process_batch(
            files, 'jpg', 1024, True
        )
        
        assert converted == 3
        assert failed == 0
        assert mock_convert.call_count == 3

    @patch.object(ImageProcessor, 'convert_image')
    def test_process_batch_mixed_results(self, mock_convert):
        """Test batch processing with mixed success/failure results."""
        mock_convert.side_effect = [True, False, True]  # Success, fail, success
        files = ['image1.jpg', 'image2.png', 'image3.gif']
        
        converted, failed = self.processor.process_batch(
            files, 'jpg', 1024, True
        )
        
        assert converted == 2
        assert failed == 1

    def test_process_batch_with_progress_callback(self):
        """Test batch processing with progress callback."""
        callback = Mock()
        files = ['image1.jpg']
        
        with patch.object(self.processor, 'convert_image', return_value=True):
            self.processor.process_batch(
                files, 'jpg', 1024, True, callback
            )
        
        callback.assert_called_once_with(1.0, 1, 1)