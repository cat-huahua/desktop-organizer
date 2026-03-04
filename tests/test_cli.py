"""Tests for the CLI module."""

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
import pytest

from desktop_organizer.cli import cli


class TestCLI:
    """Test cases for CLI commands."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def temp_desktop(self, tmp_path):
        """Create a temporary desktop with files."""
        desktop = tmp_path / "Desktop"
        desktop.mkdir()

        (desktop / "image1.jpg").touch()
        (desktop / "document.pdf").touch()

        return desktop

    def test_version(self, runner):
        """Test version flag."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "desktop-organizer" in result.output

    def test_help(self, runner):
        """Test help command."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Desktop Organizer" in result.output

    def test_status_command(self, runner, temp_desktop):
        """Test status command."""
        result = runner.invoke(cli, ["status", "--path", str(temp_desktop)])
        assert result.exit_code == 0
        assert "Desktop:" in result.output
        assert "Files: 2" in result.output

    def test_preview_command(self, runner, temp_desktop):
        """Test preview command."""
        result = runner.invoke(cli, ["preview", "--path", str(temp_desktop)])
        assert result.exit_code == 0
        assert "Would organize" in result.output
        assert "Images" in result.output
        assert "Documents" in result.output

    def test_preview_verbose(self, runner, temp_desktop):
        """Test preview command with verbose flag."""
        result = runner.invoke(cli, ["preview", "--path", str(temp_desktop), "--verbose"])
        assert result.exit_code == 0
        assert "image1.jpg" in result.output

    def test_organize_dry_run(self, runner, temp_desktop):
        """Test organize with dry-run."""
        result = runner.invoke(cli, ["organize", "--path", str(temp_desktop), "--dry-run"])
        assert result.exit_code == 0
        assert "DRY RUN" in result.output
        # Files should not be moved
        assert (temp_desktop / "image1.jpg").exists()

    def test_organize_confirm(self, runner, temp_desktop):
        """Test organize with confirmation."""
        result = runner.invoke(
            cli,
            ["organize", "--path", str(temp_desktop)],
            input="y\n"
        )
        assert result.exit_code == 0
        assert "complete" in result.output.lower()
        # Files should be moved
        assert (temp_desktop / "Images" / "image1.jpg").exists()

    def test_organize_cancel(self, runner, temp_desktop):
        """Test organize with cancellation."""
        result = runner.invoke(
            cli,
            ["organize", "--path", str(temp_desktop)],
            input="n\n"
        )
        assert result.exit_code == 0
        assert "Cancelled" in result.output
        # Files should not be moved
        assert (temp_desktop / "image1.jpg").exists()

    def test_rules_command(self, runner):
        """Test rules command."""
        result = runner.invoke(cli, ["rules"])
        assert result.exit_code == 0
        assert "Organization Rules" in result.output
        assert "Images" in result.output
        assert "Documents" in result.output

    def test_invalid_path(self, runner):
        """Test with invalid desktop path."""
        result = runner.invoke(cli, ["status", "--path", "/nonexistent/path"])
        assert result.exit_code == 0  # Click handles errors gracefully
        assert "Error" in result.output or "does not exist" in result.output
