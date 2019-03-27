from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint

from core.figures import Figure, LineSegment, Line
from ui.Sidebar import Sidebar
from ui.DrawArea import DrawArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'OOP Paint'
        self.left = 150
        self.top = 75
        self.width = 1200
        self.height = 800
        self.sidebar_width = 200
        self.status_bar_height = 25
        self.draw_area_size = [self.width,
                               self.height - self.status_bar_height]

        self.figures_list = Figure.get_all()
        self.selected_figure = self.figures_list[0]

        self._reset_data()
        self.draw_area = DrawArea(self)
        self.sidebar = Sidebar(self)
        self._render_status_bar()

        self._init_ui()
        self.show()

    def _init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.sidebar.resize(self.sidebar_width, self.size().height())

        self.draw_area.move(self.sidebar_width, 0)
        self.draw_area.resize(*self.draw_area_size)
        self._render_status_bar()

    def _render_status_bar(self):
        message = Figure.get_by_name(self.selected_figure).get_help_text()
        self.statusBar().showMessage(f'{self.selected_figure}: {message}')

    def _update(self):
        self._render_status_bar()
        self.draw_area.update()

    def _reset_data(self):
        self.figures = []   # type: List[Figure]
        self.points = []    # type: List[QPoint]
        self.drawling = False
        if hasattr(self, 'draw_area'):
            self.draw_area.update()

    def _add_figure(self):
        FigureClass = Figure.get_by_name(self.selected_figure)
        self.figures.append(FigureClass(self.points, self.draw_area_size))
