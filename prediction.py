import os
import keras
from keras.models import load_model, model_from_json
import tensorflow as tf
import numpy as np

def predict(image_path):
    flower_name = ['daisy', 'dandelion', 'rose', 'sunflower', 'tuplip']

    # Load model architecture from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'predictions', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as json_file:
        model_config = json_file.read()

    # Load model weights from model.weights.h5
    model = model_from_json(model_config)
    weights_path = os.path.join(os.path.dirname(__file__), 'predictions', 'model.weights.h5')
    model.load_weights(weights_path)

    input_image = tf.keras.utils.load_img(image_path, target_size=(180, 180))
    input_image_array = tf.keras.utils.img_to_array(input_image)
    input_image_exp_dim = tf.expand_dims(input_image_array, 0)

    predictions = model.predict(input_image_exp_dim)
    result = tf.nn.softmax(predictions[0])
    outcome = flower_name[np.argmax(result)]
    
    return outcome