from math import sin, pi, cos, sqrt
from typing import List

from cairo import Context


class Grid:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width: float = 1,
                 dash: List[float] | None = None,
                 spacing: float = 20):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.spacing = spacing

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size

        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        cur_x = x
        while cur_x < x + width:
            c.move_to(cur_x, y)
            c.line_to(cur_x, y + height)
            cur_x += self.spacing

        cur_y = y
        while cur_y < x + height:
            c.move_to(x, cur_y)
            c.line_to(x + width, cur_y)
            cur_y += self.spacing

        c.stroke()
        c.restore()


class Lines:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width: float = 1,
                 dash: List[float] | None = None,
                 spacing: float = 20):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.spacing = spacing

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        cur_y = y
        while cur_y < y + height:
            c.move_to(x, cur_y)
            c.line_to(x + width, cur_y)
            cur_y += self.spacing
        c.stroke()
        c.restore()


class HexagonalGrid:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width=1,
                 dash: List[float] | None = None,
                 radius=100):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.radius = radius

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        line_length = (cos(pi*1/3) * (self.radius / 2)) - (cos(pi * 2 / 3) * (self.radius / 2))
        horizontal_spacing = self.radius + line_length
        vertical_spacing = sin(pi*2/3) * self.radius

        angles = [(5 / 3) * pi, 0, (1 / 3) * pi, (2 / 3) * pi, pi, (4 / 3) * pi]

        cur_y = y
        while cur_y < y + height + vertical_spacing:
            cur_x = x
            while cur_x < x + width + horizontal_spacing:
                origin = (cur_x, cur_y)
                points = [
                    (cos(a) * (self.radius / 2) + origin[0], sin(a) * (self.radius / 2) + origin[1])
                    for a in angles
                ]
                c.move_to(*points[0])
                for p in points[1:]:
                    c.line_to(*p)

                c.move_to(*points[1])
                c.line_to(points[1][0] + line_length, points[1][1])
                cur_x += horizontal_spacing
            cur_y += vertical_spacing
        c.stroke()
        c.restore()


class CartesianCoordinates:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width: float = 1,
                 dash: List[float] | None = None):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size
        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        c.move_to(x, height/2 + y)
        c.line_to(width + x, height/2 + y)

        c.move_to(width/2 + x, y)
        c.line_to(width/2 + x, y + height)
        c.stroke()
        c.restore()


class PolarCoordinates:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width: float = 1,
                 spacing: float = 20,
                 dash: List[float] | None = None,
                 overflow: bool = False):
        self.position = position
        self.size = size
        self.cartesian = CartesianCoordinates(
            position=posiition,
            size=size,
            color_rgba=color_rgba,
            line_width=line_width,
            dash=dash)
        self.bullseye = Bullseye(
            position=posiition,
            size=size,
            color_rgba=color_rgba,
            line_width=line_width,
            dash=dash,
            spacing=spacing,
            overflow=overflow)

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size
        self.cartesian.draw(c)
        self.bullseye.draw(c)


class Bullseye:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 line_width: float = 1,
                 dash: List[float] | None = None,
                 spacing: float = 20,
                 overflow: bool = False):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.line_width = line_width
        self.dash = dash or []
        self.spacing = spacing
        self.overflow = overflow

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size

        c.save()
        center = (width / 2 + x, height / 2 + y)

        if self.overflow:
            max_radius = sqrt((width/2)**2 + (height/2)**2)
        else:
            max_radius = min(height / 2, width / 2)

        c.set_source_rgba(*self.color_rgba)
        c.set_line_width(self.line_width)
        c.set_dash(self.dash)

        radius = self.spacing
        while radius <= max_radius:
            c.new_sub_path()
            c.arc(*center, radius, 0, 2 * pi)
            radius += self.spacing

        c.stroke()
        c.restore()


class Dots:
    def __init__(self,
                 position: (float, float),
                 size: (float, float),
                 color_rgba=(0.5, 0.5, 0.5, 0.5),
                 dot_size: float = 1,
                 spacing: float = 20):
        self.position = position
        self.size = size
        self.color_rgba = color_rgba
        self.dot_size = dot_size
        self.spacing = spacing

    def draw(self, c: Context):
        x, y = self.position
        width, height = self.size

        c.save()
        c.set_source_rgba(*self.color_rgba)
        c.set_dash([self.dot_size, self.spacing - self.dot_size])
        c.set_line_width(self.dot_size)

        cur_y = y + (self.dot_size / 2)
        while cur_y < y + height:
            c.move_to(x, cur_y)
            c.line_to(x + width, cur_y)
            cur_y += self.spacing
        c.stroke()
        c.restore()
