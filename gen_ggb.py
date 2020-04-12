#!/usr/bin/env python3
from compute import side1, side2, pointer_radius, getThetaS, Point
import numpy as np

def ggb_def(name, value):
    print(indent+name, "=", ("\n "+indent if separate_names else "") + str(value))

def ggb_list(items):
    return "{" + ", ".join(map(str, items)) + "}"

def ggb_list_pos(positions, index):
    return ggb_list([pos[index] for pos in positions])

def ggb_readout(side, n):
    print("Next Side")
    positions = []
    for (theta, s) in getThetaS(n):
        (r, cam_angle, angle, face_pos) = side.info(s)
        positions.append((round(theta, 3), round(r, 3), round(cam_angle, 3), round(angle, 3), face_pos.rounded(3)))

    # print out a single list {{theta}, {r1}, {cam_angle}, {angle}, {face_pos}, p, f, camxy, rp, xy of side pivot}
    ggb_def("l1",
        ggb_list([
            ggb_list_pos(positions, 0),
            ggb_list_pos(positions, 1),
            ggb_list_pos(positions, 2),
            ggb_list_pos(positions, 3),
            ggb_list_pos(positions, 4),
            side.p,
            side.f,
            # still trying to figure out why y must be flipped
            # maybe there is a y-positive pointing down in some equation
            Point(side.camxy.x, -side.camxy.y),
            pointer_radius,
            side.xy
        ])
    )

separate_names = True
indent = "  "

if __name__=="__main__":
    ggb_readout(side1, 50)
    ggb_readout(side2, 50)
