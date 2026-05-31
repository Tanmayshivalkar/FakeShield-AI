from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load trained model
model = pickle.load(open("fake_news_model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


@app.route("/")
def home():
    return "Fake News Detection API Running Successfully"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    news = data["news"]

    vector = vectorizer.transform([news])

    prediction = model.predict(vector)[0]

    confidence = max(model.predict_proba(vector)[0]) * 100

    if prediction == 0:
        result = "Fake News"
    else:
        result = "Real News"

    return jsonify({
        "prediction": result,
        "confidence": round(confidence, 2)
    })


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)