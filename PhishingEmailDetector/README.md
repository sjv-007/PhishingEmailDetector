# Phishing Email Detector (Starter)

This starter pack gives you a working **Streamlit app** that detects phishing-like emails using a small sample dataset.
You can replace the dataset with a larger one later and connect to Gmail via the Gmail API.

## Quick start (Windows)
```bat
cd PhishingEmailDetector
python -m pip install -r requirements.txt
python src\train_model.py
streamlit run app\phishing_email_app.py
```

If your folder path includes spaces or apostrophes, always wrap it in quotes:
```bat
cd "E:\Lord's programs\projects\PhishingEmailDetector"
```

## Where to put Gmail credentials
Place your downloaded Google OAuth file at:
```
PhishingEmailDetector/credentials/credentials.json
```

The first time you click **Fetch from Gmail** in the app, a browser window will ask you to authorize and will create:
```
PhishingEmailDetector/credentials/token.json
```

## Replace the sample dataset
Swap `data/sample_dataset.csv` with your own CSV (two columns required):
- `email_text`: the email body/content
- `label`: 1 for phishing, 0 for safe

Then retrain:
```bat
python src\train_model.py
```
