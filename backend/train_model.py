# ============================================
# FAKE NEWS DETECTION USING NLP
# ============================================

# Import Libraries
import pandas as pd
import numpy as np
import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Download NLTK stopwords
nltk.download('stopwords')

# ============================================
# STEP 1: LOAD DATASET
# ============================================

# Read Fake News Dataset
fake_data = pd.read_csv("dataset/Fake.csv")

# Read True News Dataset
true_data = pd.read_csv("dataset/True.csv")

# Add Labels
# 0 = Fake News
# 1 = Real News

fake_data["label"] = 0
true_data["label"] = 1

# Combine Both Datasets
data = pd.concat([fake_data, true_data], axis=0)

# Shuffle Dataset
data = data.sample(frac=1, random_state=42)

# Reset Index
data.reset_index(drop=True, inplace=True)

# Keep only required columns
data = data[["text", "label"]]

print("Dataset Loaded Successfully")
print(data.head())

# ============================================
# STEP 2: TEXT PREPROCESSING
# ============================================

# Initialize Stemmer
stemmer = PorterStemmer()

# Load Stopwords
stop_words = set(stopwords.words("english"))

# Function for Cleaning Text
def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Tokenization
    words = text.split()

    # Remove stopwords and stemming
    words = [stemmer.stem(word) for word in words if word not in stop_words]

    return " ".join(words)

# Apply preprocessing
data["text"] = data["text"].apply(preprocess_text)

print("\nText Preprocessing Completed")

# ============================================
# STEP 3: SPLIT DATA
# ============================================

# Input Features
X = data["text"]

# Output Labels
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining Data Size:", X_train.shape)
print("Testing Data Size:", X_test.shape)

# ============================================
# STEP 4: TF-IDF VECTORIZATION
# ============================================

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1,2)
)

# Convert text into numerical vectors
X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

print("\nText Vectorization Completed")

# ============================================
# STEP 5: TRAIN MODEL
# ============================================

# Logistic Regression Model
model = LogisticRegression()

# Train Model
model.fit(X_train_vector, y_train)

print("\nModel Training Completed")

# ============================================
# STEP 6: TEST MODEL
# ============================================

# Predict on test data
y_pred = model.predict(X_test_vector)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

# Classification Report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ============================================
# STEP 7: CUSTOM NEWS PREDICTION
# ============================================

def predict_news(news):

    # Preprocess News
    news = preprocess_text(news)

    # Convert into vector
    vector_input = vectorizer.transform([news])

    # Predict
    prediction = model.predict(vector_input)

    if prediction[0] == 0:
        print("\nPrediction: Fake News")
    else:
        print("\nPrediction: Real News")

# ============================================
# STEP 8: TEST CUSTOM INPUT
# ============================================

sample_news = """
NASA confirms that aliens have landed in New York City.
"""

predict_news(sample_news)

import pickle

# Save trained model
pickle.dump(model, open("fake_news_model.pkl", "wb"))

# Save TF-IDF vectorizer
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\nModel and Vectorizer Saved Successfully")