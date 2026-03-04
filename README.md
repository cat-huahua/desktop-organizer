# 🖥️ Desktop Organizer

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/yourusername/desktop-organizer/workflows/CI/badge.svg)](https://github.com/yourusername/desktop-organizer/actions)

A simple yet powerful CLI tool to automatically organize your desktop icons into categorized folders.

![Demo](assets/demo.gif)

## ✨ Features

- 📁 **Smart Categorization** - Automatically sorts files into appropriate folders
- 🔍 **Dry Run Mode** - Preview changes before applying them
- ⚡ **Fast & Lightweight** - Pure Python, no heavy dependencies
- 🎨 **Customizable Rules** - Define your own organization rules
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 📊 **Progress Tracking** - See what's being organized in real-time

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install desktop-organizer
```

### From Source

```bash
git clone https://github.com/yourusername/desktop-organizer.git
cd desktop-organizer
pip install -e .
```

## 🚀 Quick Start

### Check Desktop Status

```bash
desktop-organizer status
```

### Preview Changes

```bash
desktop-organizer preview
```

### Organize Desktop

```bash
desktop-organizer organize
```

## 📖 Usage

```
Usage: desktop-organizer [OPTIONS] COMMAND [ARGS]...

  Desktop Organizer - Organize your desktop icons with ease.

Options:
  --version   Show the version and exit.
  --help      Show this message and exit.

Commands:
  organize  Organize desktop icons into categorized folders.
  preview   Preview what would be organized without making changes.
  rules     Show current organization rules.
  status    Show desktop organization status.
```

### Organize Command

```bash
# Basic usage
desktop-organizer organize

# Dry run - see what would happen
desktop-organizer organize --dry-run

# Specify custom desktop path
desktop-organizer organize --path ~/my-custom-desktop

# Verbose output
desktop-organizer organize -v
```

## 📂 Default Categories

| Category | Extensions |
|----------|-----------|
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico |
| Documents | .pdf, .doc, .docx, .txt, .rtf, .odt, .md |
| Spreadsheets | .xls, .xlsx, .csv, .ods |
| Presentations | .ppt, .pptx, .odp, .key |
| Archives | .zip, .rar, .7z, .tar, .gz, .bz2 |
| Videos | .mp4, .avi, .mkv, .mov, .wmv, .flv |
| Audio | .mp3, .wav, .flac, .aac, .ogg, .m4a |
| Code | .py, .js, .html, .css, .java, .cpp, .json, etc. |
| Executables | .exe, .msi, .dmg, .pkg, .deb, .rpm |

## ⚙️ Configuration

You can customize organization rules by creating a configuration file at `~/.config/desktop-organizer/config.yaml`:

```yaml
rules:
  - name: Images
    extensions: [".jpg", ".png", ".gif"]
    folder: "Pictures"
  
  - name: Work
    extensions: [".docx", ".xlsx", ".pptx"]
    folder: "Work_Documents"
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for a cleaner desktop
- Built with [Click](https://click.palletsprojects.com/) for the CLI interface

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - your.email@example.com

Project Link: [https://github.com/yourusername/desktop-organizer](https://github.com/yourusername/desktop-organizer)
