import time
import cv2
import dlib
import pyautogui

pyautogui.FAILSAFE = False

vid = cv2.VideoCapture(0)
find_faces = dlib.get_frontal_face_detector()
find_landmark = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

def get_bounding_box(landmarks):
    min_x = min(landmarks , key=lambda p : p.x).x
    max_x = max(landmarks , key = lambda p : p.x).x
    min_y = min(landmarks , key = lambda p : p.y).y
    max_y = max(landmarks , key = lambda p : p.y).y
    return min_x,max_x,min_y,max_y
#adding the crop function
def crop(image , bbox):
    return image[bbox[2]:bbox[3],bbox[0]:bbox[1]]

def filter_for_iris(eye_image):
    #convert to grayscale
    eye_image = cv2.cvtColor(eye_image,cv2.COLOR_BGR2GRAY)
    #blur the frame
    eye_image = cv2.bilateralFilter(eye_image,10,15,15)
    #adjust the contrast
    eye_image = cv2.equalizeHist(eye_image)
    #convert this to binary image and adjust the values for better detection
    iris_image = 255 - cv2.threshold(eye_image,50,255,cv2.THRESH_BINARY)[1]
    return iris_image

def find_iris_location(iris_image):
    #find the contours 
    contours , _ = cv2.findContours(iris_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #sort in asceneding orders
    contours = sorted(contours , key=cv2.contourArea)

    try:
        #Findin the largest one
        moments = cv2.moments(contours[-1])
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
    except (IndexError,ZeroDivisionError):
        #no iris found
        return None
    return x,y

top_left_average_offset = None
bottom_right_average_offset = None
last_time_told = None

while True:
    ret,frame = vid.read()
    left_iris = None
    right_iris = None
    for faces in find_faces(frame):

        landmarks = find_landmark(frame,faces).parts()
        # print(landmarks)
        left_bbox = get_bounding_box(landmarks[36:42])
        right_bbox = get_bounding_box(landmarks[42:48])

        cv2.rectangle(frame,(left_bbox[0],left_bbox[2]),(left_bbox[1],left_bbox[3]),(0,255,0),1)
        cv2.rectangle(frame,(right_bbox[0],right_bbox[2]),(right_bbox[1],right_bbox[3]),(0,255,0),1)

        left_eye_frame = crop(frame,left_bbox)
        right_eye_frame = crop(frame,right_bbox)

        left_iris = filter_for_iris(left_eye_frame)
        right_iris = filter_for_iris(right_eye_frame)

        #finding the center of the iris
        left_iris_location = find_iris_location(left_iris)
        right_iris_location = find_iris_location(right_iris)
        #viewing the image boxes
        # cv2.imshow('left_eye',left_iris)
        # cv2.imshow('right_eye',right_iris)
        left_eye_center = ((landmarks[36].x + landmarks[39].x) //2 - left_bbox[0]),((landmarks[36].y+landmarks[39].y)//2 - left_bbox[2])
        right_eye_center = ((landmarks[42].x + landmarks[45].x) //2 - right_bbox[0]),((landmarks[42].y+landmarks[45].y)//2 - right_bbox[2])
        # print(f"left-eye-centre = {left_eye_center}  right-eye-centre ={right_eye_center}")
        left_iris_offset = None
        right_iris_offset = None

        if left_iris_location is not None:
            left_iris_offset = (left_iris_location[0]-left_eye_center[0],left_iris_location[1]-left_eye_center[1])
            cv2.circle(left_eye_frame,left_iris_location,2,(0,0,255),-1)
        if right_iris_location is not None:
            right_iris_offset = (right_iris_location[0]-right_eye_center[0],right_iris_location[1]-right_eye_center[1])
            cv2.circle(right_eye_frame,right_iris_location,2,(0,0,255),-1)

        if left_iris_location is not None and right_iris_location is not None:
            average_offset = ((left_iris_offset[0]+right_iris_offset[0])//2 + (left_iris_offset[1]+right_iris_offset[1])//2)
            # print(average_offset[0])
            needs_callibaration = (top_left_average_offset is None) or (bottom_right_average_offset is None)
            if needs_callibaration:
                if last_time_told is None:
                    if top_left_average_offset is None:
                        print("Look at top left corner")
                    else:
                        print("Look at bottom right corner")
                    last_time_told = time.time()
                elif time.time() >= last_time_told + 5:
                    if top_left_average_offset is None:
                        top_left_average_offset = average_offset
                    elif bottom_right_average_offset is None:
                        bottom_right_average_offset = average_offset

                    last_time_told = None
            else:
                min_x,min_y = top_left_average_offset
                max_x,max_y = bottom_right_average_offset
            
                pyautogui.moveTo(
                    1920*(average_offset[0]-min_x) /(max_x-min_x) ,1080*(average_offset[1]-min_y) /(max_y-min_y)
                )
    cv2.imshow('frame',frame)
    # cv2.imshow('fjls',left_eye_frame)
    # cv2.imshow('fsf',right_eye_frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break 
cv2.destroyAllWindows()