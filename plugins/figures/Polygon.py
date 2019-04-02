from core.constants import DrawMethod
from core.figures import PolyLine


class Polygon(PolyLine):
    draw_method = DrawMethod.POINTS_CLOSED
