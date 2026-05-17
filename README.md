# Churn Prediction API

This project provides a RESTful API for predicting customer churn in the telecom sector. It uses a machine learning model trained on the `telecom_churn.csv` dataset to make predictions based on customer data.

## Features
- Train a churn prediction model using historical telecom data
- Expose a REST API for making churn predictions
- Simple and easy-to-use endpoints

## Split Architecture
- `backend/`: Flask API module that serves JSON from `/predict`
- `frontend/`: static dashboard UI hosted separately from the API
- `churn_model.pkl`: shared trained model used by the backend only

## Project Structure
- `app.py`: Thin wrapper that launches the backend API module
- `backend/app.py`: Main Flask API application
- `frontend/index.html`: Standalone dashboard entry point
- `frontend/app.js`: Browser logic for calling the API
- `frontend/styles.css`: Dashboard styling
- `train.py`: Script to train the machine learning model
- `telecom_churn.csv`: Dataset used for training
- `test_api.py`: Tests for the API endpoints
- `requirements.txt`: Python dependencies
- `Procfile`: For deployment (e.g., on Heroku)

## Getting Started

### Prerequisites
- Python 3.13.x
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/arunkg005/churn-prediction-api.git
   cd churn-prediction-api
   ```
2. Create and activate a fresh virtual environment with Python 3.13:
  ```bash
  python -m venv .venv
  ```
  On Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  On Windows Command Prompt:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
3. Upgrade pip and install dependencies:
   ```bash
  python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

> Note: this project is validated on Python 3.13. Using Python 3.14 on Windows may fail while building NumPy from source.

### Training the Model
Run the following command to train the model:
```bash
python train.py
```
This will generate a model file used by the API for predictions.

### Running the project
Use the local helper in [app.py](app.py) for development, or start the two modules separately:
```bash
python app.py backend
python app.py frontend
python app.py all
python -m http.server 3000 -d frontend
```

- `python app.py backend` starts the Flask API on `http://127.0.0.1:5000`
- `python app.py frontend` starts the dashboard UI on `http://127.0.0.1:3000`
- `python app.py all` starts both servers at once
- `python -m http.server 3000 -d frontend` starts the static UI without the helper

For production deployment, use the backend service and static UI separately. The backend should not serve the dashboard.

If you are using the virtual environment, run the command after activating it so the project uses the pinned dependencies.

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

### Deployment
- Deploy the Flask API as its own service with `gunicorn backend.app:app`.
- Keep the backend root and source the `requirements.txt` from the repository root, or use [render.yaml](render.yaml) for Render.
- Deploy the `frontend/` folder as a separate static site on Vercel, Netlify, or similar.
- On the Vercel site, save the Render API URL once in the dashboard's API URL field. The site stores it in browser local storage.
- You can also prefill the UI by opening it with `?apiUrl=https://your-api.onrender.com`.
- Keep the backend service API-only; the dashboard must not be served from Flask in production.
- Use the `Procfile` for the backend service on platforms like Render or Heroku.

## License
MIT License
