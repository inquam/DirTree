#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import fnmatch
from typing import Set, List


def should_ignore(path: Path, ignore_patterns: List[str]) -> bool:
    """Check if a path should be ignored based on patterns."""
    if not ignore_patterns:
        return False

    path_str = str(path)
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def matches_filters(entry: Path, filters: Set[str]) -> bool:
    """Check if a file matches any of the specified filters."""
    if not filters:
        return True

    if entry.suffix == '':
        return '*' in filters or '_' in filters

    for filter_pattern in filters:
        if filter_pattern == '_':
            continue
        if fnmatch.fnmatch(entry.name, filter_pattern):
            return True
    return False


def has_matching_files(directory: Path, filters: Set[str], ignore_patterns: List[str]) -> bool:
    """Check if directory contains any files matching the filters."""
    try:
        for entry in directory.iterdir():
            if should_ignore(entry, ignore_patterns):
                continue
            if entry.is_file() and matches_filters(entry, filters):
                return True
            if entry.is_dir() and has_matching_files(entry, filters, ignore_patterns):
                return True
    except PermissionError:
        return False
    return False


def print_directory_tree(root_dir: Path, filters: Set[str], ignore_patterns: List[str],
                         show_empty: bool, indent: str = "") -> None:
    """Print the directory tree with the specified filters and options."""
    try:
        if should_ignore(root_dir, ignore_patterns):
            return

        entries = sorted(root_dir.iterdir())
        entries = [e for e in entries if not should_ignore(e, ignore_patterns)]

        has_content = show_empty or has_matching_files(root_dir, filters, ignore_patterns)
        if not has_content:
            return

        print(f"{indent}📁 {root_dir.name}/")
        new_indent = indent + "  "

        for entry in entries:
            if entry.is_dir():
                print_directory_tree(entry, filters, ignore_patterns, show_empty, new_indent)
            elif matches_filters(entry, filters):
                print(f"{new_indent}📄 {entry.name}")

    except PermissionError:
        print(f"{indent}❌ Permission denied")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Directory Tree')
    parser.add_argument('dir', type=str, nargs='?', default='./',
                        help='Path to the root directory (default: current directory)')
    parser.add_argument('--filters', type=str, default=None,
                        help='Comma separated list of file patterns (e.g. *.py,*.cpp,README.md). Use _ for files without extension')
    parser.add_argument('--empty-directories', action='store_true',
                        help='Show empty directories')
    parser.add_argument('--ignore', type=str, default=None,
                        help='Comma separated list of patterns to ignore (e.g. node_modules/*,*.tmp)')

    args = parser.parse_args()

    filters = set(pattern.strip() for pattern in args.filters.split(',')) if args.filters else set()
    ignore_patterns = [pattern.strip() for pattern in args.ignore.split(',')] if args.ignore else []

    print_directory_tree(
        Path(args.dir),
        filters,
        ignore_patterns,
        args.empty_directories
    )