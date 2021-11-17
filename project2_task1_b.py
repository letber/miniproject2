"""Module made for searching and replacing substrings in a given file.
To work properly you should execute program like in the example below:
python3 project2_task1_b.py {find_string} {change_string} {file_dest} ,
Where:
    find_string - substring that we want to change
    change_string - substring that we want find_string to be changed on
    file_dest - path to a file with content.
You can also add optional arguement --inplace, If you do, the program will
overwrite given file, if not the output will be shown in console.
    """
import argparse


def create_parser() -> object:
    """returns parser object, with given positional arguements: \
find_string, change_string, file_dest, and optional arguement: \
--inplace

    Returns:
        object: parser object
    """
    parser = argparse.ArgumentParser(description='parser to find and change \
substrings')
    parser.add_argument('find_string', type=str,
                        help='substring to find and change')
    parser.add_argument('change_string', type=str,
                        help='substring which needs to be change onto')
    parser.add_argument('file_dest', type=str,
                        help='original file destination')
    parser.add_argument('--inplace', help='if given - then change original file, \
if not - print output in console', action='store_true')

    return parser


def read_file(filename: str) -> list:
    """Reads contents of file with given destination to file. \
Returns a list with lines of the file.

    Args:
        filename (str): destination to file

    Returns:
        list: list with file contents
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines_list = []
        for line in lines:
            lines_list.append(line)

    return lines_list


def search_and_change(old_list: list, search_str: str, new_str: str) -> list:
    """Changes each inclusion of search_str onto new_str \
in given old_list and returns it as new_list

    Args:
        old_list (list): list with strings
        search_str (str): substring that is changed
        new_str (str): substring onto which we change

    Returns:
        list: list with changed substring inclusions
    """
    new_list = []
    for line in old_list[:-1]:
        new_list += line.replace(search_str, new_str)
    new_list += old_list[-1].replace(search_str, new_str)

    return new_list


def show_output(lines: list, overwrite: bool, filename: str) -> None:
    """Shows output in console, or overwrites file depending on \
output_type

    Args:
        lines (list): contents that we want to show/write
        overwrite (bool): if True - overwrite given file \
if False - print in console
        filename (str): destination to a file, where to overwrite

    Returns:
        None
    """
    if overwrite:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line)
    else:
        for line in lines:
            print(line, end='')


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()
    new_file_lines = search_and_change(
        read_file(args.file_dest), args.find_string, args.change_string)
    show_output(new_file_lines, args.inplace, args.file_dest)
