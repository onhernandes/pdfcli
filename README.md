# PDF Manager

A powerful Python CLI tool for managing PDF files with merge, walk, and compression functionality.

## ✨ Features

- 🔗 **Merge**: Combine multiple PDF files into a single PDF with optional compression
- 🚶 **Walk**: Navigate through PDF files in a directory with optional range filtering and compression
- 🗜️ **Compress**: Compress PDF files with configurable quality levels (basic, medium, aggressive)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download** the PDF Manager project
2. **Navigate** to the project directory:
   ```bash
   cd pdf-manager
   ```

3. **Install** the package:
   ```bash
   # Basic installation
   pip install -e .

   # Or install with development dependencies
   pip install -e .[test]
   ```

4. **Verify** installation:
   ```bash
   pdf-manager --help
   ```

### Basic Usage

#### Merge PDFs
```bash
# Combine two or more PDFs
pdf-manager merge file1.pdf file2.pdf file3.pdf -o combined.pdf

# Merge with compression
pdf-manager merge *.pdf -o compressed_merge.pdf --compress medium
```

#### Create PDF Volumes from Directory
```bash
# Create volumes from PDFs (default: 10 files per volume)
pdf-manager walk /path/to/pdfs /path/to/output

# Create volumes with custom batch size
pdf-manager walk /path/to/pdfs /path/to/output --batch-size 5

# Create volumes with custom naming
pdf-manager walk /path/to/pdfs /path/to/output --prefix "manga_" --suffix "_vol"
```

#### Compress Single PDF
```bash
# Compress with default settings
pdf-manager compress large_file.pdf compressed_file.pdf

# Aggressive compression for maximum size reduction
pdf-manager compress input.pdf output.pdf --compress aggressive
```

## 📖 Commands Reference

### `merge` - Combine PDFs

Merge multiple PDF files into a single output file.

**Syntax:**
```bash
pdf-manager merge [FILES...] -o OUTPUT [OPTIONS]
```

**Arguments:**
- `FILES`: Two or more PDF files to merge

**Options:**
- `-o, --output` (required): Output PDF file path
- `-c, --compress`: Compression level (`basic`, `medium`, `aggressive`)

**Examples:**
```bash
pdf-manager merge doc1.pdf doc2.pdf doc3.pdf -o final.pdf
pdf-manager merge *.pdf -o all_documents.pdf --compress basic
```

### `walk` - Create PDF Volumes

Process PDF files in batches to create volume files that merge multiple PDFs together.

**Syntax:**
```bash
pdf-manager walk INPUT_DIR OUTPUT_DIR [OPTIONS]
```

**Arguments:**
- `INPUT_DIR`: Directory containing PDF files to process
- `OUTPUT_DIR`: Directory where volume files will be created

**Options:**
- `--order`: File ordering (`asc` or `desc`, default: `asc`)
- `--batch-size`: Number of files per volume (default: `10`)
- `--prefix`: Prefix for volume filenames (default: empty)
- `--suffix`: Suffix for volume filenames (default: empty)
- `-c, --compress`: Compression level (`basic`, `medium`, `aggressive`)

**Examples:**
```bash
# Basic volume creation (10 files per volume)
pdf-manager walk ./scans ./volumes

# Custom batch size and ordering
pdf-manager walk ./documents ./volumes --batch-size 5 --order desc

# Custom naming with compression
pdf-manager walk ./manga ./volumes --prefix "Chapter_" --suffix "_Complete" --compress medium

# Small batches for organization
pdf-manager walk ./papers ./organized --batch-size 3 --prefix "Collection_"
```

### `compress` - Compress Single PDF

Compress a PDF file with specified compression level.

**Syntax:**
```bash
pdf-manager compress INPUT OUTPUT [OPTIONS]
```

**Arguments:**
- `INPUT`: PDF file to compress
- `OUTPUT`: Compressed PDF output file path

**Options:**
- `-c, --compress`: Compression level (default: `medium`)
- `--info`: Show compression level information

**Examples:**
```bash
pdf-manager compress large.pdf small.pdf
pdf-manager compress input.pdf output.pdf --compress aggressive
pdf-manager compress --info  # Show compression options
```

## 🎛️ Compression Levels

| Level | Quality | Compression | Use Case |
|-------|---------|-------------|----------|
| **basic** | High | Low | Preserve quality, minimal size reduction |
| **medium** | Good | Moderate | Balanced quality and file size |
| **aggressive** | Variable | High | Maximum compression, may affect quality |

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install -e .[test]

# Run all tests
pytest

# Run with coverage report
pytest --cov=pdf_manager --cov-report=html

# Run specific test types
pytest -m unit        # Unit tests only
pytest -m cli         # CLI tests only

# Using make commands (if available)
make test             # Run all tests
make test-cov         # Run with coverage
make test-unit        # Unit tests only
make test-cli         # CLI tests only
```

### Test Structure

- **Unit tests**: Test individual functions and modules
- **CLI tests**: Test command-line interface behavior
- **Integration tests**: Test component interaction
- **Fixtures**: Automatic PDF generation for testing

## 🔧 Development

### Project Structure

```
pdf-manager/
├── pdf_manager/          # Main package
│   ├── __init__.py
│   ├── cli.py           # CLI interface
│   ├── merge.py         # PDF merging
│   ├── walk.py          # Directory walking
│   └── compress.py      # PDF compression
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures
│   ├── test_cli.py      # CLI tests
│   ├── test_merge.py    # Merge tests
│   ├── test_walk.py     # Walk tests
│   └── test_compress.py # Compression tests
├── requirements.txt     # Dependencies
├── setup.py            # Package configuration
├── pytest.ini         # Test configuration
├── Makefile           # Development commands
└── README.md          # This file
```

### Dependencies

**Runtime:**
- `PyPDF2>=3.0.0` - PDF manipulation
- `click>=8.0.0` - CLI framework

**Development:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `reportlab>=3.6.0` - PDF generation for tests

## 📚 More Examples

For more detailed usage examples and recipes, see [recipes.md](recipes.md).

## 🐛 Troubleshooting

### Common Issues

**1. Command not found: `pdf-manager`**
```bash
# Ensure you're in the right directory and installed correctly
cd pdf-manager
pip install -e .
```

**2. Permission errors**
```bash
# On Unix systems, you might need to make files executable
chmod +x pdf-manager
```

**3. Python version issues**
```bash
# Check Python version (requires 3.7+)
python --version

# Use specific Python version if needed
python3.8 -m pip install -e .
```

**4. PyPDF2 errors with certain PDF files**
- Some PDF files may have compatibility issues
- Try different compression levels
- Check if the input PDF is corrupted

### Getting Help

```bash
# General help
pdf-manager --help

# Command-specific help
pdf-manager merge --help
pdf-manager walk --help
pdf-manager compress --help

# Show compression options
pdf-manager compress --info
```

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `make test`
5. Submit a pull request

---

**Happy PDF managing! 📄✨**