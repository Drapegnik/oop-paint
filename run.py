#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from gui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
