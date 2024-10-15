import os
import pickle

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize MediaPipe Hands with static image mode
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = 'data'

data = []
labels = []

# Loop through each directory in the data directory
for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)

    # Ensure the current entry is a directory
    if os.path.isdir(dir_path):
        for img_path in os.listdir(dir_path):
            data_aux = []
            x_ = []
            y_ = []

            img_full_path = os.path.join(dir_path, img_path)
            
            # Load image
            img = cv2.imread(img_full_path)
            if img is None:
                print(f"Warning: Could not read image {img_full_path}")
                continue  # Skip if the image can't be loaded

            # Convert image to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Process image with MediaPipe Hands
            results = hands.process(img_rgb)
            
            # If hand landmarks are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Collect landmark x and y positions
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    # Normalize the coordinates relative to the minimum x and y values
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                data.append(data_aux)
                labels.append(dir_)

# Save data and labels using pickle
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

# Properly close the MediaPipe Hands object to free resources
hands.close()
