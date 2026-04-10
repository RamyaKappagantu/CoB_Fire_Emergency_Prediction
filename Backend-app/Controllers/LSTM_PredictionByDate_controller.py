from flask import jsonify, Blueprint, request
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.models import model_from_json
from datetime import datetime, timezone


bp = Blueprint('lstm_prediction', __name__, url_prefix='/lstm_prediction')

sequence_length = 16

# Load label encoders
with open('./Trained_models/LSTM/label_encoders10.pkl', 'rb') as file:
    label_encoders = pickle.load(file)

label_encoder_dauid_new = label_encoders['DAUID']
label_encoder_incident_category = label_encoders['incident_category_description']

# Load the model architecture from JSON
with open('./Trained_models/LSTM/10output_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)

# Load the model weights
model.load_weights('./Trained_models/LSTM/10output_model.weights.h5')


def load_initial_data():
    x_test_df = pd.read_excel('./Test_data/LSTM_test_data/x_test10.xlsx', header=None, engine='openpyxl')
    y_dauid_test_df = pd.read_excel('./Test_data/LSTM_test_data/y_dauid_test10.xlsx', header=None, engine='openpyxl')
    y_category_test_df = pd.read_excel('./Test_data/LSTM_test_data/y_category_test10.xlsx', header=None, engine='openpyxl')

    # Calculate the original shape
    num_samples = x_test_df.shape[0] * x_test_df.shape[1] // (16 * 18)  # 16 timesteps, 18 features
    x_test = np.array(x_test_df).reshape(num_samples, 16, 18)  # Reshape to (num_samples, 16, 18)

    # Reshape y_dauid_test and y_category_test
    num_samples_y = y_dauid_test_df.shape[0] * y_dauid_test_df.shape[1] // (10 * 246)
    num_samples_y1 = y_category_test_df.shape[0] * y_category_test_df.shape[1] // (10 * 10)

    num_dauid_classes = len(label_encoder_dauid_new.classes_)
    num_category_classes = len(label_encoder_incident_category.classes_)

    y_dauid_test = np.array(y_dauid_test_df).reshape(num_samples_y, 10, num_dauid_classes)
    y_category_test = np.array(y_category_test_df).reshape(num_samples_y1, 10,  num_category_classes)


    return x_test, y_dauid_test, y_category_test

def load_data():
    global x_test_final, y_dauid_test_final, y_category_test_final
    x_test, y_dauid_test, y_category_test = load_initial_data()
    x_test_final = preprocess_data(x_test)
    y_dauid_test_final = y_dauid_test.astype('float32')
    y_category_test_final = y_category_test.astype('float32')

def preprocess_data(x_test):
    return x_test

def predict_future_steps(total_steps, initial_window):
    current_window = initial_window.copy()

    # Determine the number of full iterations of 4 steps and remaining steps
    full_iterations = total_steps // 10
    remaining_steps = total_steps % 10

    y_pred = None
    for _ in range(full_iterations):
        y_pred = model.predict(current_window)

        # Get predictions and concatenate them correctly
        new_prediction_da = np.argmax(y_pred[0][:10], axis=-1).reshape(10, 1)
        new_prediction_type = np.argmax(y_pred[1][:10], axis=-1).reshape(10, 1)
        new_predictions = np.concatenate([new_prediction_da, new_prediction_type], axis=-1)

        current_window = update_rolling_window(current_window, new_predictions)

    if remaining_steps > 0:
        y_pred = model.predict(current_window)

        # Get predictions for the remaining steps
        pred_da = np.argmax(y_pred[0][:10], axis=-1)
        pred_type = np.argmax(y_pred[1][:10], axis=-1)

        return pred_da, pred_type

    # Get the last set of 4 predictions
    pred_da = np.argmax(y_pred[0][:10], axis=-1)
    pred_type = np.argmax(y_pred[1][:10], axis=-1)

    return pred_da, pred_type

def update_rolling_window(window, new_predictions):
    num_features = window.shape[2]
    num_new_steps = new_predictions.shape[0]

    # Ensure new_predictions is reshaped correctly
    new_predictions_reshaped = new_predictions.reshape((num_new_steps, 2))

    # Shift the window and remove the oldest rows
    updated_window = np.roll(window, -num_new_steps, axis=1)

    # Insert the new rows at the end of the window in the first two features
    updated_window[0, -num_new_steps:, :2] = new_predictions_reshaped

    return updated_window

def calculate_accuracy():
    y_pred = model.predict(x_test_final)

    pred_da = np.argmax(y_pred[0], axis=-1)
    pred_type = np.argmax(y_pred[1], axis=-1)

    y_dauid_test_labels = np.argmax(y_dauid_test_final, axis=-1).flatten()
    y_category_test_labels = np.argmax(y_category_test_final, axis=-1).flatten()

    accuracy_da = np.mean(y_dauid_test_labels == pred_da.flatten())
    accuracy_type = np.mean(y_category_test_labels == pred_type.flatten())

    return accuracy_da, accuracy_type

load_data()

@bp.route('/predictions', methods=['GET'])
def get_predictions():
    target_date_str = request.args.get('date')
    try:
        # Parse the target date from ISO 8601 format
        target_date = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400

    # Make last_data_date offset-aware (UTC)
    last_data_date = datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    # Ensure target_date is also in UTC
    if target_date.tzinfo is None:
        target_date = target_date.replace(tzinfo=timezone.utc)

    if target_date <= last_data_date:
        return jsonify({"error": "Prediction for past dates not supported"}), 400

    delta_minutes = (target_date - last_data_date).total_seconds() / 60
    steps_to_predict = int(delta_minutes // 15)

    # Initialize the rolling window for each request
    initial_rolling_window = x_test_final[-1].reshape(1, 16, 18)

    # Predict future steps
    pred_da, pred_type = predict_future_steps(steps_to_predict, initial_rolling_window)

    # Select the final prediction based on the remainder
    remainder = steps_to_predict % 10

    if pred_da.size > 0:
        if remainder == 0:
            final_pred_da = (pred_da.flatten())[-1]
            final_pred_type = (pred_type.flatten())[-1]
        else:
            final_pred_da = (pred_da.flatten())[remainder - 1]
            final_pred_type = (pred_type.flatten())[remainder - 1]

    else:
        # Handle the case where pred_da is empty or does not have the expected elements
        final_pred_da = None
        print("Warning: pred_da has no elements.")

    next_pred_da_original = label_encoders['DAUID'].inverse_transform(final_pred_da.flatten()).tolist()
    next_pred_type_original = label_encoders['incident_category_description'].inverse_transform(final_pred_type.flatten()).tolist()

    accuracy_da, accuracy_type = calculate_accuracy()
    accuracy_da = f"{accuracy_da:.2f}"
    accuracy_type = f"{accuracy_type:.2f}"

    response = {
        "da_predictions": next_pred_da_original,
        "type_predictions": next_pred_type_original,
        "accuracy_da": accuracy_da,
        "accuracy_type": accuracy_type,
        "Prediction_date": target_date_str
    }
    return jsonify(response)