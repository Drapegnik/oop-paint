from typing import List, Tuple, Type
from dataclasses import dataclass
from PyQt5.QtCore import QPoint, QRect

from core.constants import DrawMethod
from core.utils import get_line, get_line_point


@dataclass
class Field:
    name: str
    step: int = 1
    min_value: int = 0
    max_value: int = None
    default: int = None


@dataclass
class Figure:
    draw_method = None  # type: DrawMethod
    min_points = None   # type: int
    help_text = ''      # type: string
    fields = []         # type: List[Field]
    default_values = []  # type: List[int]
    _registry = {}

    points: List[QPoint]
    data: List
    draw_area_size: List[int]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        print(f'> register {cls.__name__}')

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

    @classmethod
    def get_fields(self) -> List[Field]:
        return self.fields

    def get_points(self) -> List[QPoint]:
        return self.points

    def get_data(self):
        return self.data


class LineSegment(Figure):
    draw_method = DrawMethod.POINTS_OPEN
    min_points = 2
    help_text = f'put {min_points} dots to the drawing area'


class Line(LineSegment):
    def __init__(self, points, _, draw_area_size):
        width, _ = draw_area_size
        line = get_line(*points)
        self.points = [
            get_line_point(line, 0),
            get_line_point(line, width)
        ]


class Ellipse(Figure):
    draw_method = DrawMethod.ROUND
    min_points = 1
    default_values = [100, 200]
    fields = list(map(lambda x: Field(x[0], 10, 0, 300, x[1]), zip(
        ['radx', 'rady'], default_values)))
    help_text = f'set radx, rady and choose center on the drawing area'


class Circle(Ellipse):
    default_values = [100]
    fields = [Field('radius', 10, 0, 300, 100)]
    help_text = f'set radius and choose center on the drawing area'

    def __init__(self, points, data, _):
        r = data[0]
        Ellipse.__init__(self, points, [r, r], _)
