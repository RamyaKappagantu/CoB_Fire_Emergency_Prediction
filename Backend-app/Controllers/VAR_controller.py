from flask import jsonify, Blueprint
import numpy as np
import pickle
import pandas as pd
from sklearn.metrics import mean_absolute_error
from flask_jwt_extended import jwt_required

bp = Blueprint('VAR_prediction', __name__, url_prefix='/VAR_prediction')

with open('./Trained_models/var_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
with open('./Trained_models/var_model.pkl', 'rb') as f:
    model = pickle.load(f)

X_train = pd.read_csv('./var_data/train_data.csv')
X_test = pd.read_csv('./var_data/test_data.csv')

def next_10_predictions():
    lag = model.k_ar
    prediction = model.forecast(X_train.values[-lag:], steps=10)
    prediction_df = pd.DataFrame(prediction, index=X_test[0:10].index, columns=X_train.columns)
    pred_da = prediction_df['DAUID'].apply(np.floor)
    pred_type = prediction_df['incident_category_description'].apply(np.ceil).astype('int64')

    return pred_da, pred_type

def calculate_accuracy(pred_da, pred_type):
    true_da = X_test['DAUID'][0:10]
    true_type = X_test['incident_category_description'][0:10]

    accuracy_da = mean_absolute_error(true_da, pred_da)
    accuracy_type = mean_absolute_error(true_type, pred_type)

    return accuracy_da, accuracy_type

@bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    pred_da, pred_type = next_10_predictions()
    next_10_da_original = pred_da.to_list()
    next_10_type_original = label_encoder.inverse_transform(pred_type).tolist()

    accuracy_da, accuracy_type = calculate_accuracy(pred_da, pred_type)

    response = {
        'da_predictions': next_10_da_original,
        'type_predictions': next_10_type_original,
        'accuracy_da': accuracy_da,
        'accuracy_type': accuracy_type
    }
    return jsonify(response)