import os
import joblib
from src.data_preprocessing import clean_text

MODEL_PATH = os.path.join('models', 'phishing_model.pkl')
VECT_PATH = os.path.join('models', 'vectorizer.pkl')

def _load():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH)):
        raise FileNotFoundError('Model/vectorizer not found. Run: python src/train_model.py')
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECT_PATH)
    return model, vectorizer

def predict_email(email: str) -> str:
    model, vectorizer = _load()
    cleaned = clean_text(email)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    return "🚨 Phishing" if int(pred) == 1 else "✅ Safe"
