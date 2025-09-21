import os
import streamlit as st
from src.predict import predict_email
try:
    from src.gmail_api import fetch_latest_emails
    GMAIL_READY = True
except Exception as e:
    GMAIL_READY = False

st.set_page_config(page_title='Phishing Email Detector', page_icon='📧', layout='centered')
st.title('📧 Phishing Email Detector')

mode = st.radio('Choose Mode', ['Manual Input', 'Fetch from Gmail'])

if mode == 'Manual Input':
    email_text = st.text_area('Paste email content here', height=200)
    if st.button('Check Email'):
        if email_text.strip():
            result = predict_email(email_text)
            st.success(result) if 'Safe' in result else st.error(result)
        else:
            st.warning('Please enter some text.')

else:
    if not GMAIL_READY:
        st.warning('Gmail libraries not available. Ensure requirements are installed.')
    cred_exists = os.path.exists(os.path.join('credentials','credentials.json'))
    if not cred_exists:
        st.info('Add your Google OAuth file to credentials/credentials.json to enable Gmail fetch.')
    if st.button('Fetch Latest Emails', disabled=not (GMAIL_READY and cred_exists)):
        emails = fetch_latest_emails(5)
        if not emails:
            st.write('No messages found.')
        for e in emails:
            st.subheader(e['subject'])
            st.write(e['body'][:1000] + ('...' if len(e['body'])>1000 else ''))
            res = predict_email(e['body'])
            st.success(res) if 'Safe' in res else st.error(res)
