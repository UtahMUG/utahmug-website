import os.path
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

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

service = build('people', 'v1', credentials=creds)

# Retrieve the contact groups to get the label ID for "Test Contacts"
groups = service.contactGroups().list(pageSize=200).execute()
contact_groups = groups.get('contactGroups', [])

label_id = None
label_name = 'MUG List'  # Define your label name here
for group in contact_groups:
    if group['name'] == label_name:  # Specify the label name here
        label_id = group['resourceName']
        break

if label_id is None:
    print(f"Label '{label_name}' not found.")

# Call the People API to list all contacts
results = service.people().connections().list(
    resourceName='people/me',
    pageSize=1000,  # Change this as needed
    personFields='names,emailAddresses,memberships').execute()

# Print and save the contact names, email addresses, and label
connections = results.get('connections', [])
contact_list = []
if not connections:
    print('No connections found.')
else:
    for person in connections:
        names = person.get('names', [])
        emails = person.get('emailAddresses', [])
        memberships = person.get('memberships', [])
        # Check if the contact is a member of the "Test Contacts" group
        if memberships:
            for membership in memberships:
                if membership.get('contactGroupMembership', {}).get('contactGroupResourceName') == label_id:
                    if names and emails:
                        name = names[0].get('displayName')
                        email = emails[0].get('value')
                        contact_list.append((name, email, label_name))  # Add the label name to the contact
                        print(f'Name: {name}, Email: {email}, Label: {label_name}')
                    break

# Save contacts to CSV
with open('_email/contacts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Email', 'Label'])  # Include label in the header
    writer.writerows(contact_list)


if os.path.exists('token.json'):
    os.remove('token.json')
    print("token.json file has been deleted.")