from PyQt5.QtWidgets import QWidget, QMessageBox
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

            if method == DrawMethod.ROUND:
                center = points[0]
                rad_x, rad_y = fig.get_data()
                qp.drawEllipse(center, rad_x, rad_y)
            else:
                # POINTS
                for i in range(len(points) - 1):
                    qp.drawLine(points[i], points[i + 1])
                if method == DrawMethod.POINTS_CLOSED:
                    qp.drawLine(points[0], points[-1])

    def _show_limit_warning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText('You have exceeded figures limit!')
        msg.setInformativeText('Please remove some figures and try again.')
        msg.exec_()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self._draw_points(qp)
        self._draw_figures(qp)
        qp.end()

    def mousePressEvent(self, event):
        if self.parent.is_figures_limit():
            self._show_limit_warning()
            return

        if not self.parent.drawling:
            self.parent.start_draw()

        self.parent.points.append(event.pos())
        self.parent.add_figure()
        self.update()
