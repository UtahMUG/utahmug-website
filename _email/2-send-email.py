import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


# Email configuration
sender_email = 'cday@wfrc.org'

contacts = pd.read_csv('_email/contacts.csv')
contacts_mug = contacts[contacts['Label'].str.contains('MUG List', na=False)]
receiver_emails = contacts_mug['Email'].tolist()
#receiver_emails = ['cday@wfrc.org']

#subject = "New Blog Post Alert"
subject = "Spuds, Stats, and Surveys—A Thanksgiving Treat!"
message_body = """

🦃🍂 Hello, Mashed Potato Modelers! 🍂🦃 <br/><br/>

We’re grateful to announce that the v9.1.0 validation report is hot out of the oven and ready for your review! 🥧 Dive into the delicious details <a href="https://wfrc.org/wftdm-docs/v9x/v910/validation/1-distribute.html">here</a> or view the <a href="https://utahmug.org/v910-release/">blog post</a>. <br/><br/> 

While you’re savoring the latest report, we’d love to hear how you’re using the new release. Please take a moment to fill out this <a href="https://forms.gle/oT8oET1yChgqpwbG7">survey</a> and share your thoughts—it’s the perfect side dish! The survey is also located on our <a href="https://utahmug.org/v910-survey/">website</a>. <br/><br/> 

Wishing you a bountiful Thanksgiving and a season full of data-driven success! <br/><br/>

🦃🍁🥧🍂📊🦃🍁🥧🍂<br/><br/>

<span style="font-size: 6; font-style: italic;">If you do not want to receive email updates, please let Chris Day know at cday@wfrc.org and he will take you off the list of recipients.</span>
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