from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / 'churn_model.pkl'

app = Flask(__name__)

FEATURE_ORDER = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
    'PaymentMethod', 'tenure', 'MonthlyCharges', 'TotalCharges'
]

FEATURE_SPECS = {
    'gender': {'type': 'select', 'default': 'Female'},
    'Partner': {'type': 'select', 'default': 'No'},
    'Dependents': {'type': 'select', 'default': 'No'},
    'PhoneService': {'type': 'select', 'default': 'Yes'},
    'MultipleLines': {'type': 'select', 'default': 'No'},
    'OnlineSecurity': {'type': 'select', 'default': 'No'},
    'OnlineBackup': {'type': 'select', 'default': 'No'},
    'DeviceProtection': {'type': 'select', 'default': 'No'},
    'TechSupport': {'type': 'select', 'default': 'No'},
    'StreamingTV': {'type': 'select', 'default': 'No'},
    'StreamingMovies': {'type': 'select', 'default': 'No'},
    'Contract': {'type': 'select', 'default': 'Month-to-month'},
    'PaperlessBilling': {'type': 'select', 'default': 'Yes'},
    'PaymentMethod': {'type': 'select', 'default': 'Electronic check'},
    'tenure': {'type': 'number', 'default': 1},
    'MonthlyCharges': {'type': 'number', 'default': 70.70},
    'TotalCharges': {'type': 'number', 'default': 70.70},
}

try:
    model = joblib.load(MODEL_PATH)
    print('Model loaded successfully.')
except FileNotFoundError as exc:
    raise FileNotFoundError(
        "Model file 'churn_model.pkl' not found. Please run train.py first."
    ) from exc


def build_customer_payload(raw_data):
    payload = {}

    for field_name, spec in FEATURE_SPECS.items():
        if field_name not in raw_data:
            raise ValueError(f'Missing required field: {field_name}')

        value = raw_data[field_name]
        if spec['type'] == 'number':
            if value in (None, ''):
                raise ValueError(f'Missing required field: {field_name}')
            payload[field_name] = int(float(value)) if field_name == 'tenure' else float(value)
            continue

        text_value = str(value).strip()
        if not text_value:
            raise ValueError(f'Missing required field: {field_name}')
        payload[field_name] = text_value

    return payload


def predict_customer(customer_data):
    customer_frame = pd.DataFrame(
        [[customer_data[field_name] for field_name in FEATURE_ORDER]],
        columns=FEATURE_ORDER,
    )
    prediction = model.predict(customer_frame)
    probability = float(model.predict_proba(customer_frame)[0][1])

    return {
        'churn_prediction': int(prediction[0]),
        'churn_probability': f'{probability:.4f}',
        'risk_label': 'High risk' if probability >= 0.5 else 'Lower risk',
        'risk_class': 'high' if probability >= 0.5 else 'low',
        'risk_percent': round(probability * 100, 1),
    }


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Churn Prediction API is live!'}), 200


@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return ('', 204)

    try:
        raw_payload = request.get_json(silent=True)
        if raw_payload is None:
            raw_payload = request.form.to_dict()

        customer_data = build_customer_payload(raw_payload)
        return jsonify(predict_customer(customer_data))

    except Exception as exc:
        return jsonify({'error': str(exc)}), 400


if __name__ == '__main__':
    app.run(debug=True)