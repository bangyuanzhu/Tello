import pygame
import json
import math
import time
from djitellopy import Tello

me = Tello()
MAP_SIZE_COEFF = 5.14

class Background(pygame.sprite.Sprite):
    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


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
    _magA = math.sqrt(ax**2 + ay**2)
    _magB = math.sqrt(bx**2 + by**2)
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
    me.send_rc_control(0, 50, 0, 0)
    time.sleep(interval)

def TurnAngle(interval, directionRIGHT):
    # angular speed at 100 is 64.25 degrees/s
    if directionRIGHT == True:
        me.send_rc_control(0, 0, 0, 40)
        print("Right")
        time.sleep(0.0001)

    elif directionRIGHT == False:
        me.send_rc_control(0, 0, 0, -40)
        print("Left")
        time.sleep(0.0001)

    time.sleep(interval)




