from __future__ import annotations
import os, base64
from typing import List, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    token_path = os.path.join('credentials', 'token.json')
    cred_path = os.path.join('credentials', 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(cred_path):
                raise FileNotFoundError('Missing credentials/credentials.json. Add your OAuth client file.')
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_latest_emails(max_results: int = 5) -> List[Dict[str, Any]]:
    service = get_service()
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    out = []
    for m in messages:
        msg = service.users().messages().get(userId='me', id=m['id']).execute()
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')

        body_text = ""
        def decode_data(data):
            return base64.urlsafe_b64decode(data).decode(errors='ignore')

        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data')
                    if data:
                        body_text += decode_data(data)
        else:
            data = payload.get('body', {}).get('data')
            if data:
                body_text = decode_data(data)

        out.append({'subject': subject, 'body': body_text})
    return out
