"""PDF compression functionality with configurable quality levels."""

import PyPDF2
from pathlib import Path


COMPRESSION_LEVELS = {
    'basic': {
        'quality': 85,
        'compress_streams': True,
        'compress_images': False,
        'description': 'Basic compression - keeps high quality, less compression'
    },
    'medium': {
        'quality': 65,
        'compress_streams': True,
        'compress_images': True,
        'description': 'Medium compression - good quality with more compression'
    },
    'aggressive': {
        'quality': 35,
        'compress_streams': True,
        'compress_images': True,
        'description': 'Aggressive compression - may lose quality for maximum compression'
    }
}


def compress_pdf(input_file, output_file, compression_level='medium'):
    """Compress a PDF file with specified compression level.

    Args:
        input_file: Input PDF file path
        output_file: Output PDF file path
        compression_level: Compression level ('basic', 'medium', 'aggressive')
    """
    if compression_level not in COMPRESSION_LEVELS:
        raise ValueError(f"Invalid compression level. Choose from: {list(COMPRESSION_LEVELS.keys())}")

    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    if not input_path.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {input_file}")

    settings = COMPRESSION_LEVELS[compression_level]

    try:
        with open(input_path, 'rb') as input_pdf:
            reader = PyPDF2.PdfReader(input_pdf)
            writer = PyPDF2.PdfWriter()

            # Copy pages and apply compression
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]

                # Apply compression settings
                if settings['compress_streams']:
                    page.compress_content_streams()

                if settings['compress_images']:
                    # PyPDF2 has limited image compression capabilities
                    # For more advanced image compression, consider using pikepdf
                    pass

                writer.add_page(page)

            # Apply writer-level compression
            if settings['compress_streams']:
                writer.compress_identical_objects()
                writer.remove_duplication()

            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)

        # Get file sizes for comparison
        original_size = input_path.stat().st_size
        compressed_size = output_path.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100

        print(f"Compression complete:")
        print(f"  Original size: {original_size:,} bytes")
        print(f"  Compressed size: {compressed_size:,} bytes")
        print(f"  Compression ratio: {compression_ratio:.1f}%")
        print(f"  Level: {compression_level} - {settings['description']}")

    except Exception as e:
        print(f"Error compressing PDF: {e}")
        raise


def get_compression_info():
    """Get information about available compression levels."""
    info = "Available compression levels:\n"
    for level, settings in COMPRESSION_LEVELS.items():
        info += f"  {level}: {settings['description']}\n"
    return info.strip()