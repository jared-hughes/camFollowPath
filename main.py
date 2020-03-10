#!/usr/bin/env python3

from points import points, pdiff
import math
import numpy as np
from scipy import integrate

l_u = 300
x_u = -70
h_u = 280
l_v = 300
x_v = 200
h_v = 280
n = 200

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
# print(sol.t)
pts = np.concatenate(([sol.t], sol.y)).T
for (theta, s) in pts:
    pt = getPoint(s)
    # theta_t, s_t, x_t, y_t, u_t, v_t
    print(theta, s, pt.x, pt.y, u(s), v(s), sep='\t')
