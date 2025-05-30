"""
SATISH Image Format Core Specification
Defines the format constants, structure, and validation rules
"""

import struct
from typing import NamedTuple, Dict, Any
from ..utils.exceptions import InvalidFormatError


class SatishHeader(NamedTuple):
    """SATISH file header structure"""
    magic: bytes
    width: int
    height: int
    channels: int
    version: int


class SatishFormat:
    """Core SATISH format specification and constants"""
    
    # Format constants
    MAGIC_BYTES = b"SATI"
    CURRENT_VERSION = 1
    
    # Header structure sizes (in bytes)
    MAGIC_SIZE = 4
    WIDTH_SIZE = 2
    HEIGHT_SIZE = 2
    CHANNELS_SIZE = 1
    VERSION_SIZE = 1
    HEADER_SIZE = MAGIC_SIZE + WIDTH_SIZE + HEIGHT_SIZE + CHANNELS_SIZE + VERSION_SIZE
    
    # Format limits
    MAX_WIDTH = 65535  # 2^16 - 1
    MAX_HEIGHT = 65535  # 2^16 - 1
    MAX_CHANNELS = 255  # Currently only RGB (3) supported
    
    # Supported channel configurations
    SUPPORTED_CHANNELS = {
        3: "RGB"
    }
    
    # Pixel data constants
    HEX_CHARS_PER_PIXEL = 6  # RRGGBB format
    
    @classmethod
    def create_header(cls, width: int, height: int, channels: int = 3, version: int = None) -> SatishHeader:
        """Create a SATISH header with validation"""
        if version is None:
            version = cls.CURRENT_VERSION
            
        # Validate dimensions
        if not (1 <= width <= cls.MAX_WIDTH):
            raise InvalidFormatError(f"Width must be between 1 and {cls.MAX_WIDTH}, got {width}")
        if not (1 <= height <= cls.MAX_HEIGHT):
            raise InvalidFormatError(f"Height must be between 1 and {cls.MAX_HEIGHT}, got {height}")
        
        # Validate channels
        if channels not in cls.SUPPORTED_CHANNELS:
            supported = list(cls.SUPPORTED_CHANNELS.keys())
            raise InvalidFormatError(f"Unsupported channels: {channels}. Supported: {supported}")
        
        # Validate version
        if version < 1:
            raise InvalidFormatError(f"Version must be >= 1, got {version}")
        
        return SatishHeader(
            magic=cls.MAGIC_BYTES,
            width=width,
            height=height,
            channels=channels,
            version=version
        )
    
    @classmethod
    def pack_header(cls, header: SatishHeader) -> bytes:
        """Pack header into binary format"""
        return (
            header.magic +
            struct.pack('>H', header.width) +
            struct.pack('>H', header.height) +
            struct.pack('B', header.channels) +
            struct.pack('B', header.version)
        )
    
    @classmethod
    def unpack_header(cls, data: bytes) -> SatishHeader:
        """Unpack binary header data"""
        if len(data) < cls.HEADER_SIZE:
            raise InvalidFormatError(f"Header too short: expected {cls.HEADER_SIZE} bytes, got {len(data)}")
        
        magic = data[0:4]
        if magic != cls.MAGIC_BYTES:
            raise InvalidFormatError(f"Invalid magic bytes: expected {cls.MAGIC_BYTES}, got {magic}")
        
        width = struct.unpack('>H', data[4:6])[0]
        height = struct.unpack('>H', data[6:8])[0]
        channels = struct.unpack('B', data[8:9])[0]
        version = struct.unpack('B', data[9:10])[0]
        
        header = SatishHeader(magic, width, height, channels, version)
        
        # Validate the unpacked header
        cls._validate_header(header)
        
        return header
    
    @classmethod
    def _validate_header(cls, header: SatishHeader) -> None:
        """Validate header values"""
        if header.magic != cls.MAGIC_BYTES:
            raise InvalidFormatError(f"Invalid magic bytes: {header.magic}")
        
        if not (1 <= header.width <= cls.MAX_WIDTH):
            raise InvalidFormatError(f"Invalid width: {header.width}")
        
        if not (1 <= header.height <= cls.MAX_HEIGHT):
            raise InvalidFormatError(f"Invalid height: {header.height}")
        
        if header.channels not in cls.SUPPORTED_CHANNELS:
            raise InvalidFormatError(f"Unsupported channels: {header.channels}")
        
        if header.version < 1:
            raise InvalidFormatError(f"Invalid version: {header.version}")
    
    @classmethod
    def calculate_pixel_data_size(cls, width: int, height: int, channels: int = 3) -> int:
        """Calculate expected size of pixel data in bytes"""
        num_pixels = width * height
        return num_pixels * cls.HEX_CHARS_PER_PIXEL
    
    @classmethod
    def get_format_info(cls) -> Dict[str, Any]:
        """Get format information dictionary"""
        return {
            'name': 'SATISH Image Format',
            'magic': cls.MAGIC_BYTES.decode('ascii'),
            'version': cls.CURRENT_VERSION,
            'extension': '.satish',
            'supported_channels': cls.SUPPORTED_CHANNELS,
            'max_dimensions': (cls.MAX_WIDTH, cls.MAX_HEIGHT),
            'pixel_encoding': 'Hexadecimal RGB',
            'header_size': cls.HEADER_SIZE
        }