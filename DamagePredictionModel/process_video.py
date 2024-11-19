import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from model import model  # Import the pre-trained model

def detect_damage(frame):
    """
    Detects damage in a single frame using the VGG19 model.
    """
    # Resize the image to match the input size of the model (224x224)
    img = cv2.resize(frame, (224, 224))
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize the image

    # Predict the damage
    prediction = model.predict(img)

    # If damage detected (assuming binary classification, threshold at 0.5)
    damage_percentage = prediction[0][0] * 100  # Convert to percentage
    label = "Damaged" if prediction[0][0] > 0.5 else "No Damage"
    
    return label, damage_percentage

def process_video_for_damage(video_path):
    """
    Processes a video and detects damage on each frame.
    """
    video = cv2.VideoCapture(video_path)
    frame_number = 0
    damage_images = []  # To store frames with detected damage

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_number += 1
        label, damage_percentage = detect_damage(frame)

        # If damage is detected, save the frame
        if label == "Damaged":
            # Draw a box around the damaged area (for visualization)
            cv2.putText(frame, f"Damage: {damage_percentage:.2f}%", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Optionally, save the frame as an image
            image_filename = f"damaged_frame_{frame_number}.jpg"
            cv2.imwrite(image_filename, frame)
            damage_images.append(image_filename)

    video.release()
    return damage_images
