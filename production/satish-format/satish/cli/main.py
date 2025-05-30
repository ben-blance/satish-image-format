#!/usr/bin/env python3
"""
SATISH Image Format - Command Line Interface Entry Point

This is the main entry point for the SATISH CLI tool.
It handles argument parsing and dispatches commands to appropriate handlers.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.traceback import install

from .commands import SatishCLI, print_help, print_version

# Install rich traceback handler for better error display
install(show_locals=True)

# Rich console for output
console = Console()


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='satish',
        description='SATISH Image Format - Command Line Tool',
        epilog='For more information, visit: https://github.com/satish-format'
    )
    
    # Global options
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser(
        'convert',
        help='Convert image to SATISH format',
        description='Convert standard image formats to SATISH format'
    )
    convert_parser.add_argument('input', help='Input image file')
    convert_parser.add_argument('output', nargs='?', help='Output SATISH file (optional)')
    convert_parser.add_argument(
        '--quality', '-q',
        type=int,
        default=95,
        choices=range(1, 101),
        metavar='1-100',
        help='Compression quality (1-100, default: 95)'
    )
    convert_parser.add_argument(
        '--metadata', '-m',
        help='Additional metadata as JSON string'
    )
    
    # Extract command
    extract_parser = subparsers.add_parser(
        'extract',
        help='Convert SATISH to image format',
        description='Extract SATISH files to standard image formats'
    )
    extract_parser.add_argument('input', help='Input SATISH file')
    extract_parser.add_argument('output', nargs='?', help='Output image file (optional)')
    extract_parser.add_argument(
        '--format', '-f',
        default='png',
        choices=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
        help='Output image format (default: png)'
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Show file information',
        description='Display detailed information about SATISH files'
    )
    info_parser.add_argument('file', help='SATISH file to analyze')
    info_parser.add_argument(
        '--detailed', '-d',
        action='store_true',
        help='Show detailed metadata information'
    )
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate SATISH file',
        description='Check if SATISH file is valid and well-formed'
    )
    validate_parser.add_argument('file', help='SATISH file to validate')
    
    # Batch command
    batch_parser = subparsers.add_parser(
        'batch',
        help='Batch convert files',
        description='Convert multiple files in a directory'
    )
    batch_parser.add_argument('directory', help='Input directory')
    batch_parser.add_argument(
        '--output-dir', '-o',
        help='Output directory (default: same as input)'
    )
    batch_parser.add_argument(
        '--to-satish',
        action='store_true',
        default=True,
        help='Convert TO SATISH format (default)'
    )
    batch_parser.add_argument(
        '--from-satish',
        action='store_true',
        help='Convert FROM SATISH format'
    )
    batch_parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Search directories recursively (default)'
    )
    batch_parser.add_argument(
        '--quality', '-q',
        type=int,
        default=95,
        choices=range(1, 101),
        metavar='1-100',
        help='Compression quality for SATISH conversion (1-100, default: 95)'
    )
    
    # List command
    list_parser = subparsers.add_parser(
        'list',
        help='List files in directory',
        description='List and filter files in a directory'
    )
    list_parser.add_argument('directory', help='Directory to list')
    list_parser.add_argument(
        '--type', '-t',
        choices=['all', 'images', 'satish'],
        default='all',
        help='File type filter (default: all)'
    )
    list_parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Search directories recursively (default)'
    )
    
    # Help command
    help_parser = subparsers.add_parser(
        'help',
        help='Show detailed help information'
    )
    
    return parser


def handle_convert_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle convert command."""
    try:
        # Parse metadata if provided
        metadata = None
        if args.metadata:
            import json
            try:
                metadata = json.loads(args.metadata)
            except json.JSONDecodeError:
                console.print("❌ Invalid JSON metadata format", style="red")
                return 1
        
        success = cli.convert_to_satish(
            args.input,
            args.output,
            quality=args.quality,
            metadata=metadata
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="yellow")
        return 130


def handle_extract_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle extract command."""
    try:
        success = cli.convert_from_satish(
            args.input,
            args.output,
            format=args.format
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="yellow")
        return 130


def handle_info_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle info command."""
    success = cli.show_file_info(args.file, detailed=args.detailed)
    return 0 if success else 1


def handle_validate_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle validate command."""
    success = cli.validate_file(args.file)
    return 0 if success else 1


def handle_batch_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle batch command."""
    try:
        to_satish = not args.from_satish  # Default to True unless --from-satish is specified
        
        success = cli.batch_convert(
            args.directory,
            args.output_dir,
            to_satish=to_satish,
            recursive=args.recursive
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        console.print("\n⚠️  Operation cancelled by user", style="yellow")
        return 130


def handle_list_command(args: argparse.Namespace, cli: SatishCLI) -> int:
    """Handle list command."""
    success = cli.list_files(
        args.directory,
        file_type=args.type,
        recursive=args.recursive
    )
    return 0 if success else 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the SATISH CLI.
    
    Args:
        argv: Command line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if argv is None:
        argv = sys.argv[1:]
    
    # Create parser and parse arguments
    parser = create_parser()
    
    # If no arguments provided, show help
    if not argv:
        print_help()
        return 0
    
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code if e.code is not None else 1
    
    # Handle version request
    if args.version:
        print_version()
        return 0
    
    # Handle no command specified
    if not args.command:
        print_help()
        return 0
    
    # Handle help command
    if args.command == 'help':
        print_help()
        return 0
    
    # Initialize CLI handler
    try:
        cli = SatishCLI()
    except Exception as e:
        console.print(f"❌ Failed to initialize SATISH CLI: {str(e)}", style="red")
        if args.verbose:
            console.print_exception()
        return 1
    
    # Dispatch to appropriate command handler
    try:
        if args.command == 'convert':
            return handle_convert_command(args, cli)
        elif args.command == 'extract':
            return handle_extract_command(args, cli)
        elif args.command == 'info':
            return handle_info_command(args, cli)
        elif args.command == 'validate':
            return handle_validate_command(args, cli)
        elif args.command == 'batch':
            return handle_batch_command(args, cli)
        elif args.command == 'list':
            return handle_list_command(args, cli)
        else:
            console.print(f"❌ Unknown command: {args.command}", style="red")
            print_help()
            return 1
    
    except Exception as e:
        console.print(f"❌ Unexpected error: {str(e)}", style="red")
        if args.verbose:
            console.print_exception()
        return 1


def cli_entry_point():
    """Entry point for setuptools console script."""
    sys.exit(main())


if __name__ == '__main__':
    sys.exit(main())