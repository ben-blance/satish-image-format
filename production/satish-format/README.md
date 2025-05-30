# SATISH Image Format - Modular Project Structure

satish-format/
├── README.md
├── setup.py
├── requirements.txt
├── satish/
│   ├── **init**.py
│   ├── core/
│   │   ├── **init**.py
│   │   ├── format.py          # Core format definition
│   │   ├── encoder.py         # Image → SATISH conversion
│   │   ├── decoder.py         # SATISH → Image conversion
│   │   └── validator.py       # File validation
│   ├── utils/
│   │   ├── **init**.py
│   │   ├── colors.py          # Color conversion utilities
│   │   ├── file_utils.py      # File I/O helpers
│   │   └── exceptions.py      # Custom exceptions
│   └── cli/
│       ├── **init**.py
│       ├── commands.py        # CLI command handlers
│       └── main.py           # CLI entry point
├── tests/
│   ├── **init**.py
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

## Key Benefits of This Structure:
### 🔧 Core Module (satish/core/)
- format.py: Defines the SATISH format specification
- encoder.py: Handles image → .satish conversion
- decoder.py: Handles .satish → image conversion
- validator.py: Validates .satish files
### 🛠️ Utils Module (satish/utils/)
- colors.py: RGB ↔ Hex conversion, color utilities
- file_utils.py: File I/O, path handling
- exceptions.py: Custom error types
### 💻 CLI Module (satish/cli/)
- main.py: Command-line interface entry point
- commands.py: Individual CLI commands
### 🧪 Tests (tests/)
- Unit tests for each module
- Integration tests
### 📚 Documentation (docs/)
- Format specification
- API documentation
- Usage examples
## Installation & Usage:
bash
# Development install
pip install -e .
# Use as CLI tool
satish convert image.jpg output.satish
satish view image.satish
satish info image.satish
# Use as Python library
from satish import SatishEncoder, SatishDecoder
encoder = SatishEncoder()
encoder.save('input.jpg', 'output.satish')
