from functools import partial

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow

from core.constants import MAX_FIGURES
from core.figures import Figure, LineSegment
from core.serialization import FigureEncoder
from core.processing import FileProcessor
from core.utils import get_extensions
from ui.DrawArea import DrawArea
from ui.Sidebar import Sidebar

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
        self._init_menu()

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

    def _init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(partial(self.handle_file_dialog, 'open'))
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(partial(self.handle_file_dialog, 'save'))
        file_menu.addAction(save_action)

    def handle_file_dialog(self, mode):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog.getOpenFileName if mode == 'open' else QFileDialog.getSaveFileName
        ext_string = get_extensions(FileProcessor.get_all())
        filename, _ = file_dialog(
            self, f'{mode.capitalize()} Figures File', 'dist/example.json', ext_string, options=options)
        if filename:
            handler = self._handle_open if mode == 'open' else self._handle_save
            handler(filename)

    def _handle_open(self, path):
        data = None
        processors = FileProcessor.get_all()
        for p in processors:
            if path.endswith(p.ext):
                print('zip', p.ext)
                with open(path, mode=p.r_fmt) as file:
                    data = p.parse(file.read())
                break
        if not data:
            with open(path, mode='r') as file:
                data = file.read()
        self.figures = FigureEncoder.from_json(data)
        self._update()

    def _handle_save(self, path):
        mode = 'w'
        data = FigureEncoder.to_json(self.figures)
        processors = FileProcessor.get_all()
        for p in processors:
            if path.endswith(p.ext):
                mode = p.fmt
                data = p.convert(data)
                break
        with open(path, mode) as file:
            file.write(data)

    def _update(self):
        self._render_status_bar()
        self.draw_area.update()
        self.sidebar.update_ui()

    def _reset_fields_data(self):
        FigureClass = self.get_figure_class()
        self.data = FigureClass.default_values  # type: List[int]

    ###############################################
    #   Public Methods
    ###############################################

    def reset_data(self):
        # type: List[Figure]
        self.figures = []
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

    def is_figures_limit(self):
        return len(self.figures) >= MAX_FIGURES

    def handle_data_change(self, index, value):
        self.data[index] = value

    def handle_figure_remove(self, index):
        del self.figures[index]
        self.points = []
        self._update()
