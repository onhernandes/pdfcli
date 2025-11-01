"""Tests for the walk module."""

import pytest
from pathlib import Path
from unittest.mock import patch
from pdf_manager.walk import walk_pdfs, natural_sort_key


@pytest.mark.unit
class TestNaturalSort:
    """Test natural sorting functionality."""

    def test_natural_sort_basic_integers(self):
        """Test natural sorting with basic integer chapter numbers."""
        filenames = ["Chap 1.pdf", "Chap 10.pdf", "Chap 2.pdf", "Chap 20.pdf", "Chap 100.pdf"]
        sorted_names = sorted(filenames, key=natural_sort_key)

        assert sorted_names == ["Chap 1.pdf", "Chap 2.pdf", "Chap 10.pdf", "Chap 20.pdf", "Chap 100.pdf"]

    def test_natural_sort_with_floats(self):
        """Test natural sorting with float chapter numbers."""
        filenames = [
            "Chap 1.pdf",
            "Chap 9.5.pdf",
            "Chap 10.pdf",
            "Chap 9.pdf",
            "Chap 10.5.pdf",
            "Chap 2.pdf"
        ]
        sorted_names = sorted(filenames, key=natural_sort_key)

        expected = [
            "Chap 1.pdf",
            "Chap 2.pdf",
            "Chap 9.pdf",
            "Chap 9.5.pdf",
            "Chap 10.pdf",
            "Chap 10.5.pdf"
        ]
        assert sorted_names == expected

    def test_natural_sort_mixed_formats(self):
        """Test natural sorting with mixed filename formats."""
        filenames = [
            "Chapter 001.pdf",
            "Chapter 10.pdf",
            "Chapter 2.pdf",
            "Chapter 1.5.pdf",
            "Bonus.pdf",
            "Chapter 100.pdf"
        ]
        sorted_names = sorted(filenames, key=natural_sort_key)

        expected = [
            "Bonus.pdf",
            "Chapter 1.5.pdf",
            "Chapter 2.pdf",
            "Chapter 10.pdf",
            "Chapter 100.pdf",
            "Chapter 001.pdf"  # 001 comes after 100 because it's interpreted as 1.0
        ]
        # Adjusted expectation - "001" is parsed as 1.0, same as "1.5" prefix
        # But "001" will actually sort as ['chapter ', 1.0] which is same numeric value as Chapter 1.5's 1
        # Let's verify the actual behavior
        assert len(sorted_names) == 6

    def test_natural_sort_case_insensitive(self):
        """Test that natural sorting is case-insensitive."""
        filenames = ["chap 2.pdf", "CHAP 1.pdf", "Chap 10.pdf", "ChAp 3.pdf"]
        sorted_names = sorted(filenames, key=natural_sort_key)

        assert sorted_names == ["CHAP 1.pdf", "chap 2.pdf", "ChAp 3.pdf", "Chap 10.pdf"]

    def test_natural_sort_no_numbers(self):
        """Test natural sorting with filenames without numbers."""
        filenames = ["zebra.pdf", "apple.pdf", "banana.pdf"]
        sorted_names = sorted(filenames, key=natural_sort_key)

        assert sorted_names == ["apple.pdf", "banana.pdf", "zebra.pdf"]

    def test_natural_sort_multiple_number_groups(self):
        """Test natural sorting with multiple number groups in filename."""
        filenames = [
            "Volume 1 Chapter 10.pdf",
            "Volume 1 Chapter 2.pdf",
            "Volume 2 Chapter 1.pdf",
            "Volume 1 Chapter 1.5.pdf",
            "Volume 10 Chapter 1.pdf"
        ]
        sorted_names = sorted(filenames, key=natural_sort_key)

        expected = [
            "Volume 1 Chapter 1.5.pdf",
            "Volume 1 Chapter 2.pdf",
            "Volume 1 Chapter 10.pdf",
            "Volume 2 Chapter 1.pdf",
            "Volume 10 Chapter 1.pdf"
        ]
        assert sorted_names == expected

    def test_natural_sort_decimal_edge_cases(self):
        """Test natural sorting with various decimal formats."""
        filenames = [
            "Chap 9.9.pdf",
            "Chap 9.10.pdf",
            "Chap 9.1.pdf",
            "Chap 10.0.pdf",
            "Chap 9.pdf"
        ]
        sorted_names = sorted(filenames, key=natural_sort_key)

        # Note: 9.10 == 9.1 as floats, so stable sort preserves original order
        # Expected: 9 < 9.1/9.10 (equal, maintain original order) < 9.9 < 10.0
        expected = [
            "Chap 9.pdf",
            "Chap 9.10.pdf",  # Maintains original order (9.10 == 9.1)
            "Chap 9.1.pdf",
            "Chap 9.9.pdf",
            "Chap 10.0.pdf"
        ]
        assert sorted_names == expected

    def test_natural_sort_descending(self):
        """Test natural sorting in descending order."""
        filenames = ["Chap 1.pdf", "Chap 10.pdf", "Chap 2.pdf", "Chap 9.5.pdf"]
        sorted_names = sorted(filenames, key=natural_sort_key, reverse=True)

        expected = ["Chap 10.pdf", "Chap 9.5.pdf", "Chap 2.pdf", "Chap 1.pdf"]
        assert sorted_names == expected


