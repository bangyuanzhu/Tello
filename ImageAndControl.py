from djitellopy import tello
import KeyboardModule as kb
from time import sleep
import cv2
import multiprocessing

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
        yv = -speed
    elif kb.getKey("d"):
        yv = speed

    if kb.getKey("q"):
        me.land()

    if kb.getKey("e"):
        me.takeoff()

    return [lr, fb, ud, yv]


me.streamon()
me.takeoff()

while True:
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))  # Resizes the image to 360p x 240p to minimise data processing load
    cv2.imshow("Image", img)
    cv2.waitKey(1)

