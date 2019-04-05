from abc import ABC, abstractmethod
from typing import Tuple, Type


class FileProcessor(ABC):
    _registry = {}
    fmt = 'wb'
    r_fmt = 'rb'
    ext = None
    name = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        print(f'> [FileProcessor]: register {cls.__name__}')

    @classmethod
    def get_data(cls) -> Tuple[str]:
        return (cls.name, cls.ext)

    @classmethod
    def get_all(cls) -> Tuple[Type['FileProcessor']]:
        return tuple(cls._registry.values())

    @staticmethod
    @abstractmethod
    def convert(data: str) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def parse(data: bytes) -> str:
        pass
