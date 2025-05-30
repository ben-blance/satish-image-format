"""
SATISH Image Format Color Utilities
Handles color format conversions and validations
"""

import re
from collections import Counter
from typing import Dict, List, Optional, Tuple, Union

from .exceptions import ColorConversionError


class ColorConverter:
    """Handles conversions between different color formats"""
    
    # Regex pattern for validating hex colors
    HEX_PATTERN = re.compile(r'^[0-9A-Fa-f]{6}$')
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """
        Convert RGB values to hex string
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            
        Returns:
            str: Hex color string (6 characters, no # prefix)
            
        Raises:
            ColorConversionError: If RGB values are invalid
        """
        try:
            # Validate RGB values
            self._validate_rgb(r, g, b)
            
            # Convert to hex
            return f"{r:02x}{g:02x}{b:02x}"
            
        except Exception as e:
            raise ColorConversionError(f"Failed to convert RGB({r},{g},{b}) to hex: {str(e)}") from e
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex string to RGB tuple
        
        Args:
            hex_color: Hex color string (6 characters, with or without # prefix)
            
        Returns:
            tuple: (R, G, B) values (0-255 each)
            
        Raises:
            ColorConversionError: If hex string is invalid
        """
        try:
            # Clean hex string
            hex_clean = self._clean_hex_string(hex_color)
            
            # Validate hex format
            if not self.HEX_PATTERN.match(hex_clean):
                raise ColorConversionError(f"Invalid hex format: {hex_color}")
            
            # Convert to RGB
            r = int(hex_clean[0:2], 16)
            g = int(hex_clean[2:4], 16)
            b = int(hex_clean[4:6], 16)
            
            return (r, g, b)
            
        except ColorConversionError:
            raise
        except Exception as e:
            raise ColorConversionError(f"Failed to convert hex '{hex_color}' to RGB: {str(e)}") from e
    
    def rgb_tuple_to_hex(self, rgb_tuple: Tuple[int, int, int]) -> str:
        """
        Convert RGB tuple to hex string
        
        Args:
            rgb_tuple: (R, G, B) tuple
            
        Returns:
            str: Hex color string
        """
        if len(rgb_tuple) != 3:
            raise ColorConversionError(f"RGB tuple must have 3 values, got {len(rgb_tuple)}")
        
        return self.rgb_to_hex(*rgb_tuple)
    
    def hex_to_rgb_tuple(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex string to RGB tuple (alias for hex_to_rgb)
        
        Args:
            hex_color: Hex color string
            
        Returns:
            tuple: (R, G, B) values
        """
        return self.hex_to_rgb(hex_color)
    
    def batch_rgb_to_hex(self, rgb_list: List[Tuple[int, int, int]]) -> List[str]:
        """
        Convert multiple RGB tuples to hex strings
        
        Args:
            rgb_list: List of (R, G, B) tuples
            
        Returns:
            list: List of hex color strings
        """
        try:
            return [self.rgb_tuple_to_hex(rgb) for rgb in rgb_list]
        except Exception as e:
            raise ColorConversionError(f"Failed to batch convert RGB to hex: {str(e)}") from e
    
    def batch_hex_to_rgb(self, hex_list: List[str]) -> List[Tuple[int, int, int]]:
        """
        Convert multiple hex strings to RGB tuples
        
        Args:
            hex_list: List of hex color strings
            
        Returns:
            list: List of (R, G, B) tuples
        """
        try:
            return [self.hex_to_rgb(hex_color) for hex_color in hex_list]
        except Exception as e:
            raise ColorConversionError(f"Failed to batch convert hex to RGB: {str(e)}") from e
    
    def validate_rgb(self, r: int, g: int, b: int) -> bool:
        """
        Validate RGB color values
        
        Args:
            r: Red component
            g: Green component
            b: Blue component
            
        Returns:
            bool: True if valid
        """
        try:
            self._validate_rgb(r, g, b)
            return True
        except ColorConversionError:
            return False
    
    def validate_hex(self, hex_color: str) -> bool:
        """
        Validate hex color string
        
        Args:
            hex_color: Hex color string to validate
            
        Returns:
            bool: True if valid
        """
        try:
            hex_clean = self._clean_hex_string(hex_color)
            return bool(self.HEX_PATTERN.match(hex_clean))
        except Exception:
            return False
    
    def normalize_hex(self, hex_color: str) -> str:
        """
        Normalize hex color string to 6-character lowercase format
        
        Args:
            hex_color: Input hex color string
            
        Returns:
            str: Normalized hex string (6 chars, lowercase, no #)
            
        Raises:
            ColorConversionError: If hex string is invalid
        """
        try:
            hex_clean = self._clean_hex_string(hex_color)
            
            if not self.HEX_PATTERN.match(hex_clean):
                raise ColorConversionError(f"Invalid hex format: {hex_color}")
            
            return hex_clean.lower()
            
        except ColorConversionError:
            raise
        except Exception as e:
            raise ColorConversionError(f"Failed to normalize hex '{hex_color}': {str(e)}") from e
    
    def get_brightness(self, r: int, g: int, b: int) -> float:
        """
        Calculate perceived brightness of RGB color
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            
        Returns:
            float: Brightness value (0.0 to 1.0)
        """
        self._validate_rgb(r, g, b)
        # Using standard luminance formula
        return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    
    def get_brightness_from_hex(self, hex_color: str) -> float:
        """
        Calculate brightness from hex color
        
        Args:
            hex_color: Hex color string
            
        Returns:
            float: Brightness value (0.0 to 1.0)
        """
        r, g, b = self.hex_to_rgb(hex_color)
        return self.get_brightness(r, g, b)
    
    def _validate_rgb(self, r: int, g: int, b: int) -> None:
        """Internal RGB validation"""
        for component, name in [(r, 'red'), (g, 'green'), (b, 'blue')]:
            if not isinstance(component, int):
                raise ColorConversionError(f"{name.title()} component must be integer, got {type(component).__name__}")
            if not (0 <= component <= 255):
                raise ColorConversionError(f"{name.title()} component must be 0-255, got {component}")
    
    def _clean_hex_string(self, hex_color: str) -> str:
        """Clean and prepare hex string for processing"""
        if not isinstance(hex_color, str):
            raise ColorConversionError(f"Hex color must be string, got {type(hex_color).__name__}")
        
        # Remove # prefix if present
        hex_clean = hex_color.lstrip('#')
        
        # Handle 3-character hex (expand to 6)
        if len(hex_clean) == 3:
            hex_clean = ''.join(c*2 for c in hex_clean)
        
        return hex_clean


class ColorPalette:
    """Utility class for working with color palettes"""
    
    def __init__(self, converter: Optional[ColorConverter] = None):
        self.converter = converter or ColorConverter()
    
    def extract_palette(self, rgb_pixels: List[Tuple[int, int, int]], 
                       max_colors: int = 256) -> List[Tuple[int, int, int]]:
        """
        Extract unique colors from pixel data
        
        Args:
            rgb_pixels: List of RGB tuples
            max_colors: Maximum number of colors to return
            
        Returns:
            list: List of unique RGB tuples
        """
        unique_colors = list(set(rgb_pixels))
        
        # Sort by brightness for consistent ordering
        unique_colors.sort(key=lambda rgb: self.converter.get_brightness(*rgb))
        
        return unique_colors[:max_colors]
    
    def get_palette_stats(self, rgb_pixels: List[Tuple[int, int, int]]) -> Dict[str, Union[int, float, List, None]]:
        """
        Get statistics about color usage in pixel data
        
        Args:
            rgb_pixels: List of RGB tuples
            
        Returns:
            dict: Color statistics including total pixels, unique colors, most common colors, and average brightness
        """
        if not rgb_pixels:
            return {
                'total_pixels': 0, 
                'unique_colors': 0, 
                'most_common': None,
                'average_brightness': 0.0
            }
        
        color_counts = Counter(rgb_pixels)
        
        return {
            'total_pixels': len(rgb_pixels),
            'unique_colors': len(color_counts),
            'most_common': color_counts.most_common(10),
            'average_brightness': sum(
                self.converter.get_brightness(*rgb) for rgb in rgb_pixels
            ) / len(rgb_pixels)
        }
    
    def get_dominant_colors(self, rgb_pixels: List[Tuple[int, int, int]], 
                           count: int = 5) -> List[Tuple[Tuple[int, int, int], int]]:
        """
        Get the most frequently used colors
        
        Args:
            rgb_pixels: List of RGB tuples
            count: Number of dominant colors to return
            
        Returns:
            list: List of (color, frequency) tuples
        """
        color_counts = Counter(rgb_pixels)
        return color_counts.most_common(count)
    
    def get_color_diversity(self, rgb_pixels: List[Tuple[int, int, int]]) -> float:
        """
        Calculate color diversity ratio (unique colors / total pixels)
        
        Args:
            rgb_pixels: List of RGB tuples
            
        Returns:
            float: Diversity ratio (0.0 to 1.0)
        """
        if not rgb_pixels:
            return 0.0
        
        unique_count = len(set(rgb_pixels))
        total_count = len(rgb_pixels)
        
        return unique_count / total_count


# Convenience functions for standalone use
def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex (convenience function)"""
    converter = ColorConverter()
    return converter.rgb_to_hex(r, g, b)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex to RGB (convenience function)"""
    converter = ColorConverter()
    return converter.hex_to_rgb(hex_color)


def validate_color_format(color: Union[str, Tuple[int, int, int]]) -> bool:
    """Validate color in either hex or RGB format"""
    converter = ColorConverter()
    
    if isinstance(color, str):
        return converter.validate_hex(color)
    elif isinstance(color, (tuple, list)) and len(color) == 3:
        return converter.validate_rgb(*color)
    else:
        return False


# Export list for explicit imports
__all__ = [
    # Classes
    'ColorConverter',
    'ColorPalette',
    
    # Convenience functions
    'rgb_to_hex',
    'hex_to_rgb', 
    'validate_color_format',
]