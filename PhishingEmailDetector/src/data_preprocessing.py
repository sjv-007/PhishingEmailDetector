import string
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are available
try:
    _ = stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = ''.join(ch for ch in text if ch not in string.punctuation)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)
