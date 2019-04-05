from core.processing import FileProcessor

def _find_original_class():
    that_one_class = [x for x in object.__subclasses__() if x.__name__ == 'ZipPlugin']
    if len(that_one_class) != 1:
        return None

    return that_one_class[0]

class ZipAdapter(FileProcessor):
    ext = '.zip'
    name = 'ZIP'


    @staticmethod
    def convert(data):
        original_zip = _find_original_class()()
        return original_zip.zip(str.encode(data))

    @staticmethod
    def parse(data):
        original_zip = _find_original_class()()
        return original_zip.unzip(data)
