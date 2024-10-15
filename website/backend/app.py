from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
from cv_algo.main import main_algo

app = Flask(__name__)
CORS(app)  # Allow CORS for all origins

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Open the image from the uploaded file in-memory
        image = Image.open(file.stream)

        # Convert the image to a NumPy array and handle RGBA/BGR conversion if necessary
        image = np.array(image)
        if image.shape[-1] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        
        # Process the image with your main algorithm
        output_image, predicted_char = main_algo(image)
        
        # Return the predicted character as a JSON response
        print(predicted_char)
        return jsonify({'predicted_char': predicted_char})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
