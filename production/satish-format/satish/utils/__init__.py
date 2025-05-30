"""
Utilities for SATISH image format.
Provides file handling, color conversion, and exception classes.
"""

from typing import Dict, List, Optional

# Import exceptions - using exact names from exceptions.py
from .exceptions import (
    # Base exception
    SatishError,
    
    # Format-related exceptions
    InvalidFormatError,
    UnsupportedVersionError,
    DimensionError,
    PixelDataError,
    HeaderError,
    
    # Operation exceptions
    EncodingError,
    DecodingError,
    ValidationError,
    FileError,
    ColorConversionError,
    ChecksumError,
    
    # Convenience functions
    raise_invalid_magic,
    raise_dimension_error,
    raise_pixel_error,
    raise_unsupported_version,
    raise_file_not_found,
    raise_file_permission_error,
    raise_encoding_error,
    raise_decoding_error
)

# Import file utilities - using exact names from file_utils.py
try:
    from .file_utils import (
        FileManager,
        get_file_info,
        format_file_size,
        batch_operation
    )
    _file_utils_available = True
except ImportError:
    # File utils not implemented yet
    FileManager = None
    get_file_info = None
    format_file_size = None
    batch_operation = None
    _file_utils_available = False

# Import color utilities - using exact names from colors.py
try:
    from .colors import ColorConverter, ColorPalette
    _colors_available = True
except ImportError:
    # Color module not implemented yet
    ColorConverter = None
    ColorPalette = None
    _colors_available = False

# Public API - what users can import from satish.utils
__all__ = [
    # Exceptions - Base
    'SatishError',
    
    # Exceptions - Format related
    'InvalidFormatError',
    'UnsupportedVersionError', 
    'DimensionError',
    'PixelDataError',
    'HeaderError',
    
    # Exceptions - Operations
    'EncodingError',
    'DecodingError',
    'ValidationError',
    'FileError',
    'ColorConversionError',
    'ChecksumError',
    
    # Exception convenience functions
    'raise_invalid_magic',
    'raise_dimension_error',
    'raise_pixel_error',
    'raise_unsupported_version', 
    'raise_file_not_found',
    'raise_file_permission_error',
    'raise_encoding_error',
    'raise_decoding_error',
]

# Add file utilities to __all__ if available
if _file_utils_available:
    __all__.extend([
        'FileManager',
        'get_file_info',
        'format_file_size',
        'batch_operation',
    ])

# Add color utilities to __all__ if available
if _colors_available:
    __all__.extend(['ColorConverter', 'ColorPalette'])

# Module info
__version__ = "1.0.0"
__author__ = "SATISH Format Team"

# Utility functions for module introspection
def get_available_exceptions() -> List[str]:
    """Get list of all available exception classes."""
    return [name for name in __all__ if name.endswith('Error')]


def get_available_utilities() -> List[str]:
    """Get list of all utility classes."""
    utilities = []
    if _file_utils_available:
        utilities.append('FileManager')
    if _colors_available:
        utilities.extend(['ColorConverter', 'ColorPalette'])
    return utilities


def check_dependencies() -> Dict[str, bool]:
    """Check which optional dependencies are available."""
    return {
        'colors': _colors_available,
        'file_utils': _file_utils_available,
        'exceptions': True,  # Always available
    }


# Add utility functions to __all__
__all__.extend(['get_available_exceptions', 'get_available_utilities', 'check_dependencies'])

# Debug info (only in debug mode)
if __debug__:
    def _debug_info() -> None:
        """Print debug information about available components."""
        available = [name for name in __all__ if globals().get(name) is not None]
        missing = [name for name in __all__ if globals().get(name) is None]
        
        print(f"🔧 SATISH Utils v{__version__}")
        print(f"✅ Available: {len(available)} components")
        if missing:
            print(f"⚠️  Missing: {', '.join(missing)}")
        print(f"📦 Dependencies: {check_dependencies()}")
    
    # _debug_info()  # Uncomment to enable debug output