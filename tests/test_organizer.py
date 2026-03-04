"""Tests for the organizer module."""

import os
import tempfile
from pathlib import Path

import pytest

from desktop_organizer.organizer import DesktopOrganizer, OrganizationRule, DEFAULT_RULES


class TestDesktopOrganizer:
    """Test cases for DesktopOrganizer."""

    @pytest.fixture
def temp_desktop(self):
        """Create a temporary desktop directory with test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            desktop = Path(tmpdir) / "Desktop"
            desktop.mkdir()

            # Create test files
            (desktop / "image1.jpg").touch()
            (desktop / "image2.png").touch()
            (desktop / "document.pdf").touch()
            (desktop / "spreadsheet.xlsx").touch()
            (desktop / "script.py").touch()
            (desktop / "archive.zip").touch()
            (desktop / "unknown.xyz").touch()

            # Create hidden file (should be skipped)
            (desktop / ".hidden").touch()

            yield desktop

    @pytest.fixture
    def organizer(self, temp_desktop):
        """Create an organizer instance with temp desktop."""
        return DesktopOrganizer(desktop_path=temp_desktop)

    def test_init_default_path(self):
        """Test organizer initializes with default path."""
        organizer = DesktopOrganizer()
        assert organizer.desktop_path is not None
        assert isinstance(organizer.rules, list)

    def test_init_custom_path(self, temp_desktop):
        """Test organizer with custom desktop path."""
        organizer = DesktopOrganizer(desktop_path=temp_desktop)
        assert organizer.desktop_path == temp_desktop

    def test_default_rules(self):
        """Test default rules are loaded."""
        organizer = DesktopOrganizer()
        assert len(organizer.rules) == len(DEFAULT_RULES)

    def test_get_rule_for_file(self, organizer):
        """Test finding rule for files."""
        jpg_rule = organizer._get_rule_for_file(Path("test.jpg"))
        assert jpg_rule is not None
        assert jpg_rule.name == "Images"

        pdf_rule = organizer._get_rule_for_file(Path("test.pdf"))
        assert pdf_rule is not None
        assert pdf_rule.name == "Documents"

        unknown_rule = organizer._get_rule_for_file(Path("test.xyz"))
        assert unknown_rule is None

    def test_should_skip(self, organizer):
        """Test file skipping logic."""
        assert organizer._should_skip(Path(".hidden")) is True
        assert organizer._should_skip(Path("desktop.ini")) is True
        assert organizer._should_skip(Path(".DS_Store")) is True
        assert organizer._should_skip(Path("Thumbs.db")) is True
        assert organizer._should_skip(Path("normal.txt")) is False

    def test_preview(self, organizer):
        """Test preview functionality."""
        preview = organizer.preview()

        assert "Images" in preview
        assert len(preview["Images"]) == 2  # jpg and png
        assert "Documents" in preview
        assert "spreadsheet.xlsx" in preview["Spreadsheets"]

        # Unknown files should not be in preview
        assert "unknown.xyz" not in str(preview)

    def test_organize_dry_run(self, organizer):
        """Test organize with dry_run mode."""
        organizer.dry_run = True
        stats = organizer.organize()

        assert stats["total"] == 7
        assert stats["moved"] == 6  # All except .hidden and unknown.xyz
        assert stats["skipped"] == 1  # unknown.xyz

        # Files should still be in original location
        assert (organizer.desktop_path / "image1.jpg").exists()
        assert not (organizer.desktop_path / "Images" / "image1.jpg").exists()

    def test_organize_actual(self, organizer):
        """Test actual file organization."""
        stats = organizer.organize()

        assert stats["moved"] == 6

        # Check files are moved
        assert (organizer.desktop_path / "Images" / "image1.jpg").exists()
        assert (organizer.desktop_path / "Images" / "image2.png").exists()
        assert (organizer.desktop_path / "Documents" / "document.pdf").exists()

        # Check original files are gone
        assert not (organizer.desktop_path / "image1.jpg").exists()

    def test_organize_name_conflict(self, organizer):
        """Test handling of name conflicts."""
        # Create a file in destination folder first
        images_folder = organizer.desktop_path / "Images"
        images_folder.mkdir()
        (images_folder / "image1.jpg").touch()

        stats = organizer.organize()

        # Both files should exist with different names
        assert (organizer.desktop_path / "Images" / "image1.jpg").exists()
        assert (organizer.desktop_path / "Images" / "image1_1.jpg").exists()

    def test_add_rule(self, organizer):
        """Test adding custom rules."""
        initial_count = len(organizer.rules)
        organizer.add_rule("Custom", [".xyz"], "CustomFolder")

        assert len(organizer.rules) == initial_count + 1

        # Check new rule works
        rule = organizer._get_rule_for_file(Path("test.xyz"))
        assert rule is not None
        assert rule.name == "Custom"

    def test_remove_rule(self, organizer):
        """Test removing rules."""
        initial_count = len(organizer.rules)

        result = organizer.remove_rule("Images")
        assert result is True
        assert len(organizer.rules) == initial_count - 1

        # Check rule is gone
        assert organizer._get_rule_for_file(Path("test.jpg")) is None

    def test_remove_nonexistent_rule(self, organizer):
        """Test removing a rule that doesn't exist."""
        result = organizer.remove_rule("NonExistent")
        assert result is False

    def test_organize_progress_callback(self, organizer):
        """Test progress callback is called."""
        progress_calls = []

        def callback(filename, current, total):
            progress_calls.append((filename, current, total))

        organizer.organize(progress_callback=callback)

        assert len(progress_calls) == 7  # Total files
        assert progress_calls[0][1] == 1  # First file
        assert progress_calls[-1][1] == 7  # Last file


class TestOrganizationRule:
    """Test cases for OrganizationRule dataclass."""

    def test_rule_creation(self):
        """Test rule can be created."""
        rule = OrganizationRule(
            name="Test",
            extensions=[".txt", ".md"],
            folder_name="TextFiles"
        )

        assert rule.name == "Test"
        assert rule.extensions == [".txt", ".md"]
        assert rule.folder_name == "TextFiles"
