"""CLI interface for pdf-manager."""

import click
from .merge import merge_pdfs
from .walk import walk_pdfs
from .compress import compress_pdf, get_compression_info


@click.group()
@click.version_option(version="0.1.0")
def main():
    """PDF Manager - A CLI tool for managing PDF files."""
    pass


@main.command()
@click.argument('input_files', nargs=-1, required=True)
@click.option('-o', '--output', required=True, help='Output PDF file path')
@click.option('-c', '--compress', type=click.Choice(['basic', 'medium', 'aggressive']),
              help='Compression level (basic: high quality/less compression, medium: good quality/more compression, aggressive: may lose quality/maximum compression)')
def merge(input_files, output, compress):
    """Merge multiple PDF files into a single PDF.

    INPUT_FILES: Two or more PDF files to merge
    """
    if len(input_files) < 2:
        click.echo("Error: At least two input files are required for merging.")
        return

    try:
        merge_pdfs(input_files, output, compress)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@main.command()
@click.argument('input_dir', type=click.Path(exists=True), required=False)
@click.argument('output_dir', type=click.Path(), required=False)
@click.option('--order', type=click.Choice(['asc', 'desc']), default='asc',
              help='File ordering: asc (ascending) or desc (descending) - default: asc')
@click.option('--batch-size', type=int, default=10,
              help='Number of files per volume/batch - default: 10')
@click.option('--prefix', default='',
              help='Prefix for volume filenames - default: empty')
@click.option('--suffix', default='',
              help='Suffix for volume filenames - default: empty')
@click.option('-c', '--compress', type=click.Choice(['basic', 'medium', 'aggressive']),
              help='Compression level (basic: high quality/less compression, medium: good quality/more compression, aggressive: may lose quality/maximum compression)')
@click.option('-i', '--interactive', is_flag=True,
              help='Interactive mode: prompt for arguments and allow editing each volume before merging')
def walk(input_dir, output_dir, order, batch_size, prefix, suffix, compress, interactive):
    """Walk through PDF files and create batched volumes.

    INPUT_DIR: Directory containing PDF files to process
    OUTPUT_DIR: Directory where volume files will be created

    This command processes PDF files in batches, creating volume files that merge
    multiple PDFs together. Files are sorted by name in the specified order.
    """
    # Interactive mode: prompt for missing arguments
    if interactive:
        click.echo("=== Interactive Mode ===\n")

        if not input_dir:
            input_dir = click.prompt("Input directory", type=click.Path(exists=True))
        else:
            if not click.confirm(f"Use input directory: {input_dir}?", default=True):
                input_dir = click.prompt("Input directory", type=click.Path(exists=True))

        if not output_dir:
            output_dir = click.prompt("Output directory", type=click.Path())
        else:
            if not click.confirm(f"Use output directory: {output_dir}?", default=True):
                output_dir = click.prompt("Output directory", type=click.Path())

        order = click.prompt("File ordering", type=click.Choice(['asc', 'desc']), default=order)
        batch_size = click.prompt("Batch size (files per volume)", type=int, default=batch_size)
        prefix = click.prompt("Volume filename prefix", default=prefix)
        suffix = click.prompt("Volume filename suffix", default=suffix)

        if click.confirm("Enable compression?", default=False):
            compress = click.prompt("Compression level",
                                   type=click.Choice(['basic', 'medium', 'aggressive']),
                                   default='medium')

        click.echo()
    else:
        # Non-interactive mode requires input_dir and output_dir
        if not input_dir or not output_dir:
            click.echo("Error: INPUT_DIR and OUTPUT_DIR are required in non-interactive mode.", err=True)
            return

    try:
        walk_pdfs(input_dir, output_dir, order, batch_size, prefix, suffix, compress, interactive)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file')
@click.option('-c', '--compress', type=click.Choice(['basic', 'medium', 'aggressive']), default='medium',
              help='Compression level (default: medium)')
@click.option('--info', is_flag=True, help='Show compression level information')
def compress(input_file, output_file, compress, info):
    """Compress a PDF file with specified compression level.

    INPUT_FILE: PDF file to compress
    OUTPUT_FILE: Compressed PDF output file path
    """
    if info:
        click.echo(get_compression_info())
        return

    try:
        compress_pdf(input_file, output_file, compress)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    main()