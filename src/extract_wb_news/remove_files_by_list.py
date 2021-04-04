"""Remove files from a folder according to a list of filenames."""
import os
import argparse

from extract_wb_news.split_helper import load_filenames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filefolder',
        help='Provide a folder containing files',
        )
    parser.add_argument(
        'filenames_path',
        help='Provide a file containing filenames to delete from folder',
        )

    args = parser.parse_args()
    filenames = load_filenames(args.filenames_path)

    for f in filenames:
        try:
            os.remove(os.path.join(args.filefolder, f))
        except FileNotFoundError:
            pass
        else:
            print(f'Deleted file: {f}')


if __name__ == '__main__':
    main()
