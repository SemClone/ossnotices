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
@click.argument('input_path', type=click.Path(exists=True))
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (default: NOTICE.txt in current directory)'
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
    input_path: str,
    output: Optional[str],
    format: str,
    recursive: bool,
    cache: bool,
    verbose: bool,
    quiet: bool
) -> None:
    """
    Generate legal notices for open source packages.

    INPUT_PATH can be:
    - A directory containing source code
    - A package archive (JAR, WAR, WHL, etc.)
    - A file containing PURLs (one per line)
    - A single PURL string

    Examples:

    \b
    # Scan current directory
    ossnotices .

    \b
    # Scan with recursive option and save to file
    ossnotices ./src --recursive -o NOTICE.txt

    \b
    # Generate HTML format
    ossnotices ./project -f html -o notices.html

    \b
    # Process a JAR file
    ossnotices library.jar
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

        input_path_obj = Path(input_path)

        # Determine input type and process accordingly
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            disable=quiet
        ) as progress:

            if input_path_obj.is_dir():
                task = progress.add_task("Scanning directory...", total=None)
                notices = generator.scan_directory(
                    input_path,
                    recursive=recursive,
                    output_format=format
                )
            elif input_path_obj.suffix in ['.jar', '.war', '.whl', '.zip', '.tar', '.gz']:
                task = progress.add_task("Processing archive...", total=None)
                notices = generator.process_archive(
                    input_path,
                    output_format=format
                )
            elif input_path_obj.suffix in ['.txt', '.list']:
                task = progress.add_task("Processing PURL list...", total=None)
                notices = generator.process_purl_list(
                    input_path,
                    output_format=format
                )
            else:
                # Try to process as single PURL
                task = progress.add_task("Processing input...", total=None)
                with open(input_path, 'r') as f:
                    content = f.read().strip()
                    if content.startswith('pkg:'):
                        notices = generator.process_single_purl(
                            content,
                            output_format=format
                        )
                    else:
                        notices = generator.process_purl_list(
                            input_path,
                            output_format=format
                        )

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