from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from core.figures import Figure
from core.constants import DrawMethod


class DrawArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._init_ui()
        self.show()

    def _init_ui(self):
        self.setToolTip('start drawing by putting a dot')
        self._set_bg()

    def _set_bg(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

    def _draw_points(self, qp):
        pen = QPen(Qt.red)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidth(5)
        qp.setPen(pen)

        for point in self.parent.points:
            qp.drawPoint(point)

    def _draw_figures(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for fig in self.parent.figures:
            method = fig.__class__.get_draw_method()
            points = fig.get_points()
            if method == DrawMethod.POINTS:
                for i in range(len(points) - 1):
                    qp.drawLine(points[i], points[i + 1])

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self._draw_points(qp)
        self._draw_figures(qp)
        qp.end()

    def mousePressEvent(self, event):
        if not self.parent.drawling:
            self.parent.points = []
            self.update()
            self.parent.drawling = True

        self.parent.points.append(event.pos())
        FigureClass = Figure.get_by_name(self.parent.selected_figure)

        if (len(self.parent.points) >= FigureClass.get_min_points()):
            self.parent._add_figure()
            self.parent.drawling = False
            self.update()
