#!/usr/bin/env python3

from points import points, pdiff, Point
import math
import numpy as np
from scipy import integrate

class Side:
    def __init__(self, l, x, h):
        self.l = l
        self.x = x
        self.h = h

    def r(self, s):
        pos = getPoint(s)
        return pos.y + np.sqrt(self.l**2 - (pos.x-self.x)**2) - self.h


side1 = Side(300, -70, 280)
side2 = Side(300, 200, 280)

def getPoint(s):
    """ Returns closest (x, y) source point at s """
    s %= 1
    i = s/pdiff
    frac = i - int(i)
    return points[int(i)][1] * frac + points[int(i)+1][1] * (1-frac)

def d_ds(f, s):
    d = 0.00001
    return (f(s+d)-f(s))/d

def dmaxy_ds(s):
    return max(d_ds(side1.r, s), d_ds(side2.r, s), 0)

def ds_dtheta(theta):
    # pick carefully
    return 1/(2*math.pi)

# v = [ s ]
def intarg(theta, v):
    s, = v
    # dmaxy = dmaxy_ds(s)
    return [ ds_dtheta(theta) ]

def getThetaS(n=50):
    sol = integrate.solve_ivp(intarg, (0, 2*math.pi), [0], t_eval=np.linspace(0, 2*math.pi, n+1))
    # effectively list of (theta {0..6.28}, s {0..1})
    return np.concatenate(([sol.t], sol.y)).T

def desmos_readout(n):
    for (theta, s) in getThetaS(n):
        pt = getPoint(s)
        print(round(theta, 3), round(s, 3), round(pt.x, 2), round(pt.y, 2), round(side1.r(s), 2), round(side2.r(s), 2), sep='\t')
