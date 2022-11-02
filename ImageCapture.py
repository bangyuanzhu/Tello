from djitellopy import tello
import cv2
import time

me = tello.Tello()
me.connect()                        #Connect to the tello. Make sure to connect device via wifi first.
print(me.get_battery())             #Gets battery percent

#Streams image data from the tello camera
me.streamon()



while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))#Resizes the image to 360p x 240p to minimise data processing load
    cv2.imshow("Image", img)
    cv2.waitKey(1)