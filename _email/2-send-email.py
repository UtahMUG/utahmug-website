import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


# Email configuration
sender_email = 'bhereth@wfrc.org'

contacts = pd.read_csv('_email/contacts.csv')
contacts_mug = contacts[contacts['Label'].str.contains('MUG List', na=False)]
#receiver_emails = contacts_mug['Email'].tolist()
receiver_emails = ['bhereth@wfrc.org']

#subject = "New Blog Post Alert"
subject = "MoMo 2025 - A New Conference for Transportation Modelers"
message_body = """

<p>Dear Utah Model Users Group,</p>

<p>I wanted to share some information about the <strong>Modeling Mobility Conference (MoMo 2025)</strong>, a new event that fills the current gap left by TRB's <strong>Tools of the Trade</strong> and <strong>Innovations in Travel Analysis and Planning</strong> conferences. With TRB pausing sponsorship of these practitioner-focused events, MoMo was created to provide a dedicated space for transportation modelers, planners, and data analysts to connect, share insights, and advance analytical tools for real-world decision-making.</p>

<p>The first MoMo conference will take place <strong>September 14-17, 2025, in Minneapolis, Minnesota</strong>, at the <strong>McNamara Alumni Center, University of Minnesota</strong>. Organized by a volunteer-led planning committee and sponsored by the <strong>Zephyr Foundation</strong>, the conference will feature sessions, workshops, and networking opportunities aimed at supporting the modeling community.</p>

<p>For more details, including updates on the <strong>call for abstracts (due by February 21)</strong> and for future registration information, visit <a href="https://modelingmobility.org">ModelingMobility.org</a>.</p>

<p>Best,<br/>
Bill Hereth<br/>
https://utahmug.org/momo/</p>

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