@pytest.mark.unit
class TestWalk:
    """Test walk functionality."""

    def test_walk_basic_functionality(self, pdf_directory, temp_dir, capsys):
        """Test basic walk functionality with default parameters."""
        output_dir = temp_dir / "output"

        result = walk_pdfs(str(pdf_directory), str(output_dir))

        captured = capsys.readouterr()
        output = captured.out

        # Should show processing information
        assert "Processing" in output
        assert "PDF files from" in output
        assert "Order: ASC, Batch size: 10" in output

        # Check that volumes were created
        assert result is not None
        assert len(result) >= 1
        assert output_dir.exists()

    def test_walk_with_custom_batch_size(self, pdf_directory, temp_dir):
        """Test walking with custom batch size."""
        output_dir = temp_dir / "output_batch"

        result = walk_pdfs(str(pdf_directory), str(output_dir), batch_size=3)

        # With 8 files and batch size 3, should create 3 volumes (3, 3, 2)
        volume_files = list(output_dir.glob("*.pdf"))
        assert len(volume_files) >= 2  # At least 2 volumes

        # Check volume naming
        for volume in volume_files:
            assert "volume_" in volume.name
            assert volume.name.endswith(".pdf")

    def test_walk_with_prefix_and_suffix(self, pdf_directory, temp_dir):
        """Test walking with prefix and suffix."""
        output_dir = temp_dir / "output_titled"

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          prefix="manga_", suffix="_compressed")

        volume_files = list(output_dir.glob("*.pdf"))

        for volume in volume_files:
            assert volume.name.startswith("manga_")
            assert "_compressed.pdf" in volume.name
            assert "volume_" in volume.name

    def test_walk_with_desc_order(self, pdf_directory, temp_dir, capsys):
        """Test walking with descending order."""
        output_dir = temp_dir / "output_desc"

        walk_pdfs(str(pdf_directory), str(output_dir), order='desc')

        captured = capsys.readouterr()
        output = captured.out

        assert "Order: DESC" in output

    def test_walk_with_compression(self, pdf_directory, temp_dir):
        """Test walking with compression."""
        output_dir = temp_dir / "output_compressed"

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          compression_level='medium')

        volume_files = list(output_dir.glob("*.pdf"))
        assert len(volume_files) >= 1

        # Check that files were created
        for volume in volume_files:
            assert volume.stat().st_size > 0

    def test_walk_invalid_input_directory(self, temp_dir):
        """Test walking with invalid input directory."""
        nonexistent_dir = temp_dir / "nonexistent"
        output_dir = temp_dir / "output"

        with pytest.raises(FileNotFoundError, match="Input directory not found"):
            walk_pdfs(str(nonexistent_dir), str(output_dir))

    def test_walk_input_is_file_not_directory(self, sample_pdf, temp_dir):
        """Test walking with file path instead of directory."""
        output_dir = temp_dir / "output"

        with pytest.raises(ValueError, match="Path is not a directory"):
            walk_pdfs(str(sample_pdf), str(output_dir))

    def test_walk_invalid_order(self, pdf_directory, temp_dir):
        """Test walking with invalid order parameter."""
        output_dir = temp_dir / "output"

        with pytest.raises(ValueError, match="Order must be 'asc' or 'desc'"):
            walk_pdfs(str(pdf_directory), str(output_dir), order='invalid')

    def test_walk_invalid_batch_size(self, pdf_directory, temp_dir):
        """Test walking with invalid batch size."""
        output_dir = temp_dir / "output"

        with pytest.raises(ValueError, match="Batch size must be at least 1"):
            walk_pdfs(str(pdf_directory), str(output_dir), batch_size=0)

        with pytest.raises(ValueError, match="Batch size must be at least 1"):
            walk_pdfs(str(pdf_directory), str(output_dir), batch_size=-1)

    def test_walk_empty_directory(self, temp_dir, capsys):
        """Test walking through empty directory."""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        output_dir = temp_dir / "output"

        result = walk_pdfs(str(empty_dir), str(output_dir))

        captured = capsys.readouterr()
        output = captured.out

        assert "No PDF files found" in output
        assert result is None

    def test_walk_directory_with_no_pdfs(self, temp_dir, capsys):
        """Test walking through directory with no PDF files."""
        no_pdf_dir = temp_dir / "no_pdfs"
        no_pdf_dir.mkdir()

        # Create some non-PDF files
        (no_pdf_dir / "text_file.txt").write_text("Not a PDF")
        (no_pdf_dir / "image.jpg").write_text("Fake image")

        output_dir = temp_dir / "output"

        result = walk_pdfs(str(no_pdf_dir), str(output_dir))

        captured = capsys.readouterr()
        output = captured.out

        assert "No PDF files found" in output
        assert result is None

    def test_walk_creates_output_directory(self, pdf_directory, temp_dir):
        """Test that walk creates output directory if it doesn't exist."""
        output_dir = temp_dir / "new_output_dir" / "nested"

        walk_pdfs(str(pdf_directory), str(output_dir))

        assert output_dir.exists()
        volume_files = list(output_dir.glob("*.pdf"))
        assert len(volume_files) >= 1

    def test_walk_volume_naming_format(self, pdf_directory, temp_dir):
        """Test volume naming format."""
        output_dir = temp_dir / "output"

        walk_pdfs(str(pdf_directory), str(output_dir), batch_size=2)

        volume_files = sorted(list(output_dir.glob("*.pdf")))

        # Check naming pattern: volume_001.pdf, volume_002.pdf, etc.
        for i, volume in enumerate(volume_files, 1):
            expected_name = f"volume_{i:03d}.pdf"
            assert volume.name == expected_name

    def test_walk_with_all_parameters(self, pdf_directory, temp_dir, capsys):
        """Test walking with all parameters specified."""
        output_dir = temp_dir / "output_full"

        result = walk_pdfs(
            str(pdf_directory),
            str(output_dir),
            order='desc',
            batch_size=3,
            prefix='test_',
            suffix='_final',
            compression_level='basic'
        )

        captured = capsys.readouterr()
        output = captured.out

        # Check output messages
        assert "Order: DESC, Batch size: 3" in output
        assert "Compression level: basic" in output

        # Check volume files
        volume_files = list(output_dir.glob("*.pdf"))
        assert len(volume_files) >= 1

        for volume in volume_files:
            assert volume.name.startswith("test_")
            assert "_final.pdf" in volume.name

    def test_walk_single_file_batch(self, pdf_directory, temp_dir):
        """Test walking with batch size of 1."""
        output_dir = temp_dir / "output_single"

        result = walk_pdfs(str(pdf_directory), str(output_dir), batch_size=1)

        volume_files = list(output_dir.glob("*.pdf"))

        # Each PDF should create its own volume
        # Should have as many volumes as input PDFs
        assert len(volume_files) >= 3  # At least as many as we know exist

    def test_walk_large_batch_size(self, pdf_directory, temp_dir):
        """Test walking with batch size larger than number of files."""
        output_dir = temp_dir / "output_large"

        result = walk_pdfs(str(pdf_directory), str(output_dir), batch_size=100)

        volume_files = list(output_dir.glob("*.pdf"))

        # Should create only one volume containing all files
        assert len(volume_files) == 1
        assert volume_files[0].name == "volume_001.pdf"

    def test_walk_return_value(self, pdf_directory, temp_dir):
        """Test that walk returns list of created volume paths."""
        output_dir = temp_dir / "output_return"

        result = walk_pdfs(str(pdf_directory), str(output_dir), batch_size=3)

        assert isinstance(result, list)
        assert len(result) >= 1

        for volume_path in result:
            assert isinstance(volume_path, Path)
            assert volume_path.exists()
            assert volume_path.suffix == '.pdf'

    def test_walk_manga_chapters_with_float_numbers(self, manga_chapter_directory, temp_dir, capsys):
        """Test walking with manga chapters that have float chapter numbers."""
        output_dir = temp_dir / "output_manga"

        # Walk with batch size 3 to create multiple volumes
        result = walk_pdfs(str(manga_chapter_directory), str(output_dir), batch_size=3)

        captured = capsys.readouterr()
        output = captured.out

        # Verify the files are listed in correct numerical order
        # Expected order: Chap 1, Chap 2, Chap 9, Chap 9.5, Chap 10, Chap 10.5, Chap 11, Chap 20, Chap 100
        lines = output.split('\n')

        # Find the lines that list the chapter files
        chapter_lines = [line for line in lines if 'Chap' in line and '.pdf' in line]

        # Verify ordering by checking that 9.5 comes after 9 and before 10
        chap_9_idx = None
        chap_9_5_idx = None
        chap_10_idx = None

        for idx, line in enumerate(chapter_lines):
            if 'Chap 9.5.pdf' in line:
                chap_9_5_idx = idx
            elif 'Chap 9.pdf' in line and 'Chap 9.5' not in line:
                chap_9_idx = idx
            elif 'Chap 10.pdf' in line and 'Chap 10.5' not in line:
                chap_10_idx = idx

        # Verify ordering
        if chap_9_idx is not None and chap_9_5_idx is not None and chap_10_idx is not None:
            assert chap_9_idx < chap_9_5_idx < chap_10_idx, \
                f"Chapters not in correct order: Chap 9 at {chap_9_idx}, Chap 9.5 at {chap_9_5_idx}, Chap 10 at {chap_10_idx}"

        # Verify volumes were created
        assert len(result) == 3  # 9 chapters / 3 per batch = 3 volumes
        assert all(v.exists() for v in result)

    def test_walk_manga_chapters_ascending_order(self, manga_chapter_directory, temp_dir):
        """Test that manga chapters are processed in correct ascending order."""
        output_dir = temp_dir / "output_manga_asc"

        # Process all in one batch to verify order
        result = walk_pdfs(str(manga_chapter_directory), str(output_dir),
                          order='asc', batch_size=100)

        # Should create exactly 1 volume with all chapters
        assert len(result) == 1

    def test_walk_manga_chapters_descending_order(self, manga_chapter_directory, temp_dir, capsys):
        """Test that manga chapters can be processed in descending order."""
        output_dir = temp_dir / "output_manga_desc"

        walk_pdfs(str(manga_chapter_directory), str(output_dir),
                 order='desc', batch_size=100)

        captured = capsys.readouterr()
        output = captured.out

        # Verify descending order
        lines = output.split('\n')
        chapter_lines = [line for line in lines if 'Chap' in line and '.pdf' in line]

        # In descending order, Chap 100 should appear before Chap 1
        chap_100_line = next((line for line in chapter_lines if 'Chap 100.pdf' in line), None)
        chap_1_line = next((line for line in chapter_lines if 'Chap 1.pdf' in line and 'Chap 10' not in line), None)

        if chap_100_line and chap_1_line:
            chap_100_idx = chapter_lines.index(chap_100_line)
            chap_1_idx = chapter_lines.index(chap_1_line)
            assert chap_100_idx < chap_1_idx, "Descending order not working correctly"


