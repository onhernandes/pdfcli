"""Test fixtures and configuration for pdf-manager tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_pdf(temp_dir):
    """Create a sample PDF file for testing."""
    pdf_path = temp_dir / "sample.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "This is a test PDF")
    c.drawString(100, 730, "Page 1 content")
    c.showPage()
    c.save()
    return pdf_path


@pytest.fixture
def sample_pdf_2(temp_dir):
    """Create a second sample PDF file for testing."""
    pdf_path = temp_dir / "sample2.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "This is the second test PDF")
    c.drawString(100, 730, "Page 1 of second PDF")
    c.showPage()
    c.drawString(100, 750, "Page 2 of second PDF")
    c.showPage()
    c.save()
    return pdf_path


@pytest.fixture
def sample_pdf_3(temp_dir):
    """Create a third sample PDF file for testing."""
    pdf_path = temp_dir / "sample3.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "This is the third test PDF")
    c.drawString(100, 730, "Single page content")
    c.showPage()
    c.save()
    return pdf_path


@pytest.fixture
def pdf_directory(temp_dir, sample_pdf, sample_pdf_2, sample_pdf_3):
    """Create a directory with multiple PDF files for testing walk functionality."""
    # Create additional PDFs with numbered names
    for i in range(1, 6):
        pdf_path = temp_dir / f"document_{i:02d}.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, f"Document {i}")
        c.drawString(100, 730, f"Content for document number {i}")
        c.showPage()
        c.save()

    return temp_dir


@pytest.fixture
def non_pdf_file(temp_dir):
    """Create a non-PDF file for testing error handling."""
    file_path = temp_dir / "not_a_pdf.txt"
    file_path.write_text("This is not a PDF file")
    return file_path


@pytest.fixture
def output_dir(temp_dir):
    """Create an output directory for compressed files."""
    output_path = temp_dir / "output"
    output_path.mkdir()
    return output_path


@pytest.fixture
def manga_chapter_directory(temp_dir):
    """Create a directory with manga chapter PDFs including float chapter numbers."""
    # Create chapters with integer and float numbers
    chapter_names = [
        "Chap 1.pdf",
        "Chap 2.pdf",
        "Chap 9.pdf",
        "Chap 9.5.pdf",
        "Chap 10.pdf",
        "Chap 10.5.pdf",
        "Chap 11.pdf",
        "Chap 20.pdf",
        "Chap 100.pdf"
    ]

    for name in chapter_names:
        pdf_path = temp_dir / name
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, f"Manga {name}")
        c.drawString(100, 730, f"Content for {name}")
        c.showPage()
        c.save()

    return temp_dir