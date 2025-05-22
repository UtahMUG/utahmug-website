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
#receiver_emails = contacts_mug['Email'].tolist()
receiver_emails = ['bhereth@wfrc.org']

#subject = "New Blog Post Alert"
subject = "UtahMUG Blog Post Alert: MoMo 2025 - Early Bird Registration Ends June 1!"
message_body = """

    <p>Hi Utah Model User,</p>

    <p>A quick reminder that <strong>early bird registration</strong> for <a href="https://modelingmobility.org">2025 Modeling Mobility Conference</a> ends on <strong>June 1</strong>!</p>

    <p>The conference takes place <strong>September 14-17, 2025</strong>, in Minneapolis, and brings together transportation modelers, data analysts, and planners from across the country.</p>

    <p>We've posted more details and the flyer on the Utah Model Users Group site: <a href="https://utahmug.org/momo-early-bird/">Read the announcement and download the flyer</a></p>

    <p>Please feel free to forward this to others in your network who may be interested.</p>
    
    <p>Let's help Utah show up strong at MoMo 2025!</p>

    <p>Thanks,<br>Bill Hereth<br>Wasatch Front Regional Council</p>

    <p><em>To remove yourself from the UtahMUG list, please email Chris Day at <a href="mailto:cday@wfrc.org">cday@wfrc.org</a>.</em></p>

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