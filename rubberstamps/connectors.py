import dataclasses
import math
from enum import Enum
from math import cos, pi, sin

from cairo import Context


class ConnectorOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


@dataclasses.dataclass
class ArrowStyle:
    spread: float
    filled: bool
    radius: float


class BaseConnector:
    def draw_arrow(self,
                   c: Context,
                   x: float,
                   y: float,
                   orientation: float,
                   style: ArrowStyle):
        c.save()
        r = style.radius
        angle1 = pi - style.spread
        angle2 = pi + style.spread

        c.move_to(x, y)
        c.line_to(cos(orientation + angle1) * r + x, sin(orientation + angle1) * r + y)
        c.move_to(x, y)
        c.line_to(cos(orientation + angle2) * r + x, sin(orientation + angle2) * r + y)

        if style.filled:
            c.line_to(cos(orientation + angle1) * r + x, sin(orientation + angle1) * r + y)
            c.fill_preserve()

        c.stroke()
        c.restore()


class LineConnector(BaseConnector):
    def __init__(self,
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width=1,
                 dash=None,
                 start_arrow: ArrowStyle | None = None,
                 end_arrow: ArrowStyle | None = None):
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.start_arrow = start_arrow
        self.end_arrow = end_arrow

    def draw(self, c: Context, start_x: float, start_y: float, end_x: float, end_y: float):
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        c.move_to(start_x, start_y)
        c.line_to(end_x, end_y)
        c.stroke()
        if self.start_arrow:
            self.draw_arrow(c, start_x, start_y, math.atan2(start_y - end_y, start_x - end_x), self.start_arrow)
        if self.end_arrow:
            self.draw_arrow(c, end_x, end_y, math.atan2(end_y - start_y, end_x - start_x), self.end_arrow)

        c.restore()


class ElbowConnector(BaseConnector):
    def __init__(self,
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width=1,
                 dash=None,
                 start_arrow: ArrowStyle | None = None,
                 end_arrow: ArrowStyle | None = None,
                 orientation=ConnectorOrientation.HORIZONTAL,
                 elbow_at=0.5):
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.start_arrow = start_arrow
        self.end_arrow = end_arrow
        self.orientation = orientation
        self.elbow_at = elbow_at

    def draw(self, c: Context, start_x: float, start_y: float, end_x: float, end_y: float):
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        c.move_to(start_x, start_y)
        if start_x == end_x or start_y == end_y:
            c.line_to(end_x, end_y)
            c.stroke()
            if self.start_arrow:
                self.draw_arrow(c, start_x, start_y, math.atan2(start_y - end_y, start_x - end_x), self.start_arrow)
            if self.end_arrow:
                self.draw_arrow(c, end_x, end_y, math.atan2(end_y - start_y, end_x - start_x), self.end_arrow)

        elif self.orientation == ConnectorOrientation.HORIZONTAL:
            elbow_x = start_x + ((end_x - start_x) * self.elbow_at)
            c.line_to(elbow_x, start_y)
            c.line_to(elbow_x, end_y)
            c.line_to(end_x, end_y)
            c.stroke()
            if self.start_arrow:
                self.draw_arrow(c, start_x, start_y, math.atan2(0, start_x - end_x), self.start_arrow)
            if self.end_arrow:
                self.draw_arrow(c, end_x, end_y, math.atan2(0, end_x - start_x), self.end_arrow)

        else:
            elbow_y = start_y + ((end_y - start_y) * self.elbow_at)
            c.line_to(start_x, elbow_y)
            c.line_to(end_x, elbow_y)
            c.line_to(end_x, end_y)
            c.stroke()

            if self.start_arrow:
                self.draw_arrow(c, start_x, start_y, math.atan2(start_y - end_x, 0), self.start_arrow)
            if self.end_arrow:
                self.draw_arrow(c, end_x, end_y, math.atan2(end_y - start_y, 0), self.end_arrow)

        c.restore()
