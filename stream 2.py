import cv2
import cvzone
import pygame
import time
import MappingMod as MM
from threading import Thread
from djitellopy import Tello

me = Tello()
me.connect()

running = True
flying = True
path_dist_cm = []
path_dist_px = []
path_angle = []
path_dir = []
path_wp = []
index = 0

screen = pygame.display.set_mode([720, 720])
screen.fill((255, 255, 255))

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        path_wp.append(pos)
        if index > 0:
            pygame.draw.line(screen, (255, 0, 0), path_wp[index - 1], pos, 2)
        index += 1

pygame.display.update()

# Compute the waypoints (distance and angle).

# Append first pos ref. (dummy)
# path_wp.insert(0, (path_wp[0][0], path_wp[0][1] - 10))

for index in range(len(path_wp)):
    # Skip the first and second index.
    if index > 1:
        dist_cm, dist_px = MM.get_dist_btw_pos(path_wp[index - 1], path_wp[index])
        path_dist_cm.append(dist_cm)
        path_dist_px.append(dist_px)

    # Skip the first and last index.
    if index > 0 and index < (len(path_wp) - 1):
        angle = MM.get_angle_btw_line(path_wp[index - 1], path_wp[index + 1], path_wp[index])
        path_angle.append(angle[0])
        path_dir.append(angle[1])

# Print out the information.

print('path_wp: {}'.format(path_wp))
print('dist_cm: {}'.format(path_dist_cm))
print('dist_px: {}'.format(path_dist_px))
print('dist_angle: {}'.format(path_angle))
print('dist_dir: {}'.format(path_dir))

waypoints = []
for index in range(len(path_dist_cm)):
    waypoints.append({
        "dist_cm": path_dist_cm[index],
        "dist_px": path_dist_px[index],
        "angle_deg": path_angle[index],
        "angle_dir": path_dir[index]
    })

keepRecording = True
frame_read = me.get_frame_read()

thres = 0.55
nmsThres = 0.2

# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

classNames = []
classFile = 'coco.names'
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

print(me.get_battery())
me.streamoff()
me.streamon()


def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


recorder = Thread(target=videoRecorder)
recorder.start()

while flying:

    # success, img = cap.read()
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

    me.takeoff()
    time.sleep(0.5)

    for index in range(len(path_dist_cm)):
        MM.MoveForward(path_dist_cm[index] / 300)
        MM.TurnAngle(path_angle[index] / 25.71, path_dir[index])
    MM.MoveForward(path_dist_cm[index] / 300)
    time.sleep(0.5)
    me.land()
    flying = False

keepRecording = False
recorder.join()
