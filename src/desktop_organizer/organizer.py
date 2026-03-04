"""Core organizer logic for desktop icons."""

import os
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


@dataclass
class OrganizationRule:
    """Rule for organizing files."""
    name: str
    extensions: List[str]
    folder_name: str


DEFAULT_RULES = [
    OrganizationRule("Images", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"], "Images"),
    OrganizationRule("Documents", [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"], "Documents"),
    OrganizationRule("Spreadsheets", [".xls", ".xlsx", ".csv", ".ods"], "Spreadsheets"),
    OrganizationRule("Presentations", [".ppt", ".pptx", ".odp", ".key"], "Presentations"),
    OrganizationRule("Archives", [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"], "Archives"),
    OrganizationRule("Videos", [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"], "Videos"),
    OrganizationRule("Audio", [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"], "Audio"),
    OrganizationRule("Code", [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".yaml", ".yml"], "Code"),
    OrganizationRule("Executables", [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".AppImage"], "Executables"),
]


class DesktopOrganizer:
    """Organizes desktop icons into categorized folders."""
    
    def __init__(
        self,
        desktop_path: Optional[Path] = None,
        rules: Optional[List[OrganizationRule]] = None,
        dry_run: bool = False
    ):
        self.desktop_path = desktop_path or self._get_default_desktop_path()
        self.rules = rules or DEFAULT_RULES.copy()
        self.dry_run = dry_run
        self.stats: Dict[str, int] = {}
        
    def _get_default_desktop_path(self) -> Path:
        """Get the default desktop path based on OS."""
        home = Path.home()
        
        # Try common desktop paths
        possible_paths = [
            home / "Desktop",
            home / "desktop",
            home / "Escritorio",  # Spanish
            home / "Bureau",      # French
            home / "Schreibtisch", # German
            home / "Desktop",     # OneDrive synced desktop
        ]
        
        # Check environment variable first
        if "DESKTOP" in os.environ:
            return Path(os.environ["DESKTOP"])
            
        for path in possible_paths:
            if path.exists():
                return path
                
        # Default fallback
        return home / "Desktop"
    
    def _get_rule_for_file(self, file_path: Path) -> Optional[OrganizationRule]:
        """Find matching rule for a file."""
        ext = file_path.suffix.lower()
        for rule in self.rules:
            if ext in rule.extensions:
                return rule
        return None
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        # Skip hidden files
        if file_path.name.startswith("."):
            return True
        # Skip system files
        if file_path.name in ["desktop.ini", ".DS_Store", "Thumbs.db"]:
            return True
        return False
    
    def organize(
        self,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> Dict[str, int]:
        """
        Organize desktop icons.
        
        Args:
            progress_callback: Optional callback(current_file, current, total)
            
        Returns:
            Statistics dictionary with move counts per category
        """
        if not self.desktop_path.exists():
            raise FileNotFoundError(f"Desktop path not found: {self.desktop_path}")
        
        # Get all files to organize
        files = [f for f in self.desktop_path.iterdir() if f.is_file()]
        files = [f for f in files if not self._should_skip(f)]
        
        total = len(files)
        self.stats = {"total": total, "moved": 0, "skipped": 0}
        
        for idx, file_path in enumerate(files, 1):
            if progress_callback:
                progress_callback(file_path.name, idx, total)
            
            rule = self._get_rule_for_file(file_path)
            
            if rule:
                target_folder = self.desktop_path / rule.folder_name
                target_path = target_folder / file_path.name
                
                if not self.dry_run:
                    target_folder.mkdir(exist_ok=True)
                    
                    # Handle name conflicts
                    counter = 1
                    original_target = target_path
                    while target_path.exists():
                        stem = original_target.stem
                        suffix = original_target.suffix
                        target_path = target_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(target_path))
                
                self.stats["moved"] += 1
                self.stats[rule.name] = self.stats.get(rule.name, 0) + 1
                logger.info(f"Moved: {file_path.name} -> {rule.folder_name}/")
            else:
                self.stats["skipped"] += 1
                logger.debug(f"Skipped: {file_path.name}")
        
        return self.stats
    
    def preview(self) -> Dict[str, List[str]]:
        """
        Preview what would be organized without moving files.
        
        Returns:
            Dictionary mapping folder names to lists of filenames
        """
        if not self.desktop_path.exists():
            raise FileNotFoundError(f"Desktop path not found: {self.desktop_path}")
        
        preview_dict: Dict[str, List[str]] = {}
        
        for file_path in self.desktop_path.iterdir():
            if not file_path.is_file() or self._should_skip(file_path):
                continue
            
            rule = self._get_rule_for_file(file_path)
            if rule:
                if rule.folder_name not in preview_dict:
                    preview_dict[rule.folder_name] = []
                preview_dict[rule.folder_name].append(file_path.name)
        
        return preview_dict
    
    def add_rule(self, name: str, extensions: List[str], folder_name: str) -> None:
        """Add a custom organization rule."""
        self.rules.append(OrganizationRule(name, extensions, folder_name))
    
    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                del self.rules[i]
                return True
        return False
