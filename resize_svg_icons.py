#!/usr/bin/env python3

import csv
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def strip_unit(value):
    if value is None:
        return None
    match = re.match(r"^\s*([0-9.+-eE]+)", str(value))
    return float(match.group(1)) if match else None


def parse_viewbox(viewbox):
    if not viewbox:
        return None
    parts = viewbox.replace(",", " ").split()
    if len(parts) != 4:
        return None
    return tuple(float(x) for x in parts)


def detect_original_size(root):
    viewbox = parse_viewbox(root.get("viewBox"))
    width = strip_unit(root.get("width"))
    height = strip_unit(root.get("height"))

    if viewbox:
        min_x, min_y, vb_width, vb_height = viewbox
        return min_x, min_y, vb_width, vb_height

    if width is not None and height is not None:
        return 0.0, 0.0, width, height

    raise ValueError("SVG is missing usable width/height and viewBox")


def apply_rotation(root, angle, min_x, min_y, vb_width, vb_height):
    if angle % 360 == 0:
        return

    cx = min_x + vb_width / 2.0
    cy = min_y + vb_height / 2.0

    group = ET.Element(f"{{{SVG_NS}}}g")
    group.set("transform", f"rotate({angle:g} {cx:g} {cy:g})")

    children = list(root)
    for child in children:
        root.remove(child)
        group.append(child)

    root.append(group)


def resize_svg(
    input_path: Path,
    output_path: Path,
    canvas_width: float,
    canvas_height: float,
    rotation_degrees: float = 0.0,
):
    tree = ET.parse(input_path)
    root = tree.getroot()

    min_x, min_y, orig_width, orig_height = detect_original_size(root)
    
    apply_rotation(root, rotation_degrees, min_x, min_y, orig_width, orig_height)

    root.set("width", str(canvas_width))
    root.set("height", str(canvas_height))
    root.set("viewBox", f"{min_x:g} {min_y:g} {orig_width:g} {orig_height:g}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def main():
    if len(sys.argv) != 4:
        print("Usage: python resize_svg_icons.py <input_icon_dir> <csv_table> <output_root>")
        sys.exit(1)

    input_icon_dir = Path(sys.argv[1]).resolve()
    csv_table = Path(sys.argv[2]).resolve()
    output_root = Path(sys.argv[3]).resolve()

    with csv_table.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        required = {
            "input_file",
            "output_file",
            "output_dir",
            "canvas_width",
            "canvas_height",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

        for row_num, row in enumerate(reader, start=2):
            try:
                input_path = input_icon_dir / row["input_file"]
                output_path = output_root / row["output_dir"] / row["output_file"]
                canvas_width = float(row["canvas_width"])
                canvas_height = float(row["canvas_height"])
                rotation_degrees = float((row.get("rotation_degrees") or "0").strip())

                if not input_path.exists():
                    raise FileNotFoundError(f"Input SVG not found: {input_path}")

                resize_svg(
                    input_path=input_path,
                    output_path=output_path,
                    canvas_width=canvas_width,
                    canvas_height=canvas_height,
                    rotation_degrees=rotation_degrees,
                )

                # print(f"OK    {input_path.name} -> {output_path}")
            except Exception as exc:
                print(f"ERROR row {row_num}: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
