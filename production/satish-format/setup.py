#!/usr/bin/env python3
"""
Setup configuration for SATISH Image Format package.
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Ensure we're running on Python 3.7+
if sys.version_info < (3, 7):
    raise RuntimeError("SATISH requires Python 3.7 or higher")

# Get the directory containing this file
here = Path(__file__).parent.absolute()

# Read the README file for long description
readme_file = here / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = (
        "SATISH Image Format - A modern, efficient image format with advanced "
        "compression and metadata support."
    )

# Read requirements from requirements.txt
requirements_file = here / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f.readlines()
            if line.strip() and not line.startswith("#")
        ]
else:
    # Fallback requirements if file doesn't exist
    requirements = [
        "Pillow>=9.0.0",
        "rich>=13.0.0",
        "numpy>=1.21.0",
        "tqdm>=4.64.0"
    ]

# Separate core requirements from optional ones
core_requirements = []
dev_requirements = []
for req in requirements:
    if any(dev_pkg in req.lower() for dev_pkg in ['pytest', 'black', 'flake8', 'mypy', 'sphinx']):
        dev_requirements.append(req)
    else:
        core_requirements.append(req)

# Package metadata
__version__ = "1.0.0"
__author__ = "SATISH Format Team"
__email__ = "contact@satishformat.dev"
__url__ = "https://github.com/satish-format/satish-python"

# Prepare custom command classes for setup
cmdclass = {}
try:
    from setuptools import Command

    class PostInstallCommand(Command):
        """Custom post-installation tasks."""
        description = "Run post-installation tasks"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            # Print post-install message
            print(
                "SATISH Image Format installed successfully."
                "\nQuick Start:"
                "\n    satish convert image.jpg    # Convert to SATISH"
                "\n    satish extract file.satish  # Extract to PNG"
                "\n    satish info file.satish     # Show file info"
                "\n    satish help               # Show all commands"
                "\nDocumentation: https://github.com/satish-format/satish-python/docs"
                "\nReport Issues: https://github.com/satish-format/satish-python/issues"
            )

    class TestCommand(Command):
        """Run test suite via pytest."""
        description = "Run test suite"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            import subprocess, sys
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "tests/", "-v", "--cov=satish"
            ])
            sys.exit(result.returncode)

    class LintCommand(Command):
        """Run linting checks (black, flake8, mypy)."""
        description = "Run code linting"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            import subprocess, sys
            commands = [
                [sys.executable, "-m", "black", "--check", "satish/"],
                [sys.executable, "-m", "flake8", "satish/"],
                [sys.executable, "-m", "mypy", "satish/"],
            ]
            for cmd in commands:
                print(f"Running: {' '.join(cmd)}")
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    sys.exit(result.returncode)

    cmdclass.update({
        'post_install': PostInstallCommand,
        'test': TestCommand,
        'lint': LintCommand,
    })
except ImportError:
    pass

# Setup invocation
setup(
    name="satish-format",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description="SATISH Image Format - Modern, efficient image format with advanced compression",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,

    url=__url__,
    project_urls={
        "Bug Reports": f"{__url__}/issues",
        "Source": __url__,
        "Documentation": f"{__url__}/docs",
        "Changelog": f"{__url__}/blob/main/CHANGELOG.md",
    },

    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    package_dir={"": "."},
    include_package_data=True,
    package_data={
        "satish": ["*.txt", "*.md", "*.json"],
    },

    python_requires=">=3.7",
    install_requires=core_requirements,
    extras_require={
        "dev": dev_requirements,
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinxcontrib-napoleon>=0.7",
        ],
        "testing": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.0.0",
        ],
        "linting": [
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "isort>=5.0.0",
        ],
        "all": dev_requirements + [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },

    entry_points={
        "console_scripts": [
            "satish=satish.cli.main:cli_entry_point",
            "satish-convert=satish.cli.main:cli_entry_point",
        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Environment :: Other Environment",
    ],

    keywords=[
        "image", "format", "compression", "satish", "graphics",
        "multimedia", "conversion", "metadata", "cli", "tool"
    ],

    zip_safe=False,
    platforms=["any"],
    license="MIT",
    license_files=["LICENSE"],

    test_suite="tests",
    tests_require=["pytest>=7.0.0", "pytest-cov>=4.0.0"],

    cmdclass=cmdclass,
    options={
        "build": {"build_base": "build"},
        "bdist_wheel": {"universal": False},
    },
)

# Verification that all required files exist
def verify_package_structure():
    """Verify that the package structure is correct."""
    required_files = [
        "satish/__init__.py",
        "satish/core/__init__.py",
        "satish/utils/__init__.py",
        "satish/cli/__init__.py",
    ]
    missing_files = []
    for file_path in required_files:
        if not (here / file_path).exists():
            missing_files.append(file_path)
    if missing_files:
        print("Warning: Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("Package may not work correctly without these files.")
    else:
        print("Package structure verified successfully!")

if __name__ == "__main__":
    # Verify package structure before setup
    verify_package_structure()
