import setuptools

setuptools.setup(
    entry_points={
        'console_scripts': [
            'json2txt=extract_wb_news.json2txt:main',
            'combine=extract_wb_news.combine:main',
            'splitf=extract_wb_news.splitf:main',
            'tmxdir=extract_wb_news.multiple_to_tmx:main',
            'swap=extract_wb_news.swap:main',
            'remove=extract_wb_news.remove_files_by_list:main'
        ],
    },
    )
