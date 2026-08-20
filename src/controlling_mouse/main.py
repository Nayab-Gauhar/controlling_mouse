import pyautogui
import time
import cv2
import dlib

vid = cv2.VideoCapture(0)
find_faces = dlib.get_frontal_face_detector()
find_landmark = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')


while True:
    ret,frame = vid.read()
    for faces in find_faces(frame):
        x1,y1 = faces.left(),faces.top()
        x2,y2 = faces.right(),faces.bottom()
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
        landmarks = find_landmark(frame,faces).parts()
        for landmark in landmarks:
            cv2.circle(frame,(landmark.x,landmark.y),1,(255,0,0),1)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break 
cv2.destroyAllWindows()