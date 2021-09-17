import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(0.8)
colorR = (255, 0, 255)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = img = detector.findHands(img)
    landmarkList, _ = detector.findPosition(img)
    if landmarkList:
        cursor = landmarkList[8]
        if 100 < cursor[0] < 300 and 100 < cursor[1] < 300 :
            colorR = (0, 255, 0)


    cv2.rectangle(img, (100,100), (300,300), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)