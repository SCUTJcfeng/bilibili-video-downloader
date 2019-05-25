# python 3.6

import os


def _create_folder(path):
    if os.path.exists(path):
        return
    os.mkdir(path)


def create_folder(*args):
    for i in range(len(args)):
        _create_folder(os.path.join(args[: i + 1]))
