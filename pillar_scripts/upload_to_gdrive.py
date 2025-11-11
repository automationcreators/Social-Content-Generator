#!/usr/bin/env python3
"""
Upload social media scripts to Google Drive folder.

Usage:
    python upload_to_gdrive.py social_media_scripts_2025-11-10.md
    python upload_to_gdrive.py  # Uploads all *_2025-*.md files
"""

import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# If modifying these scopes, delete token.pickle
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Google Drive folder ID (Boring Business AI - Social Scripts)
FOLDER_ID = '1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx'

# Credentials location
CREDENTIALS_DIR = Path.home() / 'Documents/claudec/systems/skills-main/boring-business-brand/credentials'
CREDENTIALS_FILE = CREDENTIALS_DIR / 'google-drive-credentials.json'
TOKEN_FILE = CREDENTIALS_DIR / 'token.pickle'


def authenticate():
    """Authenticate and return Google Drive service."""
    creds = None

    # Load existing token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"Error: Credentials file not found at {CREDENTIALS_FILE}")
                print("\nSetup Instructions:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project and enable Google Drive API")
                print("3. Create OAuth 2.0 credentials (Desktop app)")
                print("4. Download JSON and save as:")
                print(f"   {CREDENTIALS_FILE}")
                print("\nSee GOOGLE_DRIVE_INTEGRATION.md for detailed instructions.")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def upload_file(service, file_path, folder_id=FOLDER_ID):
    """Upload a file to Google Drive folder."""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return None

    # Check if file already exists in folder
    file_name = file_path.name
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    existing_files = results.get('files', [])

    if existing_files:
        # Update existing file
        file_id = existing_files[0]['id']
        media = MediaFileUpload(str(file_path), mimetype='text/markdown')
        file = service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print(f"✅ Updated: {file_name} (ID: {file.get('id')})")
        return file
    else:
        # Create new file
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(str(file_path), mimetype='text/markdown')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        print(f"✅ Uploaded: {file_name}")
        print(f"   Link: {file.get('webViewLink')}")
        return file


def main():
    """Main upload function."""
    # Get files to upload
    script_dir = Path(__file__).parent

    if len(sys.argv) > 1:
        # Upload specific files from command line
        files_to_upload = [script_dir / f for f in sys.argv[1:]]
    else:
        # Upload all scripts from current year
        from datetime import datetime
        current_year = datetime.now().year
        pattern = f"*_{current_year}-*.md"
        files_to_upload = sorted(script_dir.glob(pattern), reverse=True)

    if not files_to_upload:
        print("No files to upload.")
        print(f"Usage: {sys.argv[0]} [file1.md file2.md ...]")
        sys.exit(1)

    # Authenticate
    print("Authenticating with Google Drive...")
    service = authenticate()
    print(f"Uploading to folder ID: {FOLDER_ID}\n")

    # Upload files
    uploaded_count = 0
    for file_path in files_to_upload:
        if file_path.exists():
            result = upload_file(service, file_path)
            if result:
                uploaded_count += 1
        else:
            print(f"⚠️  Skipped (not found): {file_path.name}")

    print(f"\n✅ Upload complete! {uploaded_count} file(s) uploaded.")
    print(f"View folder: https://drive.google.com/drive/folders/{FOLDER_ID}")


if __name__ == '__main__':
    main()
