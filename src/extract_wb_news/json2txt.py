"""Step 1."""
import os

import argparse

from extract_wb_news.json2txt_helper import (
    save_file,
    load_from_json,
    extract_save_russian_content,
    extract_save_english_content,
    url_to_filename,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'rus_json',
        help='Provide Russian JSON downloaded from Internet',
        )
    parser.add_argument(
        'eng_json',
        help='Provide English JSON downloaded from Internet',
        )

    parser.add_argument(
        'save_txt_to',
        help='Specify destination folder to be created for txt files',
        )
    args = parser.parse_args()
    rus_json = args.rus_json
    eng_json = args.eng_json
    target_txt_dir = args.save_txt_to  # target dir for converted files
    rus_subdir = 'txt_rus'
    eng_subdir = 'txt_eng'

    # Create destination folder and subfolders
    try:
        os.mkdir(target_txt_dir)
    except FileExistsError:
        pass

    for folder in (rus_subdir, eng_subdir):
        try:
            os.mkdir(os.path.join(target_txt_dir, folder))
        except FileExistsError:
            pass

    # Loading JSON files downloaded from web
    rus_json = load_from_json(rus_json)
    eng_json = load_from_json(eng_json)

    # Extract and save Russian content to Destination folder/txt_rus
    # Russian URLs will be used to extract corresponding English content
    save_to = os.path.join(target_txt_dir, rus_subdir)
    rus_urls = extract_save_russian_content(rus_json, save_to)
    # Save URLs and log the number of publications extracted
    save_file(os.path.join(target_txt_dir, 'URLs_RUS.txt'), rus_urls)
    print(f'Extracted {len(rus_urls)} Russian publications')

    # Extract and save English content to Destination folder/txt_eng
    save_to = os.path.join(target_txt_dir, eng_subdir)
    eng_urls = extract_save_english_content(eng_json, rus_urls, save_to)
    # Save URLs and log the number of publications extracted
    save_file(os.path.join(target_txt_dir, 'URLs_ENG.txt'), eng_urls)
    print(f'Extracted {len(eng_urls)} English publications')

    # Remove Russian files which have no English counterparts
    if len(rus_urls) != len(eng_urls):
        print('Removing Russian files which have no English counterparts...')
        saved_rus_files = [url_to_filename(url) for url in rus_urls]
        saved_eng_files = [url_to_filename(url) for url in eng_urls]

        files_to_delete = set(saved_rus_files).difference(set(saved_eng_files))
        print(f'Deleting {len(files_to_delete)} files: {files_to_delete}')

        for f in files_to_delete:
            os.remove(os.path.join(target_txt_dir, rus_subdir, f))

        print('Files successfully deleted.')


if __name__ == '__main__':
    main()
