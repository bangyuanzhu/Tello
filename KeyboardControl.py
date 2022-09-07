from djitellopy import tello
import KeyboardModule as kb
from time import sleep
import cv2

kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())


def getKeyInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 40
    if kb.getKey("LEFT"):
        lr = -speed
    elif kb.getKey("RIGHT"):
        lr = speed

    if kb.getKey("UP"):
        fb = speed
    elif kb.getKey("DOWN"):
        fb = -speed

    if kb.getKey("w"):
        ud = speed
    elif kb.getKey("s"):
        ud = -speed

    if kb.getKey("a"):
        yv = speed
    elif kb.getKey("d"):
        yv = -speed

    if kb.getKey("q"):
        me.land()

    if kb.getKey("e"):
        me.takeoff()

    return [lr, fb, ud, yv]


me.takeoff()

while True:
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

