"""Main Streamlit application for Image Converter and Resizer."""

import os
import logging
from io import StringIO
from typing import List, Union

import streamlit as st

from .config import (
    APP_TITLE,
    APP_AUTHOR,
    OUTPUT_FORMATS,
    RESOLUTION_OPTIONS,
    DEFAULT_RESOLUTION_INDEX,
    LOG_FORMAT,
    LOG_LEVEL,
)
from .image_processor import ImageProcessor


class StreamlitLogHandler(logging.Handler):
    """Custom logging handler for Streamlit applications."""
    
    def __init__(self):
        super().__init__()
        self.log_stream = StringIO()
        
    def emit(self, record):
        log_entry = self.format(record)
        self.log_stream.write(log_entry + '\n')
        
    def get_logs(self) -> str:
        return self.log_stream.getvalue()
        
    def clear_logs(self):
        self.log_stream = StringIO()


def setup_logging() -> StreamlitLogHandler:
    """Setup logging configuration for the application."""
    # Clear any existing handlers
    logging.getLogger().handlers = []
    
    # Create custom handler
    streamlit_handler = StreamlitLogHandler()
    streamlit_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        handlers=[streamlit_handler],
        format=LOG_FORMAT
    )
    
    return streamlit_handler


def create_sidebar() -> dict:
    """Create and return sidebar configuration options."""
    st.sidebar.header("Configuration")
    
    config = {
        'output_format': st.sidebar.selectbox(
            "Output Format", 
            OUTPUT_FORMATS,
            help="Select the desired output image format"
        ),
        'enable_resizing': st.sidebar.checkbox(
            "Enable Resizing", 
            value=True,
            help="Enable or disable image resizing"
        )
    }
    
    config['max_resolution'] = st.sidebar.selectbox(
        "Max Resolution (pixels)", 
        RESOLUTION_OPTIONS, 
        index=DEFAULT_RESOLUTION_INDEX,
        disabled=not config['enable_resizing'],
        help="Maximum dimension for the resized image"
    )
    
    return config


def get_input_files() -> List[Union[str, st.runtime.uploaded_file_manager.UploadedFile]]:
    """Get input files from user selection."""
    st.header("Input Source")
    
    col1, col2 = st.columns(2)
    
    with col1:
        use_cwd = st.checkbox(
            "Use Current Working Directory", 
            value=True,
            help="Process all images in the current directory"
        )
    
    with col2:
        if use_cwd:
            processor = ImageProcessor()
            files = processor.find_images(os.getcwd())
            st.info(f"📁 Current directory: `{os.getcwd()}`")
            st.success(f"Found {len(files)} image file(s)")
            return files
        else:
            uploaded_files = st.file_uploader(
                "Choose image files",
                accept_multiple_files=True,
                type=['png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'heic'],
                help="Upload one or more image files to process"
            )
            if uploaded_files:
                st.success(f"Uploaded {len(uploaded_files)} file(s)")
            return uploaded_files or []


def display_processing_results(converted_count: int, failed_count: int, output_format: str):
    """Display processing results with appropriate styling."""
    st.header("Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Converted", converted_count)
    
    with col2:
        st.metric("❌ Failed", failed_count)
    
    with col3:
        st.metric("📁 Output Format", output_format.upper())
    
    if converted_count > 0:
        st.success(f"Successfully converted {converted_count} image(s) to {output_format.upper()} format!")
        st.info("📂 Check the 'OUTPUT' directory for your converted images.")
    
    if failed_count > 0:
        st.error(f"Failed to convert {failed_count} image(s). Check the logs below for details.")


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title=f"{APP_AUTHOR} - {APP_TITLE}",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Setup logging
    log_handler = setup_logging()
    
    # Main title
    st.title(f"🖼️ {APP_AUTHOR} - {APP_TITLE}")
    st.markdown("Convert and resize your images with ease!")
    
    # Sidebar configuration
    config = create_sidebar()
    
    # File input section
    files = get_input_files()
    
    # Processing section
    st.header("Processing")
    
    if st.button("🚀 Start Processing", type="primary", disabled=len(files) == 0):
        if files:
            processor = ImageProcessor()
            
            # Clear previous logs
            log_handler.clear_logs()
            
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def progress_callback(progress: float, current: int, total: int):
                progress_bar.progress(progress)
                status_text.text(f"Processing: {current}/{total} files...")
            
            # Process images
            with st.spinner("Processing images..."):
                converted_count, failed_count = processor.process_batch(
                    files,
                    config['output_format'],
                    config['max_resolution'] if config['enable_resizing'] else None,
                    config['enable_resizing'],
                    progress_callback
                )
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            display_processing_results(converted_count, failed_count, config['output_format'])
            
        else:
            st.warning("⚠️ No files selected for processing.")
    
    # Log output section
    with st.expander("📋 Log Output", expanded=False):
        logs = log_handler.get_logs()
        if logs:
            st.code(logs, language="plaintext")
        else:
            st.info("No logs available. Start processing to see logs.")


if __name__ == "__main__":
    main()