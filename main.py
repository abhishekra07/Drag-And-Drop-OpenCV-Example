import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(0.8)


class DragRectangle():
    def __init__(self, positionCenter, size=[200, 200], color = (255,0,255)):
        self.positionCenter = positionCenter
        self.size = size
        self.color = color

    def update(self, cursor):
        cx, cy = self.positionCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.color = (0, 255, 0)
            self.positionCenter = cursor

rectangle = DragRectangle([150, 150])

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    landmarkList, _ = detector.findPosition(img)
    if landmarkList:

        l, _, _ = detector.findDistance(8, 12, img)
        print(l)
        if l < 30:
            cursor = landmarkList[8]
            rectangle.update(cursor)
        else:
            rectangle.color = (255, 0, 255)

    cx, cy = rectangle.positionCenter
    w, h = rectangle.size
    colorR = rectangle.color
    cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
