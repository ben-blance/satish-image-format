import sys
import json
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax

# Import core SATISH modules
from ..core.encoder import SatishEncoder
from ..core.decoder import SatishDecoder
from ..core.validator import SatishValidator
from ..utils.file_utils import FileManager, get_file_info, format_file_size, batch_operation
from ..utils.exceptions import SatishError, FileError, ValidationError

# Rich console for beautiful output
console = Console()


class SatishCLI:
    """Main CLI command handler class."""
    
    def __init__(self):
        self.encoder = SatishEncoder()
        self.decoder = SatishDecoder()
        self.validator = SatishValidator()
        self.file_manager = FileManager()
    
    def convert_to_satish(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        quality: int = 95,
        metadata: Optional[dict] = None
    ) -> bool:
        """
        Convert image file to SATISH format.
        """
        try:
            input_file = Path(input_path)
            # Validate input file
            if not self.file_manager.file_exists(input_file):
                console.print(f"Input file not found: {input_file}", style="red")
                return False
            if not self.file_manager.is_supported_image(input_file):
                console.print(f"Unsupported image format: {input_file.suffix}", style="red")
                return False
            # Generate output path if not provided
            if not output_path:
                output_file = self.file_manager.generate_output_path(input_file)
            else:
                output_file = Path(output_path)
            # Show conversion info
            input_info = get_file_info(input_file)
            console.print(f"Converting: {input_file.name} ({input_info['size_human']})")
            console.print(f"Output: {output_file}")
            # Perform conversion with progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Converting to SATISH...", total=None)
                result = self.encoder.encode_image(
                    str(input_file),
                    str(output_file),
                    quality=quality,
                    metadata=metadata
                )
                progress.update(task, completed=True)
            # Show results
            if result:
                output_info = get_file_info(output_file)
                compression_ratio = (1 - output_info['size'] / input_info['size']) * 100
                console.print("Conversion successful!", style="green")
                console.print(f"Original: {input_info['size_human']}")
                console.print(f"SATISH: {output_info['size_human']}")
                console.print(f"Compression: {compression_ratio:.1f}%")
                return True
            else:
                console.print("Conversion failed", style="red")
                return False
        except Exception as e:
            console.print(f"Error: {str(e)}", style="red")
            return False

    def convert_from_satish(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        format: str = 'png'
    ) -> bool:
        """
        Convert SATISH file to image format.
        """
        try:
            input_file = Path(input_path)
            # Validate input file
            if not self.file_manager.file_exists(input_file):
                console.print(f"Input file not found: {input_file}", style="red")
                return False
            if not self.file_manager.is_satish_file(input_file):
                console.print(f"Not a SATISH file: {input_file}", style="red")
                return False
            # Generate output path if not provided
            if not output_path:
                output_file = self.file_manager.generate_output_path(
                    input_file,
                    new_extension=f'.{format.lower()}'
                )
            else:
                output_file = Path(output_path)
            # Show conversion info
            input_info = get_file_info(input_file)
            console.print(f"Converting: {input_file.name} ({input_info['size_human']})")
            console.print(f"Output: {output_file}")
            # Perform conversion with progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Converting from SATISH...", total=None)
                result = self.decoder.decode_to_image(
                    str(input_file),
                    str(output_file),
                    output_format=format
                )
                progress.update(task, completed=True)
            # Show results
            if result:
                output_info = get_file_info(output_file)
                console.print("Conversion successful!", style="green")
                console.print(f"SATISH: {input_info['size_human']}")
                console.print(f"{format.upper()}: {output_info['size_human']}")
                return True
            else:
                console.print("Conversion failed", style="red")
                return False
        except Exception as e:
            console.print(f"Error: {str(e)}", style="red")
            return False

    def show_file_info(self, file_path: str, detailed: bool = False) -> bool:
        """
        Display information about a SATISH file.
        """
        try:
            file_path = Path(file_path)
            if not self.file_manager.file_exists(file_path):
                console.print(f"File not found: {file_path}", style="red")
                return False
            # Get basic file info
            file_info = get_file_info(file_path)
            # Create info table
            table = Table(title=f"File Information: {file_info['name']}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            table.add_row("File Name", file_info['name'])
            table.add_row("File Size", file_info['size_human'])
            table.add_row(
                "File Type",
                "SATISH Image" if file_info['is_satish'] else "Regular Image"
            )
            table.add_row("Full Path", file_info['absolute_path'])
            # If it's a SATISH file, get format-specific info
            if self.file_manager.is_satish_file(file_path):
                try:
                    validation_result = self.validator.validate_file(str(file_path))
                    if validation_result['valid']:
                        satish_data = self.decoder.read_satish_file(str(file_path))
                        table.add_row("Image Width", str(satish_data.get('width', 'Unknown')))
                        table.add_row("Image Height", str(satish_data.get('height', 'Unknown')))
                        table.add_row("Color Mode", satish_data.get('color_mode', 'Unknown'))
                        table.add_row("Compression", f"{satish_data.get('quality', 'Unknown')}%")
                        if detailed and 'metadata' in satish_data:
                            metadata = satish_data['metadata']
                            for key, value in metadata.items():
                                table.add_row(f"Meta: {key}", str(value))
                    else:
                        error_msg = (
                            validation_result['errors'][0]
                            if validation_result.get('errors')
                            else "Unknown error"
                        )
                        table.add_row("Validation", f"Error: {error_msg}", style="red")
                except Exception as e:
                    table.add_row("SATISH Info", f"Error reading: {str(e)}", style="red")
            console.print(table)
            return True
        except Exception as e:
            console.print(f"Error: {str(e)}", style="red")
            return False

    def validate_file(self, file_path: str) -> bool:
        """
        Validate a SATISH file.
        """
        try:
            file_path = Path(file_path)
            if not self.file_manager.file_exists(file_path):
                console.print(f"File not found: {file_path}", style="red")
                return False
            if not self.file_manager.is_satish_file(file_path):
                console.print(f"Not a SATISH file: {file_path}", style="red")
                return False
            console.print(f"Validating: {file_path.name}")
            result = self.validator.validate_file(str(file_path))
            if result['valid']:
                console.print("File is valid!", style="green")
                if result.get('warnings'):
                    console.print("Warnings:", style="yellow")
                    for warning in result['warnings']:
                        console.print(f"   • {warning}", style="yellow")
                return True
            else:
                console.print("File is invalid!", style="red")
                if result.get('errors'):
                    console.print("Errors:", style="red")
                    for error in result['errors']:
                        console.print(f"   • {error}", style="red")
                if result.get('warnings'):
                    console.print("Warnings:", style="yellow")
                    for warning in result['warnings']:
                        console.print(f"   • {warning}", style="yellow")
                return False
        except Exception as e:
            console.print(f"Error during validation: {str(e)}", style="red")
            return False

    def batch_convert(
        self,
        input_dir: str,
        output_dir: Optional[str] = None,
        to_satish: bool = True,
        recursive: bool = True
    ) -> bool:
        """
        Batch convert files in directory.
        """
        try:
            input_path = Path(input_dir)
            if not input_path.exists() or not input_path.is_dir():
                console.print(f"Directory not found: {input_path}", style="red")
                return False
            if to_satish:
                files = self.file_manager.find_images(input_path, recursive)
                operation_name = "Converting to SATISH"
            else:
                files = self.file_manager.find_satish_files(input_path, recursive)
                operation_name = "Converting from SATISH"
            if not files:
                file_type = "images" if to_satish else "SATISH files"
                console.print(f"No {file_type} found in {input_path}", style="yellow")
                return False
            console.print(f"Found {len(files)} files to convert")
            if output_dir:
                output_path = Path(output_dir)
                self.file_manager.ensure_directory_exists(output_path)
            else:
                output_path = input_path
            successful, failed = 0, 0
            with Progress(console=console) as progress:
                task = progress.add_task(operation_name, total=len(files))
                for file_path in files:
                    try:
                        if to_satish:
                            output_file = output_path / f"{file_path.stem}.satish"
                            success = self.encoder.encode_image(str(file_path), str(output_file))
                        else:
                            output_file = output_path / f"{file_path.stem}.png"
                            success = self.decoder.decode_to_image(str(file_path), str(output_file))
                        if success:
                            successful += 1
                        else:
                            failed += 1
                    except Exception as e:
                        console.print(f"Failed to convert {file_path.name}: {str(e)}", style="red")
                        failed += 1
                    progress.update(task, advance=1)
            console.print("Batch conversion complete!")
            console.print(f"Successful: {successful}")
            if failed > 0:
                console.print(f"Failed: {failed}", style="red")
            return successful > 0
        except Exception as e:
            console.print(f"Batch conversion error: {str(e)}", style="red")
            return False

    def list_files(self, directory: str, file_type: str = 'all', recursive: bool = True) -> bool:
        """
        List files in directory.
        """
        try:
            dir_path = Path(directory)
            if not dir_path.exists() or not dir_path.is_dir():
                console.print(f"Directory not found: {dir_path}", style="red")
                return False
            if file_type == 'images':
                files = self.file_manager.find_images(dir_path, recursive)
                title = "Image Files"
            elif file_type == 'satish':
                files = self.file_manager.find_satish_files(dir_path, recursive)
                title = "SATISH Files"
            else:
                all_files = self.file_manager.find_files(dir_path, '*', recursive)
                files = [f for f in all_files if f.is_file()]
                title = "All Files"
            if not files:
                console.print(f"No files found in {dir_path}", style="yellow")
                return False
            table = Table(title=f"{title} in {dir_path}")
            table.add_column("Name", style="cyan")
            table.add_column("Size", style="white")
            table.add_column("Type", style="green")
            files.sort(key=lambda x: x.name.lower())
            for file_path in files:
                file_info = get_file_info(file_path)
                file_type_str = (
                    "SATISH" if file_info['is_satish'] else
                    "Image" if file_info['is_image'] else
                    file_path.suffix.upper()[1:] or "File"
                )
                table.add_row(
                    file_info['name'],
                    file_info['size_human'],
                    file_type_str
                )
            console.print(table)
            console.print(f"\nTotal files: {len(files)}")
            return True
        except Exception as e:
            console.print(f"Error listing files: {str(e)}", style="red")
            return False


def print_help():
    """Print comprehensive help information."""
    help_text = """
    SATISH Image Format - Command Line Interface
    
    USAGE:
        satish <command> [options]

    COMMANDS:
        convert <input> [output]     Convert image to SATISH format
        extract <input> [output]     Convert SATISH to image format
        info <file>                  Show file information
        validate <file>              Validate SATISH file
        batch <directory>            Batch convert files
        list <directory>             List files in directory
        help                         Show this help message

    EXAMPLES:
        satish convert image.jpg              # Convert to SATISH
        satish convert image.jpg custom.satish # Convert with custom name
        satish extract file.satish            # Extract to PNG
        satish extract file.satish image.jpg  # Extract to specific format
        satish info file.satish               # Show file information
        satish validate file.satish           # Validate SATISH file
        satish batch ./images                 # Batch convert directory
        satish list ./directory               # List all files

    OPTIONS:
        --quality, -q <1-100>        Compression quality (default: 95)
        --format, -f <format>        Output format (png, jpg, bmp, etc.)
        --recursive, -r              Search directories recursively
        --detailed, -d               Show detailed information
        --output-dir, -o <dir>       Output directory for batch operations
        --help, -h                   Show help for specific command
    """
    console.print(Panel(help_text, title="SATISH CLI Help", border_style="blue"))


def print_version():
    """Print version information."""
    version_info = """
    SATISH Image Format
    Version: 1.0.0
    Author: SATISH Format Team
    Website: https://github.com/satish-format
    """
    console.print(Panel(version_info, title="Version Information", border_style="green"))

if __name__ == "__main__":
    # Entry point for CLI
    SatishCLI().cli_main()
