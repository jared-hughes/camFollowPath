#!/usr/bin/env python3

from points import points, pdiff, Point
import math
import numpy as np
from scipy import integrate

class Side:
    def __init__(self, p, f, xy, camxy, z):
        """
        p: perpendicular distance from pivot of side to follower
        f: length of follower (negative if clockwise)
        camx, camy: offsets from pivot of side to center of cam
        x, y, z: offset from pivot of pointer to pivot of side
            * z should measure to the face of the side further from the pointer pivot
              since that is what the pointer touches
        """
        self.p = p
        self.f = f
        self.camxy = camxy
        self.xy = xy
        self.z = z

    def info(self, s):
        """
            returns tuple (radius of cam, angle on cam, angle from vertical, position of pointer along face)
        """
        # (x, y)
        pos = getPoint(s)
        face_pos = pos * (self.z / projection_distance)
        face_pos -= self.xy
        # small angle: assume cross section of pointer is always circle
        # CCW angle from vertical
        angle = face_pos.angle() - math.asin(pointer_radius/face_pos.mag())
        radius = math.sqrt(self.p**2 + self.f**2)
        # CCW angle
        side_angle = math.atan2(self.p, self.f)
        f = Point(0, radius).rotated(angle + side_angle)
        cam_vector = f - self.camxy
        r = cam_vector.mag()
        cam_angle = cam_vector.angle()
        return (r, cam_angle, angle, face_pos)

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

pointer_radius = 8
""" z Distance from pivot of pointer to projection wall, effectively inverse scale factor """
projection_distance = 1000
#            p   f      xy           camxy        z
side1 = Side(20, 10, Point(5, -10), Point(20, -5), 100)
side2 = Side(20, -10, Point(-5, -10), Point(-20, -5), 100)
