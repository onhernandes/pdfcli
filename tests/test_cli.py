"""Tests for the CLI interface."""

import pytest
from click.testing import CliRunner
from pathlib import Path
from pdf_manager.cli import main


@pytest.mark.cli
class TestCLI:
    """Test CLI interface."""

    def setup_method(self):
        """Set up test method with CLI runner."""
        self.runner = CliRunner()

    def test_main_help(self):
        """Test main command help."""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert "PDF Manager" in result.output
        assert "merge" in result.output
        assert "walk" in result.output
        assert "compress" in result.output

    def test_main_version(self):
        """Test main command version."""
        result = self.runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_merge_help(self):
        """Test merge command help."""
        result = self.runner.invoke(main, ['merge', '--help'])
        assert result.exit_code == 0
        assert "Merge multiple PDF files" in result.output
        assert "--output" in result.output
        assert "--compress" in result.output

    def test_merge_command(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merge command execution."""
        output_file = temp_dir / "merged_cli.pdf"

        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            str(sample_pdf_2),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()
        assert "Successfully merged" in result.output

    def test_merge_with_compression(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merge command with compression."""
        output_file = temp_dir / "merged_compressed_cli.pdf"

        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            str(sample_pdf_2),
            '--output', str(output_file),
            '--compress', 'medium'
        ])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_merge_insufficient_files(self, sample_pdf, temp_dir):
        """Test merge command with insufficient input files."""
        output_file = temp_dir / "merged_fail.pdf"

        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0  # Click doesn't exit with error code for this
        assert "At least two input files are required" in result.output

    def test_merge_nonexistent_file(self, sample_pdf, temp_dir):
        """Test merge command with nonexistent file."""
        nonexistent = temp_dir / "nonexistent.pdf"
        output_file = temp_dir / "merged_fail.pdf"

        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            str(nonexistent),
            '--output', str(output_file)
        ])

        assert result.exit_code == 0
        assert "Error:" in result.output

    def test_walk_help(self):
        """Test walk command help."""
        result = self.runner.invoke(main, ['walk', '--help'])
        assert result.exit_code == 0
        assert "Walk through PDF files" in result.output
        assert "--start" in result.output
        assert "--end" in result.output
        assert "--compress" in result.output
        assert "--output-dir" in result.output

    def test_walk_command(self, pdf_directory):
        """Test walk command execution."""
        result = self.runner.invoke(main, ['walk', str(pdf_directory)])

        assert result.exit_code == 0
        assert "Walking through PDF files" in result.output
        assert "Total files in range:" in result.output

    def test_walk_with_range(self, pdf_directory):
        """Test walk command with range."""
        result = self.runner.invoke(main, [
            'walk',
            str(pdf_directory),
            '--start', '2',
            '--end', '4'
        ])

        assert result.exit_code == 0
        assert "Walking through PDF files 2 to 4" in result.output

    def test_walk_with_compression(self, pdf_directory, output_dir):
        """Test walk command with compression."""
        result = self.runner.invoke(main, [
            'walk',
            str(pdf_directory),
            '--start', '1',
            '--end', '2',
            '--compress', 'basic',
            '--output-dir', str(output_dir)
        ])

        assert result.exit_code == 0
        assert "Compressed files saved to:" in result.output

        # Check files were created
        compressed_files = list(output_dir.glob("*.pdf"))
        assert len(compressed_files) == 2

    def test_walk_nonexistent_directory(self, temp_dir):
        """Test walk command with nonexistent directory."""
        nonexistent_dir = temp_dir / "nonexistent"

        result = self.runner.invoke(main, ['walk', str(nonexistent_dir)])

        assert result.exit_code == 2  # Click path validation error

    def test_compress_help(self):
        """Test compress command help."""
        result = self.runner.invoke(main, ['compress', '--help'])
        assert result.exit_code == 0
        assert "Compress a PDF file" in result.output
        assert "--compress" in result.output
        assert "--info" in result.output

    def test_compress_command(self, sample_pdf, temp_dir):
        """Test compress command execution."""
        output_file = temp_dir / "compressed_cli.pdf"

        result = self.runner.invoke(main, [
            'compress',
            str(sample_pdf),
            str(output_file)
        ])

        assert result.exit_code == 0
        assert output_file.exists()
        assert "Compression complete:" in result.output

    def test_compress_with_level(self, sample_pdf, temp_dir):
        """Test compress command with specific level."""
        output_file = temp_dir / "compressed_aggressive_cli.pdf"

        result = self.runner.invoke(main, [
            'compress',
            str(sample_pdf),
            str(output_file),
            '--compress', 'aggressive'
        ])

        assert result.exit_code == 0
        assert output_file.exists()
        assert "aggressive" in result.output

    def test_compress_info_flag(self):
        """Test compress command info flag."""
        result = self.runner.invoke(main, ['compress', '--info'])

        assert result.exit_code == 0
        assert "Available compression levels:" in result.output
        assert "basic:" in result.output
        assert "medium:" in result.output
        assert "aggressive:" in result.output

    def test_compress_nonexistent_file(self, temp_dir):
        """Test compress command with nonexistent file."""
        nonexistent = temp_dir / "nonexistent.pdf"
        output_file = temp_dir / "compressed_fail.pdf"

        result = self.runner.invoke(main, [
            'compress',
            str(nonexistent),
            str(output_file)
        ])

        assert result.exit_code == 2  # Click path validation error

    def test_invalid_compression_level_merge(self, sample_pdf, sample_pdf_2, temp_dir):
        """Test merge with invalid compression level."""
        output_file = temp_dir / "merged.pdf"

        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            str(sample_pdf_2),
            '--output', str(output_file),
            '--compress', 'invalid'
        ])

        assert result.exit_code == 2  # Click choice validation error

    def test_invalid_compression_level_walk(self, pdf_directory, output_dir):
        """Test walk with invalid compression level."""
        result = self.runner.invoke(main, [
            'walk',
            str(pdf_directory),
            '--compress', 'invalid',
            '--output-dir', str(output_dir)
        ])

        assert result.exit_code == 2  # Click choice validation error

    def test_invalid_compression_level_compress(self, sample_pdf, temp_dir):
        """Test compress with invalid compression level."""
        output_file = temp_dir / "compressed.pdf"

        result = self.runner.invoke(main, [
            'compress',
            str(sample_pdf),
            str(output_file),
            '--compress', 'invalid'
        ])

        assert result.exit_code == 2  # Click choice validation error

    def test_walk_compression_without_output_dir(self, pdf_directory):
        """Test walk with compression but no output directory."""
        result = self.runner.invoke(main, [
            'walk',
            str(pdf_directory),
            '--compress', 'medium'
        ])

        assert result.exit_code == 0
        assert "Error:" in result.output
        assert "Output directory is required" in result.output

    def test_merge_no_output_specified(self, sample_pdf, sample_pdf_2):
        """Test merge command without output file."""
        result = self.runner.invoke(main, [
            'merge',
            str(sample_pdf),
            str(sample_pdf_2)
        ])

        assert result.exit_code == 2  # Missing required option

    def test_compress_info_with_input_files(self, sample_pdf, temp_dir):
        """Test compress info flag with input files (should ignore files and show info)."""
        output_file = temp_dir / "output.pdf"

        result = self.runner.invoke(main, [
            'compress',
            str(sample_pdf),
            str(output_file),
            '--info'
        ])

        assert result.exit_code == 0
        assert "Available compression levels:" in result.output
        # Should not create output file when showing info
        assert not output_file.exists()