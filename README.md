# gLabels Icon Theme Builder

Generate gLabels icon themes from LibreOffice SVG assets using a small CSV-driven build pipeline.

This repository contains scripts that resize SVG icons, apply optional rotation, and generate freedesktop-compatible `index.theme` files for multiple icon themes.

## What it does

- Resizes SVG icons to theme-specific canvas sizes.
- Applies optional SVG rotation around the icon center.
- Generates `index.theme` files from CSV metadata.
- Builds light and dark variants for multiple theme families.
- Automates the conversion process with a shell script.

## Repository layout

- `convert_themes.sh` — runs the full conversion pipeline for all supported themes.
- `resize_svg_icons.py` — resizes and rewrites SVG files based on CSV instructions.
- `generate_theme.py` — creates `index.theme` files from CSV input.
- `icon_table_*.csv` — per-theme icon mapping and canvas metadata.
- `LibreOffice/icon-themes/` — source SVG theme assets.
- `freedesktop/` — source SVG theme assets.
- `build/` — generated output themes.

## Requirements

- Python 3.10+
- Bash
- SVG source assets from LibreOffice or freedesktop icon themes
- CSV input files describing the output layout

## Usage

Run the full build:

```bash
./convert_libreoffice_themes.sh
```