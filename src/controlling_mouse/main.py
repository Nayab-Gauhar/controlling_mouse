import pyautogui
import time
import cv2
import dlib

vid = cv2.VideoCapture(0)
find_faces = dlib.get_frontal_face_detector()
find_landmark = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

def get_bounding_box(landmarks):
    min_x = min(landmarks , key=lambda p : p.x).x
    max_x = max(landmarks , key = lambda p : p.x).x
    min_y = min(landmarks , key = lambda p : p.y).y
    max_y = max(landmarks , key = lambda p : p.y).y
    return min_x,max_x,min_y,max_y

while True:
    ret,frame = vid.read()
    for faces in find_faces(frame):
        x1,y1 = faces.left(),faces.top()
        x2,y2 = faces.right(),faces.bottom()
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
        landmarks = find_landmark(frame,faces).parts()
        for landmark in landmarks:
            cv2.circle(frame,(landmark.x,landmark.y),1,(255,0,0),1)

        left_bbox = get_bounding_box(landmarks[36:42])
        right_bbox = get_bounding_box(landmarks[42:48])

        cv2.rectangle(frame,(left_bbox[0],left_bbox[2]),(left_bbox[1],left_bbox[3]),(0,255,0),1)
        cv2.rectangle(frame,(right_bbox[0],right_bbox[2]),(right_bbox[1],right_bbox[3]),(0,255,0),1)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break 
cv2.destroyAllWindows()