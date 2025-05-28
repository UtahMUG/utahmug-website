import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


# Email configuration
sender_email = 'utahmug@gmail.com'

contacts = pd.read_csv('_email/contacts.csv')
contacts_mug = contacts[contacts['Label'].str.contains('MUG List', na=False)]
receiver_emails = contacts_mug['Email'].tolist()
#receiver_emails = ['cday@wfrc.org']

#subject = "New Blog Post Alert"
subject = "🚓 v911 Has Arrived – Call It In!"
message_body = """

Hello Model Patrol, <br/><br/>

The sirens are blaring —  Version 911 of the WF TDM is officially on the scene. No need to call for backup — it's already faster, sharper, and ready to enforce some serious modeling order. For the official briefing, head straight to the <a href="https://utahmug.org/v911-release/">blog post</a> on our website.<br/><br/>

Stay safe out there. Model responsibly. 🕶️ <br/><br/>

"""

# Set up Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        '_email/client_secrets.json', SCOPES, redirect_uri='http://localhost/8080') #maybe 8000
    creds = flow.run_local_server(port=8080)

# Save the credentials for the next run
with open('token.json', 'w') as token:
    token.write(creds.to_json())

# Create the Gmail service
service = build('gmail', 'v1', credentials=creds)

# Send the email to multiple recipients
for receiver_email in receiver_emails:
    # Create the email message using MIMEText
    message = MIMEText(message_body, 'html')
    message['to'] = receiver_email
    message['from'] = sender_email
    message['subject'] = subject

    # Encode the message as base64
    email_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        message = (service.users().messages().send(userId='me', body={'raw': email_message})
                   .execute())
        print(f"Email sent successfully to {receiver_email}.")
    except Exception as e:
        print(f"An error occurred while sending the email to {receiver_email}: {e}")

if os.path.exists('token.json'):
    os.remove('token.json')
    print("token.json file has been deleted.")