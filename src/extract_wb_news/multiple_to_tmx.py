"""Step 4: Convert multiple txt files to tmx."""
import os
import argparse

from to_tmx.to_tmx import create_tmx


# credits to https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        help='Provide path to folder with many tab-del txt files',
        )
    args = parser.parse_args()
    filenames = absoluteFilePaths(args.path)

    for filename in filenames:
        create_tmx(filename)


if __name__ == '__main__':
    main()
