import cv2
import mediapipe as mp
import time
import math


class hand_detector():
    def __init__(self,mode=False,max_hand=1,dic_conf=0.5,track_conf=0.5):
        self.mode=mode
        self.max_hand=max_hand
        self.dic_conf=dic_conf
        self.track_conf=track_conf
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.max_hand,self.dic_conf,self.track_conf)
        self.mpdraw = mp.solutions.drawing_utils
        self.tipids=[4,8,12,16,20]


    def find_hands(self,img,draw=True):
        rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgbimg)

        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for mh in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, mh, self.mphands.HAND_CONNECTIONS)
        return img
    def find_position(self,img,hand_no=0,draw=True):
        self.lm_list=[]
        bbox=[]
        xList=[]
        yList=[]
        if self.result.multi_hand_landmarks:
            myhand=self.result.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax

                if draw:
                    cv2.rectangle(img,(xmin-20,ymin-20), (xmax + 20, ymax + 20),(0, 255, 0), 2)

        return self.lm_list, bbox

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]

        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2-x1,y2-y1)

    def fing_up(self):
        fingers=[]
        if self.lm_list[self.tipids[0]][1]>self.lm_list[self.tipids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)



        for id in range(1,5):
            if self.lm_list[self.tipids[id]][2]<self.lm_list[self.tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers







def main():
    cap = cv2.VideoCapture(0)
    ptime = 0
    detector=hand_detector()
    while True:
        frame, img = cap.read()
        img=detector.find_hands(img)
        lm_list,bbox=detector.find_position(img)

        if len(lm_list) !=0:
            print(lm_list[0])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.imshow('1st', img)
        if cv2.waitKey(10) == ord('a'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()