
import os
import json


class PathUtil:

    @classmethod
    def _create_folder(cls, path):
        if os.path.exists(path):
            return
        os.mkdir(path)

    @classmethod
    def create_folder(cls, *args):
        arg_list = list(args)
        path = ''
        for i in range(len(arg_list)):
            path = os.path.join(*arg_list[: i + 1])
            cls._create_folder(path)
        return path

    @staticmethod
    def join_path(base, filename):
        return os.path.join(base, filename)

    @staticmethod
    def check_path(path):
        return os.path.exists(path)
