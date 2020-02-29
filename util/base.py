
import os
import time
from .file import PathUtil


class ConfigLoader:

    @staticmethod
    def default_config(root_path):
        return {
            'AUTO_MERGE': True,
            'FFMPEG_PATH': 'ffmpeg',
            'UP_ID': None,
            'KEYWORD': None,
            'ORDER': 'pubdate',
            'AV_ID_LIST': [],
            'SESSION_DATA': '',
            'ROOT_FOLDER': 'av',
            'ROOT_PATH': os.path.dirname(root_path),
            'DOWNLOAD_PATH': '',
        }

    @classmethod
    def load_config(cls):
        import config as config_prod
        config = cls.default_config(config_prod.__file__)

        def load_custom_config(file_):
            for key in dir(file_):
                if key.isupper():
                    config[key] = getattr(file_, key)
        load_custom_config(config_prod)
        try:
            import config_local
            load_custom_config(config_local)
        except ImportError:
            pass
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
