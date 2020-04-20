#!/usr/bin/env python3

from compute import side1, side2, getThetaS
from points import Point
import pyautogui
from time import sleep
import math

t1 = Point(-1897, 429)
t100 = Point(-816, 429)
dt = (t100-t1)/99
y360 = Point(-816, 108)
dy = (y360-t100)/360
joints = [
    Point(-720, 72),
	Point(-720, 100),
	Point(-720, 128),
	Point(-720, 161),
	Point(-720, 187),
	Point(-720, 218),
	Point(-720, 248)
]
red_angle_joint = joints[0]
green_angle_joint = joints[1]
# blue is number 2, not needed
follower1_joint = joints[3] # done
cam1_joint = joints[4] # done
follower2_joint = joints[5] # done
cam2_joint = joints[6] # done

double_click_interval = 0.1

def clickPos(pt):
    pyautogui.click(pt.x, pt.y)

def click(theta, val):
    steps = 99*theta/(2*math.pi)
    clickPos(t1 + steps*dt + val*dy)

def setValue(lastValue, theta, val):
    click(theta, lastValue)
    pyautogui.typewrite(str(val))

def warm_up_motion():
    # to enforce proper y-axis scaling, must add one point with value 360
    # conveniently, the cams should turn from 0 to 360 degrees over the full timespan
    clickPos(cam1_joint)
    setValue(0, 2*math.pi, 360)
    clickPos(cam2_joint)
    setValue(0, 2*math.pi, 360)

def applyThetaVals(ls):
    last_val = 0
    for theta, val in ls:
        val *= 180/math.pi
        setValue(last_val, theta, val)
        last_val = val

def deploy_motion_study(dry=False):
    if not dry:
        warm_up_motion()
    follower1_vals = []
    follower2_vals = []
    green_angle_vals = []
    red_angle_vals = []
    # must be at most 100 keyframes because fusion limits steps from 1 to 100
    # 50 gives a good spacing
    for (theta, s) in getThetaS(20):
        (r1, cam_angle1, angle1, face_pos1, pos) = side1.info(s)
        (r2, cam_angle2, angle2, face_pos2, pos) = side2.info(s)
        """
            s should range from 0 to 1
            theta guaranteed linear from 0 to 2pi
            angle1 and angle2, the angles of followers, are in a limited angle range
            pos.x, pos.y are the locations on the wall
        """
        follower1_vals.append((theta, math.pi/2 - angle1))
        follower2_vals.append((theta, math.pi/2 - angle2))
        # The coordinate system is not normal cartesian (y is up)
        # And the output is not normal spherical (green is angle from x=y=0 line,
        # red is angle from segment (0,0,1)--(0,y,1))
        x = pos.x
        y = pos.y
        green = math.acos(1/math.sqrt(1+x*x+y*y))
        red = math.pi/2 - math.atan2(y, x)
        green_angle_vals.append((theta, green))
        red_angle_vals.append((theta, red))
    if dry:
        print(follower1_vals, follower2_vals, green_angle_vals, red_angle_vals, sep="\n")
    else:
        clickPos(follower1_joint)
        applyThetaVals(follower1_vals)
        clickPos(follower2_joint)
        applyThetaVals(follower2_vals)
        clickPos(green_angle_joint)
        applyThetaVals(green_angle_vals)
        clickPos(red_angle_joint)
        applyThetaVals(red_angle_vals)

if __name__=="__main__":
    deploy_motion_study(False)
