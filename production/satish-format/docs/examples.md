🔧 Installation & Setup
First, install your package in development mode:
bash# Navigate to your satish-format directory
cd satish-format/

# Install in development mode (creates the 'satish' command)
pip install -e .
🚀 CLI Usage Examples
1. Convert Images to SATISH Format
bash# Convert a single image
satish convert photo.jpg photo.satish

# Convert with specific output path
satish convert /path/to/image.png /path/to/output.satish

# Overwrite existing files
satish convert image.jpg output.satish --overwrite
2. Convert SATISH Back to Standard Images
bash# Convert SATISH to PNG
satish convert photo.satish photo.png

# Convert to JPEG with quality setting
satish convert photo.satish photo.jpg --quality 90
3. View SATISH Images
bash# Display a SATISH image (opens in default image viewer)
satish view photo.satish

# View without showing file info
satish view photo.satish --no-info
4. Get File Information
bash# Basic file info
satish info photo.satish

# Show more pixel details
satish info photo.satish --hex-preview 10

# Show raw header bytes
satish info photo.satish --show-header
5. Validate Files
bash# Basic validation
satish validate photo.satish

# Strict validation mode
satish validate photo.satish --strict
6. Batch Convert Multiple Files
bash# Convert all JPGs in current directory
satish batch *.jpg --output-dir satish_files/

# Parallel processing for faster conversion
satish batch *.jpg *.png --parallel --workers 8

# Add suffix to output files
satish batch photos/*.jpg --suffix "_converted" --output-dir output/
📋 Complete Command Reference
Global Options
bashsatish --help              # Show help
satish --version           # Show version
satish --verbose convert   # Enable verbose output
Convert Command
bashsatish convert INPUT OUTPUT [OPTIONS]

Options:
  --quality INT     Output quality for lossy formats (1-100)
  --overwrite       Overwrite existing output file
View Command
bashsatish view FILE [OPTIONS]

Options:
  --no-info         Don't show image information
Info Command
bashsatish info FILE [OPTIONS]

Options:
  --hex-preview INT    Number of pixels to show in hex (default: 5)
  --show-header        Show raw header bytes
Validate Command
bashsatish validate FILE [OPTIONS]

Options:
  --strict             Use strict validation mode
Batch Command
bashsatish batch FILES... [OPTIONS]

Options:
  --output-dir, -o DIR    Output directory (default: current)
  --suffix TEXT           Suffix to add to filenames
  --parallel, -p          Enable parallel processing
  --workers INT           Number of worker processes (default: 4)
🎯 Real-World Usage Examples
Convert a Photo Collection
bash# Convert all photos in a directory
satish batch ~/Photos/*.jpg --output-dir ~/SatishPhotos/ --parallel

# Convert with progress tracking
satish batch vacation/*.* --output-dir satish/ --verbose
Quality Comparison
bash# Convert and check file sizes
satish convert large_image.png compressed.satish
satish info compressed.satish
Validation Workflow
bash# Validate a batch of files
for file in *.satish; do
    echo "Checking $file..."
    satish validate "$file" --strict
done
🛠️ Troubleshooting
If satish command not found:
bash# Make sure you installed the package
pip install -e .

# Check if it's in your PATH
which satish

# Try running directly
python -m satish.cli.main --help
Import Errors:
bash# Make sure all dependencies are installed
pip install -r requirements.txt

# Check your Python path
python -c "import satish; print('OK')"
Permission Issues:
bash# On some systems, you might need
pip install --user -e .
📊 Example Workflow
bash# 1. Convert some images
satish batch *.jpg --output-dir satish_images/ --parallel

# 2. Check what was created
ls satish_images/

# 3. Inspect a file
satish info satish_images/photo.satish --hex-preview 3

# 4. View an image
satish view satish_images/photo.satish

# 5. Convert back to verify
satish convert satish_images/photo.satish verification.png

# 6. Validate the files
satish validate satish_images/*.satish