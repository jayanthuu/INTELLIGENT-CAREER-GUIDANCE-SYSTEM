
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset9000.csv")  # Replace with actual dataset file

# Separate features (X) and target (Y)
X = df.iloc[:, :-1]  # All columns except last
Y = df.iloc[:, -1]   # Last column (Target Role)

# Convert categorical data into numerical values using Label Encoding
label_encoders = {}
for column in X.columns:
    le = LabelEncoder()
    X.loc[:, column] = le.fit_transform(X[column])
    label_encoders[column] = le

# Encode target column
target_encoder = LabelEncoder()
Y = target_encoder.fit_transform(Y)

# Define model and cross-validation
model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=10)

kfold = model_selection.KFold(n_splits=10)

# Perform cross-validation
results = model_selection.cross_val_score(model, X, Y, cv=kfold)
print(f"Model Accuracy: {results.mean() * 100:.2f}%")
