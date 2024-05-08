from flask import Flask, jsonify, request
from flask_cors import CORS
from prediction import predict
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required
from middleware import jwt_middleware

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_dotenv(os.path.join(os.path.dirname(__file__), 'sample.env'))
secret_key = os.environ.get('SECRET')
app.config['SECRET'] = secret_key
jwt = JWTManager(app)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# NODE.js and FLASK jwt tokens are diff even if u use same SECRET_KEY
# Middleware
# @app.before_request
def before_request():
    return jwt_middleware()


@app.route("/predict", methods=['POST', 'OPTIONS'])
# @jwt_required()
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
    print(secret_key)
    app.run(debug=True)