import numpy as np
from opencvprojects import handrecmodule as ht
import cv2
import time
import os
import math
ethick=50
f=0
draw_color=(255,255,255)
thick=5
xp,yp=0,0
image_can=np.zeros((480,640,3),np.uint8)
cap = cv2.VideoCapture(1)
ptime = 0
detector = ht.hand_detector(dic_conf=.3)
path = 'tools'
file = os.listdir(path)
file_list = []

for i in file:
    image = cv2.imread(f'{path}/{i}')
    file_list.append(image)
# print(len(file_list))
head = file_list[0]

while True:
    frame, img = cap.read()

    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    if len(lm_list) != 0:

        # print(lm_list[0])
        x1, y1 = lm_list[8][1], lm_list[8][2]
        x2, y2 = lm_list[12][1], lm_list[12][2]

        fingers = detector.fing_up()
        print(fingers)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), draw_color, cv2.FILLED)
            print('select')

            if y1 < 75:
                if 40 < x1 <120:
                    head = file_list[0]
                    draw_color=(255,255,255)

                elif 160 < x1 < 240:
                    head = file_list[1]
                    draw_color=(255, 0, 0)
                elif 320 < x1 < 400:
                    head = file_list[2]
                    draw_color=(0,0,255)
                elif 480 < x1 <550:
                    head = file_list[3]
                    f=1
                    draw_color=(0,0,0)


        if fingers[1] and fingers[2] == False:

            cv2.circle(img, (x1, y1), 11, draw_color, cv2.FILLED)
            print('draw')
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if draw_color==(0,0,0):
               cv2.line(image_can, (xp, yp), (x1, y1), draw_color, ethick)
               cv2.line(image_can, (xp, yp), (x1, y1), draw_color, ethick)
            else:
                cv2.line(img, (xp, yp), (x1, y1), draw_color, thick)
                cv2.line(image_can, (xp, yp), (x1, y1), draw_color, thick)
            xp, yp = x1, y1
    imgry=cv2.cvtColor(image_can,cv2.COLOR_BGR2GRAY)
    _,imgin=cv2.threshold(imgry,50,255,cv2.THRESH_BINARY_INV)
    imgin=cv2.cvtColor(imgin,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgin)
    img=cv2.bitwise_or(img,image_can)
    h, w, c = img.shape

    img[0:75, 0:640] = head


    #img=cv2.addWeighted(img,0.5,image_can,0.5,0)
    cv2.flip(img, 1)
    # cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    #cv2.imshow('2nd',image_can)
    img = cv2.resize(img, (720, 640))
    cv2.imshow('1st', img)
    if cv2.waitKey(10) == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()
