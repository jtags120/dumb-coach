import mediapipe as mp
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import numpy as np
import cv2 as cv
import datetime

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
        base_options = BaseOptions(model_asset_path=)
)


path_to_video = input("What is the path of the video you are uploading?: ")

cap = cv.VideoCapture(path_to_video)
CAM_FPS = int(cap.get(cv.CAP_PROP_FPS))

if(cap.isOpened==False):
    print("Error opening video stream or file")

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret:
        np_frame = np.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        
        cv.imshow('Frame', frame)

cap.release()
cv.destroyAllWindows()