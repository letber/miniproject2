import os
import argparse
import re
import zipfile


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
    parser.add_argument('zip_src', type=str,
                        help='path to archive where to search')
    parser.add_argument('zip_dst', type=str,
                        help='path wehere to move file/directory archive')

    return parser


def search_zip(path, pattern):
    good_files = []
    with zipfile.ZipFile(path, 'r') as archive:
        files = archive.namelist()
        for file in files:
            if file[-1] != '/' and file[-4::-1] != '.zip':
                with archive.open(file, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    if re.search(pattern, line.decode('utf-8')):
                        good_files.append(file)
                        break
    
    return good_files


def write_file(path, files_list, dst):
    with zipfile.ZipFile(dst, 'w') as archive:
        with zipfile.ZipFile(path, 'r') as old_archive:
            for file in files_list:
                with old_archive.open(file, 'r') as f:
                    with archive.open(file, 'w') as new_f:
                        new_f.writelines(f.readlines())
    


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()
    if args.zip_src[-4::] == '.zip':
        if os.path.isfile(args.zip_src):
            write_file(args.zip_src, search_zip(args.zip_src, args.find), args.zip_dst)
        else:
            print('Error! source path does not exist or is a directory')
    else:
        print('Error! path to source is not an archive')
