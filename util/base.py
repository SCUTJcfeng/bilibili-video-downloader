
import os
import time


class ConfigLoader:

    @staticmethod
    def default_config(config_file):
        return {
            'UP_ID_LIST': [],
            'AV_ID_LIST': [],
            'ROOT_PATH': os.path.dirname(config_file.__file__),
        }

    @classmethod
    def load_config(cls):
        import config as config_file
        config = cls.default_config(config_file)
        for key in dir(config_file):
            if key.isupper():
                config[key] = getattr(config_file, key)
        return config


def current_timestamp():
    return int(time.time())


def secure_string(string):
    string = string.replace('！', '!').replace('\\', '-').replace('/', '-')
    string = string.replace('？', '-').replace('<', '-').replace('>', '-')
    string = string.replace('<', '-').replace('|', '1').replace('*', '.')
    string = string.replace(':', '.').replace('"', '\'').strip()
    return string
