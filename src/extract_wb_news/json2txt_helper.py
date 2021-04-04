import os
import re
import json

BASE_URL_R = 'http://www.vsemirnyjbank.org/ru'
BASE_URL_E = 'http://www.worldbank.org/en'


def load_from_json(path):
    with open(path, 'r', encoding='utf-8') as from_f:
        json_data = json.load(from_f)
    return json_data


def save_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        for para in content:
            f.write(para)
            f.write('\n')


def clean_string(para):
    para = para.replace('&nbsp;', ' ')
    para = para.replace('\u2013', '-')  # en-dash
    para = para.replace('\u2014', '-')  # em-dash
    para = para.replace('\u2015', '-')
    para = para.replace('\u2018', "'")  # single quote
    para = para.replace('\u2019', "'")  # single quote
    para = para.replace('\u2060', '')  # a zero width non-breaking space
    para = para.replace('\u202f', ' ')  # narrow no-break space

    para = para.replace('\u201c', '"')
    para = para.replace('\u201d', '"')

    para = para.replace('\u00E9', 'é')
    para = para.replace('\u00e9', 'é')
    para = para.replace('\u2116', '№')
    para = para.replace('\u00fb', 'û')

    para = para.replace('\u00e0', 'û')
    para = para.replace('\u00fb', 'à')

    para = para.replace(';', '; ')
    para = para.replace(':', ': ')
    para = para.replace('?', '? ')
    para = para.replace('!', '! ')
    para = para.replace('http: //', 'http://')
    para = para.replace('https: //', 'https://')
    # '3Noteworthy' -> '3 Noteworthy'  NOTE: also splits 10th, 2nd etc.
    # para = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', para)

    # investigations.956 firms,  торговля.9 марта
    para = re.sub(r'([a-z]|[а-я])(\.)(\d+)', r'\1\2 \3', para)

    # 'U.S.A.A countrys' -> 'U.S.A. A countrys'
    # '18).Fertility' -> '18). Fertility'
    para = re.sub(r'(\.)([A-Z])([a-z]| )', r'\1 \2\3', para)
    para = re.sub(r'(\.)([А-Я])([а-я]| )', r'\1 \2\3', para)

    # 'fkdhGvkvs' -> 'fkdh. Gvkvs'
    # 'странахВ ' -> 'странах. В'
    # 'СтАР' -> 'СтАР
    para = re.sub(r'([a-z])([A-Z]([a-z]| ))', r'\1. \2', para)
    # para = re.sub(r'([а-я])([А-Я]([а-я]| ))', r'\1. \2', para)

    para = ' '.join(para.split())
    return para


def get_content(content_json, doc_id):
    content = []

    for el in ['title', 'descr', 'content']:
        try:
            para = content_json['documents'][doc_id][el]['cdata!']
            para = clean_string(para)
            content.append(para)
        except KeyError:
            print(f'Missing element: {el}, in doc: {doc_id}')

    return content


def url_to_filename(url):
    """Assume the following URL structure.

    input: http://www.vsemirnyjbank.org/ru/news/factsheet/2020/02/11/how-the-wo

    output: '20200211-factsheet-how-the-wo.txt'

    http://www.worldbank.org/en/news/factsheet/2020/10/15/world-bank-gr

    Breaks on the following URLs:
    http://www.vsemirnyjbank.org/ru/country/tajikistan/brief/consultation-tajikistan-essa-report
    http://www.vsemirnyjbank.org/ru/region/eca/brief/central-asia-knowledge-network-buil
    http://www.vsemirnyjbank.org/ru/country/tajikistan/publication/economic-update-fall-2020
    """
    url = url.split("/")
    date = ''.join(url[6:9])
    conttype = url[5]
    title = url[9]
    filename = f'{date}-{conttype}-{title}.txt'

    return filename


def get_doc_idx(mapping, url):
    try:
        idx = mapping[url]
    except KeyError as err:
        rus_url = url.replace(BASE_URL_E, BASE_URL_R)
        print(f'WARNING: No corresponding English publication for {rus_url}')
        print(f'         Expected English URL: {url}')
        idx = ''
    return idx


def extract_save_russian_content(rus_json, destination_dir):
    """Save Russian content and return Russian URLs."""
    # Get indexes of all Russian publications
    rus_idx = list(rus_json['documents'].keys())

    # Keep URLs of Russian publications because they uniquely identify
    # each publication and can be used to find corresponding English pieces
    rus_urls = []
    try:
        for idx in rus_idx:
            url = rus_json['documents'][idx]['url']
            rus_urls.append(url)
            filename = url_to_filename(url)

            content = get_content(rus_json, idx)

            save_to = os.path.join(destination_dir, filename)
            save_file(save_to, content)
    except KeyError:
        pass
    return rus_urls


def extract_save_english_content(eng_json, rus_urls, destination_dir):
    # Get indexes of all Russian publications
    eng_idx = list(eng_json['documents'].keys())
    # Build a map from English URLs to English doc indexes
    url2idx = {}
    try:
        for idx in eng_idx:
            url = eng_json['documents'][idx]['url']
            url2idx[url] = idx
    except KeyError:
        pass

    # By using earlier collected Russian URLs
    eng_urls = []
    for rus_url in rus_urls:
        # hypothetical English URL
        eng_url = rus_url.replace(BASE_URL_R, BASE_URL_E)

        eng_doc_id = get_doc_idx(url2idx, eng_url)

        if eng_doc_id:  # there may be no corresponding English publication
            eng_urls.append(eng_url)

            filename = url_to_filename(eng_url)

            content = get_content(eng_json, eng_doc_id)

            save_to = os.path.join(destination_dir, filename)
            save_file(save_to, content)

    return eng_urls
