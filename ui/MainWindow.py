from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

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

        # FIXME
        self.figures_list = ['circle', 'rectangle', 'line']
        self.selected_figure = self.figures_list[0]

        self.draw_area = DrawArea(self)
        self._reset_data()
        self.sidebar = Sidebar(self)

        self._init_ui()
        self.show()

    def _init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.sidebar.resize(self.sidebar_width, self.size().height())

        self.draw_area.move(self.sidebar_width, 0)
        self.draw_area.resize(self.size())

        # self.statusBar().showMessage('Status: OK')

    def _reset_data(self):
        self.figures = []
        self.points = []
        self.drawling = False
        self.draw_area.update()
        print('reset')
