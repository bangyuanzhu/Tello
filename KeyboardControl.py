from djitellopy import tello
import KeyboardModule as kb
from threading import Thread
import time
from time import sleep
import cv2

kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
keepRecording = True
me.stream_on()
frame_read = me.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()
# we need to run the recorder in a seperate thread, otherwise blocking options
# would prevent frames from getting added to the video


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
recorder = Thread(target=videoRecorder)
recorder.start()

while True:
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

keepRecording = False
recorder.join()