from enum import Enum

from cairo import Context


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ElbowConnector:
    def __init__(self,
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width=1,
                 orientation=Orientation.HORIZONTAL,
                 elbow_at=0.5):
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.orientation = orientation
        self.elbow_at = elbow_at

    def draw(self, c: Context, start_x: float, start_y: float, end_x: float, end_y: float):
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)

        c.move_to(start_x, start_y)
        if start_x == end_x or start_y == end_y:
            c.line_to(end_x, end_y)

        elif self.orientation == Orientation.HORIZONTAL:
            elbow_x = start_x + ((end_x - start_x) * self.elbow_at)
            c.line_to(elbow_x, start_y)
            c.line_to(elbow_x, end_y)
            c.line_to(end_x, end_y)

        else:
            elbow_y = start_y + ((end_y - start_y) * self.elbow_at)
            c.line_to(start_x, elbow_y)
            c.line_to(end_x, elbow_y)
            c.line_to(end_x, end_y)

        c.stroke()
        c.restore()
