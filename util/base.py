
import os
import time
from .file import PathUtil


class ConfigLoader:

    @staticmethod
    def default_config(config_file):
        return {
            'UP_ID_LIST': [],
            'AV_ID_LIST': [],
            'SESSDATA': '',
            'ROOT_FOLDER': 'av',
            'ROOT_PATH': os.path.dirname(config_file.__file__),
            'DOWNLOAD_PATH': '',
        }

    @classmethod
    def load_config(cls):
        import config as config_file
        config = cls.default_config(config_file)
        for key in dir(config_file):
            if key.isupper():
                config[key] = getattr(config_file, key)
        cls.after_config(config)
        return config

    @classmethod
    def after_config(cls, config):
        config['DOWNLOAD_PATH'] = PathUtil.join_path(config['ROOT_PATH'], config['ROOT_FOLDER'])
        PathUtil.create_folder(config['ROOT_PATH'], config['ROOT_FOLDER'])


def current_timestamp():
    return int(time.time())


def secure_string(string):
    string = string.replace('！', '!').replace('\\', '-').replace('/', '-')
    string = string.replace('？', '-').replace('<', '-').replace('>', '-')
    string = string.replace('<', '-').replace('|', '1').replace('*', '.')
    string = string.replace(':', '.').replace('"', '\'').strip()
    return string


# 全局 config 对象
CONFIG = ConfigLoader.load_config()
