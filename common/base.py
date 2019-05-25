# python 3.6

import os


def _create_folder(path):
    if os.path.exists(path):
        return
    os.mkdir(path)


def create_folder(*args):
    arg_list = list(args)
    for i in range(len(arg_list)):
        path = os.path.join(*arg_list[: i + 1])
        _create_folder(path)
    return path


def create_path(base, filename):
    return os.path.join(base, filename)


def check_path(path):
    return os.path.exists(path)
