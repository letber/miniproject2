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
    parser.add_argument('src', type=str,
                        help='path to file/directory that is to be moved')
    parser.add_argument('dst', type=str,
                        help='path wehere to move file/directory')

    return parser


def create_dir_list(directory, count=0):
    files = os.listdir(directory)
    dir_list = []
    for file in files:
        if os.path.isdir(directory + file):
            dir_list.append((file + '/', count, True))
            dir_list.extend(create_dir_list(
                directory + file + '/', count + 1))
        else:
            dir_list.append((file, count, False))

    return dir_list


def move_file(origin, destination):
    with open(destination, 'w') as dst:
        with open(origin, 'r') as org:
            dst.writelines(org.readlines())
    os.remove(origin)


def move_dir(origin, destination):
    for file in create_dir_list(origin):
        if os.path.isfile(os.path.join(origin, file[0])):
            move_file(os.path.join(
                origin, file[0]), destination + '/' + file[0])
        elif os.path.isdir(os.path.join(origin, file[0])):
            new_dir = destination + file[0].split('/')[0]
            os.mkdir(new_dir)
            move_dir(os.path.join(origin, file[0]), new_dir)
            os.rmdir(os.path.join(origin, file[0]))


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()

    if not os.path.exists(args.src):
        print('Error! file/direcotry src does not exist, wrong path')
    elif os.path.isdir(args.src):
        if not os.path.exists(args.dst):
            os.mkdir(args.dst)
            move_dir(args.src, args.dst)
        if os.path.isfile(args.dst):
            print('Error! trying to move directory onto file')
        if os.path.isdir(args.dst):
            # moving files from directory src to directory dst
            move_dir(args.src, args.dst)

    elif os.path.isfile(args.src):
        if not os.path.exists(args.dst):
            move_file(args.src, args.dst)
        elif os.path.isfile(args.dst):
            move_file(args.src, args.dst)
        elif os.path.isdir(args.dst):
            filename = args.src.split('/')[-1]
            move_file(args.src, args.dst + filename)
