from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLabel, QComboBox, QPushButton
)


class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._init_ui()
        self.show()

    def _init_ui(self):
        layout = QFormLayout()
        self._add_select(layout)
        self._add_reset(layout)
        self.setLayout(layout)

    def _add_select(self, layout):
        self.select = QComboBox()
        self.select.addItems(self.parent.figures_list)
        self.select.activated[str].connect(self.handle_select)
        layout.addRow(QLabel('Figure:'), self.select)

    def _add_reset(self, layout):
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.setDefault(True)
        self.reset_btn.clicked.connect(lambda: self.parent._reset_data())
        layout.addRow(self.reset_btn)

    def handle_select(self, item):
        self.parent.selected_figure = item
        self.parent._reset_data()
