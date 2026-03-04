"""Command-line interface for Desktop Organizer."""

import sys
import click
from pathlib import Path
from typing import Optional

from .organizer import DesktopOrganizer, DEFAULT_RULES
from . import __version__


@click.group()
@click.version_option(version=__version__, prog_name="desktop-organizer")
def cli():
    """Desktop Organizer - Organize your desktop icons with ease."""
    pass


@cli.command()
@click.option(
    "--path", "-p",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Path to desktop directory (default: auto-detect)"
)
@click.option(
    "--dry-run", "-n",
    is_flag=True,
    help="Show what would be moved without actually moving files"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed output"
)
def organize(path: Optional[Path], dry_run: bool, verbose: bool):
    """Organize desktop icons into categorized folders."""
    try:
        organizer = DesktopOrganizer(desktop_path=path, dry_run=dry_run)
        
        if dry_run:
            click.echo(click.style("🔍 DRY RUN - No files will be moved", fg="yellow", bold=True))
            click.echo()
        
        # Show preview
        preview = organizer.preview()
        
        if not preview:
            click.echo(click.style("✨ Desktop is already organized!", fg="green"))
            return
        
        click.echo(click.style(f"📁 Desktop: {organizer.desktop_path}", fg="cyan", bold=True))
        click.echo()
        
        # Show preview
        total_files = sum(len(files) for files in preview.values())
        click.echo(click.style(f"Found {total_files} file(s) to organize:", fg="blue"))
        
        for folder, files in sorted(preview.items()):
            click.echo(click.style(f"  📂 {folder}/", fg="green"))
            if verbose:
                for f in sorted(files):
                    click.echo(f"     - {f}")
            else:
                click.echo(f"     ({len(files)} file(s))")
        
        click.echo()
        
        if dry_run:
            return
        
        # Confirm before organizing
        if not click.confirm("Do you want to proceed with organization?"):
            click.echo("Cancelled.")
            return
        
        # Perform organization with progress
        click.echo()
        
        def progress_callback(filename: str, current: int, total: int):
            if verbose:
                click.echo(f"  [{current}/{total}] Processing: {filename}")
        
        stats = organizer.organize(progress_callback)
        
        click.echo()
        click.echo(click.style("✅ Organization complete!", fg="green", bold=True))
        click.echo(f"   Files moved: {stats['moved']}")
        click.echo(f"   Files skipped: {stats['skipped']}")
        
        if stats['moved'] > 0:
            click.echo()
            click.echo("Breakdown:")
            for rule in DEFAULT_RULES:
                count = stats.get(rule.name, 0)
                if count > 0:
                    click.echo(f"   📂 {rule.folder_name}: {count} file(s)")
                    
    except FileNotFoundError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"❌ Unexpected error: {e}", fg="red"), err=True)
        if verbose:
            raise
        sys.exit(1)


@cli.command()
@click.option(
    "--path", "-p",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Path to desktop directory (default: auto-detect)"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show all files"
)
def preview(path: Optional[Path], verbose: bool):
    """Preview what would be organized without making changes."""
    try:
        organizer = DesktopOrganizer(desktop_path=path)
        preview_dict = organizer.preview()
        
        click.echo(click.style(f"📁 Desktop: {organizer.desktop_path}", fg="cyan", bold=True))
        click.echo()
        
        if not preview_dict:
            click.echo(click.style("✨ No files to organize!", fg="green"))
            return
        
        total_files = sum(len(files) for files in preview_dict.values())
        click.echo(click.style(f"Would organize {total_files} file(s):", fg="blue"))
        
        for folder, files in sorted(preview_dict.items()):
            click.echo(click.style(f"  📂 {folder}/", fg="green"))
            if verbose:
                for f in sorted(files):
                    click.echo(f"     - {f}")
            else:
                click.echo(f"     ({len(files)} file(s))")
                
    except FileNotFoundError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
def rules():
    """Show current organization rules."""
    click.echo(click.style("📋 Organization Rules:", fg="cyan", bold=True))
    click.echo()
    
    for rule in DEFAULT_RULES:
        click.echo(click.style(f"  {rule.name}:", fg="green"))
        click.echo(f"    Folder: {rule.folder_name}/")
        click.echo(f"    Extensions: {', '.join(rule.extensions)}")
        click.echo()


@cli.command()
@click.option(
    "--path", "-p",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Path to desktop directory (default: auto-detect)"
)
def status(path: Optional[Path]):
    """Show desktop organization status."""
    try:
        organizer = DesktopOrganizer(desktop_path=path)
        
        click.echo(click.style(f"📁 Desktop: {organizer.desktop_path}", fg="cyan", bold=True))
        click.echo()
        
        if not organizer.desktop_path.exists():
            click.echo(click.style("❌ Desktop path does not exist!", fg="red"))
            return
        
        files = [f for f in organizer.desktop_path.iterdir() if f.is_file()]
        folders = [f for f in organizer.desktop_path.iterdir() if f.is_dir()]
        
        click.echo(f"Total items: {len(files) + len(folders)}")
        click.echo(f"  📄 Files: {len(files)}")
        click.echo(f"  📂 Folders: {len(folders)}")
        click.echo()
        
        # Count files by type
        preview = organizer.preview()
        organized_count = sum(len(f) for f in preview.values())
        
        if organized_count > 0:
            click.echo(click.style(f"🔧 {organized_count} file(s) can be organized", fg="yellow"))
            for folder, files in sorted(preview.items()):
                click.echo(f"   → {folder}: {len(files)} file(s)")
        else:
            click.echo(click.style("✅ All files are organized!", fg="green"))
            
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"), err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
