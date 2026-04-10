from flask import Flask, jsonify, Blueprint
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score
import pickle
import numpy as np
from flask_jwt_extended import jwt_required
from sklearn.preprocessing import LabelEncoder

bp = Blueprint('prophet', __name__, url_prefix='/prophet')

with open('./Trained_models/Prophet/model_proph_dauid.pkl', 'rb') as f:
    model_dauid = pickle.load(f)
    
with open('./Trained_models/Prophet/model_proph_category.pkl', 'rb') as f:
    model_category = pickle.load(f)
    
with open('./Trained_models/Prophet/label_proph_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

# Load the test data
test_dauid = pd.read_csv('./Test_data/proph_test_dauid.csv')
test_category = pd.read_csv('./Test_data/proph_test_category.csv')


# API endpoint for prediction using predefined test data
@bp.route('/predict-prophet', methods=['GET'])
@jwt_required()
def predict():
    # Preparing the future dataframe for Prophet prediction
    future_dauid = model_dauid.make_future_dataframe(periods=len(test_dauid), freq='H', include_history=False)
    future_category = model_category.make_future_dataframe(periods=len(test_category), freq='H', include_history=False)
    
    # Predicting DAUID and Category
    forecast_dauid = model_dauid.predict(future_dauid)
    predicted_dauid = forecast_dauid['yhat'].iloc[-len(test_dauid):].values
    forecast_category = model_category.predict(future_category)
    predicted_category = forecast_category['yhat'].iloc[-len(test_category):].values
    
    true_dauid = test_dauid['y'].values
    true_category = test_category['y'].values
    
    # Calculating evaluation metrics
    mse_dauid = mean_squared_error(true_dauid, predicted_dauid)
    mae_dauid = mean_absolute_error(true_dauid, predicted_dauid)
    mse_category = mean_squared_error(true_category, predicted_category)
    mae_category = mean_absolute_error(true_category, predicted_category)
    accuracy_category = accuracy_score(true_category, predicted_category.round().astype(int))
    
    # Calculating directional accuracy for DAUID
    test_dauid['yhat'] = predicted_dauid
    test_dauid['correct_direction'] = np.sign(test_dauid['y'].diff().fillna(0)) == np.sign(test_dauid['yhat'].diff().fillna(0))
    directional_accuracy_dauid = test_dauid['correct_direction'].mean()
    
    # Predicting the next DAUID and Category
    future_dauid_next = model_dauid.make_future_dataframe(periods=1, freq='H', include_history=False)
    future_category_next = model_category.make_future_dataframe(periods=1, freq='H', include_history=False)
    next_dauid = model_dauid.predict(future_dauid_next)['yhat'].iloc[-1]
    next_category = model_category.predict(future_category_next)['yhat'].iloc[-1]

    pred_dauid_label = label_encoders['DAUID'].inverse_transform([int(next_dauid)])[0]
    pred_category_label = label_encoders['incident_category_description'].inverse_transform([int(next_category)])[0]
    
    directional_accuracy_dauid = f"{directional_accuracy_dauid:.2f}"
    accuracy_category = f"{accuracy_category:.2f}"
    
    response = {
        'next_dauid': int(pred_dauid_label),
        'next_category': pred_category_label,
        'dauid_mse': mse_dauid,
        'dauid_mae': mae_dauid,
        'dauid_directional_accuracy': directional_accuracy_dauid,
        'category_mse': mse_category,
        'category_mae': mae_category,
        'category_accuracy': accuracy_category
    }
    return jsonify(response)
