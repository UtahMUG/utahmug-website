from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes your application requires
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  # Example scope for sending emails via Gmail

def main():
    # Load the credentials from the downloaded client_secret.json file
    flow = InstalledAppFlow.from_client_secrets_file(
        'E:/GitHub/utahmug-website/_email/client_secrets.json', SCOPES)

    # Run the flow to get the credentials, with access_type specified for offline access
    creds = flow.run_local_server(port=0, access_type='offline')

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Now you can use creds to access Google APIs
    print("Authentication successful!")

if __name__ == '__main__':
    main()
