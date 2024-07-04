# All the imports go here
import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Giving different arrays to handle colour points of different colour
blue_points = [deque(maxlen=1024)]
green_points = [deque(maxlen=1024)]
red_points = [deque(maxlen=1024)]
yellow_points = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_idx = 0
green_idx = 0
red_idx = 0
yellow_idx = 0

# The kernel to be used for dilation purpose 
dilation_kernel = np.ones((5,5),np.uint8)

color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
current_color_idx = 0

# Here is code for Canvas setup
canvas_window = np.zeros((471, 636, 3)) + 255
canvas_window = cv2.rectangle(canvas_window, (40, 1), (140, 65), (0, 0, 0), 2)
canvas_window = cv2.rectangle(canvas_window, (160, 1), (255, 65), (255, 0, 0), 2)
canvas_window = cv2.rectangle(canvas_window, (275, 1), (370, 65), (0, 255, 0), 2)
canvas_window = cv2.rectangle(canvas_window, (390, 1), (485, 65), (0, 0, 255), 2)
canvas_window = cv2.rectangle(canvas_window, (505, 1), (600, 65), (0, 255, 255), 2)

cv2.putText(canvas_window, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(canvas_window, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(canvas_window, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(canvas_window, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(canvas_window, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# initialize mediapipe
mediapipe_hands = mp.solutions.hands
hand_detector = mediapipe_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mediapipe_draw = mp.solutions.drawing_utils

# Initialize the webcam
webcam = cv2.VideoCapture(0)
frame_captured = True
while frame_captured:
    # Read each frame from the webcam
    frame_captured, current_frame = webcam.read()

    height, width, _ = current_frame.shape

    # Flip the frame vertically
    current_frame = cv2.flip(current_frame, 1)
    frame_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)

    current_frame = cv2.rectangle(current_frame, (40, 1), (140, 65), (0, 0, 0), 2)
    current_frame = cv2.rectangle(current_frame, (160, 1), (255, 65), (255, 0, 0), 2)
    current_frame = cv2.rectangle(current_frame, (275, 1), (370, 65), (0, 255, 0), 2)
    current_frame = cv2.rectangle(current_frame, (390, 1), (485, 65), (0, 0, 255), 2)
    current_frame = cv2.rectangle(current_frame, (505, 1), (600, 65), (0, 255, 255), 2)
    cv2.putText(current_frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(current_frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(current_frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(current_frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(current_frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    # Get hand landmark prediction
    hand_results = hand_detector.process(frame_rgb)

    # post process the result
    if hand_results.multi_hand_landmarks:
        hand_landmarks = []
        for hand_landmark_set in hand_results.multi_hand_landmarks:
            for landmark in hand_landmark_set.landmark:
                landmark_x = int(landmark.x * 640)
                landmark_y = int(landmark.y * 480)

                hand_landmarks.append([landmark_x, landmark_y])

            # Drawing landmarks on frames
            mediapipe_draw.draw_landmarks(current_frame, hand_landmark_set, mediapipe_hands.HAND_CONNECTIONS)
        
        index_finger_tip = (hand_landmarks[8][0], hand_landmarks[8][1])
        fingertip_center = index_finger_tip
        thumb_tip = (hand_landmarks[4][0], hand_landmarks[4][1])
        cv2.circle(current_frame, fingertip_center, 3, (0, 255, 0), -1)
        print(fingertip_center[1] - thumb_tip[1])
        
        if (thumb_tip[1] - fingertip_center[1] < 30):
            blue_points.append(deque(maxlen=512))
            blue_idx += 1
            green_points.append(deque(maxlen=512))
            green_idx += 1
            red_points.append(deque(maxlen=512))
            red_idx += 1
            yellow_points.append(deque(maxlen=512))
            yellow_idx += 1

        elif fingertip_center[1] <= 65:
            if 40 <= fingertip_center[0] <= 140: # Clear Button
                blue_points = [deque(maxlen=512)]
                green_points = [deque(maxlen=512)]
                red_points = [deque(maxlen=512)]
                yellow_points = [deque(maxlen=512)]

                blue_idx = 0
                green_idx = 0
                red_idx = 0
                yellow_idx = 0

                canvas_window[67:,:,:] = 255
            elif 160 <= fingertip_center[0] <= 255:
                    current_color_idx = 0 # Blue
            elif 275 <= fingertip_center[0] <= 370:
                    current_color_idx = 1 # Green
            elif 390 <= fingertip_center[0] <= 485:
                    current_color_idx = 2 # Red
            elif 505 <= fingertip_center[0] <= 600:
                    current_color_idx = 3 # Yellow
        else:
            if current_color_idx == 0:
                blue_points[blue_idx].appendleft(fingertip_center)
            elif current_color_idx == 1:
                green_points[green_idx].appendleft(fingertip_center)
            elif current_color_idx == 2:
                red_points[red_idx].appendleft(fingertip_center)
            elif current_color_idx == 3:
                yellow_points[yellow_idx].appendleft(fingertip_center)
    else:
        blue_points.append(deque(maxlen=512))
        blue_idx += 1
        green_points.append(deque(maxlen=512))
        green_idx += 1
        red_points.append(deque(maxlen=512))
        red_idx += 1
        yellow_points.append(deque(maxlen=512))
        yellow_idx += 1

    # Draw lines of all the colors on the canvas and frame
    all_points = [blue_points, green_points, red_points, yellow_points]
    for color_idx in range(len(all_points)):
        for point_set_idx in range(len(all_points[color_idx])):
            for point_idx in range(1, len(all_points[color_idx][point_set_idx])):
                if all_points[color_idx][point_set_idx][point_idx - 1] is None or all_points[color_idx][point_set_idx][point_idx] is None:
                    continue
                cv2.line(current_frame, all_points[color_idx][point_set_idx][point_idx - 1], all_points[color_idx][point_set_idx][point_idx], color_list[color_idx], 2)
                cv2.line(canvas_window, all_points[color_idx][point_set_idx][point_idx - 1], all_points[color_idx][point_set_idx][point_idx], color_list[color_idx], 2)

    cv2.imshow("Output", current_frame) 
    cv2.imshow("Paint", canvas_window)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
webcam.release()
cv2.destroyAllWindows()
