from djitellopy import tello
from time import sleep

"""
This program contains code for
1) Connecting to the tello drone
2) Checking tello battery percentage
3) Basic movements of the tello drone

"""

me = tello.Tello()
me.connect()                        #connect to the tello. Make sure to connect device via wifi first.
print(me.get_battery())             #Gets battery percent

me.takeoff()
sleep(2)

me.send_rc_control(0, 20, 0, 0)      #(L/R, F/B, Up/Down, Yaw) - values all -100 ~ 100
sleep(2)                             #Delays 2s

me.send_rc_control(0, 0, 0, 0)      #Stop moving forward
me.land()
