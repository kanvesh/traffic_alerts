from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Path to your service account key or credentials.json file
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build('drive', 'v3', credentials=credentials)

# Define the file to upload
file_metadata = {'name': 'my_file.csv'}
media = MediaFileUpload('my_file.csv', mimetype='text/csv')

# Upload the file
file = service.files().create(body=file_metadata,
                              media_body=media,
                              fields='id').execute()

print(f'File ID: {file.get("id")}')
