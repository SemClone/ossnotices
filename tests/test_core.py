"""Unit tests for core functionality."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

from ossnotices.core import NoticeGenerator


class TestNoticeGenerator:
    """Tests for NoticeGenerator class."""

    def test_init_default(self):
        """Test initialization with default parameters."""
        generator = NoticeGenerator()
        assert generator.verbose is False
        assert generator.quiet is False
        assert generator.use_cache is True
        assert generator.cache_file == ".ossnotices.cache.json"

    def test_init_custom(self):
        """Test initialization with custom parameters."""
        generator = NoticeGenerator(
            verbose=True,
            quiet=False,
            use_cache=False,
            cache_file="custom.cache.json"
        )
        assert generator.verbose is True
        assert generator.quiet is False
        assert generator.use_cache is False
        assert generator.cache_file == "custom.cache.json"

    @patch('ossnotices.core.subprocess.run')
    def test_scan_directory_basic(self, mock_run):
        """Test basic directory scanning."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="License notices generated",
            stderr=""
        )

        generator = NoticeGenerator()
        result = generator.scan_directory("./test_dir")

        assert result == "License notices generated"
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert 'purl2notices' in call_args
        assert '-i' in call_args
        assert './test_dir' in call_args
        assert '--mode' in call_args
        assert 'scan' in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_scan_directory_recursive(self, mock_run):
        """Test recursive directory scanning."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="License notices generated",
            stderr=""
        )

        generator = NoticeGenerator()
        result = generator.scan_directory("./test_dir", recursive=True)

        call_args = mock_run.call_args[0][0]
        assert '--recursive' in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_scan_directory_with_format(self, mock_run):
        """Test directory scanning with different output formats."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="<html>License notices</html>",
            stderr=""
        )

        generator = NoticeGenerator()
        result = generator.scan_directory("./test_dir", output_format='html')

        call_args = mock_run.call_args[0][0]
        assert '-f' in call_args
        assert 'html' in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_process_archive(self, mock_run):
        """Test archive processing."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Archive processed",
            stderr=""
        )

        generator = NoticeGenerator()
        result = generator.process_archive("test.jar")

        assert result == "Archive processed"
        call_args = mock_run.call_args[0][0]
        assert 'purl2notices' in call_args
        assert '-i' in call_args
        assert 'test.jar' in call_args
        assert '--mode' in call_args
        assert 'archive' in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_no_cache(self, mock_run):
        """Test with caching disabled."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="No cache",
            stderr=""
        )

        generator = NoticeGenerator(use_cache=False)
        result = generator.scan_directory("./test_dir")

        call_args = mock_run.call_args[0][0]
        assert '--cache' not in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_verbose_mode(self, mock_run):
        """Test verbose mode."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Verbose output",
            stderr=""
        )

        generator = NoticeGenerator(verbose=True)
        result = generator.scan_directory("./test_dir")

        call_args = mock_run.call_args[0][0]
        assert '-v' in call_args

    @patch('ossnotices.core.subprocess.run')
    def test_handle_error_with_output(self, mock_run):
        """Test handling errors when there's still output."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="Partial output",
            stderr="Some warning"
        )

        generator = NoticeGenerator()
        result = generator.scan_directory("./test_dir")

        assert result == "Partial output"

    @patch('ossnotices.core.subprocess.run')
    def test_handle_error_no_output(self, mock_run):
        """Test handling errors with no output."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error occurred"
        )

        generator = NoticeGenerator()
        result = generator.scan_directory("./test_dir")

        assert result == "No packages with license information found.\n"

    @patch('ossnotices.core.subprocess.run')
    def test_purl2notices_not_found(self, mock_run):
        """Test when purl2notices is not installed."""
        mock_run.side_effect = FileNotFoundError()

        generator = NoticeGenerator()
        with pytest.raises(SystemExit):
            generator.scan_directory("./test_dir")