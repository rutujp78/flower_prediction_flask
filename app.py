from flask import Flask, jsonify, request
from flask_cors import CORS
from prediction import predict
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/predict", methods=['POST'])
def index():
    if 'image' not in request.files:
        return jsonify({ 'error': 'Image upload failed' })

    image = request.files['image']
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

    result = predict(image_path)

    os.remove(image_path)

    return jsonify({ 'result': result })

if __name__ in "__main__":
    app.run(debug=True)