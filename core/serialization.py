import json
from json import JSONEncoder
from typing import List

from PyQt5.QtCore import QPoint

from core.figures import Figure


class FigureEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Figure):
            return obj.dict()
        elif isinstance(obj, QPoint):
            return (obj.x(), obj.y())
        else:
            # Let the base class default method raise the TypeError
            return JSONEncoder.default(self, obj)

    @staticmethod
    def _parse_figure(fig):
        FigureClass = Figure.get_by_name(fig['name'])
        return FigureClass.new(fig['points'], fig['data'])

    @classmethod
    def to_json(cls, data: List[Figure]) -> str:
        return json.dumps(data, cls=cls)

    @classmethod
    def from_json(cls, string) -> List[Figure]:
        return list(map(cls._parse_figure, json.loads(string)))
