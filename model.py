import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("Historical_ticket_data.csv")  # Update with your file path

# Clean column names
df.columns = df.columns.str.strip()
print("Cleaned Column Names:", df.columns)

# Remove leading/trailing spaces from all string values
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Check for missing values
print("Missing Values in Each Column:\n", df.isnull().sum())

# Print unique values in 'Resolution Status'
print("Unique values in 'Resolution Status':\n", df["Resolution Status"].value_counts())

# Strip spaces from 'Resolution Status'
df["Resolution Status"] = df["Resolution Status"].str.strip()
print("After stripping spaces:", df["Resolution Status"].unique())

# Define target variable
y = df["Resolution Status"]  # Target variable

# Drop target column to get features
X = df.drop(columns=["Resolution Status"])  # Features

# Identify categorical columns in features
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
print("Categorical Columns:", categorical_cols)

# Apply One-Hot Encoding to categorical columns
column_transformer = ColumnTransformer(
    transformers=[("encoder", OneHotEncoder(handle_unknown="ignore"), categorical_cols)],
    remainder="passthrough"
)

# Apply transformation
X = column_transformer.fit_transform(X)
print("Encoding successful!")

# Apply SMOTE only if more than one class exists in 'y'
if len(np.unique(y)) > 1:
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)
    print("SMOTE applied successfully!")
else:
    print("Skipping SMOTE due to a single class in target variable.")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Model evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Plot distribution of 'Solution'
plt.figure(figsize=(12,6))
sns.barplot(x=pd.Series(df["Solution"]).value_counts().index, 
            y=pd.Series(df["Solution"]).value_counts().values)
plt.xticks(rotation=90)
plt.title("Distribution of Solutions")
plt.show()


joblib.dump(model, "final_model.pkl")  
print("Model saved successfully!")