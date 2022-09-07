from djitellopy import tello
import KeyboardModule as kb
from time import sleep
import cv2
import numpy as np
import math

##### PARAMETERS ######
fspeed = 117 / 10  # Self determine speed in cm/s - 15cm/s
aspeed = 360 / 10  # Angular speed in Degrees/s
interval = 0.25

dInterval = fspeed * interval
aInterval = aspeed * interval
x, y = 250, 250
a = 0

kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = []

def getKeyInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 40
    yaw = 0
    d = 0
    if kb.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kb.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kb.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kb.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kb.getKey("w"):
        ud = speed
    elif kb.getKey("s"):
        ud = -speed

    if kb.getKey("a"):
        yv = speed
        yaw += aInterval
    elif kb.getKey("d"):
        yv = -speed
        yaw -= aInterval

    if kb.getKey("q"):
        me.land()

    if kb.getKey("e"):
        me.takeoff()
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))
    return [lr, fb, ud, yv]


def drawPoints(img, points):
    # Colour code in this case is BGR
    cv2.circle(img, (points[0], points[1]), 5, (0, 0, 255), cv2.FILLED)


while True:
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((500, 500, 3), np.uint8)
    points = (vals[4], vals[5])
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
