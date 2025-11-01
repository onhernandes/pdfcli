"""Tests for the compression module."""

import pytest
from pathlib import Path
from pdf_manager.compress import compress_pdf, get_compression_info, COMPRESSION_LEVELS


@pytest.mark.unit
class TestCompression:
    """Test compression functionality."""

    def test_compress_pdf_basic(self, sample_pdf, temp_dir):
        """Test basic PDF compression."""
        output_file = temp_dir / "compressed_basic.pdf"

        compress_pdf(str(sample_pdf), str(output_file), 'basic')

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_compress_pdf_medium(self, sample_pdf, temp_dir):
        """Test medium PDF compression."""
        output_file = temp_dir / "compressed_medium.pdf"

        compress_pdf(str(sample_pdf), str(output_file), 'medium')

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_compress_pdf_aggressive(self, sample_pdf, temp_dir):
        """Test aggressive PDF compression."""
        output_file = temp_dir / "compressed_aggressive.pdf"

        compress_pdf(str(sample_pdf), str(output_file), 'aggressive')

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_compress_pdf_creates_output_directory(self, sample_pdf, temp_dir):
        """Test that compression creates output directory if it doesn't exist."""
        output_dir = temp_dir / "new_directory"
        output_file = output_dir / "compressed.pdf"

        compress_pdf(str(sample_pdf), str(output_file), 'medium')

        assert output_file.exists()
        assert output_dir.exists()

    def test_compress_pdf_invalid_level(self, sample_pdf, temp_dir):
        """Test compression with invalid compression level."""
        output_file = temp_dir / "compressed.pdf"

        with pytest.raises(ValueError, match="Invalid compression level"):
            compress_pdf(str(sample_pdf), str(output_file), 'invalid')

    def test_compress_pdf_nonexistent_input(self, temp_dir):
        """Test compression with nonexistent input file."""
        input_file = temp_dir / "nonexistent.pdf"
        output_file = temp_dir / "compressed.pdf"

        with pytest.raises(FileNotFoundError, match="Input file not found"):
            compress_pdf(str(input_file), str(output_file), 'medium')

    def test_compress_pdf_non_pdf_input(self, non_pdf_file, temp_dir):
        """Test compression with non-PDF input file."""
        output_file = temp_dir / "compressed.pdf"

        with pytest.raises(ValueError, match="File is not a PDF"):
            compress_pdf(str(non_pdf_file), str(output_file), 'medium')

    def test_compression_reduces_file_size(self, sample_pdf_2, temp_dir):
        """Test that compression actually reduces file size (with larger PDF)."""
        output_file = temp_dir / "compressed.pdf"
        original_size = sample_pdf_2.stat().st_size

        compress_pdf(str(sample_pdf_2), str(output_file), 'aggressive')
        compressed_size = output_file.stat().st_size

        # Compression should reduce size or at least not increase it significantly
        assert compressed_size <= original_size * 1.1  # Allow 10% margin for metadata

    def test_get_compression_info(self):
        """Test getting compression level information."""
        info = get_compression_info()

        assert isinstance(info, str)
        assert "basic" in info
        assert "medium" in info
        assert "aggressive" in info
        assert "High quality" in info
        assert "Good quality" in info
        assert "may lose quality" in info

    def test_compression_levels_structure(self):
        """Test that compression levels have correct structure."""
        for level_name, level_config in COMPRESSION_LEVELS.items():
            assert 'quality' in level_config
            assert 'compress_streams' in level_config
            assert 'compress_images' in level_config
            assert 'description' in level_config

            assert isinstance(level_config['quality'], int)
            assert isinstance(level_config['compress_streams'], bool)
            assert isinstance(level_config['compress_images'], bool)
            assert isinstance(level_config['description'], str)

    def test_compression_levels_quality_order(self):
        """Test that compression levels have quality in correct order."""
        basic_quality = COMPRESSION_LEVELS['basic']['quality']
        medium_quality = COMPRESSION_LEVELS['medium']['quality']
        aggressive_quality = COMPRESSION_LEVELS['aggressive']['quality']

        assert basic_quality > medium_quality > aggressive_quality