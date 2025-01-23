import os
import argparse
from pathlib import Path


def print_directory_tree(root_dir, allowed_extensions=None, indent=""):
    root = Path(root_dir)

    # Print the current directory name
    print(f"{indent}📁 {root.name}/")

    # Increase indentation for subdirectories and files
    indent += "  "

    try:
        # Sort entries to get a consistent output
        entries = sorted(root.iterdir())

        # Print all subdirectories first
        for entry in entries:
            if entry.is_dir():
                print_directory_tree(entry, indent)
            elif allowed_extensions is None or entry.suffix in allowed_extensions:
                print(f"{indent}📄 {entry.name}")

    except PermissionError:
        print(f"{indent}❌ Permission denied")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Directory Tree')
    parser.add_argument('dir', type=str, nargs='?', default='./',
                        help='Path to the root directory (default: current directory)')

    parser.add_argument('--types', type=str, default=None,
                        help='Comma separated list of file extensions')

    args = parser.parse_args()

    # Parse the allowed file extensions if provided
    allowed_extensions = None
    if args.types:
        allowed_extensions = {f".{ext.strip()}" for ext in args.types.split(',')}

    print_directory_tree(Path(args.dir), allowed_extensions)