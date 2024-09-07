''' Create a executable file from this script using the following command: 
    pyinstaller --onefile --noconsole Convert_and_Resize_512.py
streamlit run convert_and_resizeV2_0.py 
'''

import os
import streamlit as st
from PIL import Image
from glob import glob
import subprocess
import shutil
import logging
from io import StringIO


# Configuration Constants
OUTPUT_DIRECTORY = "OUTPUT"


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# Create a StringIO object to capture log output
log_stream = StringIO()
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)


def find_files(directory="."):
    extensions = ["jpg", "jpeg", "png", "gif", "tiff", "bmp", "heic"]
    files = []
    for ext in extensions:
        files.extend(glob(os.path.join(directory, f"*.{ext}")))
    return files


def convert_image(file, output_format, max_resolution, enable_resizing):
    try:
        if isinstance(file, str):
            # File is a path string
            base_name = os.path.splitext(os.path.basename(file))[0]
            img = Image.open(file)
        else:
            # File is an uploaded file object
            base_name = os.path.splitext(file.name)[0]
            img = Image.open(file)

        if output_format.lower() == "jpg" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if enable_resizing:
            # Calculate the new dimensions while maintaining aspect ratio
            width, height = img.size
            if width > height:
                new_width = min(width, max_resolution)
                new_height = int(height * (new_width / width))
            else:
                new_height = min(height, max_resolution)
                new_width = int(width * (new_height / height))
            img = img.resize((new_width, new_height), Image.LANCZOS)
            output_file = os.path.join(OUTPUT_DIRECTORY, f"{base_name}_{max_resolution}.{output_format}")
        else:
            output_file = os.path.join(OUTPUT_DIRECTORY, f"{base_name}.{output_format}")

        img.save(output_file, quality=95)
        logger.info(f"Converted and resized: {base_name} to {os.path.basename(output_file)}")
        return True
    except Exception as e:
        logger.error(f"Error converting {base_name}: {e}")
        return False


def process_images(files, output_format, max_resolution, enable_resizing):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    total_files = len(files)
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    converted_count = 0
    failed_count = 0

    for i, file in enumerate(files):
        if convert_image(file, output_format, max_resolution, enable_resizing):
            converted_count += 1
        else:
            failed_count += 1
        
        # Update progress
        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        status_text.text(f"Processing: {i+1}/{total_files}")

    status_text.text(f"Conversion complete. {converted_count} files converted to {output_format.upper()}. {failed_count} files failed to convert.")


def main():
    st.set_page_config(layout="wide", page_title="jBone - Image Converter and Resizer")
    st.title("jBone - Image Converter and Resizer")

    col1, col2 = st.columns(2)

    with col1:
        output_format = st.selectbox("Output Format", ["jpg", "png", "gif", "tiff", "bmp"])
        enable_resizing = st.checkbox("Enable Resizing", value=True)
        max_resolution = st.selectbox("Max Resolution", [256, 512, 1024, 2048, 4096], index=1, disabled=not enable_resizing)

    with col2:
        use_cwd = st.checkbox("Use Current Working Directory", value=True)
        if use_cwd:
            st.info(f"Using current directory: {os.getcwd()}")
            files = find_files(os.getcwd())
            st.write(f"Found {len(files)} files in the current directory.")
        else:
            uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'heic'])
            files = uploaded_files if uploaded_files else []

    if st.button("Start Processing", type="primary"):
        if files:
            process_images(files, output_format, max_resolution, enable_resizing)
        else:
            st.warning("No files selected for processing.")

    # Display log messages
    st.subheader("Log Output")
    log_output = st.empty()

    # Update log output
    def update_log():
        log_output.code(log_stream.getvalue(), language="plaintext")

    # Run the log update function
    update_log()


if __name__ == "__main__":
    main()
