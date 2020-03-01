
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
    def join_path(base, *args):
        return os.path.join(base, *args)

    @staticmethod
    def check_path(path):
        return os.path.exists(path)

    @staticmethod
    def remove(path):
        return os.remove(path)

    @staticmethod
    def rename(tmp_filepath, filepath):
        os.rename(tmp_filepath, filepath)
