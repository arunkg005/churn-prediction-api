# Churn Prediction Dashboard

A churn prediction service for telecom customers, split into two separate parts:

- A Flask API that serves predictions from a trained machine learning model.
- A static dashboard UI that calls the API and shows the result visually.

The backend and frontend are deployed independently so the API behaves like a reusable service and the dashboard stays lightweight.

## Architecture

- `backend/` contains the Flask API.
- `frontend/` contains the static dashboard UI.
- `app.py` is a local helper for starting the backend, frontend, or both.
- `churn_model.pkl` is the saved model used by the API.

The dashboard connects to the API automatically. It does not ask the user for an API URL.

## Tech Stack

- Python 3.13.x
- Flask
- pandas
- numpy
- scikit-learn
- gunicorn for production serving
- Plain HTML, CSS, and JavaScript for the dashboard

## Project Files

- `backend/app.py`: Flask API with `/` and `/predict`
- `frontend/index.html`: Dashboard markup
- `frontend/app.js`: Dashboard behavior and API calls
- `frontend/styles.css`: Dashboard styling
- `frontend/config.js`: Fixed API base URL for the dashboard
- `app.py`: Local launcher for development
- `train.py`: Model training script
- `telecom_churn.csv`: Training dataset
- `test_api.py`: API smoke test
- `requirements.txt`: Runtime dependencies
- `Procfile`: Production start command for the API
- `render.yaml`: Render deployment config

## Getting Started

### Prerequisites

- Python 3.13.x
- pip

> This project was validated on Python 3.13.3. Python 3.14 on Windows can fail while building NumPy from source.

### Clone the repository

```bash
git clone https://github.com/arunkg005/churn-prediction-api.git
cd churn-prediction-api
```

### Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run Locally

### Start the API only

```bash
python app.py backend
```

This starts the Flask API on `http://127.0.0.1:5000`.

### Start the dashboard only

```bash
python app.py frontend
```

This serves the static dashboard on `http://127.0.0.1:3000`.

### Start both together

```bash
python app.py all
```

This launches the backend API and the frontend dashboard at the same time.

### Alternative static frontend server

```bash
python -m http.server 3000 -d frontend
```

## API

### Health check

`GET /`

Returns a simple JSON status response.

### Prediction

`POST /predict`

Send a JSON body with the customer fields used by the model.

Example:

```json
{
  "gender": "Male",
  "Partner": "No",
  "Dependents": "No",
  "PhoneService": "Yes",
  "MultipleLines": "Yes",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "Yes",
  "StreamingMovies": "Yes",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "tenure": 5,
  "MonthlyCharges": 95.2,
  "TotalCharges": 476
}
```

The response includes the churn prediction and a risk score.

## Train the Model

If you want to retrain the model from the dataset, run:

```bash
python train.py
```

This generates the `churn_model.pkl` file consumed by the API.

## Test the API

```bash
python test_api.py
```

This performs a smoke test against the health and prediction endpoints.

## Deployment

### Backend API on Render

- Start command: `gunicorn backend.app:app`
- Use the repository root `requirements.txt`
- Keep the API service separate from the frontend

The backend is deployed as a standalone Flask service. It should not serve the dashboard in production.

### Frontend dashboard on Vercel

- Deploy the `frontend/` folder as a static site
- The dashboard is preconfigured to call the Render API URL
- No runtime API URL input is required from the user

### Process files

- `Procfile` is included for platform compatibility
- `render.yaml` contains the Render service definition

## Notes

- The dashboard uses short helper notes on each input to explain what the field means and how it affects churn risk.
- The UI is intentionally separate from the API so the backend can be reused independently.
- The frontend shows connection status automatically on load.
