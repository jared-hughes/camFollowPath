#!/usr/bin/env python3

from points import load_path, Point
import math
import numpy as np
from scipy import integrate

class Side:
    def __init__(self, p, f, xy, camxy, z, is_flipped):
        """
        p: perpendicular distance from pivot of side to follower
        f: length of follower
        camx, camy: offsets from pivot of side to center of cam
        x, y, z: offset from pivot of pointer to pivot of side
            * z should measure to the face of the side further from the pointer pivot
              since that is what the pointer touches
        is_flipped: True if the cam is left of side pivot and side is left of pointer
        """
        self.p = p
        # f should be negative if counterclockwise
        self.f = abs(f) * (-1 if is_flipped else 1)
        self.camxy = camxy
        self.xy = xy
        self.z = z
        self.is_flipped = is_flipped

    def info(self, s):
        """
        returns tuple (radius of cam, angle on cam, angle from horizontal,
            position of pointer along face, position of pointer on z=1 "wall")
        """
        # (x, y)
        pos_norm = path.getPoint(s) / projection_distance
        face_pos_abs = pos_norm * self.z
        face_pos = face_pos_abs - self.xy
        # small angle: assume cross section of pointer is always circle
        # CCW angle from vertical
        angle = face_pos.angle() - \
            (-1 if self.is_flipped else 1) * math.asin(pointer_radius/face_pos.mag())
        radius = math.sqrt(self.p**2 + self.f**2)
        # CCW angle
        side_angle = math.atan2(self.p, self.f)
        f = Point(0, radius).rotated(angle + side_angle)
        cam_vector = f - self.camxy
        r = cam_vector.mag()
        cam_angle = cam_vector.angle()
        return (r, cam_angle, angle, face_pos_abs, pos_norm)

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

pointer_radius = 25
""" z Distance from pivot of pointer to projection wall; effectively inverse scale factor """
projection_distance = 1000
#            p   f      xy           camxy        z
side1 = Side(80, 60, Point(5, -200), Point(170, -20), 100, False)
side2 = Side(80, 60, Point(-5, -200), Point(-170, -20), 100, True)
path = load_path("inputs/heart.svg", Point(64, 64), 6)
