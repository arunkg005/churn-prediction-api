import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# --- 1. Load Data ---
try:
    df = pd.read_csv('telecom_churn.csv')
except FileNotFoundError:
    print("Dataset not found. Please download 'telecom_churn.csv' and place it in the project folder.")
    exit()

print("Data loaded successfully.")

# --- 2. Data Cleaning & Preprocessing ---

# Drop customerID as it's just an identifier
df = df.drop('customerID', axis=1)

# Convert TotalCharges to numeric, coercing errors (like empty strings) to NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Convert our target variable 'Churn' to 1 (Yes) or 0 (No)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# --- 3. Define Features (X) and Target (y) ---

# We'll drop rows with any missing values for simplicity in this project
df = df.dropna()

X = df.drop('Churn', axis=1)
y = df['Churn']

# --- 4. Identify Feature Types ---
# We need to tell our pipeline which columns are numbers and which are categories

# Numeric features to be scaled
numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']

# Categorical features to be one-hot encoded
categorical_features = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod'
]

# --- 5. Create the Preprocessing Pipeline ---

# Create a transformer for numeric features
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Create a transformer for categorical features
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # handle_unknown='ignore' is crucial for new data
])

# Bundle preprocessing for numeric and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# --- 6. Create the Full Model Pipeline ---

# We will use Logistic Regression for our model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

# --- 7. Split Data and Train Model ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- 8. Evaluate Model (Optional but good) ---
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# --- 9. Save the Model ---
joblib.dump(model, 'churn_model.pkl')
print("Model saved successfully as 'churn_model.pkl'")