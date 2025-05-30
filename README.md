# SATISH Image Format

A custom image format with CLI and Python library support for encoding, decoding, viewing, and validating `.satish` files.

## 🔧 Installation & Setup

Install in development mode:

```bash
# Navigate to your satish-format directory
cd satish-format/

# Install in development mode (creates the 'satish' command)
pip install -e .
```

## 🚀 CLI Usage Examples

### 1. Convert Images to SATISH Format

```bash
# Convert a single image
satish convert photo.jpg photo.satish

# Convert with specific output path
satish convert /path/to/image.png /path/to/output.satish

# Overwrite existing files
satish convert image.jpg output.satish --overwrite
```

### 2. Convert SATISH Back to Standard Images

```bash
# Convert SATISH to PNG
satish convert photo.satish photo.png

# Convert to JPEG with quality setting
satish convert photo.satish photo.jpg --quality 90
```

### 3. View SATISH Images

```bash
# Display a SATISH image
satish view photo.satish

# View without showing file info
satish view photo.satish --no-info
```

### 4. Get File Information

```bash
# Basic file info
satish info photo.satish

# Show more pixel details
satish info photo.satish --hex-preview 10

# Show raw header bytes
satish info photo.satish --show-header
```

### 5. Validate Files

```bash
# Basic validation
satish validate photo.satish

# Strict validation mode
satish validate photo.satish --strict
```

### 6. Batch Convert Multiple Files

```bash
# Convert all JPGs in current directory
satish batch *.jpg --output-dir satish_files/

# Parallel processing for faster conversion
satish batch *.jpg *.png --parallel --workers 8

# Add suffix to output files
satish batch photos/*.jpg --suffix "_converted" --output-dir output/
```

## 📋 Complete Command Reference

### Global Options

```bash
satish --help         # Show help
satish --version      # Show version
satish --verbose      # Enable verbose output
```

### Convert Command

```bash
satish convert INPUT OUTPUT [OPTIONS]

Options:
  --quality INT       Output quality for lossy formats (1-100)
  --overwrite         Overwrite existing output file
```

### View Command

```bash
satish view FILE [OPTIONS]

Options:
  --no-info           Don't show image information
```

### Info Command

```bash
satish info FILE [OPTIONS]

Options:
  --hex-preview INT   Number of pixels to show in hex (default: 5)
  --show-header       Show raw header bytes
```

### Validate Command

```bash
satish validate FILE [OPTIONS]

Options:
  --strict            Use strict validation mode
```

### Batch Command

```bash
satish batch FILES... [OPTIONS]

Options:
  --output-dir, -o DIR    Output directory (default: current)
  --suffix TEXT           Suffix to add to filenames
  --parallel, -p          Enable parallel processing
  --workers INT           Number of worker processes (default: 4)
```

## 🎯 Real-World Usage Examples

### Convert a Photo Collection

```bash
satish batch ~/Photos/*.jpg --output-dir ~/SatishPhotos/ --parallel

# Convert with progress tracking
satish batch vacation/*.* --output-dir satish/ --verbose
```

### Quality Comparison

```bash
satish convert large_image.png compressed.satish
satish info compressed.satish
```

### Validation Workflow

```bash
for file in *.satish; do
    echo "Checking $file..."
    satish validate "$file" --strict
done
```

## 🛠️ Troubleshooting

### Command Not Found

```bash
pip install -e .
which satish
python -m satish.cli.main --help
```

### Import Errors

```bash
pip install -r requirements.txt
python -c "import satish; print('OK')"
```

### Permission Issues

```bash
pip install --user -e .
```

## 📊 Example Workflow

```bash
satish batch *.jpg --output-dir satish_images/ --parallel
ls satish_images/
satish info satish_images/photo.satish --hex-preview 3
satish view satish_images/photo.satish
satish convert satish_images/photo.satish verification.png
satish validate satish_images/*.satish
```

## 🧱 Project Structure

```
satish-format/
├── README.md
├── setup.py
├── requirements.txt
├── satish/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── format.py
│   │   ├── encoder.py
│   │   ├── decoder.py
│   │   └── validator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── colors.py
│   │   ├── file_utils.py
│   │   └── exceptions.py
│   └── cli/
│       ├── __init__.py
│       ├── commands.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_core/
│   │   ├── test_encoder.py
│   │   ├── test_decoder.py
│   │   └── test_format.py
│   └── test_utils/
│       ├── test_colors.py
│       └── test_file_utils.py
├── examples/
│   ├── basic_usage.py
│   ├── batch_convert.py
│   └── custom_metadata.py
└── docs/
    ├── format_spec.md
    ├── api_reference.md
    └── examples.md
```

## 📚 Python Library Example

```python
from satish import SatishEncoder, SatishDecoder

encoder = SatishEncoder()
success = encoder.encode_image('images.jpeg', 'test.satish')
print(f"Encoding successful: {success}")
```
