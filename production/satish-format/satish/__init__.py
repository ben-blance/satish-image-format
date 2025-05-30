"""
SATISH Image Format - Python Implementation

A modern, efficient image format with advanced compression and metadata support.

This package provides:
- Core format implementation (encoding/decoding)
- Command-line interface
- File validation and utilities
- Comprehensive metadata support

Basic Usage:
    >>> from satish import SatishEncoder, SatishDecoder
    >>> encoder = SatishEncoder()
    >>> encoder.encode_image('input.jpg', 'output.satish')
    >>> 
    >>> decoder = SatishDecoder()
    >>> decoder.decode_to_image('input.satish', 'output.png')

CLI Usage:
    $ satish convert image.jpg
    $ satish extract file.satish
    $ satish info file.satish
"""

# Version information
__version__ = "1.0.0"
__author__ = "SATISH Format Team"
__email__ = "contact@satishformat.dev"
__license__ = "MIT"
__url__ = "https://github.com/satish-format/satish-python"

# Import core classes
try:
    from .core.encoder import SatishEncoder
    from .core.decoder import SatishDecoder
    from .core.validator import SatishValidator
    from .core.format import SatishFormat
except ImportError:
    # Handle case where core modules might not be fully implemented yet
    SatishEncoder = None
    SatishDecoder = None
    SatishValidator = None
    SatishFormat = None

# Import utilities
try:
    from .utils.file_utils import FileManager
except ImportError:
    FileManager = None

try:
    from .utils.colors import ColorConverter, ColorPalette
except ImportError:
    ColorConverter = None
    ColorPalette = None

# Import exceptions explicitly (no wildcards)
try:
    from .utils.exceptions import (
        SatishError,
        InvalidFormatError,
        EncodingError,
        DecodingError,
        ValidationError,
        FileError,
        ColorConversionError,
        UnsupportedVersionError,
        DimensionError,
        PixelDataError,
        HeaderError,
        ChecksumError
    )
except ImportError:
    # Fallback definitions
    SatishError = None
    InvalidFormatError = None
    EncodingError = None
    DecodingError = None
    ValidationError = None
    FileError = None
    ColorConversionError = None
    UnsupportedVersionError = None
    DimensionError = None
    PixelDataError = None
    HeaderError = None
    ChecksumError = None

# Import CLI (optional, as it's mainly for command-line use)
try:
    from .cli.main import main as cli_main
    from .cli.commands import SatishCLI
except ImportError:
    cli_main = None
    SatishCLI = None

# Public API - main classes and functions users should import
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__license__',
    
    # Core classes
    'SatishEncoder',
    'SatishDecoder', 
    'SatishValidator',
    'SatishFormat',
    
    # Utilities
    'FileManager',
    'ColorConverter',
    'ColorPalette',
    
    # Exceptions
    'SatishError',
    'InvalidFormatError',
    'EncodingError',
    'DecodingError',
    'ValidationError',
    'FileError',
    'ColorConversionError',
    'UnsupportedVersionError',
    'DimensionError',
    'PixelDataError',
    'HeaderError',
    'ChecksumError',
    
    # CLI (for programmatic use)
    'SatishCLI',
    'cli_main',
]

# Package-level configuration
DEFAULT_QUALITY = 95
SUPPORTED_INPUT_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
SATISH_EXTENSION = '.satish'

def get_version():
    """Get the current version of the SATISH package."""
    return __version__

def get_supported_formats():
    """Get list of supported input image formats."""
    return SUPPORTED_INPUT_FORMATS.copy()

def quick_convert(input_path, output_path=None, quality=None):
    """
    Quick conversion function for simple use cases.
    
    Args:
        input_path (str): Path to input image
        output_path (str, optional): Path to output SATISH file
        quality (int, optional): Compression quality (1-100)
    
    Returns:
        bool: True if successful
    
    Example:
        >>> import satish
        >>> satish.quick_convert('photo.jpg', 'photo.satish', quality=90)
    """
    if SatishEncoder is None:
        raise ImportError("SatishEncoder not available. Please check your installation.")
    
    encoder = SatishEncoder()
    return encoder.encode_image(
        input_path, 
        output_path, 
        quality=quality or DEFAULT_QUALITY
    )

def quick_extract(input_path, output_path=None, format='png'):
    """
    Quick extraction function for simple use cases.
    
    Args:
        input_path (str): Path to input SATISH file
        output_path (str, optional): Path to output image file
        format (str): Output format ('png', 'jpg', etc.)
    
    Returns:
        bool: True if successful
    
    Example:
        >>> import satish
        >>> satish.quick_extract('photo.satish', 'photo.png')
    """
    if SatishDecoder is None:
        raise ImportError("SatishDecoder not available. Please check your installation.")
    
    decoder = SatishDecoder()
    return decoder.decode_to_image(input_path, output_path, output_format=format)

def validate_file(file_path):
    """
    Quick validation function.
    
    Args:
        file_path (str): Path to SATISH file
    
    Returns:
        bool: True if valid
    
    Example:
        >>> import satish
        >>> satish.validate_file('photo.satish')
    """
    if SatishValidator is None:
        raise ImportError("SatishValidator not available. Please check your installation.")
    
    validator = SatishValidator()
    result = validator.validate_file(file_path)
    return result.is_valid

# Add convenience functions to __all__
__all__.extend(['quick_convert', 'quick_extract', 'validate_file', 'get_version', 'get_supported_formats'])

# Package initialization message (only shown in debug mode)
def _init_debug():
    """Debug initialization - only runs if __debug__ is True."""
    if __debug__:
        available_components = [c for c in __all__ if globals().get(c) is not None]
        print(f"🖼️  SATISH Image Format v{__version__} loaded")
        print(f"📦 Available components: {', '.join(available_components)}")

# Run debug init
_init_debug()