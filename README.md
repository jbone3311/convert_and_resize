# Image Converter and Resizer

## Description
This Streamlit application provides a user-friendly interface for converting and resizing image files. It supports various image formats and allows users to process images either from the current working directory or via drag-and-drop file upload.

## Features
- Convert images to different formats (jpg, png, gif, tiff, bmp)
- Resize images to predefined resolutions (256, 512, 1024, 2048, 4096 pixels)
- Process images from the current working directory or via file upload
- Support for multiple image formats including HEIC
- Progress bar and status updates during processing
- Detailed logging of conversion process

## Installation

### Prerequisites
- Python 3.6+
- pip

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/jbone3311/image-converter-resizer.git
   cd image-converter-resizer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```
   streamlit run convert_and_resizeV2_0.py
   ```

2. Open the provided URL in your web browser.

3. Choose your settings:
   - Select the output format
   - Enable or disable resizing
   - Choose the max resolution (if resizing is enabled)
   - Select whether to use the current working directory or upload files

4. Click "Start Processing" to begin the conversion and resizing process.

5. Monitor the progress and check the log output for details on each processed file.

## Notes
- For HEIC file conversion, ensure that ImageMagick is installed and accessible in your system's PATH.
- The application will create an "OUTPUT" directory to store the processed images.
