"""
File utilities for SATISH image format.
Handles file I/O operations, path validation, and file system interactions.
"""

import os
import shutil
from pathlib import Path
from typing import Union, List, Optional, Tuple
from .exceptions import FileError, ValidationError


class FileManager:
    """Handles file operations for SATISH format."""
    
    SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    SATISH_EXTENSION = '.satish'
    
    @staticmethod
    def validate_path(path: Union[str, Path]) -> Path:
        """
        Validate and convert path to Path object.
        
        Args:
            path: File path as string or Path object
            
        Returns:
            Validated Path object
            
        Raises:
            FileError: If path is invalid
        """
        if isinstance(path, str):
            path = Path(path)
        
        if not isinstance(path, Path):
            raise FileError(f"Invalid path type: {type(path)}")
        
        return path
    
    @staticmethod
    def ensure_directory_exists(path: Union[str, Path]) -> None:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            path: Directory path
            
        Raises:
            FileError: If directory cannot be created
        """
        try:
            path = FileManager.validate_path(path)
            if path.is_file():
                path = path.parent
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise FileError(f"Cannot create directory {path}: {e}")
    
    @staticmethod
    def is_supported_image(path: Union[str, Path]) -> bool:
        """
        Check if file is a supported image format.
        
        Args:
            path: File path
            
        Returns:
            True if supported image format
        """
        path = FileManager.validate_path(path)
        return path.suffix.lower() in FileManager.SUPPORTED_IMAGE_EXTENSIONS
    
    @staticmethod
    def is_satish_file(path: Union[str, Path]) -> bool:
        """
        Check if file is a SATISH file.
        
        Args:
            path: File path
            
        Returns:
            True if SATISH file
        """
        path = FileManager.validate_path(path)
        return path.suffix.lower() == FileManager.SATISH_EXTENSION
    
    @staticmethod
    def file_exists(path: Union[str, Path]) -> bool:
        """
        Check if file exists.
        
        Args:
            path: File path
            
        Returns:
            True if file exists
        """
        try:
            path = FileManager.validate_path(path)
            return path.exists() and path.is_file()
        except:
            return False
    
    @staticmethod
    def get_file_size(path: Union[str, Path]) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: File path
            
        Returns:
            File size in bytes
            
        Raises:
            FileError: If file doesn't exist or cannot be read
        """
        path = FileManager.validate_path(path)
        
        if not path.exists():
            raise FileError(f"File does not exist: {path}")
        
        try:
            return path.stat().st_size
        except Exception as e:
            raise FileError(f"Cannot get file size for {path}: {e}")
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """
        Generate a safe filename by removing/replacing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Safe filename
        """
        # Characters not allowed in filenames on various systems
        invalid_chars = '<>:"/\\|?*'
        safe_filename = filename
        
        for char in invalid_chars:
            safe_filename = safe_filename.replace(char, '_')
        
        # Remove leading/trailing dots and spaces
        safe_filename = safe_filename.strip('. ')
        
        # Ensure filename is not empty
        if not safe_filename:
            safe_filename = "untitled"
        
        return safe_filename
    
    @staticmethod
    def generate_output_path(input_path: Union[str, Path], 
                           output_dir: Optional[Union[str, Path]] = None,
                           new_extension: str = '.satish') -> Path:
        """
        Generate output path for converted file.
        
        Args:
            input_path: Input file path
            output_dir: Output directory (optional)
            new_extension: New file extension
            
        Returns:
            Generated output path
        """
        input_path = FileManager.validate_path(input_path)
        
        # Generate base filename
        base_name = input_path.stem
        safe_name = FileManager.get_safe_filename(base_name)
        
        # Determine output directory
        if output_dir:
            output_dir = FileManager.validate_path(output_dir)
            FileManager.ensure_directory_exists(output_dir)
        else:
            output_dir = input_path.parent
        
        # Generate full output path
        output_path = output_dir / f"{safe_name}{new_extension}"
        
        return output_path
    
    @staticmethod
    def backup_file(path: Union[str, Path], backup_suffix: str = '.backup') -> Path:
        """
        Create a backup of existing file.
        
        Args:
            path: File to backup
            backup_suffix: Suffix for backup file
            
        Returns:
            Path to backup file
            
        Raises:
            FileError: If backup cannot be created
        """
        path = FileManager.validate_path(path)
        
        if not path.exists():
            raise FileError(f"Cannot backup non-existent file: {path}")
        
        backup_path = path.with_name(f"{path.name}{backup_suffix}")
        
        try:
            shutil.copy2(path, backup_path)
            return backup_path
        except Exception as e:
            raise FileError(f"Cannot create backup of {path}: {e}")
    
    @staticmethod
    def find_files(directory: Union[str, Path], 
                   pattern: str = '*',
                   recursive: bool = True) -> List[Path]:
        """
        Find files matching pattern in directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern (glob style)
            recursive: Search recursively
            
        Returns:
            List of matching file paths
        """
        directory = FileManager.validate_path(directory)
        
        if not directory.exists():
            return []
        
        if not directory.is_dir():
            return []
        
        try:
            if recursive:
                return list(directory.rglob(pattern))
            else:
                return list(directory.glob(pattern))
        except Exception:
            return []
    
    @staticmethod
    def find_images(directory: Union[str, Path], recursive: bool = True) -> List[Path]:
        """
        Find all supported image files in directory.
        
        Args:
            directory: Directory to search
            recursive: Search recursively
            
        Returns:
            List of image file paths
        """
        all_files = FileManager.find_files(directory, '*', recursive)
        return [f for f in all_files if FileManager.is_supported_image(f)]
    
    @staticmethod
    def find_satish_files(directory: Union[str, Path], recursive: bool = True) -> List[Path]:
        """
        Find all SATISH files in directory.
        
        Args:
            directory: Directory to search
            recursive: Search recursively
            
        Returns:
            List of SATISH file paths
        """
        return FileManager.find_files(directory, '*.satish', recursive)
    
    @staticmethod
    def get_available_filename(path: Union[str, Path]) -> Path:
        """
        Get available filename by adding number suffix if file exists.
        
        Args:
            path: Desired file path
            
        Returns:
            Available file path
        """
        path = FileManager.validate_path(path)
        
        if not path.exists():
            return path
        
        base = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1
        
        while True:
            new_name = f"{base}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    @staticmethod
    def read_file_safely(path: Union[str, Path], mode: str = 'rb') -> bytes:
        """
        Safely read file contents.
        
        Args:
            path: File path
            mode: File open mode
            
        Returns:
            File contents
            
        Raises:
            FileError: If file cannot be read
        """
        path = FileManager.validate_path(path)
        
        if not path.exists():
            raise FileError(f"File does not exist: {path}")
        
        try:
            with open(path, mode) as f:
                return f.read()
        except Exception as e:
            raise FileError(f"Cannot read file {path}: {e}")
    
    @staticmethod
    def write_file_safely(path: Union[str, Path], data: bytes, mode: str = 'wb') -> None:
        """
        Safely write data to file.
        
        Args:
            path: File path
            data: Data to write
            mode: File open mode
            
        Raises:
            FileError: If file cannot be written
        """
        path = FileManager.validate_path(path)
        
        # Ensure parent directory exists
        FileManager.ensure_directory_exists(path.parent)
        
        try:
            with open(path, mode) as f:
                f.write(data)
        except Exception as e:
            raise FileError(f"Cannot write file {path}: {e}")


