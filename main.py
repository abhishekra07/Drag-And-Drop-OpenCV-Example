import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Start video cam
cap = cv2.VideoCapture(0)
# set window size
cap.set(3, 1280)
cap.set(4, 720)
# initialize detector
detector = HandDetector(0.8)


# define class for rectangle box
class DragRectangle:
    def __init__(self, positionCenter, size=[200, 200], color=(255, 0, 255)):
        self.positionCenter = positionCenter
        self.size = size
        self.color = color

    def update(self, cursor):
        cx, cy = self.positionCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.color = (0, 255, 0)
            self.positionCenter = cursor


# create multiple rectangles
rectangles = []
for i in range(3):
    rectangles.append(DragRectangle([i * 250 + 150, 150]))

while True:
    success, img = cap.read()
    # remove image mirror
    img = cv2.flip(img, 1)
    # detect hand movement
    img = detector.findHands(img)
    # find hand landmarks
    landmarkList, _ = detector.findPosition(img)
    if landmarkList:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        if l < 30:
            cursor = landmarkList[8]
            for rectangle in rectangles:
                rectangle.update(cursor)
        else:
            for rectangle in rectangles:
                rectangle.color = (255, 0, 255)

    imgNew = np.zeros_like(img, np.uint8)
    taskCount = 1
    for rectangle in rectangles:
        cx, cy = rectangle.positionCenter
        w, h = rectangle.size
        colorR = rectangle.color
        # cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        rect = cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cv2.putText(rect, 'Task ' + str(taskCount), ((cx - w // 2 + 50, cy - h // 2 + 50)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        taskCount = taskCount + 1

    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)
