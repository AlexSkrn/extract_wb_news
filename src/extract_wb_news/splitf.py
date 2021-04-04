"""Step3: Split a tab-delimited txt file (converted from tmx)."""

import os
import argparse

from extract_wb_news.split_helper import (
    load_filenames,
    parse_multifile,
    )


# After alignment, check that all file-end markers are in place
def main():
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'multifile',
        help='Provide tab-del filename',
        )
    parser.add_argument(
        'filenames',
        help='Provide file with a list of filenames',
        )
    parser.add_argument(
        '-w',
        action='store_true',
        help='Specify "-w" to split multifile. If not, just validate content.'
    )
    args = parser.parse_args()

    multifile = args.multifile  # tab-del content filename to process
    filenames_path = args.filenames
    write = args.w  # default False

    filenames = load_filenames(filenames_path)

    destination_dir = ''

    if write:
        head, tail = os.path.split(args.filenames)
        destination_dir = os.path.join(head, 'txt_dual')
        try:
            os.mkdir(destination_dir)
            print(f'\nWriting txt files to: {destination_dir}...\n')
        except FileExistsError:
            pass

    ends_num, total_lines = parse_multifile(filenames, multifile, destination_dir)

    num_filenames = len(filenames)
    print(f'{num_filenames} filenames read into memory.')
    assert num_filenames == ends_num

    print(f'End_marks: {ends_num}')
    print(f'Total # of segments: {total_lines}')


if __name__ == '__main__':
    main()
