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
            if re.search(reg_file, file) != None:
                good_files.append(os.path.join(root, file))

    return good_files


def find_patterns(files_list, pattern):
    pass


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()