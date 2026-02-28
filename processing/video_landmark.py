import mediapipe as mp
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import cv2 as cv
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
import config
#from kalman_smooth import *
import sys


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
app = QApplication([])

options = PoseLandmarkerOptions(
        base_options = BaseOptions(model_asset_path=config.model_path),
        running_mode=VisionRunningMode.VIDEO)

def draw_landmarks_on_image(rgb_image, result):
    pose_landmarks_list = result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
    pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    for pose_landmarks in pose_landmarks_list:
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=pose_landmarks,
            connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
            landmark_drawing_spec=pose_landmark_style,
            connection_drawing_spec=pose_connection_style)

    return annotated_image

def run():
    global annotated_frame
    with PoseLandmarker.create_from_options(options) as landmarker:
        cv.namedWindow("Landmarks", cv.WINDOW_KEEPRATIO)
        
        cap = cv.VideoCapture(config.video_path)
        CAM_FPS = int(cap.get(cv.CAP_PROP_FPS))
        
        annotated_frames = []
        timestamps = []
        
        ret, frame = cap.read()           
        

        start_time = int(cap.get(cv.CAP_PROP_POS_MSEC))
        frame_resized = frame.astype(np.uint8)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_resized)
        result = landmarker.detect_for_video(mp_image, start_time)
        #filters = make_filters(result.pose_landmarks[0], CAM_FPS)
        
        
        ###    gui = get_window()
        
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            start_time = int(cap.get(cv.CAP_PROP_POS_MSEC))
            frame_resized = frame.astype(np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_resized)
            result = landmarker.detect_for_video(mp_image, start_time)
                
            
            # if result.pose_landmarks:
            #         smoothed = smooth_landmarks(result.pose_landmarks[0], filters)

            # for i, filter in enumerate(smoothed):
            #     result.pose_landmarks[0][i].x = filter[0]
            #     result.pose_landmarks[0][i].y = filter[1]
            #     result.pose_landmarks[0][i].z = filter[2]
            
            annotated_frame = draw_landmarks_on_image(frame_resized, result)
            
            
            annotated_frames.append(annotated_frame)
            timestamps.append(start_time)
        
        cap.release()
        
        total_frames = len(annotated_frames) - 1
        current_frame = 0
        paused = False
        updating_trackbar = False
        
        def on_scrub(val):
            nonlocal current_frame, paused, updating_trackbar
            if updating_trackbar:
                return
            current_frame = val
            paused = True
        
        cv.createTrackbar('', 'Landmarks', 0, total_frames, on_scrub)
        
        while True:
            key = cv.waitKey(int(1000/CAM_FPS)) & 0xFF
            for frame in annotated_frames:
                cv.imshow("Landmarks", frame)
                
                if key == ord('q'):
                    cv.destroyAllWindows()
                    print("Goodbye!")
                    break
                
                if key == ord(' '):
                    paused = not paused
                    print(f"Paused: {paused}")
                
                if not paused:
                    current_frame = min(current_frame + 1, total_frames)
                    updating_trackbar = True
                    cv.setTrackbarPos('', 'Landmarks', current_frame)
                    updating_trackbar = False
            
            
            
            