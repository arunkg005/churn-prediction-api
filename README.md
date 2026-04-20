# Churn Prediction API

This project provides a RESTful API for predicting customer churn in the telecom sector. It uses a machine learning model trained on the `telecom_churn.csv` dataset to make predictions based on customer data.

## Features
- Train a churn prediction model using historical telecom data
- Expose a REST API for making churn predictions
- Simple and easy-to-use endpoints

## Project Structure
- `app.py`: Main Flask API application
- `train.py`: Script to train the machine learning model
- `telecom_churn.csv`: Dataset used for training
- `test_api.py`: Tests for the API endpoints
- `requirements.txt`: Python dependencies
- `Procfile`: For deployment (e.g., on Heroku)

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/arunkg005/churn-prediction-api.git
   cd churn-prediction-api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Training the Model
Run the following command to train the model:
```bash
python train.py
```
This will generate a model file used by the API for predictions.

### Running the API
Start the Flask API server:
```bash
python app.py
```
The API will be available at `http://localhost:5000/`.

### API Usage
- **POST /predict**: Predict churn for a customer.
  - Request: JSON with customer features
  - Response: JSON with churn prediction

Example request:
```json
{
  "feature1": value1,
  "feature2": value2,
  ...
}
```

### Testing
Run the API tests with:
```bash
python test_api.py
```

## Deployment
This project includes a `Procfile` for easy deployment to platforms like Heroku.

## License
MIT License
