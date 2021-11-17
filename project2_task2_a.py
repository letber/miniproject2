"""module for creating a directory tree
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
    parser.add_argument('dst', type=str,
                        help='destination of directory where to start')

    return parser


def create_alt_tree(directory, count):
    files = os.listdir(directory)
    tree_list = []
    for file in files:
        if os.path.isdir(directory + file):
            tree_list.append((file + '/', count, True))
            tree_list.extend(create_alt_tree(
                directory + file + '/', count + 1))
        else:
            tree_list.append((file, count, False))

    return tree_list


def show_tree(tree_list):
    tree = []
    for file in tree_list:
        line = []
        for i in range(file[1]):
            line.append('  ')
        line.extend(['├── ', file[0]])
        tree.append(line)
    for file in tree:
        try:
            while True:
                file.remove('')
        except ValueError:
            pass

    for i in range(len(tree) - 1):
        stop = False
        count = 1
        while len(tree[i + count]) > len(tree[i]):
            count += 1
            try:
                if len(tree[i + count]) == len(tree[i]):
                    stop = True
                    break
            except IndexError:
                break
        if stop:
            for j in range(i + 1,  i + count):
                tree[j][len(tree[i]) - 2] = '│ '

    for i in range(len(tree) - 1):
        if len(tree[i]) != len(tree[i + 1]):
            try:
                line_copy = tree[i + 1].copy()
                line_copy.reverse()
                ind = len(line_copy) - line_copy.index('│ ') - 1
                if tree[i].index('├── ') != ind:
                    tree[i][tree[i].index('├── ')] = '└── '
            except ValueError:
                tree[i][tree[i].index('├── ')] = '└── '

    tree[-1][tree[-1].index('├── ')] = '└── '
    return tree


if __name__ == '__main__':
    pars = create_parser()
    args = pars.parse_args()
    # with open('tree.txt', 'w', encoding='utf-8') as file:
    #     file.write(args.dst + '\n')
    #     new_tree = []
    #     for line in show_tree(create_alt_tree(args.dst, 0)):
    #         line_str = ''
    #         for item in line:
    #             line_str += item
    #         new_tree.append(line_str + '\n')
    #     file.writelines(new_tree)
    
    print(args.dst)
    for line in show_tree(create_alt_tree(args.dst, 0)):
        line_str = ''
        for item in line:
            line_str += item
        print(line_str)
