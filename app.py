import joblib
import pandas as pd
from flask import Flask, request, jsonify

# 1. Initialize Flask App
app = Flask(__name__)

# 2. Load Your Model
# Load the pipeline model you saved in train.py
try:
    model = joblib.load('churn_model.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model file 'churn_model.pkl' not found. Please run train.py first.")
    exit()

# 3. Define a "Home" Route
# This is just a simple route to check if your API is running.
@app.route('/')
def home():
    return "Churn Prediction API is live!"

# 4. Define the "Predict" Route
# This is the main route that will receive data and return a prediction.
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data sent from the request
        json_data = request.json
        
        # The data should be a dictionary. We convert it to a DataFrame
        # because our pipeline (preprocessor) expects it.
        # We use [0] because we are predicting for one customer at a time.
        df = pd.DataFrame(json_data, index=[0])
        
        # --- Data Validation (Optional but good) ---
        # You can add checks here to ensure all required columns are present
        
        # Make a prediction using the loaded model
        prediction = model.predict(df)
        
        # Get the probability of churn (class 1)
        # model.predict_proba(df) returns probabilities for [class 0, class 1]
        probability = model.predict_proba(df)[0][1] 
        
        # Convert prediction (numpy int) to a standard Python int
        output = int(prediction[0])
        
        # Return the prediction and probability as a JSON response
        return jsonify({
            'churn_prediction': output,  # 1 for Yes, 0 for No
            'churn_probability': f"{probability:.4f}"
        })

    except Exception as e:
        # Handle any errors that occur during the process
        return jsonify({'error': str(e)}), 400

# 5. Run the App
# This block ensures the app runs only when you execute "python app.py"
if __name__ == '__main__':
    # 'debug=True' means the server will auto-reload when you save changes
    app.run(debug=True)