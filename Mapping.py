from djitellopy import tello
import KeyboardModule as kb
from time import sleep
import cv2
import numpy as np
import math

##### PARAMETERS ######
fspeed = 100 / 10  # Self determine speed in cm/s
aspeed = 10  # Angular speed in Rad/s
interval = 0.15
dInterval = fspeed * interval
aInterval = aspeed * interval
x, y = 500, 500
a = 0
b = 0
cirx, ciry = 500, 500
kb.init()
me = tello.Tello()
# me.connect()
# print(me.get_battery())

points = [(0, 0), (0, 0)]


def getKeyInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 20
    aspeed = 20
    global x, y, a, b, cirx, ciry
    d = 0

    if kb.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = b + 3*math.pi / 2
        sleep(0.005)

    if kb.getKey("RIGHT"):
        lr = speed
        d = dInterval
        a = b + math.pi / 2
        sleep(0.005)

    if kb.getKey("UP"):
        fb = speed
        d = dInterval
        sleep(0.005)

    elif kb.getKey("DOWN"):
        fb = speed
        d = dInterval
        a = b + math.pi
        sleep(0.005)

    if kb.getKey("w"):
        ud = speed
    elif kb.getKey("s"):
        ud = -speed

    if kb.getKey("a"):
        dummy = 0
        # Set the drone to turn 45 degrees left
        #tello.rotate_clockwise(me, 45)


    elif kb.getKey("d"):
        dummy = 0
        # Set the drone to turn 45 degrees right
        #tello.rotate_clockwise(me, -45)


    if kb.getKey("q"):
        dummy = 1
        # me.land()

    if kb.getKey("e"):
        dummy = 0
        # me.takeoff()

    x += int(d * math.sin(a))
    y -= int(d * math.cos(a))
    a = b
    return [lr, fb, ud, yv, x, y]


def Circlearrow():
    global cirx, ciry, a, b

    if kb.getKey("a"):
        b -= 2*math.pi/8
        sleep(1)

    elif kb.getKey("d"):
        b += 2*math.pi/8
        sleep(1)

    while 2 * math.pi < b:
        b = b - (2*math.pi)

    while b < -2 * math.pi:
        b = b + (2 * math.pi)


    cirx = x + int(15 * (math.sin(b)))
    ciry = y - int(15 * (math.cos(b)))

    print((a/(2*math.pi))*360, (b/(2*math.pi))*360)
    return cirx, ciry


def drawPoints(img, points):
    # Colour code in this case is BGR
    for point in points:
        cv2.circle(img, point, 2, (0, 0, 255), cv2.FILLED)
    cv2.arrowedLine(img, point, Circlearrow(), (0, 255, 0), 3, 6)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


while True:
    vals = getKeyInput()
    # me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)
    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
