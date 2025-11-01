"""PDF merging functionality."""

import PyPDF2
from pathlib import Path
from .compress import compress_pdf


def merge_pdfs(input_files, output_file, compression_level=None):
    """Merge multiple PDF files into a single PDF.

    Args:
        input_files: List of input PDF file paths
        output_file: Output PDF file path
        compression_level: Optional compression level ('basic', 'medium', 'aggressive')
    """
    merger = PyPDF2.PdfMerger()

    try:
        for file_path in input_files:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"Input file not found: {file_path}")
            if not path.suffix.lower() == '.pdf':
                raise ValueError(f"File is not a PDF: {file_path}")

            with open(path, 'rb') as pdf_file:
                merger.append(pdf_file)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as output:
            merger.write(output)

        print(f"Successfully merged {len(input_files)} files into {output_file}")

        # Apply compression if requested
        if compression_level:
            temp_output = str(output_path) + '.tmp'
            output_path.rename(temp_output)
            compress_pdf(temp_output, output_file, compression_level)
            Path(temp_output).unlink()

    except Exception as e:
        print(f"Error merging PDFs: {e}")
        raise
    finally:
        merger.close()