"""
SATISH Image Format Encoder
Handles conversion from standard image formats to .satish files
"""

import os
from typing import Union, Tuple, List, Optional, Dict, Any
from PIL import Image

from .format import SatishFormat, SatishHeader
from ..utils.exceptions import EncodingError, FileError


class SatishEncoder:
    """Encoder for converting images to SATISH format"""
    
    def __init__(self):
        self.format = SatishFormat()
    
    def encode_image(self, image_path: Union[str, os.PathLike], output_path: Union[str, os.PathLike], 
                    quality: int = 95, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Convert a standard image to SATISH format
        
        Args:
            image_path: Path to input image
            output_path: Path for output .satish file
            quality: Compression quality (1-100, currently not used but kept for compatibility)
            metadata: Additional metadata (currently not used but kept for compatibility)
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            FileError: If input file doesn't exist or can't be read
            EncodingError: If encoding fails
        """
        try:
            # Validate input file
            if not self._validate_input_image(image_path):
                raise FileError(f"Invalid input image: {image_path}")
            
            # Load and prepare image
            img = self._load_image(image_path)
            width, height = img.size
            
            # Create header
            header = self.format.create_header(width, height, channels=3)
            
            # Extract pixel data
            pixels = self._extract_pixels(img)
            
            # Convert to hex format
            hex_pixels = self._convert_pixels_to_hex(pixels)
            
            # Write SATISH file
            self._write_satish_file(header, hex_pixels, output_path)
            
            return True
            
        except Exception as e:
            raise EncodingError(f"Failed to encode {image_path}: {str(e)}") from e
    
    def encode_from_pil_image(self, pil_image: Image.Image, output_path: Union[str, os.PathLike], 
                             quality: int = 95, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Encode a PIL Image object to SATISH format
        
        Args:
            pil_image: PIL Image object
            output_path: Path for output .satish file
            quality: Compression quality (1-100, currently not used but kept for compatibility)
            metadata: Additional metadata (currently not used but kept for compatibility)
            
        Returns:
            bool: True if successful
            
        Raises:
            EncodingError: If encoding fails
        """
        try:
            # Ensure RGB mode
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            width, height = pil_image.size
            
            # Create header
            header = self.format.create_header(width, height, channels=3)
            
            # Extract pixels
            pixels = self._extract_pixels(pil_image)
            
            # Convert to hex
            hex_pixels = self._convert_pixels_to_hex(pixels)
            
            # Write file
            self._write_satish_file(header, hex_pixels, output_path)
            
            return True
            
        except Exception as e:
            raise EncodingError(f"Failed to encode PIL image: {str(e)}") from e
    
    def encode_from_array(self, pixel_array: List[Tuple[int, int, int]], 
                         width: int, height: int, 
                         output_path: Union[str, os.PathLike],
                         quality: int = 95, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Encode pixel array to SATISH format
        
        Args:
            pixel_array: List of (R, G, B) tuples
            width: Image width
            height: Image height
            output_path: Path for output .satish file
            quality: Compression quality (1-100, currently not used but kept for compatibility)
            metadata: Additional metadata (currently not used but kept for compatibility)
            
        Returns:
            bool: True if successful
            
        Raises:
            EncodingError: If encoding fails
        """
        try:
            # Validate array size
            expected_pixels = width * height
            if len(pixel_array) != expected_pixels:
                raise EncodingError(f"Pixel array size mismatch: expected {expected_pixels}, got {len(pixel_array)}")
            
            # Create header
            header = self.format.create_header(width, height, channels=3)
            
            # Convert to hex
            hex_pixels = self._convert_pixels_to_hex(pixel_array)
            
            # Write file
            self._write_satish_file(header, hex_pixels, output_path)
            
            return True
            
        except Exception as e:
            raise EncodingError(f"Failed to encode pixel array: {str(e)}") from e
    
    def _validate_input_image(self, image_path: Union[str, os.PathLike]) -> bool:
        """Validate input image file"""
        try:
            return os.path.exists(image_path) and os.path.isfile(image_path)
        except:
            return False
    
    def _load_image(self, image_path: Union[str, os.PathLike]) -> Image.Image:
        """Load image and convert to RGB"""
        try:
            img = Image.open(image_path)
            return img.convert('RGB')
        except Exception as e:
            raise FileError(f"Cannot load image {image_path}: {str(e)}") from e
    
    def _extract_pixels(self, img: Image.Image) -> List[Tuple[int, int, int]]:
        """Extract pixel data from PIL image"""
        try:
            return list(img.getdata())
        except Exception as e:
            raise EncodingError(f"Failed to extract pixel data: {str(e)}") from e
    
    def _convert_pixels_to_hex(self, pixels: List[Tuple[int, int, int]]) -> List[str]:
        """Convert RGB pixels to hex strings"""
        try:
            hex_pixels = []
            for r, g, b in pixels:
                hex_pixels.append(f"{r:02x}{g:02x}{b:02x}")
            return hex_pixels
        except Exception as e:
            raise EncodingError(f"Failed to convert pixels to hex: {str(e)}") from e
    
    def _write_satish_file(self, header: SatishHeader, hex_pixels: List[str], 
                          output_path: Union[str, os.PathLike]) -> None:
        """Write SATISH file to disk"""
        try:
            with open(output_path, 'wb') as f:
                # Write header
                header_bytes = self.format.pack_header(header)
                f.write(header_bytes)
                
                # Write pixel data
                pixel_data = ''.join(hex_pixels)
                f.write(pixel_data.encode('ascii'))
                
        except Exception as e:
            raise FileError(f"Failed to write SATISH file {output_path}: {str(e)}") from e
    
    def get_encoding_info(self, image_path: Union[str, os.PathLike]) -> dict:
        """
        Get information about what the encoding would produce
        
        Args:
            image_path: Path to input image
            
        Returns:
            dict: Encoding information
        """
        try:
            img = self._load_image(image_path)
            width, height = img.size
            num_pixels = width * height
            
            # Calculate file sizes
            header_size = self.format.HEADER_SIZE
            pixel_data_size = self.format.calculate_pixel_data_size(width, height)
            total_size = header_size + pixel_data_size
            
            return {
                'input_path': str(image_path),
                'dimensions': (width, height),
                'num_pixels': num_pixels,
                'channels': 3,
                'header_size': header_size,
                'pixel_data_size': pixel_data_size,
                'total_file_size': total_size,
                'original_mode': img.mode
            }
            
        except Exception as e:
            raise EncodingError(f"Failed to analyze image {image_path}: {str(e)}") from e


def encode_image(input_path: Union[str, os.PathLike], 
                output_path: Union[str, os.PathLike],
                quality: int = 95, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Convenience function to encode an image to SATISH format
    
    Args:
        input_path: Path to input image
        output_path: Path for output .satish file
        quality: Compression quality (1-100, currently not used but kept for compatibility)
        metadata: Additional metadata (currently not used but kept for compatibility)
        
    Returns:
        bool: True if successful
    """
    encoder = SatishEncoder()
    return encoder.encode_image(input_path, output_path, quality=quality, metadata=metadata)