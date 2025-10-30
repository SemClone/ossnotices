"""Core functionality for ossnotices - wrapper around purl2notices."""

import sys
import subprocess
import json
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


class NoticeGenerator:
    """Simplified wrapper for purl2notices functionality."""

    def __init__(
        self,
        verbose: bool = False,
        quiet: bool = False,
        use_cache: bool = True,
        cache_file: Optional[str] = None
    ):
        """
        Initialize the NoticeGenerator.

        Args:
            verbose: Enable verbose logging
            quiet: Suppress all output except errors
            use_cache: Enable caching
            cache_file: Custom cache file location
        """
        self.verbose = verbose
        self.quiet = quiet
        self.use_cache = use_cache
        self.cache_file = cache_file or ".ossnotices.cache.json"

    def scan_directory(
        self,
        directory: str,
        recursive: bool = False,
        output_format: str = 'text'
    ) -> str:
        """
        Scan a directory for packages and generate notices.

        Args:
            directory: Path to directory to scan
            recursive: Whether to scan recursively
            output_format: Output format (text, html, json)

        Returns:
            Generated notices as string
        """
        if not self.quiet:
            console.print(f"Scanning directory: {directory}")

        # Build purl2notices command
        cmd = ['purl2notices', '-i', directory, '--mode', 'scan']

        if recursive:
            cmd.append('--recursive')

        if self.use_cache:
            cmd.extend(['--cache', self.cache_file])

        if self.verbose:
            cmd.append('-v')

        # Add format option
        cmd.extend(['-f', output_format])

        # Run the command
        result = self._run_purl2notices(cmd)

        if not self.quiet and result:
            lines = result.strip().split('\n')
            # Count packages found (look for lines that start with package indicators)
            package_count = sum(1 for line in lines if line.strip() and not line.startswith('#'))
            if package_count > 0:
                console.print(f"Found packages in directory")

        return result

    def process_archive(
        self,
        archive_path: str,
        output_format: str = 'text'
    ) -> str:
        """
        Process an archive file and generate notices.

        Args:
            archive_path: Path to archive file
            output_format: Output format (text, html, json)

        Returns:
            Generated notices as string
        """
        if not self.quiet:
            console.print(f"Processing archive: {archive_path}")

        # Build purl2notices command
        cmd = ['purl2notices', '-i', archive_path, '--mode', 'archive']

        if self.use_cache:
            cmd.extend(['--cache', self.cache_file])

        if self.verbose:
            cmd.append('-v')

        # Add format option
        cmd.extend(['-f', output_format])

        # Run the command
        result = self._run_purl2notices(cmd)

        return result

    def _run_purl2notices(self, cmd: list) -> str:
        """
        Run purl2notices command and capture output.

        Args:
            cmd: Command list to execute

        Returns:
            Output from purl2notices
        """
        try:
            # Run purl2notices and capture output
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            if process.returncode != 0:
                if self.verbose:
                    console.print(f"[yellow]purl2notices stderr: {process.stderr}[/yellow]")

                # Try to extract meaningful output even if there's an error
                if process.stdout:
                    return process.stdout
                else:
                    # Return a default message if no packages found
                    return "No packages with license information found.\n"

            return process.stdout

        except FileNotFoundError:
            console.print("[red]Error: purl2notices is not installed[/red]")
            console.print("Please install it with: pip install purl2notices")
            sys.exit(1)
        except Exception as e:
            if self.verbose:
                console.print(f"[red]Error running purl2notices: {e}[/red]")
            raise