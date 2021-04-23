# Конвертация текстов новостей с сайта WB в tmx-формат

## Инструкции для себя

1. Скачиваешь json-файлы с сайта (см. список в Google Colab) и кладешь их в папку `json_data`

1. Команда `json2txt ru-json en-json txt_doctype_region` (где `txt_doctype_region` -- это
директория, которую нужно предварительно создать) извлечет из json-ов параллельные тексты
и запишет их в соответствующие txt-файлы в поддиректории `txt_eng` и `txt_rus`

1. Исользуй команду `remove txt_doctype_region\txt_rus[eng] processed_files.txt`, чтобы удалить
файлы, которые уже встречались раньше

1. Команда `combine txt_doctype_region` объединит все отдельные русские txt-файлы в один документ
**`combined_rus.txt`** и все английские txt-файлы в один документ **`combined_eng.txt`**,
с разделителем `FILE_END` после каждого текста. Кроме того, будет создан файл **`filenames_in_order.txt`**

1. Скопируй строки из файла **`filenames_in_order.txt`** в конец файла **`processed_files.txt**

1. Используешь любой инструмент для alignment-а файлов  **`combined_eng.txt`** и **`combined_rus.txt`**;
при этом  разделители `FILE_END` должны сохраниться

1. Проверяешь и редактируешь результаты alignment-а в tmx-редакторах и TermChecker.
Для TermChecker есть команда `swap` (`swap glossary.txt`) для перемены местами колонок
в глоссарии, чтобы можно было проверить alignment по списку терминов в обе стороны

1. Конвертируешь (в tmx-редакторе) tmx-файл в txt-файл, где на каждой стороке
по сегменту, с разделителем табуляцией

1. Команда `splitf [-w] tab-delimited-file.txt filenames_in_order.txt` запишет
все отдельные тексты из единого файла в отдельные двуязычные документы с названиями из
**`filenames_in_order.txt`**. То есть количество раделителей `FILE_END` и названий файлов
должно совпадать. Без флажка `-w` команда просто проверит, что количество разделителей
и названий файлов совпадает, но записывать файлы не будет

1. Команда `tmxdir dual-txt-files-dir` конвертирует все двуязычные файлы
в формат tmx

1. Команда `tmx-batch-tradosize` попросит выбрать папку с несколькими tmx-файлами,
а результат сохранит в папку `tmx-trados-style`

## Установка

```
git clone https://github.com/AlexSkrn/extract_wb_news.git
python -m venv .venv
.venv\Scripts\activate.bat  # Windows, Anaconda prompt
python -m pip install --upgrade build
python -m build
pip install -e .
```
