from typing import List, Tuple, Type
from dataclasses import dataclass
from PyQt5.QtCore import QPoint, QRect

from core.constants import DrawMethod
from core.utils import get_line, get_line_point


class Figure:
    draw_method = None  # type: DrawMethod
    min_points = None   # type: int
    points = None       # type: List[QPoint]
    help_text = None    # type: string
    draw_area_size = None     # type: List[int]
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        print(f'Called __init_subclass({cls}, {cls.__name__})')

    @classmethod
    def get_all(cls) -> Tuple[Type['Figure']]:
        return tuple(cls._registry.keys())

    @classmethod
    def get_by_name(cls, name: str) -> Type['Figure']:
        return cls._registry[name]

    @classmethod
    def get_help_text(cls):
        return cls.help_text

    @classmethod
    def get_draw_method(cls):
        return cls.draw_method

    @classmethod
    def get_min_points(self):
        return self.min_points

    def get_points(self) -> List[QPoint]:
        return self.points


@dataclass
class LineSegment(Figure):
    draw_method = DrawMethod.POINTS
    min_points = 2
    help_text = f'put {min_points} dots to the drawing area'

    points: List[QPoint]
    draw_area_size: List[int]


class Line(LineSegment):
    def __init__(self, points, draw_area_size):
        self.draw_area_size = draw_area_size
        width, _ = self.draw_area_size
        line = get_line(*points)
        self.points = [
            get_line_point(line, 0),
            get_line_point(line, width)
        ]
