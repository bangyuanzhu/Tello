import cv2
import cvzone
import pygame
import time
import math
import numpy as np
import threading
from djitellopy import Tello

# General Variables
me = Tello()
#me.connect()
pygame.init()

running = True
flying = True


# Waypoint Mapping Variables
path_dist_cm = []
path_dist_px = []
path_angle = []
path_dir = []
path_wp = []
index = 0


# Image Processing Variables
screen = pygame.display.set_mode([720, 720])
screen.fill((255, 255, 255))
MAP_SIZE_COEFF = 5.14


# Environment Mapping Variables
points = [(0, 0), (0, 0)]
spoints = [(0, 0)]
x, y = 500, 500
cirx, ciry = 500, 500
a = 0
b = 0

"""""                      ~~~~~~~~~~~          Waypoint Mapping Functions            ~~~~~~~~~~~~~              """""

def get_dist_btw_pos(pos0, pos1):
    """
    Get distance between 2 mouse position.
    """
    x = abs(pos0[0] - pos1[0])
    y = abs(pos0[1] - pos1[1])
    dist_px = math.hypot(x, y)
    dist_cm = dist_px * MAP_SIZE_COEFF
    return int(dist_cm), int(dist_px)


def get_angle_btw_line(pos0, pos1, posref):
    """
    Get angle between two lines respective to 'posref'
    NOTE: using dot product calculation.
    """
    ax = posref[0] - pos0[0]
    ay = posref[1] - pos0[1]
    bx = posref[0] - pos1[0]
    by = posref[1] - pos1[1]
    RIGHT = True

    # Get dot product of pos0 and pos1.
    _dot = (ax * bx) + (ay * by)
    # Get magnitude of pos0 and pos1.
    _magA = math.sqrt(ax ** 2 + ay ** 2)
    _magB = math.sqrt(bx ** 2 + by ** 2)
    _rad = math.acos(_dot / (_magA * _magB))
    # Angle in degrees.
    crossdir = - ax * by + ay * bx

    if crossdir > 0:
        angle = 180 - (_rad * 180) / math.pi
        RIGHT = True

    elif crossdir < 0:
        angle = 180 - (_rad * 180) / math.pi
        RIGHT = False

    return [int(angle), RIGHT]


def MoveForward(interval):
    global cirx, ciry, a, x, y, b
    print(interval)
    counter = 0
    while counter != 1:
        # me.send_rc_control(0, 50, 0, 0)
        print(counter)
        counter += 1/interval*100

    time.sleep(interval)


def TurnAngle(interval, directionRIGHT):
    # angular speed at 100 is 64.25 degrees/s
    global cirx, ciry, a, x, y, b
    if directionRIGHT == True:
        #me.send_rc_control(0, 0, 0, 40)
        print("Right")
        time.sleep(0.0001)

    elif directionRIGHT == False:
        #me.send_rc_control(0, 0, 0, -40)
        print("Left")
        time.sleep(0.0001)

    time.sleep(interval)


"""""            ~~~~~~~~~~~~~~~~~~~~~~~     Environment Mapping Functions     ~~~~~~~~~~~~~~~~~~~~~~~         """""
def Circlearrow():
    # Variables referenced from MoveForward and TurnAngle
    global cirx, ciry, a, x, y, b

    while 2 * math.pi < b:
        b = b - (2*math.pi)

    while b < -2 * math.pi:
        b = b + (2 * math.pi)

    cirx = x + math.floor(15 * (math.sin(b)))
    ciry = y - math.floor(15 * (math.cos(b)))

    return cirx, ciry

def drawPoints(imgg, points):
    # Colour code in this case is BGR

    # Draws red dot at current location
    for point in points:
        cv2.circle(imgg, point, 2, (0, 0, 255), cv2.FILLED)

    # Locates point for end of pointing arrow
    cv2.arrowedLine(imgg, point, Circlearrow(), (0, 255, 0), 3, 1)

    # Annotates the current xy coordinates
    cv2.putText(imgg, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)



"""              ~~~~~~~~~~~~~~~~~~~~~~~~~~     Waypoint Mapping Setup   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~              """


class Background(pygame.sprite.Sprite):
    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# Draws points on waypoint window when mouse button is pressed
while running:
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
for index in range(len(path_wp)):
    # Skip the first and second index.
    if index > 1:
        dist_cm, dist_px = get_dist_btw_pos(path_wp[index - 1], path_wp[index])
        path_dist_cm.append(dist_cm)
        path_dist_px.append(dist_px)

    # Skip the first and last index.
    if index > 0 and index < (len(path_wp) - 1):
        angle = get_angle_btw_line(path_wp[index - 1], path_wp[index + 1], path_wp[index])
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

"""""                        ---------------- Runtime Code Section -----------------                           """""


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

"""""
def task2():
    # Environment Mapping Thread
    global flying
    while flying:
        imgg = np.zeros((1000, 1000, 3), np.uint8)
        if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
            points.append((vals[4], vals[5]))
        drawPoints(imgg, points)
        scream(imgg, x, y)
        cv2.imshow("Output", imgg)
        cv2.waitKey(1)
    
"""""

def task3():
    # Waypoint Mapping Thread
    global flying
    #me.takeoff()
    for index in range(len(path_dist_cm)):
        MoveForward(path_dist_cm[index] / 300)
        TurnAngle(path_angle[index] / 25.71, path_dir[index])
    MoveForward(path_dist_cm[index] / 300)
    time.sleep(0.5)
    #me.land()
    flying = False


t1 = threading.Thread(target=task1, name='t1')
#t2 = threading.Thread(target=task2, name='t2')
t3 = threading.Thread(target=task3, name='t3')

#print(me.get_battery())
#me.streamon()

#t1.start()
#time.sleep(3)
#t2.start()
t3.start()


#t1.join()
#t2.join()
t3.join()
