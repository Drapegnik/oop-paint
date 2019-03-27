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
        self.draw_area_size = [
            self.width, self.height - self.status_bar_height
        ]

        self._selected_figure = Figure.get_all()[0]

        self.reset_data()
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
        message = self.get_figure_class().get_help_text()
        self.statusBar().showMessage(f'{self._selected_figure}: {message}')

    def _update(self):
        self._render_status_bar()
        self.draw_area.update()
        self.sidebar._update()

    def _reset_fields_data(self):
        FigureClass = self.get_figure_class()
        self.data = FigureClass.default_values  # type: List[int]

    ###############################################
    #   Public Methods
    ###############################################

    def reset_data(self):
        self.figures = []   # type: List[Figure]
        self.points = []    # type: List[QPoint]
        self._reset_fields_data()

        self.drawling = False
        if hasattr(self, 'draw_area'):
            self.draw_area.update()
            self.sidebar._update()

    def set_figure(self, figure):
        self._selected_figure = figure
        self._reset_fields_data()
        self._update()

    def get_figure_class(self):
        return Figure.get_by_name(self._selected_figure)

    def start_draw(self):
        self.points = []
        self.drawling = True
        self._update()

    def add_figure(self):
        FigureClass = self.get_figure_class()
        data_copy = self.data[:]

        if (len(self.points) < FigureClass.get_min_points(data_copy)):
            return
        self.figures.append(
            FigureClass(self.points, data_copy, self.draw_area_size))
        self.drawling = False
        self._update()

    def handle_data_change(self, index, value):
        self.data[index] = value
