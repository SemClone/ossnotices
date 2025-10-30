"""Simplified CLI interface for generating legal notices."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import __version__
from .core import NoticeGenerator

console = Console()


@click.command()
@click.version_option(version=__version__, prog_name='ossnotices')
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (default: NOTICE.txt)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['text', 'html', 'json']),
    default='text',
    help='Output format (default: text)'
)
@click.option(
    '--recursive', '-r',
    is_flag=True,
    help='Scan directories recursively'
)
@click.option(
    '--cache/--no-cache',
    default=True,
    help='Enable/disable caching (default: enabled)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Suppress all output except errors'
)
def main(
    path: str,
    output: Optional[str],
    format: str,
    recursive: bool,
    cache: bool,
    verbose: bool,
    quiet: bool
) -> None:
    """
    Generate legal notices for open source packages in local source code.

    PATH is the directory or archive file to scan (default: current directory).
    Supported archives: JAR, WAR, WHL, ZIP, TAR, etc.

    Examples:

    \b
    # Scan current directory
    ossnotices

    \b
    # Scan specific directory
    ossnotices ./src

    \b
    # Scan with recursive option and save to file
    ossnotices ./project --recursive -o NOTICE.txt

    \b
    # Generate HTML format
    ossnotices ./project -f html -o notices.html

    \b
    # Process a JAR file
    ossnotices library.jar -o NOTICE.txt
    """

    if quiet and verbose:
        console.print("[red]Error: Cannot use --quiet and --verbose together[/red]")
        sys.exit(1)

    # Set default output path if not specified
    if not output:
        output = f"NOTICE.{format if format != 'json' else 'json'}"

    try:
        generator = NoticeGenerator(
            verbose=verbose,
            quiet=quiet,
            use_cache=cache
        )

        path_obj = Path(path)

        # Process based on path type
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            disable=quiet
        ) as progress:

            if path_obj.is_dir():
                task = progress.add_task(f"Scanning directory: {path}...", total=None)
                notices = generator.scan_directory(
                    path,
                    recursive=recursive,
                    output_format=format
                )
            elif path_obj.is_file():
                # Check if it's an archive
                archive_extensions = {'.jar', '.war', '.whl', '.zip', '.tar', '.gz', '.bz2', '.egg'}
                if path_obj.suffix.lower() in archive_extensions:
                    task = progress.add_task(f"Processing archive: {path}...", total=None)
                    notices = generator.process_archive(
                        path,
                        output_format=format
                    )
                else:
                    console.print(f"[red]Error: {path} is not a supported archive format[/red]")
                    console.print("Supported archives: JAR, WAR, WHL, ZIP, TAR, GZ, BZ2, EGG")
                    sys.exit(1)
            else:
                console.print(f"[red]Error: {path} is neither a directory nor a file[/red]")
                sys.exit(1)

        # Write output
        output_path = Path(output)
        output_path.write_text(notices)

        if not quiet:
            console.print(f"[green]✓[/green] Legal notices generated successfully: {output}")

    except FileNotFoundError as e:
        console.print(f"[red]Error: File not found - {e}[/red]")
        sys.exit(1)
    except PermissionError as e:
        console.print(f"[red]Error: Permission denied - {e}[/red]")
        sys.exit(1)
    except Exception as e:
        if verbose:
            console.print_exception()
        else:
            console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()