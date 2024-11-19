from flask import Flask, request, jsonify
from flask_cors import CORS
from process_video import process_video_for_damage

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for mobile app communication

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    video_path = f'uploads/{file.filename}'
    file.save(video_path)
    
    # Process the video to detect damage
    damage_images = process_video_for_damage(video_path)
    
    # Return the list of image paths containing detected damage
    return jsonify({"damage_images": damage_images})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
