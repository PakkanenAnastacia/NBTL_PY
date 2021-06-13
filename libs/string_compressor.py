import zlib


class StringCompressor:
    """
    This class compresses strings in different formats
    """

    @staticmethod
    def compress(element: str) -> bytes:
        """Compresses a string encoding it as UTF-8"""
        a = element.encode("UTF-8")
        return zlib.compress(a)

    @staticmethod
    def decompress(element: bytes) -> str:
        """Decompresses a UTF-8 string"""
        return zlib.decompress(element).decode("UTF-8")

