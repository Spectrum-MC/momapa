from typing import Optional, Self


class File:
    url: str = None
    size: int = None
    hash: str = None

    @staticmethod
    def parse(file: Optional[dict]) -> Self:
        if not file:
            return None

        f = File()

        f.url = file.get('url')
        f.size = file.get('size')
        f.hash = file.get('sha1')

        return f


class PathFile(File):
    path: str = None

    @staticmethod
    def parse(file: Optional[dict]) -> Self:
        if not file:
            return None

        f = PathFile()

        f.url = file.get('url')
        f.size = file.get('size')
        f.hash = file.get('sha1')
        f.path = file.get('path')

        return f
