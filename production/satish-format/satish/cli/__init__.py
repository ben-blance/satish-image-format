"""
SATISH Image Format - Command Line Interface Module

This module provides a comprehensive command-line interface for the SATISH image format.
It includes commands for converting, validating, and managing SATISH files.

Usage:
    satish convert image.jpg output.satish
    satish extract file.satish image.png
    satish info file.satish
    satish validate file.satish
    satish batch ./images
    satish list ./directory

Commands:
    convert  - Convert images to SATISH format
    extract  - Extract SATISH files to standard image formats
    info     - Display file information and metadata
    validate - Validate SATISH file integrity
    batch    - Batch process multiple files
    list     - List and filter files in directories
    help     - Show detailed help information
"""

# Import main CLI components
from .main import main, cli_entry_point
from .commands import SatishCLI, print_help, print_version

# Version info
__version__ = "1.0.0"
__author__ = "SATISH Format Team"

# Public API
__all__ = [
    'main',
    'cli_entry_point', 
    'SatishCLI',
    'print_help',
    'print_version'
]