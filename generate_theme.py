#!/usr/bin/env python3
import argparse
import csv
import io
from collections import OrderedDict
from pathlib import Path


def infer_context(directory: str) -> str:
    parts = directory.strip('/').split('/')
    leaf = parts[-1].lower() if parts else ''
    if leaf == 'actions':
        return 'Actions'
    if leaf == 'apps':
        return 'Applications'
    return leaf.capitalize() if leaf else 'Unknown'


def infer_section(directory: str, rows: list[dict]) -> list[str]:
    width_values = {str(r.get('canvas_width', '')).strip() for r in rows if str(r.get('canvas_width', '')).strip()}
    height_values = {str(r.get('canvas_height', '')).strip() for r in rows if str(r.get('canvas_height', '')).strip()}
    if directory.startswith('scalable/'):
        return [f'[{directory}]', 'Type=Scalable', f'Context={infer_context(directory)}']
    if len(width_values) == 1 and len(height_values) == 1 and next(iter(width_values)) == next(iter(height_values)):
        size = next(iter(width_values))
        return [f'[{directory}]', f'Size={size}', 'Type=Fixed', f'Context={infer_context(directory)}']
    raise ValueError(f'Cannot infer a single square fixed size for directory {directory!r}')


def build_index_theme(theme_name: str, comment: str, csv_text: str) -> str:
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    if not reader.fieldnames:
        raise ValueError('CSV input is missing a header row.')
    required = {'output_dir', 'canvas_width', 'canvas_height'}
    missing = required - set(reader.fieldnames)
    if missing:
        raise ValueError(f'Missing required CSV columns: {sorted(missing)}')

    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for row in reader:
        directory = row['output_dir'].strip()
        if not directory:
            continue
        grouped.setdefault(directory, []).append(row)

    directories = list(grouped.keys())
    if not directories:
        raise ValueError('No output_dir values were found in the CSV.')

    lines = [
        '[Icon Theme]',
        f'Name={theme_name}',
        f'Comment={comment}',
        f'Directories={",".join(directories)}',
        ''
    ]

    for directory, rows in grouped.items():
        lines.extend(['', *infer_section(directory, rows)])

    return '\n'.join(lines).strip() + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate a freedesktop icon-theme index.theme file from CSV rows.'
    )
    parser.add_argument('--name', required=True, help='Theme name for the Name= field')
    parser.add_argument('--comment', required=True, help='Theme comment for the Comment= field')
    parser.add_argument('--csv', dest='csv_path', help='Input CSV file path; reads stdin if omitted')
    parser.add_argument('-o', '--output', default='index.theme', help='Output file path')
    args = parser.parse_args()

    if args.csv_path:
        csv_text = Path(args.csv_path).read_text(encoding='utf-8')
    else:
        import sys
        csv_text = sys.stdin.read()

    content = build_index_theme(args.name, args.comment, csv_text)
    output_path = Path(args.output)
    output_path.write_text(content, encoding='utf-8')
    # print(output_path)


if __name__ == '__main__':
    main()