#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MainWindow
from core.constants import PLUGINS_DIR
from core.utils import load_plugins

def run():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    load_plugins(PLUGINS_DIR)
    run()

