import cv2
from djitellopy import tello
import cvzone
import KeyboardModule as kb
from time import sleep

thres = 0.55
nmsThres = 0.2
 #cap = cv2.VideoCapture(0)
 #cap.set(3, 640)
 #cap.set(4, 480)

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
print(classNames)

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = "saved_model.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

kb.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()

#me.takeoff()
#me.move_up(80)

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


while True:
    #success, img = cap.read()
    vals = getKeyInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
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
