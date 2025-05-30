"""
SATISH Image Format Validator
Provides validation and integrity checking for SATISH files
"""

import os
from typing import Union, List, Dict, Any, Tuple
from pathlib import Path

from .format import SatishFormat, SatishHeader
from ..utils.exceptions import (
    ValidationError, 
    InvalidFormatError, 
    FileError,
    HeaderError,
    PixelDataError,
    DimensionError,
    UnsupportedVersionError
)


class SatishValidator:
    """Validator for SATISH format files and data"""
    
    def __init__(self):
        self.format = SatishFormat()
    
    def validate_file(self, file_path: Union[str, os.PathLike]) -> Dict[str, Any]:
        """
        Comprehensive validation of a SATISH file
        
        Args:
            file_path: Path to .satish file
            
        Returns:
            dict: Validation results with details
            
        Raises:
            ValidationError: If file cannot be validated
        """
        results = {
            'valid': False,
            'file_path': str(file_path),
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        try:
            # Check file existence and readability
            self._validate_file_access(file_path, results)
            if results['errors']:
                return results
            
            # Check file extension
            self._validate_file_extension(file_path, results)
            
            # Validate file structure
            self._validate_file_structure(file_path, results)
            
            # Validate header
            header = self._validate_header(file_path, results)
            if not header:
                return results
            
            # Validate pixel data
            self._validate_pixel_data(file_path, header, results)
            
            # Check overall integrity
            self._validate_integrity(file_path, header, results)
            
            # Mark as valid if no errors
            results['valid'] = len(results['errors']) == 0
            
            return results
            
        except Exception as e:
            results['errors'].append(f"Validation failed: {str(e)}")
            return results
    
    def quick_validate(self, file_path: Union[str, os.PathLike]) -> bool:
        """
        Quick validation check (header only)
        
        Args:
            file_path: Path to .satish file
            
        Returns:
            bool: True if file appears valid
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'rb') as f:
                # Check minimum file size
                f.seek(0, 2)
                file_size = f.tell()
                if file_size < self.format.HEADER_SIZE:
                    return False
                
                # Check header
                f.seek(0)
                header_data = f.read(self.format.HEADER_SIZE)
                header = self.format.unpack_header(header_data)
                
                # Quick checks
                if header.magic != self.format.MAGIC_BYTES:
                    return False
                if header.channels not in self.format.SUPPORTED_CHANNELS:
                    return False
                
                return True
                
        except Exception:
            return False
    
    def validate_header_data(self, header: SatishHeader) -> List[str]:
        """
        Validate header data structure
        
        Args:
            header: SatishHeader object
            
        Returns:
            list: List of validation errors (empty if valid)
        """
        errors = []
        
        try:
            # Magic bytes
            if header.magic != self.format.MAGIC_BYTES:
                errors.append(f"Invalid magic bytes: {header.magic}")
            
            # Dimensions
            if not (1 <= header.width <= self.format.MAX_WIDTH):
                errors.append(f"Invalid width: {header.width}")
            if not (1 <= header.height <= self.format.MAX_HEIGHT):
                errors.append(f"Invalid height: {header.height}")
            
            # Channels
            if header.channels not in self.format.SUPPORTED_CHANNELS:
                errors.append(f"Unsupported channels: {header.channels}")
            
            # Version
            if header.version < 1:
                errors.append(f"Invalid version: {header.version}")
            if header.version > self.format.CURRENT_VERSION:
                errors.append(f"Unsupported version: {header.version} (current: {self.format.CURRENT_VERSION})")
            
        except Exception as e:
            errors.append(f"Header validation error: {str(e)}")
        
        return errors
    
    def validate_pixel_array(self, pixels: List[Tuple[int, int, int]], 
                           width: int, height: int) -> List[str]:
        """
        Validate pixel data array
        
        Args:
            pixels: List of (R, G, B) tuples
            width: Expected image width
            height: Expected image height
            
        Returns:
            list: List of validation errors (empty if valid)
        """
        errors = []
        
        try:
            # Check pixel count
            expected_count = width * height
            if len(pixels) != expected_count:
                errors.append(f"Pixel count mismatch: expected {expected_count}, got {len(pixels)}")
            
            # Validate individual pixels
            for i, pixel in enumerate(pixels):
                if not isinstance(pixel, (tuple, list)) or len(pixel) != 3:
                    errors.append(f"Invalid pixel format at index {i}: {pixel}")
                    continue
                
                r, g, b = pixel
                if not all(isinstance(c, int) and 0 <= c <= 255 for c in [r, g, b]):
                    errors.append(f"Invalid RGB values at index {i}: ({r}, {g}, {b})")
                
                # Stop after finding too many errors
                if len(errors) > 10:
                    errors.append("... (too many pixel errors, stopping validation)")
                    break
            
        except Exception as e:
            errors.append(f"Pixel array validation error: {str(e)}")
        
        return errors
    
    def validate_hex_string(self, hex_string: str, expected_length: int = None) -> List[str]:
        """
        Validate hex color string
        
        Args:
            hex_string: Hex color string to validate
            expected_length: Expected length (default: 6 for RGB)
            
        Returns:
            list: List of validation errors (empty if valid)
        """
        errors = []
        
        if expected_length is None:
            expected_length = self.format.HEX_CHARS_PER_PIXEL
        
        try:
            # Check length
            if len(hex_string) != expected_length:
                errors.append(f"Invalid hex string length: expected {expected_length}, got {len(hex_string)}")
            
            # Check valid hex characters
            try:
                int(hex_string, 16)
            except ValueError:
                errors.append(f"Invalid hex characters in: {hex_string}")
            
        except Exception as e:
            errors.append(f"Hex validation error: {str(e)}")
        
        return errors
    
    def _validate_file_access(self, file_path: Union[str, os.PathLike], results: dict) -> None:
        """Validate file exists and is readable"""
        try:
            if not os.path.exists(file_path):
                results['errors'].append(f"File does not exist: {file_path}")
                return
            
            if not os.path.isfile(file_path):
                results['errors'].append(f"Path is not a file: {file_path}")
                return
            
            if not os.access(file_path, os.R_OK):
                results['errors'].append(f"File is not readable: {file_path}")
                return
            
            # Get file size
            file_size = os.path.getsize(file_path)
            results['info']['file_size'] = file_size
            
            if file_size < self.format.HEADER_SIZE:
                results['errors'].append(f"File too small: {file_size} bytes (minimum: {self.format.HEADER_SIZE})")
                
        except OSError as e:
            raise FileError(f"File access error: {str(e)}") from e
    
    def _validate_file_extension(self, file_path: Union[str, os.PathLike], results: dict) -> None:
        """Validate file extension"""
        try:
            path = Path(file_path)
            if path.suffix.lower() != '.satish':
                results['warnings'].append(f"Unexpected file extension: {path.suffix} (expected: .satish)")
        except Exception as e:
            results['warnings'].append(f"Could not validate file extension: {str(e)}")
    
    def _validate_file_structure(self, file_path: Union[str, os.PathLike], results: dict) -> None:
        """Validate basic file structure"""
        try:
            with open(file_path, 'rb') as f:
                # Check if file can be read as binary
                f.seek(0, 2)
                file_size = f.tell()
                
                if file_size < self.format.HEADER_SIZE:
                    results['errors'].append("File too small for valid SATISH format")
                    return
                
                # Check if remaining data after header is appropriate size
                pixel_data_size = file_size - self.format.HEADER_SIZE
                if pixel_data_size % self.format.HEX_CHARS_PER_PIXEL != 0:
                    results['warnings'].append("Pixel data size not aligned to pixel boundaries")
                
        except OSError as e:
            raise FileError(f"File structure validation failed: {str(e)}") from e
        except Exception as e:
            results['errors'].append(f"File structure validation failed: {str(e)}")
    
    def _validate_header(self, file_path: Union[str, os.PathLike], results: dict) -> SatishHeader:
        """Validate and return header"""
        try:
            with open(file_path, 'rb') as f:
                header_data = f.read(self.format.HEADER_SIZE)
                
                if len(header_data) < self.format.HEADER_SIZE:
                    raise HeaderError(f"Incomplete header: got {len(header_data)} bytes, expected {self.format.HEADER_SIZE}")
                
                header = self.format.unpack_header(header_data)
                
                # Validate header contents
                header_errors = self.validate_header_data(header)
                results['errors'].extend(header_errors)
                
                # Store header info
                results['info']['header'] = {
                    'magic': header.magic.decode('ascii', errors='replace'),
                    'width': header.width,
                    'height': header.height,
                    'channels': header.channels,
                    'version': header.version
                }
                
                return header if not header_errors else None
                
        except (OSError, IOError) as e:
            raise FileError(f"Could not read header: {str(e)}") from e
        except HeaderError:
            raise
        except Exception as e:
            results['errors'].append(f"Header validation failed: {str(e)}")
            return None
    
    def _validate_pixel_data(self, file_path: Union[str, os.PathLike], 
                           header: SatishHeader, results: dict) -> None:
        """Validate pixel data section"""
        try:
            with open(file_path, 'rb') as f:
                # Skip header
                f.seek(self.format.HEADER_SIZE)
                
                # Read pixel data
                pixel_data_raw = f.read()
                
                # Check size
                expected_size = self.format.calculate_pixel_data_size(
                    header.width, header.height, header.channels
                )
                
                if len(pixel_data_raw) != expected_size:
                    raise PixelDataError(
                        f"Pixel data size mismatch: expected {expected_size}, got {len(pixel_data_raw)}"
                    )
                
                # Try to decode as ASCII
                try:
                    pixel_hex = pixel_data_raw.decode('ascii')
                except UnicodeDecodeError as e:
                    raise PixelDataError(f"Pixel data contains non-ASCII characters: {str(e)}") from e
                
                # Validate hex format (sample first few pixels to avoid performance issues)
                sample_size = min(len(pixel_hex), 60)  # First 10 pixels
                sample_hex = pixel_hex[:sample_size]
                
                for i in range(0, len(sample_hex), self.format.HEX_CHARS_PER_PIXEL):
                    hex_pixel = sample_hex[i:i+self.format.HEX_CHARS_PER_PIXEL]
                    if len(hex_pixel) == self.format.HEX_CHARS_PER_PIXEL:
                        hex_errors = self.validate_hex_string(hex_pixel)
                        if hex_errors:
                            pixel_index = i // self.format.HEX_CHARS_PER_PIXEL
                            results['errors'].extend([f"Pixel {pixel_index}: {error}" for error in hex_errors])
                            break  # Stop on first hex error
                
                results['info']['pixel_data_size'] = len(pixel_data_raw)
                results['info']['pixel_count'] = header.width * header.height
                
        except (OSError, IOError) as e:
            raise FileError(f"Could not read pixel data: {str(e)}") from e
        except PixelDataError:
            raise
        except Exception as e:
            results['errors'].append(f"Pixel data validation failed: {str(e)}")
    
    def _validate_integrity(self, file_path: Union[str, os.PathLike], 
                          header: SatishHeader, results: dict) -> None:
        """Validate overall file integrity"""
        try:
            # Check if calculated size matches actual size
            expected_file_size = self.format.HEADER_SIZE + self.format.calculate_pixel_data_size(
                header.width, header.height, header.channels
            )
            
            actual_file_size = results['info']['file_size']
            
            if expected_file_size != actual_file_size:
                results['errors'].append(
                    f"File size mismatch: expected {expected_file_size}, got {actual_file_size}"
                )
            
            # Add integrity info
            results['info']['integrity'] = {
                'expected_size': expected_file_size,
                'actual_size': actual_file_size,
                'size_match': expected_file_size == actual_file_size
            }
            
        except Exception as e:
            results['warnings'].append(f"Integrity check failed: {str(e)}")


# Convenience functions for external use
def validate_satish_file(file_path: Union[str, os.PathLike]) -> Dict[str, Any]:
    """
    Convenience function to validate a SATISH file
    
    Args:
        file_path: Path to .satish file
        
    Returns:
        dict: Validation results
        
    Raises:
        ValidationError: If validation cannot be performed
    """
    try:
        validator = SatishValidator()
        return validator.validate_file(file_path)
    except Exception as e:
        raise ValidationError(f"Could not validate file {file_path}: {str(e)}") from e


def is_valid_satish_file(file_path: Union[str, os.PathLike]) -> bool:
    """
    Convenience function for quick validation check
    
    Args:
        file_path: Path to .satish file
        
    Returns:
        bool: True if file appears valid
    """
    try:
        validator = SatishValidator()
        return validator.quick_validate(file_path)
    except Exception:
        return False