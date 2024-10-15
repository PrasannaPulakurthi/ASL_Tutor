from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
import io
from cv_algo.main import *

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

        grayscale_image = main_algo(image)
        

        # Save the grayscale image to an in-memory bytes buffer
        img_io = io.BytesIO()
        grayscale_image.save(img_io, 'PNG')
        img_io.seek(0)

        # Send the processed image back to the frontend
        return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
