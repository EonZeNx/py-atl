from enum import Enum

# these may produce expected warnings
from System.IO import FileStream, FileMode


class PyFileMode(Enum):
    CREATE_NEW = 1
    CREATE = 2
    OPEN = 3
    OPEN_OR_CREATE = 4
    TRUNCATE = 5
    APPEND = 6

    def to_cs(self):
        match self:
            case PyFileMode.CREATE_NEW:
                return FileMode.CreateNew
            case PyFileMode.CREATE:
                return FileMode.Create
            case PyFileMode.OPEN:
                return FileMode.Open
            case PyFileMode.OPEN_OR_CREATE:
                return FileMode.OpenOrCreate
            case PyFileMode.TRUNCATE:
                return FileMode.Truncate
            case PyFileMode.APPEND:
                return FileMode.Append
            case _:
                return FileMode.OpenOrCreate


class PyFileStream:
    __slots__ = ("path", "mode", "stream")

    def __init__(self, path: str, file_mode: PyFileMode):
        self.path: str = path
        self.mode: PyFileMode = file_mode
        self.stream: FileStream | None = None

    def __enter__(self):
        self.stream: FileStream = FileStream(self.path, self.mode.to_cs())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream is not None:
            self.stream.Close()