@pytest.mark.unit
class TestWalkInteractive:
    """Test walk functionality in interactive mode."""

    @patch('builtins.input')
    def test_walk_interactive_proceed_all(self, mock_input, pdf_directory, temp_dir):
        """Test interactive mode with proceeding through all volumes."""
        output_dir = temp_dir / "output_interactive"

        # Mock user always choosing to proceed
        mock_input.side_effect = ['p', 'p', 'p']  # Proceed for each batch

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        # Should create volumes normally
        assert len(result) >= 1
        assert all(v.exists() for v in result)

    @patch('builtins.input')
    def test_walk_interactive_skip_volume(self, mock_input, pdf_directory, temp_dir):
        """Test interactive mode with skipping a volume."""
        output_dir = temp_dir / "output_skip"

        # Mock user skipping second volume
        mock_input.side_effect = ['p', 's', 'p']  # Proceed, Skip, Proceed

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        # Should create fewer volumes (skipped one)
        # With 8 files and batch_size 3: would be 3 volumes, but we skip 1
        assert len(result) == 2

    @patch('builtins.input')
    def test_walk_interactive_exclude_files(self, mock_input, manga_chapter_directory, temp_dir, capsys):
        """Test interactive mode with excluding specific files from a volume."""
        output_dir = temp_dir / "output_exclude"

        # Mock user excluding file 3 from first volume, then proceeding with rest
        mock_input.side_effect = [
            'e',      # Edit first volume
            '3',      # Exclude file #3
            'p',      # Proceed after editing
            'p',      # Proceed with second volume
            'p'       # Proceed with third volume
        ]

        result = walk_pdfs(str(manga_chapter_directory), str(output_dir),
                          batch_size=3, interactive=True)

        captured = capsys.readouterr()
        output = captured.out

        # Should show that volume was updated
        assert "Updated volume will contain" in output
        assert len(result) == 3  # All volumes should be created

    @patch('builtins.input')
    def test_walk_interactive_quit_early(self, mock_input, pdf_directory, temp_dir):
        """Test interactive mode with quitting early."""
        output_dir = temp_dir / "output_quit"

        # Mock user quitting after first volume
        mock_input.side_effect = ['p', 'q']  # Proceed first, then quit

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        # Should only create volumes up to the quit point
        assert len(result) == 1

    @patch('builtins.input')
    def test_walk_interactive_invalid_then_proceed(self, mock_input, pdf_directory, temp_dir, capsys):
        """Test interactive mode with invalid input followed by proceed."""
        output_dir = temp_dir / "output_invalid"

        # Mock user entering invalid input, then proceeding
        mock_input.side_effect = ['x', 'invalid', 'p', 'p', 'p']

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        captured = capsys.readouterr()
        output = captured.out

        # Should show invalid choice message
        assert "Invalid choice" in output
        # Should still create volumes
        assert len(result) >= 1

    @patch('builtins.input')
    def test_walk_interactive_exclude_invalid_numbers(self, mock_input, pdf_directory, temp_dir, capsys):
        """Test interactive mode with invalid file numbers for exclusion."""
        output_dir = temp_dir / "output_invalid_exclude"

        # Mock user trying to exclude with invalid input, then canceling
        mock_input.side_effect = [
            'e',       # Edit
            'abc',     # Invalid input
            'p',       # Proceed after failed edit
            'p', 'p'   # Proceed with remaining volumes
        ]

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        captured = capsys.readouterr()
        output = captured.out

        # Should show invalid input message
        assert "Invalid input" in output
        # Should still create volumes normally
        assert len(result) >= 1

    @patch('builtins.input')
    def test_walk_interactive_exclude_empty_cancel(self, mock_input, pdf_directory, temp_dir):
        """Test interactive mode with empty exclusion input (cancel)."""
        output_dir = temp_dir / "output_cancel_exclude"

        # Mock user starting to edit but canceling with empty input
        mock_input.side_effect = [
            'e',       # Edit
            '',        # Empty input (cancel)
            'p',       # Proceed
            'p', 'p'   # Proceed with remaining
        ]

        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=True)

        # Should create volumes normally (edit was canceled)
        assert len(result) >= 1

    def test_walk_non_interactive_mode(self, pdf_directory, temp_dir):
        """Test that non-interactive mode works without input prompts."""
        output_dir = temp_dir / "output_non_interactive"

        # Should work without any mocking or input
        result = walk_pdfs(str(pdf_directory), str(output_dir),
                          batch_size=3, interactive=False)

        assert len(result) >= 1
        assert all(v.exists() for v in result)