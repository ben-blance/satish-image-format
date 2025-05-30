"""
SATISH Image Format Decoder
Handles conversion from .satish files to standard image formats
"""

import os
from typing import Union, Tuple, List, Optional, Dict, Any
from PIL import Image

from .format import SatishFormat, SatishHeader
from ..utils.exceptions import DecodingError, FileError, InvalidFormatError


class SatishDecoder:
    """Decoder for converting SATISH format to images"""
    
    def __init__(self):
        self.format = SatishFormat()
    
    def decode_to_image(self, satish_path: Union[str, os.PathLike], 
                       output_path: Union[str, os.PathLike],
                       output_format: Optional[str] = None) -> bool:
        """
        Convert SATISH file to standard image format
        
        Args:
            satish_path: Path to input .satish file
            output_path: Path for output image file
            output_format: Output format (PNG, JPEG, BMP, etc.). If None, inferred from output_path extension
            
        Returns:
            bool: True if successful
            
        Raises:
            FileError: If input file doesn't exist or can't be read
            DecodingError: If decoding fails
        """
        try:
            # Validate input file
            if not self._validate_satish_file(satish_path):
                raise FileError(f"Invalid SATISH file: {satish_path}")
            
            # Load SATISH data
            satish_data = self._load_satish_file(satish_path)
            
            # Create PIL image
            pil_image = self._create_pil_image(satish_data)
            
            # Determine output format
            if output_format:
                # Use specified format
                save_format = output_format.upper()
            else:
                # Infer from file extension
                _, ext = os.path.splitext(output_path)
                if ext.lower() in ['.jpg', '.jpeg']:
                    save_format = 'JPEG'
                elif ext.lower() == '.png':
                    save_format = 'PNG'
                elif ext.lower() == '.bmp':
                    save_format = 'BMP'
                elif ext.lower() == '.gif':
                    save_format = 'GIF'
                elif ext.lower() == '.tiff':
                    save_format = 'TIFF'
                else:
                    save_format = 'PNG'  # Default to PNG
            
            # Handle JPEG format (no alpha channel)
            if save_format == 'JPEG' and pil_image.mode in ('RGBA', 'LA'):
                # Convert to RGB for JPEG
                pil_image = pil_image.convert('RGB')
            
            # Save as standard image
            pil_image.save(output_path, format=save_format)
            
            return True
            
        except Exception as e:
            raise DecodingError(f"Failed to decode {satish_path}: {str(e)}") from e
    
    def decode_to_pil_image(self, satish_path: Union[str, os.PathLike]) -> Image.Image:
        """
        Convert SATISH file to PIL Image object
        
        Args:
            satish_path: Path to input .satish file
            
        Returns:
            PIL.Image.Image: The decoded image
            
        Raises:
            FileError: If input file doesn't exist or can't be read
            DecodingError: If decoding fails
        """
        try:
            # Load SATISH data
            satish_data = self._load_satish_file(satish_path)
            
            # Create and return PIL image
            return self._create_pil_image(satish_data)
            
        except Exception as e:
            raise DecodingError(f"Failed to decode {satish_path} to PIL image: {str(e)}") from e
    
    def decode_to_array(self, satish_path: Union[str, os.PathLike]) -> Tuple[List[Tuple[int, int, int]], int, int]:
        """
        Convert SATISH file to pixel array
        
        Args:
            satish_path: Path to input .satish file
            
        Returns:
            tuple: (pixel_array, width, height)
            
        Raises:
            FileError: If input file doesn't exist or can't be read
            DecodingError: If decoding fails
        """
        try:
            # Load SATISH data
            satish_data = self._load_satish_file(satish_path)
            
            return (
                satish_data['pixels'],
                satish_data['header'].width,
                satish_data['header'].height
            )
            
        except Exception as e:
            raise DecodingError(f"Failed to decode {satish_path} to array: {str(e)}") from e
    
    def get_satish_info(self, satish_path: Union[str, os.PathLike]) -> Dict[str, Any]:
        """
        Get information about a SATISH file without full decoding
        
        Args:
            satish_path: Path to .satish file
            
        Returns:
            dict: File information
            
        Raises:
            FileError: If file can't be read
            InvalidFormatError: If file format is invalid
        """
        try:
            with open(satish_path, 'rb') as f:
                # Read and parse header only
                header_data = f.read(self.format.HEADER_SIZE)
                header = self.format.unpack_header(header_data)
                
                # Get file size
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                
                # Calculate expected vs actual pixel data size
                expected_pixel_size = self.format.calculate_pixel_data_size(
                    header.width, header.height, header.channels
                )
                actual_pixel_size = file_size - self.format.HEADER_SIZE
                
                return {
                    'file_path': str(satish_path),
                    'file_size': file_size,
                    'header': {
                        'magic': header.magic.decode('ascii'),
                        'width': header.width,
                        'height': header.height,
                        'channels': header.channels,
                        'version': header.version
                    },
                    'pixel_count': header.width * header.height,
                    'pixel_data_size': {
                        'expected': expected_pixel_size,
                        'actual': actual_pixel_size,
                        'valid': expected_pixel_size == actual_pixel_size
                    },
                    'channel_format': self.format.SUPPORTED_CHANNELS.get(header.channels, 'Unknown')
                }
                
        except Exception as e:
            raise FileError(f"Failed to read SATISH file info {satish_path}: {str(e)}") from e
    
    def read_satish_file(self, satish_path: Union[str, os.PathLike]) -> Dict[str, Any]:
        """
        Read SATISH file and return metadata (for CLI info command)
        
        Args:
            satish_path: Path to .satish file
            
        Returns:
            dict: File metadata and image information
        """
        try:
            satish_data = self._load_satish_file(satish_path)
            header = satish_data['header']
            
            return {
                'width': header.width,
                'height': header.height,
                'channels': header.channels,
                'color_mode': self.format.SUPPORTED_CHANNELS.get(header.channels, 'Unknown'),
                'version': header.version,
                'quality': 95,  # Default quality, you might want to store this in the format
                'metadata': {}  # Add metadata support if needed
            }
            
        except Exception as e:
            raise DecodingError(f"Failed to read SATISH file {satish_path}: {str(e)}") from e
    
    def _validate_satish_file(self, satish_path: Union[str, os.PathLike]) -> bool:
        """Validate SATISH file exists and is readable"""
        try:
            return os.path.exists(satish_path) and os.path.isfile(satish_path)
        except:
            return False
    
    def _load_satish_file(self, satish_path: Union[str, os.PathLike]) -> Dict[str, Any]:
        """Load and parse complete SATISH file"""
        try:
            with open(satish_path, 'rb') as f:
                # Read header
                header_data = f.read(self.format.HEADER_SIZE)
                header = self.format.unpack_header(header_data)
                
                # Read pixel data
                pixel_data_raw = f.read().decode('ascii')
                
                # Validate pixel data size
                expected_size = self.format.calculate_pixel_data_size(
                    header.width, header.height, header.channels
                )
                if len(pixel_data_raw) != expected_size:
                    raise InvalidFormatError(
                        f"Pixel data size mismatch: expected {expected_size}, got {len(pixel_data_raw)}"
                    )
                
                # Convert hex data to RGB pixels
                pixels = self._parse_pixel_data(pixel_data_raw)
                
                # Validate pixel count
                expected_pixels = header.width * header.height
                if len(pixels) != expected_pixels:
                    raise InvalidFormatError(
                        f"Pixel count mismatch: expected {expected_pixels}, got {len(pixels)}"
                    )
                
                return {
                    'header': header,
                    'pixels': pixels
                }
                
        except Exception as e:
            if isinstance(e, (InvalidFormatError, DecodingError)):
                raise
            raise DecodingError(f"Failed to load SATISH file {satish_path}: {str(e)}") from e
    
    def _parse_pixel_data(self, pixel_data_raw: str) -> List[Tuple[int, int, int]]:
        """Parse hex pixel data into RGB tuples"""
        try:
            pixels = []
            hex_per_pixel = self.format.HEX_CHARS_PER_PIXEL
            
            for i in range(0, len(pixel_data_raw), hex_per_pixel):
                hex_color = pixel_data_raw[i:i+hex_per_pixel]
                
                if len(hex_color) != hex_per_pixel:
                    raise InvalidFormatError(f"Invalid hex color length: {hex_color}")
                
                rgb = self._hex_to_rgb(hex_color)
                pixels.append(rgb)
            
            return pixels
            
        except Exception as e:
            raise DecodingError(f"Failed to parse pixel data: {str(e)}") from e
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple"""
        try:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except ValueError as e:
            raise InvalidFormatError(f"Invalid hex color: {hex_color}") from e
    
    def _create_pil_image(self, satish_data: Dict[str, Any]) -> Image.Image:
        """Create PIL Image from SATISH data"""
        try:
            header = satish_data['header']
            pixels = satish_data['pixels']
            
            # Create image
            img = Image.new('RGB', (header.width, header.height))
            img.putdata(pixels)
            
            return img
            
        except Exception as e:
            raise DecodingError(f"Failed to create PIL image: {str(e)}") from e
    
    def display_image(self, satish_path: Union[str, os.PathLike]) -> None:
        """
        Display SATISH image using PIL's show method
        
        Args:
            satish_path: Path to .satish file
            
        Raises:
            DecodingError: If decoding or display fails
        """
        try:
            img = self.decode_to_pil_image(satish_path)
            img.show()
        except Exception as e:
            raise DecodingError(f"Failed to display image {satish_path}: {str(e)}") from e


def decode_image(satish_path: Union[str, os.PathLike], 
                output_path: Union[str, os.PathLike],
                output_format: Optional[str] = None) -> bool:
    """
    Convenience function to decode a SATISH file to standard image format
    
    Args:
        satish_path: Path to input .satish file
        output_path: Path for output image file
        output_format: Output format (PNG, JPEG, BMP, etc.). If None, inferred from output_path extension
        
    Returns:
        bool: True if successful
    """
    decoder = SatishDecoder()
    return decoder.decode_to_image(satish_path, output_path, output_format)


def get_image_info(satish_path: Union[str, os.PathLike]) -> Dict[str, Any]:
    """
    Convenience function to get SATISH file information
    
    Args:
        satish_path: Path to .satish file
        
    Returns:
        dict: File information
    """
    decoder = SatishDecoder()
    return decoder.get_satish_info(satish_path)