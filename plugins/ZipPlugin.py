from gzip import compress, decompress

class ZipPlugin:
    def zip(self, data: bytes) -> bytes:
        return compress(data)

    def unzip(self, data: bytes) -> bytes:
        return decompress(data)
