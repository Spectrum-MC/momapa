from typing import Optional, Self
from .file import PathFile


class LoggingFile:
    type: str
    file: PathFile
    argument: str

    @staticmethod
    def parse(data: dict) -> Optional[Self]:
        if not data:
            return None

        lf = LoggingFile()

        lf.type = data.get('type')
        lf.argument = data.get('argument')
        lf.file = PathFile.parse(data.get('file'))
        lf.file.path = data.get('file', {}).get('id')

        return lf


class Logging:
    client: LoggingFile

    @staticmethod
    def parse(data: dict) -> Optional[Self]:
        if not data:
            return None

        log = Logging()

        log.client = LoggingFile.parse(data.get('client'))

        return log
