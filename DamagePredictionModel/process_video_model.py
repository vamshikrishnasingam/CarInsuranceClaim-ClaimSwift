from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
import cv2
from werkzeug.utils import secure_filename
import numpy as np
import base64
from io import BytesIO

# Initialize YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# Initialize Flask app
app = Flask(__name__)

# Allow CORS for only the /upload_video endpoint
CORS(app, resources={r"/upload_video": {"origins": "*"}})

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if the uploaded file is a valid video
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert an image to base64 string
def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

# Process video and detect damage
def process_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Calculate the frame interval (in frames) based on 0.75 seconds
        frame_interval = int(fps * 0.75)
        damage_info = {
            "front": {"windshield": 0, "bumper": 0, "left": 0, "right": 0, "side_scratch": 0},
            "rear": {"windshield": 0, "bumper": 0, "left": 0, "right": 0, "side_scratch": 0}
        }
        images = []

        # Process video frames
        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)  # Set the video to the correct frame position
            ret, frame = cap.read()
            if not ret:
                break

            # Use YOLOv5 for damage detection
            results = model(frame)
            detected_boxes = results.pandas().xyxy[0]  # Get bounding boxes

            # Process detected boxes to estimate damage areas
            for part in damage_info["front"].keys():
                damage_area = 0
                for _, row in detected_boxes.iterrows():
                    x1, y1, x2, y2 = row['xmin'], row['ymin'], row['xmax'], row['ymax']
                    damage_area += (x2 - x1) * (y2 - y1)
                damage_info["front"][part] = (damage_area / (frame.shape[0] * frame.shape[1])) * 100

            # Save frame with damage for sending to frontend
            damage_image = frame  # You can modify this to highlight damage areas (optional)
            images.append(image_to_base64(damage_image))

        cap.release()
        return damage_info, images
    except Exception as e:
        print(f"Error processing video: {e}")
        return {"error": str(e)}, []

@app.route('/upload_video', methods=['POST'])
def upload_video():
    print("Uploading video...")

    # Check if the 'video' part is in the request
    if 'video' not in request.files:
        return jsonify({"error": "No video part in the request"}), 400

    # Get the video file from the request
    video = request.files['video']

    # Check if the video has a valid file extension
    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        video.save(file_path)

        # Process the video and detect damage
        damage_info, images = process_video(file_path)

        # Clean up by removing the uploaded video file
        os.remove(file_path)

        # Return the damage info and images as a response
        return jsonify({"damage_info": damage_info, "images": images}), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    # Run the Flask app on all network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
