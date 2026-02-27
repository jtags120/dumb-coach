import numpy as np
import filterpy
from filterpy import kalman
from filterpy.kalman import KalmanFilter

def make_filters(landmark_list, CAM_FPS):
    filters = [KalmanFilter(9, 3) for i in range(33)]
    dt = 1/CAM_FPS
    for i, filter in enumerate(filters):
        #state_transition_matrix
        filter.F = np.array([
            [1, 0, 0, dt, 0,  0,  0.5*dt**2, 0,         0        ],
            [0, 1, 0, 0,  dt, 0,  0,         0.5*dt**2, 0        ],
            [0, 0, 1, 0,  0,  dt, 0,         0,         0.5*dt**2],
            [0, 0, 0, 1,  0,  0,  dt,        0,         0        ],
            [0, 0, 0, 0,  1,  0,  0,         dt,        0        ],
            [0, 0, 0, 0,  0,  1,  0,         0,         dt       ],
            [0, 0, 0, 0,  0,  0,  1,         0,         0        ],
            [0, 0, 0, 0,  0,  0,  0,         1,         0        ],
            [0, 0, 0, 0,  0,  0,  0,         0,         1        ],
])
        #Control matrix
        filter.B = None
        #Measurement matrix
        filter.H =  np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0, 0]])
        #Process Noise Covariance
        filter.Q = np.eye(9) * 0.5
        #Measurement Noise
        filter.R = np.eye(3) * 0.01
        
        filter.P = np.eye(9) * 1000.
        
        x = landmark_list[i].x
        y = landmark_list[i].y
        z = landmark_list[i].z
        
        filter.x = np.array([x, y, z, 0, 0, 0, 0, 0, 0])
        
    return filters
    
def smooth_landmarks(landmark_list: list, filters: list): # type: ignore
    smoothed = []
    
    for i, landmark in enumerate(landmark_list):
        z = np.array([landmark.x, landmark.y, landmark.z])
        curr_filter = filters[i]
        curr_filter.predict()
        curr_filter.update(z)
        smoothed.append(filters[i].x[:3])
    return smoothed    