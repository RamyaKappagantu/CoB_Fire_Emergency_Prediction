from flask import jsonify, Blueprint
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.models import model_from_json
from flask_jwt_extended import jwt_required

bp = Blueprint('lstm_prediction2', __name__, url_prefix='/lstm_prediction2')

sequence_length = 16
rolling_window = None

# Load label encoders
with open('./Trained_models/LSTM/label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)

label_encoder_dauid_new = label_encoders['DAUID']
label_encoder_incident_category = label_encoders['incident_category_description']

# Load the model architecture from JSON
with open('./Trained_models/LSTM/model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)

# Load the model weights
model.load_weights('./Trained_models/LSTM/model.weights.h5')


def load_initial_data():
    x_test_df = pd.read_excel('./Test_data/LSTM_test_data/x_test.xlsx', header=None)
    y_dauid_test_df = pd.read_excel('./Test_data/LSTM_test_data/y_dauid_test.xlsx', header=None)
    y_category_test_df = pd.read_excel('./Test_data/LSTM_test_data/y_category_test.xlsx', header=None)

    # Calculate the original shape
    num_samples = x_test_df.shape[0] * x_test_df.shape[1] // (16 * 18)  # 16 timesteps, 18 features
    x_test = np.array(x_test_df).reshape(num_samples, 16, 18)  # Reshape to (num_samples, 16, 18)

    # Reshape y_dauid_test and y_category_test
    num_samples_y = y_dauid_test_df.shape[0]
    num_dauid_classes = len(label_encoder_dauid_new.classes_)
    num_category_classes = len(label_encoder_incident_category.classes_)

    y_dauid_test = np.array(y_dauid_test_df).reshape(num_samples_y, num_dauid_classes)
    y_category_test = np.array(y_category_test_df).reshape(num_samples_y, num_category_classes)

    return x_test, y_dauid_test, y_category_test

def load_data():
    global rolling_window, x_test_final, y_dauid_test_final, y_category_test_final
    x_test, y_dauid_test, y_category_test = load_initial_data()
    x_test_final = preprocess_data(x_test)
    y_dauid_test_final = y_dauid_test.astype('float32')
    y_category_test_final = y_category_test.astype('float32')
    rolling_window = x_test_final[-1]
    rolling_window = np.expand_dims(rolling_window, axis=0)
    rolling_window = rolling_window.astype('float32')
def preprocess_data(x_test):
    return x_test
def predict_next_sequence():
    global rolling_window
    print(f"Rolling window shape before prediction: {rolling_window.shape}")

    # Predict without reshaping the rolling_window
    y_pred = model.predict(rolling_window)
    print(f"Prediction shape: {[pred.shape for pred in y_pred]}")

    pred_da = np.argmax(y_pred[0], axis=-1)
    pred_type = np.argmax(y_pred[1], axis=-1)
    new_prediction = np.concatenate([y_pred[0], y_pred[1]], axis=-1)

    # Extract the new prediction values
    new_prediction_values = new_prediction[0, :2]

    # Update rolling window with new prediction
    rolling_window = update_rolling_window(rolling_window, new_prediction_values)

    return pred_da, pred_type

def update_rolling_window(window, new_prediction):
    num_features = window.shape[2]

    # Create a new row to hold the new prediction values and maintain existing features
    new_row = np.zeros((1, 1, num_features))

    new_row[0, 0, -new_prediction.shape[0]:] = new_prediction

    # Roll the window to remove the oldest entry and add the new one
    updated_window = np.roll(window, -1, axis=1)
    updated_window[0, -1, :] = new_row

    return updated_window
def calculate_accuracy():
    y_pred = model.predict(x_test_final)

    print(f"Shape of y_pred[0] (DAUID predictions): {y_pred[0].shape}")
    print(f"Shape of y_pred[1] (Category predictions): {y_pred[1].shape}")
    print(f"Shape of y_dauid_test_final: {y_dauid_test_final.shape}")
    print(f"Shape of y_category_test_final: {y_category_test_final.shape}")

    # Convert predictions to class labels
    pred_da = np.argmax(y_pred[0], axis=-1)
    pred_type = np.argmax(y_pred[1], axis=-1)

    # Ensure predictions and true labels have compatible shapes for comparison
    pred_da = pred_da.flatten()
    pred_type = pred_type.flatten()
    y_dauid_test_labels = np.argmax(y_dauid_test_final, axis=-1).flatten()
    y_category_test_labels = np.argmax(y_category_test_final, axis=-1).flatten()

    print(f"Shape of pred_da: {pred_da.shape}")
    print(f"Shape of pred_type: {pred_type.shape}")
    print(f"Shape of y_dauid_test_labels: {y_dauid_test_labels.shape}")
    print(f"Shape of y_category_test_labels: {y_category_test_labels.shape}")

    # Calculate accuracy
    accuracy_da = np.mean(y_dauid_test_labels == pred_da)
    accuracy_type = np.mean(y_category_test_labels == pred_type)

    return accuracy_da, accuracy_type


load_data()


@bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    pred_da, pred_type = predict_next_sequence()

    next_pred_da_original = label_encoders['DAUID'].inverse_transform(pred_da.flatten()).tolist()
    next_pred_type_original = label_encoders['incident_category_description'].inverse_transform(pred_type.flatten()).tolist()

    accuracy_da, accuracy_type = calculate_accuracy()
    # Format accuracy values to 2 decimal places
    accuracy_da = f"{accuracy_da:.2f}"
    accuracy_type = f"{accuracy_type:.2f}"

    response = {
        "da_predictions": next_pred_da_original,
        "type_predictions": next_pred_type_original,
        "accuracy_da": accuracy_da,
        "accuracy_type": accuracy_type
    }
    return jsonify(response)