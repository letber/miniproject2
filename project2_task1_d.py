"""[summary]
    """
import os
import argparse


def create_parser() -> object:
    """returns parser object, with given positional arguements: \
find_string, change_string, file_dest, and optional arguement: \
--inplace

    Returns:
        object: parser object
    """
    parser = argparse.ArgumentParser(description='some description')
    parser.add_argument('src1', type=str,
                        help='destination of first file')
    parser.add_argument('src2', type=str,
                        help='destination of second file')
    parser.add_argument('dst', type=str,
                        help='destination of file where to write')

    return parser


def show_diff(src1: str, src2: str) -> set:
    with open(src1, 'r', encoding='utf-8') as file:
        first_file = set(file.readlines())
    with open(src2, 'r', encoding='utf-8') as file:
        second_file = set(file.readlines())
    diff = first_file ^ second_file

    return diff


def check_and_write(diff: set, dst: str):
    if os.path.isdir(dst):
        print('Error! path leads to a directory')
    elif os.path.isfile(dst):
        print('Error! path leads to an existing file')
    else:
        with open(dst, 'w', encoding='utf-8') as file:
            file.writelines(diff)


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()
    check_and_write(show_diff(args.src1, args.src2), args.dst)
    