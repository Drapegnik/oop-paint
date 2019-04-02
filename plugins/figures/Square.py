from core.figures import Rectangle, Field


class Square(Rectangle):
    default = 100
    default_values = [default]
    fields = [Field('side size', step=10, min_value=10,
                    max_value=400, default=default)]
    help_text = f'set side size and choose center on the drawing area'

    def __init__(self, points, data, _):
        size = data[0]
        Rectangle.__init__(self, points, [size, size], _)
