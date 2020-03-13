#!/usr/bin/env python3

from points import points, pdiff, Point
import math
import numpy as np
from scipy import integrate

l_u = 300
x_u = -70
h_u = 280
l_v = 300
x_v = 200
h_v = 280
n = 50

def u(s):
    """ y1 """
    pos = getPoint(s)
    return pos.y + np.sqrt(l_u**2 - (pos.x-x_u) ** 2) - h_u

def v(s):
    """ y2 """
    pos = getPoint(s)
    return pos.y + np.sqrt(l_v**2 - (pos.x-x_v) ** 2) - h_v

def getPoint(s):
    s %= 1
    i = s/pdiff
    frac = i - int(i)
    return points[int(i)][1] * frac + points[int(i)+1][1] * (1-frac)

def d_ds(f, s):
    d = 0.00001
    return (f(s+d)-f(s))/d

def dmaxy_ds(s):
    return max(d_ds(u, s), d_ds(v, s), 0)

def ds_dtheta(theta):
    # pick carefully
    return 1/(2*math.pi)

# v = [ s ]
def intarg(theta, v):
    s, = v
    # dmaxy = dmaxy_ds(s)
    return [ ds_dtheta(theta) ]

sol = integrate.solve_ivp(intarg, (0, 2*math.pi), [0], t_eval=np.linspace(0, 2*math.pi, n+1))
pts = np.concatenate(([sol.t], sol.y)).T

def desmos_readout():
    for (theta, s) in pts:
        pt = getPoint(s)
        print(theta, s, pt.x, pt.y, u(s), v(s), sep='\t')

def cr(x):
    return round(x, 2)

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

def gen_svg(r_func, filename):
    with open(filename, "w") as f:
        f.write(format_svg([(theta, r_func(s)) for (theta, s) in pts]))

gen_svg(u, "cam_u.html")
gen_svg(u, "cam_u.svg")
gen_svg(v, "cam_v.html")
gen_svg(v, "cam_v.svg")
