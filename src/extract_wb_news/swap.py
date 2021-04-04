#!/usr/bin/env python3
"""This script swaps columns in 2-column tab-delimited file.

This is for swapping columns in a glossary for TermChecker
"""

import os
import argparse


def swap_line(line):
    """Return a swaped line."""
    try:
        column_a, column_b = line.strip().split('\t')
    except ValueError as err:
        print(f'ERROR in line: {line}\n')
        raise err
    else:
        swapped_line = f'{column_b}\t{column_a}\n'
    return swapped_line


def get_swapped_filename(filename):
    """Return a filename for the swapped file to be created."""
    _, tail = os.path.split(filename)
    target_file_name = '{}-swapped.txt'.format(os.path.splitext(tail)[0])
    return target_file_name


def swap_columns(filename):
    """Write content to filename."""
    target_file_name = get_swapped_filename(filename)
    with open(filename, 'r', encoding='utf-8') as from_f,\
            open(target_file_name, 'w', encoding='utf-8') as to_f:
        for line in from_f:
            swapped_line = swap_line(line)
            if line:
                to_f.write(swapped_line)


def main():
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='Provide tab-del file name to swap columns')
    args = parser.parse_args()

    filename = args.path
    swap_columns(filename)


if __name__ == '__main__':
    main()
