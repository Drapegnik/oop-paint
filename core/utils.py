import os
import sys
from importlib import import_module

from PyQt5.QtCore import QPoint


def get_line(a, b):
    return [a.y() - b.y(), b.x() - a.x(), a.x()*b.y() - b.x()*a.y()]


def get_y_from_x(line, x):
    return -(line[0]*x + line[2])/line[1]


def get_line_point(line, x):
    return QPoint(x, get_y_from_x(line, x))


def load_plugins(path):
    for root, _, files in os.walk(path):
        if '__pycache__' in root:
            continue
        sys.path.append(root)
        for filename in files:
            if not filename.endswith('.py'):
                continue
            plugin = import_module(filename[:-3])
            print(f'> load plugin: {plugin}')

def get_extensions(processors):
    separator = ';; '
    default = ('JSON', '.json')
    items = [default] + [p.get_data() for p in processors]
    return separator.join(list(map(lambda x: f'{x[0]} (*{x[1]})', items)))
