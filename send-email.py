import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# Email configuration
sender_email = 'cday@wfrc.org'  # Replace with your Gmail email address
receiver_email = 'cday@wfrc.org'
subject = "New Blog Post Alert"
message_body  = """
Hey Model Users! <br><br>

A new blog post has been posted to the website. See <a href="https://utahmug.org">here</a>. <br><br>

Thank you.
"""

# Create the email message using MIMEText
message = MIMEText(message_body, 'html')
message['to'] = receiver_email
message['from'] = sender_email
message['subject'] = subject

# Encode the message as base64
email_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

# Set up Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', SCOPES, redirect_uri = 'https://localhost:8000')
    creds = flow.run_local_server(port=0)

# Save the credentials for the next run
with open('token.json', 'w') as token:
    token.write(creds.to_json())

# Create the Gmail service
service = build('gmail', 'v1', credentials=creds)

# Send the email
try:
    message = (service.users().messages().send(userId='me', body={'raw': email_message})
              .execute())
    print("Email sent successfully.")
except Exception as e:
    print(f"An error occurred: {e}")