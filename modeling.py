# This script trains a simple regression model to predict Airbnb listing prices
# using cleaned data. It uses scikit-learn's RandomForestRegressor.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("data/clean_airbnb.csv")

# Select features and target variable
features = ["room_type", "neighbourhood", "bedrooms", "beds", "baths", "availability_365", "number_of_reviews"]
target = "price"

X = df[features]
y = df[target]

X = X.dropna()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical = ["room_type", "neighbourhood"]
numeric = ["bedrooms", "beds", "baths", "availability_365", "number_of_reviews"]

preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown='ignore'), categorical)],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Model trained. Mean Absolute Error: ${mae:.2f}")
