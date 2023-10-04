import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# Email configuration
sender_email = 'cday@wfrc.org'
receiver_emails = [
    'cday@wfrc.org',
    "andyli@wfrc.org",
    "austin.feula@wcg.us",
    "awilding@utah.gov",
    "bbrady@summitcounty.org",
    "ben.swanson@wcg.us",
    "bgranberg@wfrc.org",
    "bhereth@wfrc.org",
    "blucas@hwlochner.com",
    "c.gresham@fehrandpeers.com",
    "callen@parametrix.com",
    "cworthen@wfrc.org",
    "dbassett@avenueconsultants.com",
    "erasband@utah.gov",
    "eray@rideuta.com",
    "ewing@arch.utah.edu",
    "fkiani@utah.gov",
    "future@xmission.com",
    #"gfarnsworth@utah.gov", #asked to be removed from email list
    "gregmacfarlane@byu.edu",
    "guang.tian@utah.edu",
    "ihartman@jub.com",
    "ihooper@avenueconsultants.com",
    "imanuel.aswandi@aecom.com",
    "jay.evans@rsginc.com",
    "jayson@horrocks.com",
    "jeff.gilbert@cachecounty.org",
    "jjohn@parametrix.com",
    "jlocquiao@rideuta.com",
    "josha@horrocks.com",
    "jreynolds@wfrc.org",
    "jsearle@wcecengineers.com",
    "jsonnen@jub.com",
    "jwadley@rideuta.com",
    "KellyNjord@gmail.com", #"kburns@utah.gov" -- wrong email
    "kdoane@rideuta.com",
    "kordel.braley@aecom.com",
    "kshabani@camsys.com",
    "ktohinaka@parametrix.com",
    "kvonarath@utah.gov",
    "kyle.cook@slcgov.com",
    "maren.outwater@rsginc.com",
    "mbrown@metroanalytics.com",
    "mdelora@mountainland.org",
    "mlee@fivecounty.utah.gov",
    "mlin@hwlochner.com",
    "nataliabrown@utah.gov",
    "ngayer@fivecounty.utah.gov",
    "patrick.singleton@usu.edu",
    "pukar.bhandari@outlook.com",
    "r.brockmyer@fehrandpeers.com",
    "sarah.hinners@redbutte.utah.edu",
    "sarah.hinners@utah.edu",
    "satomlin@utah.gov",
    "seliot@mountainland.org",
    "sswim@wfrc.org",
    "stephen.tuttle@rsginc.com",
    "t.baird@fehrandpeers.com",
    "thereth@mountainland.org",
    "tknowlton@wfrc.org",
    "utahmug@gmail.com",
    "vkornala@jub.com",
    "wbennion@wfrc.org"
]

#subject = "New Blog Post Alert"
subject = "New Blog Post Alert - WF TDM Version 9 What\'s New Doc"
message_body = """
Hey Model Users! <br><br>

A new blog post relating to the release of the WF TDM Version 9 What's New doc has been posted to the website. Check it out <a href="https://utahmug.org">here</a>. <br><br>

Thanks. <br><br>

<span style="font-size: 6; font-style: italic;">If you do not want to recieve email updates, please let Chris Day know at cday@wfrc.org and he will take you off the list of recipients.</span>
"""

# Set up Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        '_email/client_secrets.json', SCOPES, redirect_uri='https://localhost:8000')
    creds = flow.run_local_server(port=0)

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