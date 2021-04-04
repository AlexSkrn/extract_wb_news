"""Step 2. Combine all Russian and all English files into 2 single docs."""
import os
import argparse


def combine(dir, subdir, filenames, to_file):
    """Combine content from multiple files and return filenames."""
    target_path = os.path.join(dir, to_file)
    with open(target_path, 'w', encoding='utf-8') as to_f:
        for filename in filenames:
            source_file_path = os.path.join(dir, subdir, filename)
            with open(source_file_path, 'r', encoding='utf-8') as from_f:
                # to_f.write('FILE_START\n')
                to_f.write(from_f.read())
                to_f.write('FILE_END\n')
    return filenames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'src_txt_dir',
        help='Provide a source folder with 2 subfolders: txt_rus, txt_eng',
        )
    args = parser.parse_args()
    src_txt_dir = args.src_txt_dir
    RUS_SUBDIR = 'txt_rus'
    ENG_SUBDIR = 'txt_eng'

    # This dir and files in it are created by json2txt.py
    RUS_FILENAMES = os.listdir(os.path.join(src_txt_dir, RUS_SUBDIR))

    rus_filenames = combine(src_txt_dir, RUS_SUBDIR, RUS_FILENAMES, 'combined_rus.txt')
    eng_filenames = combine(src_txt_dir, ENG_SUBDIR, RUS_FILENAMES, 'combined_eng.txt')

    assert rus_filenames == eng_filenames

    # Save the list of filenames to be able to reverse the process
    FILE_LIST_IN_ORDER = os.path.join(src_txt_dir, 'filenames_in_order.txt')
    with open(FILE_LIST_IN_ORDER, 'w', encoding='utf-8') as to_f:
        for filename in rus_filenames:
            to_f.write(filename)
            to_f.write('\n')


if __name__ == '__main__':
    main()
