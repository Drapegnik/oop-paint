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
    _registry = {}
    draw_method = None  # type: DrawMethod
    min_points = None   # type: int
    help_text = ''      # type: string
    fields = []         # type: List[Field]
    default_values = []  # type: List[int]

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
    def get_min_points(cls, _):
        return cls.min_points

    @classmethod
    def get_fields(cls) -> List[Field]:
        return cls.fields

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
        ['x radius', 'y radius'], default_values)))
    help_text = f'set radiuses and choose center on the drawing area'


class Circle(Ellipse):
    default = 100
    default_values = [default]
    fields = [Field('radius', step=10, min_value=0,
                    max_value=300, default=default)]
    help_text = f'set radius and choose center on the drawing area'

    def __init__(self, points, data, _):
        r = data[0]
        Ellipse.__init__(self, points, [r, r], _)


class PolyLine(LineSegment):
    default = 5
    default_values = [default]
    fields = [Field('num of vertex', step=1, min_value=3,
                    max_value=50, default=default)]
    help_text = f'set number of vertex and put them on the drawing area'

    @staticmethod
    def get_min_points(data):
        return data[0]


class Polygon(PolyLine):
    draw_method = DrawMethod.POINTS_CLOSED


class Rectangle(Figure):
    draw_method = DrawMethod.POINTS_CLOSED
    min_points = 1
    default_values = [100, 200]
    fields = list(map(lambda x: Field(x[0], 10, 10, 500, x[1]), zip(
        ['x length', 'y length'], default_values)))
    help_text = f'set sides and choose center on the drawing area'

    def __init__(self, points, data, _):
        center = points[0]
        x_half_len, y_half_len = map(lambda x: x / 2, data)
        self.points = [
            QPoint(center.x() - x_half_len, center.y() - y_half_len),
            QPoint(center.x() + x_half_len, center.y() - y_half_len),
            QPoint(center.x() + x_half_len, center.y() + y_half_len),
            QPoint(center.x() - x_half_len, center.y() + y_half_len)
        ]


class Square(Rectangle):
    default = 100
    default_values = [default]
    help_text = f'set side size and choose center on the drawing area'

    def __init__(self, points, data, _):
        size = data[0]
        Rectangle.__init__(self, points, [size, size], _)
