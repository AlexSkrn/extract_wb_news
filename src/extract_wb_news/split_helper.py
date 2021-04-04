import os


def load_filenames(filenames_path):
    filenames = []
    with open(filenames_path, 'r', encoding='utf-8') as in_f:
        for filename in in_f:
            filenames.append(filename.strip())
    return filenames


def parse_multifile(filenames: list, filepath: str, writepath: str):
    filenames = iter(filenames)
    end_marks = 0
    total_line_count = 0  # check if my appoarch is okey
    content = []
    sum_of_lines = 0
    with open(filepath, 'r', encoding='utf-8') as in_f:
        in_f.readline()  # because the 1st line is: en-US	ru-RU
        for line in in_f:
            line = line.strip()
            if line:  # Ignore blank lines
                if line == 'FILE_END\tFILE_END':
                    end_marks += 1
                    # Write current content buffer to file, then empty buffer
                    if writepath:
                        write_file(content, filenames, writepath)
                        print(f'{len(content)} lines read.')
                    sum_of_lines += len(content)
                    content = []
                else:
                    content.append(line)  # add a line to content buffer
                    total_line_count += 1
    # with open(filepath, 'r', encoding='utf-8') as in_f:
    #     for line in in_f:
    #         line = line.strip()
    #         if line:  # Ignore blank lines
    #             if line == 'FILE_START\tFILE_START':
    #
    #                 start_marks += 1
    #                 inside_file = True
    #             elif line == 'FILE_END\tFILE_END':
    #                 end_marks += 1
    #                 # Write current content buffer to file, then empty buffer
    #                 if write:
    #                     write_file(content, filenames)
    #                     print(f'{len(content)} lines read.')
    #                 sum_of_lines += len(content)
    #                 content = []
    #
    #                 inside_file = False
    #             elif inside_file:
    #                 content.append(line)  # add a line to content buffer
    #                 total_line_count += 1
    print(f'Total lines: {total_line_count}')
    print(f'Sum of lines: {sum_of_lines}')
    return (end_marks, total_line_count)


def write_file(content: list, filenames: list, writepath: str):
    filename = next(filenames)
    write_to = os.path.join(writepath, filename)
    with open(write_to, 'w', encoding='utf-8') as to_f:
        for line in content:
            to_f.write(line)
            to_f.write('\n')
