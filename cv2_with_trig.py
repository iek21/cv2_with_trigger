import RPi.GPIO as GPIO
from time import sleep
import cv2
import numpy as np


mosfet_pin = 3


kamera = cv2.VideoCapture('kayit.avi')
dusuk = np.array([100, 150, 50])
yuksek = np.array([130, 255, 255])


def mosfet_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(mosfet_pin, GPIO.OUT)
    

mosfet_init()


while True:
    ret, goruntu = kamera.read()
    hsv = cv2.cvtColor(goruntu, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, dusuk, yuksek)
    toplam_resim = cv2.bitwise_and(goruntu, goruntu, mask=mask)

    median = cv2.medianBlur(toplam_resim, 15)
    # convert the grayscale image to binary image
    ret, thresh = cv2.threshold(mask, 127, 255, 0)

    # calculate moments of binary image
    M = cv2.moments(thresh)

    # calculate x,y coordinate of center
    if int(M["m00"]) > 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    # put text and highlight the center
        cv2.circle(toplam_resim, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(toplam_resim, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2),

        if cX > 320 :
            GPIO.output(mosfet_pin, GPIO.HIGH)
        else:
            GPIO.output(mosfet_pin, GPIO.LOW)

    cv2.imshow("merkez", toplam_resim)
    cv2.imshow("merkez1", goruntu)


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
kamera.release()
cv2.destroyAllWindows()