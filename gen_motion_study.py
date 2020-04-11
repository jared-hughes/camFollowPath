#!/usr/bin/env python3
from compute import getPoint, side1, side2, pointer_radius, getThetaS
import numpy as np

def geogebra_declaration(name, value):
    print(indent+name, "=", ("\n "+indent if separate_names else "") + str(value))

def geogebra_list(name, positions, index):
    geogebra_declaration(name, "{" + ", ".join([str(pos[index]) for pos in positions]) + "}")

def geogebra_readout(side, n):
    print("Next Side")
    positions = []
    for (theta, s) in getThetaS(n):
        (r, cam_angle, angle, face_pos) = side.info(s)
        positions.append((round(theta, 3), round(r, 3), round(cam_angle, 3), round(angle, 3), face_pos.rounded(3)))

    geogebra_list("theta", positions, 0)
    geogebra_list("r1", positions, 1)
    geogebra_list("cama", positions, 2)
    geogebra_list("a1", positions, 3)
    geogebra_list("f1", positions, 4)
    geogebra_declaration("p", side.p)
    geogebra_declaration("f", side.f)
    geogebra_declaration("camxy", side.camxy)
    geogebra_declaration("rp", pointer_radius)

separate_names = True
indent = "  "

if __name__=="__main__":
    geogebra_readout(side1, 50)
    geogebra_readout(side2, 50)
