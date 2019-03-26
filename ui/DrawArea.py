from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class DrawArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._init_ui()
        self.show()

    def _init_ui(self):
        self.setToolTip('start drawing by putting a point')
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

    def paintEvent(self, event):
        print('redraw', self.parent.selected_figure)
        qp = QPainter()
        qp.begin(self)
        self._draw_points(qp)
        qp.end()

    def mousePressEvent(self, event):
        print('mouse', event.pos())
        self.parent.points.append(event.pos())
        self.update()
