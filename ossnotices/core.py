"""Core functionality for ossnotices - wrapper around purl2notices."""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional

from purl2notices import Purl2Notices
from purl2notices.cache import CacheManager
from purl2notices.config import Config
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

        # Setup logging
        if quiet:
            logging.basicConfig(level=logging.ERROR)
        elif verbose:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            logging.basicConfig(level=logging.WARNING)

        # Suppress verbose warnings from underlying libraries unless in debug mode
        if not verbose:
            logging.getLogger('osslili').setLevel(logging.ERROR)
            logging.getLogger('upmex').setLevel(logging.ERROR)
            logging.getLogger('purl2notices').setLevel(logging.WARNING)

        # Initialize configuration
        self.config = Config()

        # Setup cache manager if caching is enabled
        if use_cache:
            cache_path = cache_file or ".ossnotices.cache.json"
            self.cache_manager = CacheManager(Path(cache_path))
        else:
            self.cache_manager = None

        # Initialize purl2notices processor
        self.processor = Purl2Notices(config=self.config)

        # Set cache manager if available
        if self.cache_manager:
            self.processor.cache_manager = self.cache_manager

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

        # Run the async scan
        packages = asyncio.run(
            self.processor.scan_directory(
                Path(directory),
                recursive=recursive
            )
        )

        if not self.quiet:
            console.print(f"Found {len(packages)} packages")

        return self._generate_output(packages, output_format)

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

        # Run the async processing
        packages = asyncio.run(
            self.processor.process_archive(Path(archive_path))
        )

        if not self.quiet:
            console.print(f"Found {len(packages)} packages")

        return self._generate_output(packages, output_format)

    def process_purl_list(
        self,
        file_path: str,
        output_format: str = 'text'
    ) -> str:
        """
        Process a file containing PURLs and generate notices.

        Args:
            file_path: Path to file containing PURLs (one per line)
            output_format: Output format (text, html, json)

        Returns:
            Generated notices as string
        """
        if not self.quiet:
            console.print(f"Processing PURL list: {file_path}")

        # Read PURLs from file
        with open(file_path, 'r') as f:
            purls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        if not self.quiet:
            console.print(f"Processing {len(purls)} PURLs")

        # Process PURLs
        packages = asyncio.run(
            self.processor.process_purls(purls)
        )

        return self._generate_output(packages, output_format)

    def process_single_purl(
        self,
        purl: str,
        output_format: str = 'text'
    ) -> str:
        """
        Process a single PURL and generate notices.

        Args:
            purl: Package URL string
            output_format: Output format (text, html, json)

        Returns:
            Generated notices as string
        """
        if not self.quiet:
            console.print(f"Processing PURL: {purl}")

        # Process single PURL
        package = asyncio.run(
            self.processor.process_single_purl(purl)
        )

        packages = [package] if package else []
        return self._generate_output(packages, output_format)

    def _generate_output(self, packages: List, output_format: str) -> str:
        """
        Generate output in the specified format.

        Args:
            packages: List of processed packages
            output_format: Output format (text, html, json)

        Returns:
            Formatted output string
        """
        if not packages:
            if not self.quiet:
                console.print("[yellow]Warning: No packages found[/yellow]")
            return "No packages found to generate notices for.\n"

        # Filter out packages without meaningful license info
        valid_packages = [
            p for p in packages
            if p and hasattr(p, 'licenses') and p.licenses
        ]

        if not valid_packages:
            if not self.quiet:
                console.print("[yellow]Warning: No packages with license information found[/yellow]")
            return "No packages with license information found.\n"

        if output_format == 'json':
            # Return as JSON
            import json
            return json.dumps(
                [self._package_to_dict(p) for p in valid_packages],
                indent=2
            )
        else:
            # Generate notices using purl2notices
            notices = self.processor.generate_notices(
                valid_packages,
                format=output_format
            )
            return notices

    def _package_to_dict(self, package) -> dict:
        """Convert package object to dictionary for JSON output."""
        return {
            'name': getattr(package, 'name', 'Unknown'),
            'version': getattr(package, 'version', 'Unknown'),
            'licenses': getattr(package, 'licenses', []),
            'copyrights': getattr(package, 'copyrights', []),
            'authors': getattr(package, 'authors', []),
            'purl': getattr(package, 'purl', ''),
            'homepage': getattr(package, 'homepage_url', ''),
            'repository': getattr(package, 'repository_url', '')
        }