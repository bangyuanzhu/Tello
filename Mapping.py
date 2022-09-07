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
x, y = 500, 500
a = 0
yaw = 0

kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0, 0), (0, 0)]


def getKeyInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 40
    aspeed = 50
    global x, y, yaw, a
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
        yv = -aspeed
        yaw += aInterval
    elif kb.getKey("d"):
        yv = aspeed
        yaw -= aInterval

    if kb.getKey("q"):
        me.land()

    if kb.getKey("e"):
        me.takeoff()

    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))
    return [lr, fb, ud, yv]


def drawPoints(img, points):
    # Colour code in this case is BGR
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, point, 5, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


while True:
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((500, 500, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append([vals[4], vals[5]])
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
