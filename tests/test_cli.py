"""End-to-end tests for CLI interface."""

import pytest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
import tempfile
import os

from ossnotices.cli import main


class TestCLI:
    """Tests for CLI interface."""

    def setup_method(self):
        """Setup test environment."""
        self.runner = CliRunner()

    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert 'ossnotices, version' in result.output

    def test_help(self):
        """Test help command."""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Generate legal notices' in result.output
        assert 'Options:' in result.output

    @patch('ossnotices.cli.NoticeGenerator')
    def test_scan_current_directory(self, mock_generator):
        """Test scanning current directory (default)."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, [])
            assert result.exit_code == 0
            mock_instance.scan_directory.assert_called_once_with(
                '.',
                recursive=False,
                output_format='text'
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_scan_specific_directory(self, mock_generator):
        """Test scanning specific directory."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            os.mkdir('test_dir')
            result = self.runner.invoke(main, ['test_dir'])
            assert result.exit_code == 0
            mock_instance.scan_directory.assert_called_once_with(
                'test_dir',
                recursive=False,
                output_format='text'
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_scan_recursive(self, mock_generator):
        """Test recursive scanning."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ['--recursive'])
            assert result.exit_code == 0
            mock_instance.scan_directory.assert_called_once_with(
                '.',
                recursive=True,
                output_format='text'
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_output_formats(self, mock_generator):
        """Test different output formats."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "<html>Test</html>"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            # Test HTML format
            result = self.runner.invoke(main, ['-f', 'html'])
            assert result.exit_code == 0
            mock_instance.scan_directory.assert_called_with(
                '.',
                recursive=False,
                output_format='html'
            )

            # Test JSON format
            mock_instance.scan_directory.return_value = '{"packages": []}'
            result = self.runner.invoke(main, ['-f', 'json'])
            assert result.exit_code == 0
            mock_instance.scan_directory.assert_called_with(
                '.',
                recursive=False,
                output_format='json'
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_custom_output_file(self, mock_generator):
        """Test custom output file."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ['-o', 'custom.txt'])
            assert result.exit_code == 0
            assert Path('custom.txt').exists()
            assert Path('custom.txt').read_text() == "Test notices"

    @patch('ossnotices.cli.NoticeGenerator')
    def test_process_archive(self, mock_generator):
        """Test processing archive files."""
        mock_instance = MagicMock()
        mock_instance.process_archive.return_value = "Archive notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            # Create a dummy JAR file
            Path('test.jar').touch()
            result = self.runner.invoke(main, ['test.jar'])
            assert result.exit_code == 0
            mock_instance.process_archive.assert_called_once_with(
                'test.jar',
                output_format='text'
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_unsupported_file(self, mock_generator):
        """Test error for unsupported file types."""
        with self.runner.isolated_filesystem():
            Path('test.txt').touch()
            result = self.runner.invoke(main, ['test.txt'])
            assert result.exit_code == 1
            assert 'not a supported archive format' in result.output

    def test_quiet_verbose_conflict(self):
        """Test error when both quiet and verbose are specified."""
        result = self.runner.invoke(main, ['-q', '-v'])
        assert result.exit_code == 1
        assert 'Cannot use --quiet and --verbose together' in result.output

    @patch('ossnotices.cli.NoticeGenerator')
    def test_quiet_mode(self, mock_generator):
        """Test quiet mode."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ['-q'])
            assert result.exit_code == 0
            assert 'Legal notices generated' not in result.output
            mock_generator.assert_called_with(
                verbose=False,
                quiet=True,
                use_cache=True
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_verbose_mode(self, mock_generator):
        """Test verbose mode."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ['-v'])
            assert result.exit_code == 0
            mock_generator.assert_called_with(
                verbose=True,
                quiet=False,
                use_cache=True
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_no_cache(self, mock_generator):
        """Test with caching disabled."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.return_value = "Test notices"
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ['--no-cache'])
            assert result.exit_code == 0
            mock_generator.assert_called_with(
                verbose=False,
                quiet=False,
                use_cache=False
            )

    @patch('ossnotices.cli.NoticeGenerator')
    def test_nonexistent_path(self, mock_generator):
        """Test error for nonexistent path."""
        result = self.runner.invoke(main, ['nonexistent_path'])
        assert result.exit_code == 2
        assert 'does not exist' in result.output or 'Invalid value' in result.output

    @patch('ossnotices.cli.NoticeGenerator')
    def test_permission_error(self, mock_generator):
        """Test handling permission errors."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.side_effect = PermissionError("Access denied")
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, [])
            assert result.exit_code == 1
            assert 'Permission denied' in result.output

    @patch('ossnotices.cli.NoticeGenerator')
    def test_general_exception(self, mock_generator):
        """Test handling general exceptions."""
        mock_instance = MagicMock()
        mock_instance.scan_directory.side_effect = Exception("Unexpected error")
        mock_generator.return_value = mock_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, [])
            assert result.exit_code == 1
            assert 'Error: Unexpected error' in result.output