def get_file_info(path: Union[str, Path]) -> dict:
    """
    Get comprehensive file information.
    
    Args:
        path: File path
        
    Returns:
        Dictionary with file information
    """
    path = FileManager.validate_path(path)
    
    if not path.exists():
        raise FileError(f"File does not exist: {path}")
    
    stat = path.stat()
    
    return {
        'name': path.name,
        'stem': path.stem,
        'suffix': path.suffix,
        'size': stat.st_size,
        'size_human': format_file_size(stat.st_size),
        'modified': stat.st_mtime,
        'is_image': FileManager.is_supported_image(path),
        'is_satish': FileManager.is_satish_file(path),
        'absolute_path': str(path.absolute()),
        'parent': str(path.parent)
    }


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def batch_operation(files: List[Union[str, Path]], 
                   operation: callable,
                   *args, **kwargs) -> Tuple[List[Path], List[str]]:
    """
    Perform batch operation on multiple files.
    
    Args:
        files: List of file paths
        operation: Function to call on each file
        *args, **kwargs: Arguments to pass to operation
        
    Returns:
        Tuple of (successful_files, error_messages)
    """
    successful = []
    errors = []
    
    for file_path in files:
        try:
            path = FileManager.validate_path(file_path)
            result = operation(path, *args, **kwargs)
            successful.append(path)
        except Exception as e:
            errors.append(f"{file_path}: {str(e)}")
    
    return successful, errors