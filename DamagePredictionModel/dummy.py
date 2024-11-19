import cv2
import numpy as np

def process_video_for_damage(video_path):
    # Load the video
    cap = cv2.VideoCapture(video_path)
    output_images = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Detect car in the frame
        car_frame = detect_car_in_frame(frame)
        if car_frame is None:
            continue

        # Detect potential damage areas on the car frame
        damage_boxes = detect_damage(car_frame)

        # Annotate damage boxes on the car frame
        for (x, y, w, h) in damage_boxes:
            damage_percentage = estimate_damage_percentage(car_frame[y:y+h, x:x+w])
            cv2.rectangle(car_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(car_frame, f"{damage_percentage:.1f}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Save annotated frame
        output_image_path = f'output_images/frame_{frame_count}.jpg'
        cv2.imwrite(output_image_path, car_frame)
        output_images.append((output_image_path, damage_percentage))

    cap.release()
    return output_images

def detect_car_in_frame(frame):
    # Placeholder for car detection; in a production setup, use an object detection model like YOLO.
    # For this implementation, we'll assume the whole frame is the car region.
    return frame

def detect_damage(car_frame):
    # Convert to grayscale
    gray_frame = cv2.cvtColor(car_frame, cv2.COLOR_BGR2GRAY)

    # Use edge detection to find potential damage areas
    edges = cv2.Canny(gray_frame, threshold1=100, threshold2=200)

    # Find contours from the edge-detected areas
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    damage_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Filter out small contours that are unlikely to be damage
        if w * h > 500:  # Adjust this threshold based on typical damage size
            damage_boxes.append((x, y, w, h))

    return damage_boxes

def estimate_damage_percentage(damage_region):
    # A basic estimation function based on the intensity of edges
    # Calculate the ratio of edge pixels to total pixels in the damage region
    gray_damage = cv2.cvtColor(damage_region, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_damage, threshold1=100, threshold2=200)
    edge_pixel_count = np.sum(edges > 0)
    total_pixel_count = damage_region.shape[0] * damage_region.shape[1]
    damage_percentage = (edge_pixel_count / total_pixel_count) * 100
    return damage_percentage
