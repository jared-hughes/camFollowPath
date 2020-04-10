#!/usr/bin/env python3

import math
from main import side1, side2, getThetaS
from points import Point

# https://medium.com/@francoisromain/smooth-a-svg-path-with-cubic-bezier-curves-e37b49d46c74

def line(a, b):
    diff = b-a
    dx, dy = diff.x, diff.y

    return (
        math.atan2(dy, dx),
        math.sqrt(dx*dx + dy*dy)
    )

def control_point(current, prev, next, reverse=False):
    p = prev if prev else current
    n = next if next else current
    smoothing = 0.2
    line_angle, line_length = line(p, n)
    angle = line_angle + (math.pi if reverse else 0)
    length = line_length * smoothing
    return Point(
        current.x + math.cos(angle) * length,
        current.y + math.sin(angle) * length
    )


def cr(x):
    return round(x, 2)

def bezier_command(point, i, a):
    cp_start = control_point(a[i-1], a[i-2], point)
    cp_end = control_point(point, a[i-1], a[i+1], True)
    return f"C {cr(cp_start.x)},{cr(cp_start.y)} {cr(cp_end.x)},{cr(cp_end.y)} {cr(point.x)},{cr(point.y)}"

def format_path(points):
    points = map(lambda tr: Point(tr[1]*math.cos(tr[0]), tr[1]*math.sin(tr[0])), points)
    points = list(points)
    for i, point in enumerate(points):
        if i == 0:
            s = f"M {cr(point.x)},{cr(point.y)} "
        else:
            s += bezier_command(point, i, [*points, None])
    return s

def format_svg(points):
    max_r = max(r for theta,r in points)
    return (
        f"<svg viewbox='{-max_r} {-max_r} {2*max_r} {2*max_r}'>\n"
        f"  <path d='{format_path(points)}'/>\n"
        f"  <circle cx=0 cy=0 r=10 fill='white'/>\n"
        f"</svg>\n"
    )

def gen_svg(side, filename):
    with open(filename, "w") as f:
        f.write(format_svg([(theta, side.r(s)) for (theta, s) in getThetaS()]))

if __name__=="__main__":
    # html for browser preview
    # svg for import into fusion
    gen_svg(side1, "outputs/cam_u.html")
    gen_svg(side1, "outputs/cam_u.svg")
    gen_svg(side2, "outputs/cam_v.html")
    gen_svg(side2, "outputs/cam_v.svg")
