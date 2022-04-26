import cv2 
import time
cap=cv2.VideoCapture(1)
print(cap.isOpened())

while True:
    ret, frame = cap.read()
    print(ret)
    time.sleep(1)