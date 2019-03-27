from functools import partial
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLabel, QComboBox, QPushButton, QSpinBox
)

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
        self.layout.addRow(QLabel(''))

        self._render_fields()
        self.setLayout(self.layout)

    def _add_select(self):
        self.select = QComboBox()
        self.select.addItems(Figure.get_all())
        self.select.activated[str].connect(self._handle_select)
        self.layout.addRow(QLabel('Figure:'), self.select)

    def _add_reset(self):
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.setDefault(True)
        self.reset_btn.clicked.connect(lambda: self.parent.reset_data())
        self.layout.addRow(self.reset_btn)

    def _render_fields(self):
        FigureClass = self.parent.get_figure_class()
        fields = FigureClass.get_fields()
        if not len(fields):
            self.form.hide()
            return

        if hasattr(self, 'form'):
            self.form.hide()
            self.layout.removeWidget(self.form)
        self.form = QGroupBox()
        self.form_layout = QFormLayout()
        self.form.setLayout(self.form_layout)
        self.layout.addRow(self.form)

        self.form.setTitle(f'{FigureClass.__name__} props:')

        for i, field in enumerate(fields):
            input = QSpinBox()
            input.setRange(field.min_value, field.max_value)
            input.setSingleStep(field.step)
            input.setValue(field.default)
            input.valueChanged.connect(
                partial(self.parent.handle_data_change, i))
            self.form_layout.addRow(QLabel(f'{field.name}:'), input)
        self.form.show()

    def _handle_select(self, item):
        self.parent.set_figure(item)
        self._render_fields()
