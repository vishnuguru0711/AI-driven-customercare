import pandas as pd
import re
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Ensure NLTK resources are available
nltk.download('punkt')

# Sample dataset (Modify this to read from your dataset file)
conversations = [
    {"Conversation ID": "TECH_001", "Category": "Technical Support", "Sentiment": "Frustrated", "Priority": "High",
     "Customer": "Hi there! I’ve been trying to install the latest update for hours. It keeps failing at 75%. What’s wrong?",
     "Agent": "This is a known conflict with antivirus tools. Try disabling antivirus and retry."},

    {"Conversation ID": "TECH_002", "Category": "Technical Support", "Sentiment": "Confused", "Priority": "Medium",
     "Customer": "My app says ‘no internet connection,’ but Wi-Fi is working fine. Other apps work normally.",
     "Agent": "Check app’s network permissions and clear cache."},

    {"Conversation ID": "TECH_003", "Category": "Technical Support", "Sentiment": "Annoyed", "Priority": "Critical",
     "Customer": "Your app crashes when I connect my older thermostat. It worked on my old phone!",
     "Agent": "HT-2019 isn’t supported in newer versions. You can downgrade the app or get a discount."}
]

# Convert to DataFrame
df = pd.DataFrame(conversations)

# Extract Features and Labels
X = df["Customer"]  # Customer's query as input
y = df["Category"]  # Predict category as output

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorizer + Naive Bayes Classifier Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# Train Model
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "chatbot_model.pkl")
print("Chatbot Model Trained & Saved Successfully!")
