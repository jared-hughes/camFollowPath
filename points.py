#!/usr/bin/env python3

import math
import numpy as np
import re
import svg.path

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, t):
        return Point(self.x*t, self.y*t)

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return self+other*(-1)

    def __mag__(self):
        return np.sqrt(self.x*self.x + self.y*self.y)

    def mag(self):
        return self.__mag__()

    def __str__(self):
        return f"({self.x}, {self.y})"

    def angle(self):
        return np.arctan2(self.y, self.x)

    def rotated(self, angle):
        """ clockwise angle """
        return Point(
            self.x*np.cos(angle) + self.y*np.sin(angle),
            -self.x*np.sin(angle) + self.y*np.cos(angle)
        )

    def rounded(self, roundoff=0):
        return Point(
            round(self.x, roundoff),
            round(self.y, roundoff)
        )

class Path:
    def __init__(self, svg_path, center, scale):
        self.path = svg_path
        self.center = center
        self.scale = scale

    def getPoint(self, s):
        point_complex = self.path.point(s % 1)
        # flip y value to get positive y pointing up
        out = Point(point_complex.real, -point_complex.imag)
        out -= self.center
        out *= self.scale
        return out

def load_path(file, center, scale=1):
    with open(file) as f:
        text = f.read()
    # not a perfect regex but it's close enough
    path_d = re.search(r"d=[\"']([^\"']+)[\"']", text).group(1)
    path = svg.path.parse_path(path_d)
    return Path(path, center, scale)

def dp(fp):
    s = list(map(float, fp.split("\t")));
    return [s[0], Point(s[1], s[2])]
