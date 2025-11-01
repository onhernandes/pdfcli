"""Tests for the merge module."""

import pytest
import PyPDF2
from pathlib import Path
from pdf_manager.merge import merge_pdfs


@pytest.mark.unit
class TestMerge:
    """Test merge functionality."""

    def test_merge_two_pdfs(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merging two PDF files."""
        output_file = temp_dir / "merged.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file))

        assert output_file.exists()
        assert output_file.stat().st_size > 0

        # Verify the merged PDF has pages from both inputs
        with open(output_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            # sample_pdf has 1 page, sample_pdf_2 has 2 pages
            assert len(reader.pages) == 3

    def test_merge_three_pdfs(self, sample_pdf, sample_pdf_2, sample_pdf_3, temp_dir):
        """Test merging three PDF files."""
        output_file = temp_dir / "merged_three.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2), str(sample_pdf_3)]

        merge_pdfs(input_files, str(output_file))

        assert output_file.exists()

        # Verify page count
        with open(output_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            # 1 + 2 + 1 pages
            assert len(reader.pages) == 4

    def test_merge_with_compression(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merging PDFs with compression."""
        output_file = temp_dir / "merged_compressed.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file), compression_level='medium')

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_merge_with_basic_compression(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merging PDFs with basic compression."""
        output_file = temp_dir / "merged_basic.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file), compression_level='basic')

        assert output_file.exists()

    def test_merge_with_aggressive_compression(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merging PDFs with aggressive compression."""
        output_file = temp_dir / "merged_aggressive.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file), compression_level='aggressive')

        assert output_file.exists()

    def test_merge_creates_output_directory(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test that merge creates output directory if it doesn't exist."""
        output_dir = temp_dir / "new_output_dir"
        output_file = output_dir / "merged.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file))

        assert output_file.exists()
        assert output_dir.exists()

    def test_merge_nonexistent_input_file(self, sample_pdf, temp_dir):
        """Test merge with nonexistent input file."""
        nonexistent_file = temp_dir / "nonexistent.pdf"
        output_file = temp_dir / "merged.pdf"
        input_files = [str(sample_pdf), str(nonexistent_file)]

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            merge_pdfs(input_files, str(output_file))

    def test_merge_non_pdf_input_file(self, sample_pdf, non_pdf_file, temp_dir):
        """Test merge with non-PDF input file."""
        output_file = temp_dir / "merged.pdf"
        input_files = [str(sample_pdf), str(non_pdf_file)]

        with pytest.raises(ValueError, match="File is not a PDF"):
            merge_pdfs(input_files, str(output_file))

    def test_merge_empty_input_list(self, temp_dir):
        """Test merge with empty input list."""
        output_file = temp_dir / "merged.pdf"
        input_files = []

        # This should complete without error but create an empty PDF
        merge_pdfs(input_files, str(output_file))

        assert output_file.exists()

    def test_merge_single_pdf(self, sample_pdf, temp_dir):
        """Test merge with single PDF (should work as copy)."""
        output_file = temp_dir / "single_merged.pdf"
        input_files = [str(sample_pdf)]

        merge_pdfs(input_files, str(output_file))

        assert output_file.exists()

        # Verify page count matches original
        with open(output_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            assert len(reader.pages) == 1

    def test_merge_preserves_content(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test that merge preserves content from input PDFs."""
        output_file = temp_dir / "merged_content.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file))

        # Read the merged PDF and check it has content
        with open(output_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            # First page should have content from first PDF
            first_page_text = reader.pages[0].extract_text()
            assert "test PDF" in first_page_text

            # Second page should have content from second PDF
            second_page_text = reader.pages[1].extract_text()
            assert "second test PDF" in second_page_text

    def test_merge_invalid_compression_level(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merge with invalid compression level."""
        output_file = temp_dir / "merged.pdf"
        input_files = [str(sample_pdf), str(sample_pdf_2)]

        with pytest.raises(ValueError, match="Invalid compression level"):
            merge_pdfs(input_files, str(output_file), compression_level='invalid')

    def test_merge_file_order_preservation(self, sample_pdf, sample_pdf_2, sample_pdf_3, temp_dir):
        """Test that merge preserves the order of input files."""
        output_file = temp_dir / "ordered_merge.pdf"
        input_files = [str(sample_pdf_3), str(sample_pdf), str(sample_pdf_2)]

        merge_pdfs(input_files, str(output_file))

        with open(output_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            # First page should be from sample_pdf_3
            first_page_text = reader.pages[0].extract_text()
            assert "third test PDF" in first_page_text

            # Second page should be from sample_pdf
            second_page_text = reader.pages[1].extract_text()
            assert "This is a test PDF" in second_page_text