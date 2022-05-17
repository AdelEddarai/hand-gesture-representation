from __future__ import annotations
from tkinter import Button
from turtle import width
import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np


# variable
width, height = 1200, 720
folderpath = 'Presentation'
#camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get list of the presentation images
pathimage = sorted(os.listdir(folderpath), key=len)
print(pathimage)

# variables

imgNumber = 2
hs, ws = int(120*1),  int(213*1)
gesturethreshold = 300
ButtonPressed = False
buttoncounter = 0
buttondelay = 5
annotations = [[]]
annotationnumber = 0
annotationstart = False 

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)
while True:
    # import images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathfullimage = os.path.join(folderpath,pathimage[imgNumber])
    imgCurrent = cv2.imread(pathfullimage)


    hands, img = detector.findHands(img)

    cv2.line(img,(0, gesturethreshold),(width, gesturethreshold), (0,255,0), 10)
    #print(annotationnumber)
    if hands and ButtonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # constrain values for easer drawing
        indexfinger = lmList[8][0], lmList[8][1]
        #xval = int(np.interp(lmList[8][0], [width //2, w], [0, width]))
        #yval = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        #indexfinger = xval , yval

        #print(fingers)

        if cy <=gesturethreshold: #if hands is the at hieght of the face

            # gesture 1 - left
            if fingers == [1,0,0,0,0]:
                print('left')    
                if imgNumber>0:
                    ButtonPressed = True
                    annotations = [[]]
                    annotationnumber = 0
                    annotationstart = False
                    imgNumber -= 1

            # gesture 2 - right
            if fingers == [0,0,0,0,1]:
                print('right')
                if imgNumber < len(pathimage) - 1:
                    ButtonPressed = True
                    annotations = [[]]
                    annotationnumber = 0
                    annotationstart = False
                    imgNumber += 1

        # gesture 3 - show pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent, indexfinger, 12,(0,0,255), cv2.FILLED)

        # gesture 4 - draw pointer
        if fingers == [0,1,0,0,0]:
            if annotationstart is False:
                annotationstart = True
                annotationnumber +=1
                annotations.append([])
            cv2.circle(imgCurrent, indexfinger, 12,(0,0,255), cv2.FILLED)
            annotations[annotationnumber].append(indexfinger)
        else:
            annotationstart = False

        # gesture 5 erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                if annotationnumber >= 0:
                    annotations.pop(-1)
                    annotationnumber -=1
                    ButtonPressed = True
    else:
        annotationstart = False

    # button Pressed iterations
    if ButtonPressed:
        buttoncounter +=1
        if buttoncounter> buttondelay:
            buttoncounter = 0
            ButtonPressed = False
    
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!= 0:
                cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], (0,0,200), 12)



    # Adding webcam image in the slides
    imgsmall = cv2.resize(img, (ws, hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgsmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break