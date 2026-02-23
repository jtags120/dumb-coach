import cv2 as cv
import numpy as np
import threading
import time
from datetime import datetime

class video_feed:

    def __init__(self):
        self.filming = True
        self.footage = {}
        self.fps = 0
        self.i = 0
        self.thread = threading.Thread()
        self.aspect_ratio = 0.0
        self.CAM_FPS = 0
        self.realtime_fps = 0.0
        
    def __call__(self):
        self.getVideo()
 
    def getVideo(self):
        cap = cv.VideoCapture(0)
        ONE_MORBILLION = 1_000_000
        self.CAM_FPS = cap.get(cv.CAP_PROP_FPS)
        
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
            
        width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.aspect_ratio = width / height
        
        start_timestamp = time.perf_counter_ns() // ONE_MORBILLION
        
        while self.filming:
            
            timestamp = time.perf_counter_ns() // ONE_MORBILLION
            world_clock = datetime.now()
            
            ret, frame, = cap.read()

            if not ret:
                print("Can't receive frame (stream end?) Exiting.")
                break
            
            self.footage[self.i] = [frame, timestamp, world_clock]
           
            self.i += 1
            
        cap.release()
        cv.destroyAllWindows()
        
        self.filming = False
        
        #Something for fps
        footage_keys = self.footage.keys()
        self.num_of_frame = len(footage_keys)
        end_timestamp = int(time.perf_counter_ns()) / ONE_MORBILLION 
        total_time = end_timestamp - start_timestamp
        
        self.realtime_fps = self.num_of_frame // total_time


vid_object=video_feed()

vid_object.thread = threading.Thread(target=vid_object)

vid_object.thread.start()