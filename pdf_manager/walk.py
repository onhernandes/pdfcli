"""PDF walking functionality for batch processing files into volumes."""

import os
import re
from pathlib import Path
from .merge import merge_pdfs


def natural_sort_key(text):
    """
    Convert a string into a list of mixed numbers and strings for natural sorting.

    This ensures that filenames with numbers are sorted numerically rather than
    alphabetically. Supports both integers and floats.

    Examples:
        "Chap 2" -> ['chap ', 2.0]
        "Chap 10" -> ['chap ', 10.0]
        "Chap 9.5" -> ['chap ', 9.5]
        Results in order: Chap 2, Chap 9, Chap 9.5, Chap 10
    """
    def atof(part):
        """Convert string to float if it's a number, otherwise return lowercase string."""
        try:
            return float(part)
        except ValueError:
            return part.lower()

    # Split on numbers (including decimals like 9.5)
    # Pattern matches: optional digits, optional decimal point, digits
    parts = re.split(r'(\d+\.?\d*)', text)

    # Filter out empty strings and convert to appropriate types
    return [atof(part) for part in parts if part]


def walk_pdfs(
    input_dir,
    output_dir,
    order="asc",
    batch_size=10,
    prefix="",
    suffix="",
    compression_level=None,
    interactive=False,
):
    """Walk through PDF files in a directory and create batched volumes.

    Args:
        input_dir: Input directory path to search for PDFs
        output_dir: Output directory for generated volumes
        order: File ordering ('asc' or 'desc', default: 'asc')
        batch_size: Number of files per batch/volume (default: 10)
        prefix: Prefix for volume filenames (default: '')
        suffix: Suffix for volume filenames (default: '')
        compression_level: Optional compression level ('basic', 'medium', 'aggressive')
        interactive: Enable interactive mode for volume editing (default: False)
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    if not input_path.is_dir():
        raise ValueError(f"Path is not a directory: {input_dir}")

    # Validate parameters
    if order not in ["asc", "desc"]:
        raise ValueError("Order must be 'asc' or 'desc'")

    if batch_size < 1:
        raise ValueError("Batch size must be at least 1")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Get PDF files and sort them
    pdf_files = [
        f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    # Sort files based on order using natural sorting
    pdf_files = sorted(pdf_files, key=lambda f: natural_sort_key(f.name), reverse=order == "desc")

    total_files = len(pdf_files)
    total_batches = (total_files + batch_size - 1) // batch_size  # Ceiling division

    print(f"Processing {total_files} PDF files from {input_dir}")
    print(f"Order: {order.upper()}, Batch size: {batch_size}")
    print(f"Will create {total_batches} volume(s)")
    print("-" * 60)

    volumes_created = []

    # Process files in batches
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_files)
        batch_files = pdf_files[start_idx:end_idx]

        # Generate volume filename
        volume_num = batch_num + 1
        volume_filename = f"{prefix}volume_{volume_num:03d}{suffix}.pdf"
        volume_path = output_path / volume_filename

        print(f"Creating Volume {volume_num:3d}: {volume_filename}")
        print(f"  Files {start_idx + 1:3d}-{end_idx:3d} ({len(batch_files)} files)")

        # List files in this batch
        for i, pdf_file in enumerate(batch_files, start=start_idx + 1):
            file_size = pdf_file.stat().st_size
            print(f"    {i:3d}. {pdf_file.name} ({file_size:,} bytes)")

        # Interactive mode: allow editing volume before merging
        if interactive:
            print()
            while True:
                choice = input("  Action: [p]roceed, [e]dit (exclude files), [s]kip volume, or [q]uit? ").lower().strip()

                if choice == 'p':
                    break
                elif choice == 'e':
                    print("\n  Enter file numbers to EXCLUDE (comma-separated, e.g., 1,3,5):")
                    print("  Or press Enter to cancel editing")
                    exclude_input = input("  Files to exclude: ").strip()

                    if exclude_input:
                        try:
                            # Parse excluded file numbers
                            exclude_nums = [int(x.strip()) for x in exclude_input.split(',')]
                            exclude_indices = [n - 1 - start_idx for n in exclude_nums if start_idx < n <= end_idx]

                            if exclude_indices:
                                # Remove excluded files
                                batch_files = [f for idx, f in enumerate(batch_files) if idx not in exclude_indices]
                                print(f"\n  Updated volume will contain {len(batch_files)} files:")
                                for i, pdf_file in enumerate(batch_files, start=1):
                                    file_size = pdf_file.stat().st_size
                                    print(f"    {i}. {pdf_file.name} ({file_size:,} bytes)")
                            else:
                                print("  No valid files to exclude.")
                        except ValueError:
                            print("  Invalid input. Please enter comma-separated numbers.")
                    print()
                elif choice == 's':
                    print("  Skipping this volume.\n")
                    batch_files = []
                    break
                elif choice == 'q':
                    print("\n  Quitting volume creation.")
                    print("-" * 60)
                    print(f"Summary:")
                    print(f"  Volumes created so far: {len(volumes_created)}")
                    return volumes_created
                else:
                    print("  Invalid choice. Please enter 'p', 'e', 's', or 'q'.")

        # Skip if no files in batch (user skipped or excluded all)
        if not batch_files:
            print()
            continue

        try:
            # Merge files in this batch
            batch_file_paths = [str(f) for f in batch_files]
            merge_pdfs(batch_file_paths, str(volume_path), compression_level)

            volumes_created.append(volume_path)

            # Show volume info
            volume_size = volume_path.stat().st_size
            print(f"  ✓ Volume created: {volume_size:,} bytes")

        except Exception as e:
            print(f"  ✗ Error creating volume: {e}")

        print()

    print("-" * 60)
    print(f"Summary:")
    print(f"  Total files processed: {total_files}")
    print(f"  Volumes created: {len(volumes_created)}")
    print(f"  Output directory: {output_dir}")

    if compression_level:
        print(f"  Compression level: {compression_level}")

    if volumes_created:
        print(f"  Volume files:")
        for volume in volumes_created:
            volume_size = volume.stat().st_size
            print(f"    {volume.name} ({volume_size:,} bytes)")

    return volumes_created
