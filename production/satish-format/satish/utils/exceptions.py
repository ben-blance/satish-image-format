"""
SATISH Image Format Custom Exceptions
Defines all custom exception classes used throughout the SATISH library
"""

from typing import List, Optional, Union


class SatishError(Exception):
    """Base exception class for all SATISH-related errors"""
    pass


class InvalidFormatError(SatishError):
    """Raised when a file doesn't conform to SATISH format specification"""
    pass


class EncodingError(SatishError):
    """Raised when encoding an image to SATISH format fails"""
    pass


class DecodingError(SatishError):
    """Raised when decoding a SATISH file fails"""
    pass


class ValidationError(SatishError):
    """Raised when validation of SATISH data fails"""
    pass


class FileError(SatishError):
    """Raised when file I/O operations fail"""
    pass


class ColorConversionError(SatishError):
    """Raised when color format conversion fails"""
    pass


# Specific InvalidFormatError subclasses
class UnsupportedVersionError(InvalidFormatError):
    """Raised when encountering an unsupported SATISH format version"""
    
    def __init__(self, version: int, supported_versions: Optional[List[int]] = None):
        self.version = version
        self.supported_versions = supported_versions or [1]
        
        if supported_versions:
            msg = f"Unsupported SATISH version {version}. Supported versions: {supported_versions}"
        else:
            msg = f"Unsupported SATISH version {version}"
            
        super().__init__(msg)


class DimensionError(InvalidFormatError):
    """Raised when image dimensions are invalid or unsupported"""
    
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None, 
                 message: Optional[str] = None):
        self.width = width
        self.height = height
        
        if message:
            super().__init__(message)
        elif width is not None and height is not None:
            super().__init__(f"Invalid dimensions: {width}x{height}")
        else:
            super().__init__("Invalid image dimensions")


class PixelDataError(InvalidFormatError):
    """Raised when pixel data is corrupted or invalid"""
    
    def __init__(self, message: str, pixel_index: Optional[int] = None):
        self.pixel_index = pixel_index
        
        if pixel_index is not None:
            msg = f"Pixel data error at index {pixel_index}: {message}"
        else:
            msg = f"Pixel data error: {message}"
            
        super().__init__(msg)


class HeaderError(InvalidFormatError):
    """Raised when SATISH file header is invalid or corrupted"""
    
    def __init__(self, field: Optional[str] = None, value: Optional[Union[str, int, bytes]] = None, 
                 message: Optional[str] = None):
        self.field = field
        self.value = value
        
        if message:
            super().__init__(message)
        elif field and value is not None:
            super().__init__(f"Invalid header field '{field}': {value}")
        elif field:
            super().__init__(f"Invalid header field: {field}")
        else:
            super().__init__("Invalid SATISH file header")


# Specific ValidationError subclasses
class ChecksumError(ValidationError):
    """Raised when file integrity check fails"""
    
    def __init__(self, expected: Optional[Union[str, int]] = None, 
                 actual: Optional[Union[str, int]] = None):
        self.expected = expected
        self.actual = actual
        
        if expected is not None and actual is not None:
            super().__init__(f"Checksum mismatch: expected {expected}, got {actual}")
        else:
            super().__init__("File integrity check failed")


# Convenience functions for raising common errors
def raise_invalid_magic(actual_magic: bytes, expected_magic: bytes = b"SATI") -> None:
    """Raise InvalidFormatError for wrong magic bytes"""
    raise InvalidFormatError(f"Invalid magic bytes: expected {expected_magic}, got {actual_magic}")


def raise_dimension_error(width: int, height: int, max_width: int = 65535, 
                         max_height: int = 65535) -> None:
    """Raise DimensionError for invalid dimensions"""
    if width < 1 or width > max_width:
        raise DimensionError(width, height, f"Width must be between 1 and {max_width}")
    if height < 1 or height > max_height:
        raise DimensionError(width, height, f"Height must be between 1 and {max_height}")


def raise_pixel_error(message: str, pixel_index: Optional[int] = None) -> None:
    """Raise PixelDataError with optional pixel index"""
    raise PixelDataError(message, pixel_index)


def raise_unsupported_version(version: int, supported: Optional[List[int]] = None) -> None:
    """Raise UnsupportedVersionError"""
    raise UnsupportedVersionError(version, supported)


def raise_file_not_found(file_path: str) -> None:
    """Raise FileError for missing file"""
    raise FileError(f"File not found: {file_path}")


def raise_file_permission_error(file_path: str, operation: str = "access") -> None:
    """Raise FileError for permission issues"""
    raise FileError(f"Permission denied: cannot {operation} {file_path}")


def raise_encoding_error(source: str, details: Optional[str] = None) -> None:
    """Raise EncodingError with context"""
    if details:
        raise EncodingError(f"Failed to encode {source}: {details}")
    else:
        raise EncodingError(f"Failed to encode {source}")


def raise_decoding_error(source: str, details: Optional[str] = None) -> None:
    """Raise DecodingError with context"""
    if details:
        raise DecodingError(f"Failed to decode {source}: {details}")
    else:
        raise DecodingError(f"Failed to decode {source}")


# Export list for explicit imports
__all__ = [
    # Base exceptions
    'SatishError',
    'InvalidFormatError', 
    'EncodingError',
    'DecodingError',
    'ValidationError',
    'FileError',
    'ColorConversionError',
    
    # Specific exceptions
    'UnsupportedVersionError',
    'DimensionError',
    'PixelDataError', 
    'HeaderError',
    'ChecksumError',
    
    # Convenience functions
    'raise_invalid_magic',
    'raise_dimension_error',
    'raise_pixel_error',
    'raise_unsupported_version',
    'raise_file_not_found',
    'raise_file_permission_error',
    'raise_encoding_error',
    'raise_decoding_error',
]