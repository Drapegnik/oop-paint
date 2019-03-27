from PyQt5.QtCore import QPoint


def get_line(a, b):
    return [a.y() - b.y(), b.x() - a.x(), a.x()*b.y() - b.x()*a.y()]


def get_y_from_x(line, x):
    return -(line[0]*x + line[2])/line[1]


def get_line_point(line, x):
    return QPoint(x, get_y_from_x(line, x))
