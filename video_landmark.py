import mediapipe as mp
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import cv2 as cv
import numpy as np


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
saved = False

options = PoseLandmarkerOptions(
        base_options = BaseOptions(model_asset_path=r"C:\Users\joshu\Documents\projects\idk_man_the_fucking_shotput_coach_thing\pose_landmarker_heavy.task"),
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


with PoseLandmarker.create_from_options(options) as landmarker:
    #path_to_video = input("What is the path of the video you are uploading?: ")
    number_of_frames = 0
    cap = cv.VideoCapture(input("Enter the path of the file you want to save to: "))
    CAM_FPS = int(cap.get(cv.CAP_PROP_FPS))

    if(cap.isOpened()==False):
        print("Error opening video stream or file")
        
    target_ratio = 1920 // 1080
    

    while(cap.isOpened()):
        ret, frame = cap.read()
        
        
        if ret:
            frame_ratio = frame.shape[1] / frame.shape[0]
            cropped_frame = None
            if frame_ratio > target_ratio:
                new_width = int(frame.shape[0] * target_ratio)
                offset = (frame.shape[1] - new_width) // 2
                cropped_frame = frame[:, offset:offset+new_width]
            elif frame_ratio < target_ratio:
                new_height = int(frame.shape[1] / target_ratio)
                offset = (frame.shape[0] - new_height) // 2
                cropped_frame = frame[offset:offset+new_height, :]
            else:
                cropped_frame = frame
                
            frame_resized = cv.resize(cropped_frame, (1920, 1080), interpolation=cv.INTER_AREA) 
            frame_resized = frame_resized.astype(np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_resized)
            
            frame_timestamp = int(number_of_frames * (1000 / CAM_FPS))
             
            pose_landmarker_result = landmarker.detect_for_video(mp_image, frame_timestamp)
            number_of_frames += 1
            rgb_image = mp_image.numpy_view()
            annotated_frame = draw_landmarks_on_image(rgb_image, pose_landmarker_result)
            latest_frame = cv.cvtColor(annotated_frame, cv.COLOR_RGB2BGR)
        
            cv.imshow("Landmarks", latest_frame)
            
            if cv.waitKey(1) == ord("q"):
                cap.release()
                cv.destroyAllWindows()
                print("Goodbye!")