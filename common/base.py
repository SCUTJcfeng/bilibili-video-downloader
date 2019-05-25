# python 3.6

import os


def _create_folder(path):
    if os.path.exists(path):
        return
    os.mkdir(path)


def create_folder(*args):
    arg_list = list(args)
    for i in range(len(arg_list)):
        _create_folder(os.path.join(*arg_list[: i + 1]))
