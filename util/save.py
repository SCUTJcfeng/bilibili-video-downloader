
import csv
import json
import codecs
from tqdm import tqdm


class SaveTool:
    @staticmethod
    def saveText(data, filename, encoding='utf8'):
        with open(filename, 'w', encoding=encoding) as f:
            f.write(data)

    @staticmethod
    def saveJson(data, filename, encoding='utf8'):
        SaveTool.saveText(json.dumps(data, indent=4, ensure_ascii=False), filename, encoding)

    @staticmethod
    def saveChunk(r, filename):
        assert hasattr(r, '__iter__')
        with tqdm(total=int(r.headers['content-length']), unit='B', unit_scale=True, unit_divisor=1000) as bar:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                    bar.update(len(chunk))

    @staticmethod
    def saveCSV(data, filename, header, encoding='utf8'):
        with open(filename, 'wb') as f:
            f.write(codecs.BOM_UTF8)
        with open(filename, 'a', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
