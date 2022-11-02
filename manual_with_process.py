from djitellopy import tello
import KeyboardModule as kb
import cv2
import cvzone
import time
import threading
from djitellopy import Tello


kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
flying = True

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
        flying = False
        me.land()

    if kb.getKey("e"):
        me.takeoff()

    return [lr, fb, ud, yv]


me.streamon()
me.takeoff()

def task2():
    while flying == True:
        vals = getKeyInput()
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

def task1():
    # Image Processing Thread
    thres = 0.55
    nmsThres = 0.2
    global flying
    # cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)

    classNames = []
    classFile = 'coco.names2'
    with open(classFile, 'rt') as f:
        classNames = f.read().split('\n')
    print(classNames)

    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = "frozen_inference_graph.pb"

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    while flying:
        img = me.get_frame_read().frame
        # success, img = cap.read()
        classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
        try:
            for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cvzone.cornerRect(img, box)

                cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                            (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (0, 255, 0), 2)
        except:
            pass

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    if flying == False:
        return

t1 = threading.Thread(target=task1, name='t1')
t2 = threading.Thread(target=task2, name='t2')


me.streamon()

t1.start()
time.sleep(3)
t2.start()

t1.join()
t2.join()