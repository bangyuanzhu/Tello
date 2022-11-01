import cv2
from djitellopy import tello
import cvzone
import KeyboardModule as kb
from time import sleep
import math

thres = 0.55
nmsThres = 0.2
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
past_points = [(0, 0)]
counter = 0
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

#kb.init()
me = tello.Tello()


me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()


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

    #if kb.getKey("e"):
        #me.takeoff()

    return [lr, fb, ud, yv]


while True:
    # success, img = cap.read()
    #vals = getKeyInput()
    #me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cvzone.cornerRect(img, box)

            cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                        (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 0), 2)


            x = box[0] + box[2]/2
            y = box[1] + box[3]/2
            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), cv2.FILLED)
            permdist = math.sqrt((x - past_points[-1][0]) + (y - past_points[-1][1]))
            print(past_points[-1][0], past_points[-1][1])
            sleep(0.05)

            if permdist > 1:
                counter += 1
            print("count of objects is ", counter)
            print("travel distance", permdist)
            past_points.append((x, y))

    except:
        pass
    cv2.imshow("Image", img)
    cv2.waitKey(1)
