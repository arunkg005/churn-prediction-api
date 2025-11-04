import requests

# The URL of our local API endpoint
URL = 'http://127.0.0.1:5000/predict'

# A sample customer's data.
# This dictionary must contain all the features your model was trained on.
# This sample is a customer who just joined and is on a month-to-month contract.
sample_customer = {
    "gender": "Female",
    "Partner": "No",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "tenure": 1,
    "MonthlyCharges": 70.70,
    "TotalCharges": 70.70
}

# Send a POST request to the API with the customer's data in JSON format
try:
    response = requests.post(URL, json=sample_customer)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Print the JSON response from the API
    print("API Response:")
    print(response.json())

except requests.exceptions.ConnectionError:
    print(f"Error: Could not connect to the API at {URL}.")
    print("Please ensure your 'app.py' server is running in another terminal.")
except Exception as e:
    print(f"An error occurred: {e}")
    