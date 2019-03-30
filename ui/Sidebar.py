from functools import partial

from PyQt5.QtWidgets import (QComboBox, QFormLayout, QGroupBox, QLabel,
                             QPushButton, QSpinBox, QWidget)

from core.figures import Figure


class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._init_ui()
        self.show()

    def _init_ui(self):
        self.layout = QFormLayout()
        self._add_select()
        self._add_reset()

        self.form = QGroupBox()
        self.figures_list = QGroupBox()
        self.layout.addRow(QLabel(''))

        self._render_fields()
        self._render_figures()
        self.setLayout(self.layout)

    def _add_select(self):
        self.select = QComboBox()
        self.select.addItems(Figure.get_all())
        self.select.activated[str].connect(self._handle_select)
        self.layout.addRow(QLabel('Figure:'), self.select)

    def _add_reset(self):
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.setDefault(True)
        self.reset_btn.clicked.connect(self.parent.reset_data)
        self.layout.addRow(self.reset_btn)

    def _render_fields(self):
        FigureClass = self.parent.get_figure_class()
        fields = FigureClass.get_fields()
        if not fields:
            self.form.hide()
            return

        self.form.hide()
        self.layout.removeWidget(self.form)
        self.form = QGroupBox()
        self.form_layout = QFormLayout()
        self.form.setLayout(self.form_layout)
        self.layout.insertRow(3, self.form)

        self.form.setTitle(f'{FigureClass.__name__} props:')

        for i, field in enumerate(fields):
            input_f = QSpinBox()
            input_f.setRange(field.min_value, field.max_value)
            input_f.setSingleStep(field.step)
            input_f.setValue(field.default)
            input_f.valueChanged.connect(
                partial(self.parent.handle_data_change, i))
            self.form_layout.addRow(QLabel(f'{field.name}:'), input_f)
        self.form.show()

    def _render_figures(self):
        self.figures_list.hide()
        self.layout.removeWidget(self.figures_list)

        if not self.parent.figures:
            return

        self.figures_list = QGroupBox('Figures list:')
        self.figures_layout = QFormLayout()
        self.figures_list.setLayout(self.figures_layout)
        self.layout.addRow(self.figures_list)

        for index, fig in enumerate(self.parent.figures):
            button = QPushButton('x')
            button.setToolTip('Remove')
            button.clicked.connect(
                partial(self.parent.handle_figure_remove, index))
            self.figures_layout.addRow(
                QLabel(f'{index + 1}. {fig.__class__.__name__}'), button)

        self.figures_list.show()

    def _handle_select(self, item):
        self.parent.set_figure(item)
        self._render_fields()

    def update_ui(self):
        self.update()
        self._render_figures()
