import os
import argparse
import re


def create_parser() -> object:
    """returns parser object, with given positional arguements: \
find_string, change_string, file_dest, and optional arguement: \
--inplace

    Returns:
        object: parser object
    """
    parser = argparse.ArgumentParser(description='some description')
    parser.add_argument('find', type=str,
                        help='regular expression to find in files')
    parser.add_argument('filename', type=str,
                        help='regular expression of filenames where to search')
    parser.add_argument('--show_lines', action='store_true',
                        help='if given show only line number and content')
    parser.add_argument('--only_show_counts', action='store_true',
                        help='if given show only number of matches')

    return parser


def find_files(reg_file):
    good_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if re.search(reg_file, file):
                good_files.append(os.path.join(root, file))

    return good_files


def find_patterns(files_list, pattern):
    good_list = []
    for file in files_list:
        with open(file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if re.search(pattern, line):
                good_list.append([file, line, lines.index(line) + 1])

    return good_list


def show_files(f_list, show_lines, show_counts):
    show_list = dict()
    names = []
    for name in f_list:
        names.append(name[0])
    if show_counts:
        for file in names:
            if file in show_list:
                value = show_list[file]
                show_list[file] = [value[0] + 1]
            else:
                show_list[file] = [1]

        return show_list

    if show_lines:
        for file in f_list:
            if file[0] in show_list:
                value = show_list[file[0]]
                value.append(str(file[2]) + ' ' + file[1])
                show_list[file[0]] = value
            else:
                show_list[file[0]] = [str(file[2]) + ' ' + file[1]]

        return show_list

    for file in f_list:
        if file[0] in show_list:
            value = show_list[file[0]]
            value.append(file[1])
            show_list[file[0]] = value
        else:
            show_list[file[0]] = [file[1]]

    return show_list


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()

    lines = show_files(find_patterns(find_files(args.filename),
                                     args.find), args.show_lines, args.only_show_counts)
    for line in lines:
        print(line)
        for sub_line in lines[line]:
            if not isinstance(sub_line, int):
                print(sub_line.rstrip('\n'))
            else:
                print(sub_line)
        print()
