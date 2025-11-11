# Google Drive Integration for Social Media Scripts

Complete guide for automatically uploading generated social media scripts to Google Drive.

## Table of Contents

- [Overview](#overview)
- [Option 1: MCP Server Integration (Recommended for Claude Desktop)](#option-1-mcp-server-integration)
- [Option 2: Python API Direct Upload (Recommended for Automation)](#option-2-python-api-direct-upload)
- [Option 3: Manual Upload](#option-3-manual-upload)
- [Folder Configuration](#folder-configuration)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Target Google Drive Folder:**
- **URL:** https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx
- **Folder ID:** `1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx`

**Files to Upload:**
- `social_media_scripts_YYYY-MM-DD.md`
- `SCRIPTS_SUMMARY_YYYY-MM-DD.md`

**Current Status:** Three integration options available based on your workflow needs.

---

## Option 1: MCP Server Integration

Model Context Protocol (MCP) servers enable Claude Desktop and other AI tools to interact with Google Drive.

### Available MCP Implementations

#### 1.1 Commercial Platforms (Full Upload Support)

**Simtheory Google Drive MCP** (Recommended for Full Features)
- **Features:** Upload, download, create folders, share, search, export
- **Pricing:** Requires Simtheory workspace account
- **Setup:** https://simtheory.ai/mcp-servers/google-drive/
- **Capabilities:**
  - ✅ Upload files to Google Drive
  - ✅ Create and manage folders
  - ✅ Share files and manage permissions
  - ✅ Search and filter files
  - ✅ Export Google Workspace files

**Installation:**
1. Sign up at https://simtheory.ai/
2. Install Google Drive from your Simtheory workspace
3. Authorize access to your Google Drive account
4. Add to Claude Code configuration

**Zapier MCP AI**
- **Features:** Create files from plain text, create folders
- **Pricing:** Requires Zapier account
- **Setup:** https://zapier.com/mcp/google-drive
- **Capabilities:**
  - ✅ Create new files from plain text
  - ✅ Create new folders
  - ⚠️ Limited to basic file operations

#### 1.2 Open Source (Read-Only or Limited Write)

**⚠️ Important Limitation:** Most open-source Google Drive MCP servers are currently **read-only** and do not support file uploads.

**Anthropic's Official Google Drive MCP**
- **Repository:** https://github.com/modelcontextprotocol/servers
- **Status:** Read-only
- **Capabilities:**
  - ✅ Search files and folders
  - ✅ Read file contents
  - ❌ No upload capability

**felores/gdrive-mcp-server**
- **Repository:** https://github.com/felores/gdrive-mcp-server
- **Status:** Read-only
- **Capabilities:**
  - ✅ Search, list, and read files
  - ❌ No upload capability

**isaacphi/mcp-gdrive**
- **Repository:** https://github.com/isaacphi/mcp-gdrive
- **Status:** Read + limited write (spreadsheets only)
- **Capabilities:**
  - ✅ Search and read files
  - ✅ Update spreadsheet cells
  - ❌ No file upload capability

**piotr-agier/google-drive-mcp**
- **Repository:** https://github.com/piotr-agier/google-drive-mcp
- **Status:** Read + write (limited documentation on upload)
- **Installation:**

```bash
# Using npx (recommended)
npx @piotr-agier/google-drive-mcp

# Or local installation
git clone https://github.com/piotr-agier/google-drive-mcp.git
cd google-drive-mcp
npm install
npm run build
```

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["@piotr-agier/google-drive-mcp"],
      "env": {
        "GOOGLE_DRIVE_OAUTH_CREDENTIALS": "/path/to/gcp-oauth.keys.json"
      }
    }
  }
}
```

### MCP Setup Requirements

All MCP servers require Google Cloud OAuth credentials:

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing

2. **Enable Required APIs**
   - Google Drive API
   - Google Docs API (optional)
   - Google Sheets API (optional)

3. **Configure OAuth Consent Screen**
   - Add application name and support email
   - Add your email to test users

4. **Create OAuth 2.0 Credentials**
   - Application type: Desktop app
   - Download JSON file as `gcp-oauth.keys.json`

5. **First-Time Authentication**
   - Run the MCP server
   - Complete browser-based OAuth flow
   - Tokens stored automatically for future use

**Token Storage Locations:**
- **piotr-agier:** `~/.config/google-drive-mcp/tokens.json`
- **felores:** `credentials/.gdrive-server-credentials.json`
- **isaacphi:** Directory specified in `GDRIVE_CREDS_DIR`

---

## Option 2: Python API Direct Upload

**Recommended for:** Automated workflows, command-line usage, integration with existing scripts

This approach uses the official Google Drive API via Python, providing full control over file uploads.

### Installation

```bash
# Install Google API client
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Setup Google Cloud Credentials

1. Follow steps 1-4 from [MCP Setup Requirements](#mcp-setup-requirements) above
2. Download OAuth credentials JSON file
3. Place in: `/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/credentials/`
4. Rename to: `google-drive-credentials.json`

### Upload Script

Save this as `pillar_scripts/upload_to_gdrive.py`:

```python
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
                print("Please download OAuth credentials from Google Cloud Console")
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
```

### Usage

**First-Time Setup:**

```bash
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts

# Make script executable
chmod +x upload_to_gdrive.py

# Run authentication (opens browser)
python upload_to_gdrive.py
```

**Upload Specific Files:**

```bash
python upload_to_gdrive.py social_media_scripts_2025-11-10.md
python upload_to_gdrive.py social_media_scripts_2025-11-10.md SCRIPTS_SUMMARY_2025-11-10.md
```

**Upload All Scripts from Current Year:**

```bash
python upload_to_gdrive.py
```

**Automated Upload After Generation:**

Add to your content generation workflow:

```bash
# After generating scripts
python upload_to_gdrive.py social_media_scripts_$(date +%Y-%m-%d).md
```

### Features

✅ **Automatic duplicate handling** - Updates existing files instead of creating duplicates
✅ **Batch upload** - Upload multiple files at once
✅ **Direct links** - Returns shareable Google Drive links
✅ **Token caching** - No re-authentication needed after first run
✅ **Error handling** - Clear error messages and validation

---

## Option 3: Manual Upload

**Recommended for:** Occasional uploads, one-time transfers

### Quick Upload Steps

1. **Open pillar_scripts folder:**
   ```bash
   open ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/
   ```

2. **Open Google Drive folder in browser:**
   https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx

3. **Drag and drop files:**
   - `social_media_scripts_2025-11-10.md`
   - `SCRIPTS_SUMMARY_2025-11-10.md`

### Using Google Drive Desktop App

If you have Google Drive for Desktop installed:

1. Find your Google Drive folder (usually `~/Google Drive/`)
2. Navigate to the Social Scripts folder
3. Copy files from pillar_scripts to Google Drive folder
4. Files sync automatically

---

## Folder Configuration

### Google Drive Folder Structure

```
Boring Business AI - Social Scripts/
├── social_media_scripts_2025-11-09.md
├── SCRIPTS_SUMMARY_2025-11-09.md
├── social_media_scripts_2025-11-10.md
├── SCRIPTS_SUMMARY_2025-11-10.md
└── [future scripts...]
```

### Local Folder Structure

```
pillar_scripts/
├── README.md
├── GOOGLE_DRIVE_INTEGRATION.md (this file)
├── upload_to_gdrive.py
├── social_media_scripts_2025-11-09.md
├── SCRIPTS_SUMMARY_2025-11-09.md
└── [generated scripts...]
```

### Credentials Storage

```
~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/
├── google-drive-credentials.json (OAuth client secret)
├── token.pickle (Cached access token)
└── .gitignore (Ensures credentials not committed)
```

**Important:** Add to `.gitignore`:

```gitignore
credentials/
*.pickle
*-credentials.json
```

---

## Troubleshooting

### Authentication Issues

**Problem:** "Credentials file not found"
```bash
# Verify credentials location
ls ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/

# Should contain google-drive-credentials.json
# If not, download from Google Cloud Console
```

**Problem:** "Access denied" or "Invalid credentials"
```bash
# Delete cached token and re-authenticate
rm ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/token.pickle
python upload_to_gdrive.py
```

**Problem:** "Token expired"
```python
# Script automatically refreshes tokens
# If issues persist, delete token.pickle and re-authenticate
```

### Upload Issues

**Problem:** "File not found"
```bash
# Verify you're in the correct directory
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts/

# Check file exists
ls -la social_media_scripts_*.md
```

**Problem:** "Folder not found" or "Insufficient permissions"
```
# Verify folder ID is correct
# Ensure your Google account has access to folder 1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx
# Check folder permissions in Google Drive
```

**Problem:** Duplicates being created
```python
# The script checks for existing files by name
# If duplicates appear, the folder may have been changed
# Verify FOLDER_ID in script matches target folder
```

### MCP Server Issues

**Problem:** MCP server not appearing in Claude Desktop
```bash
# Verify configuration file location
cat ~/.config/Claude/claude_desktop_config.json

# Check server is running
ps aux | grep mcp

# Restart Claude Desktop after config changes
```

**Problem:** OAuth flow not starting
```bash
# Ensure credentials file is in correct location
# Check environment variables are set correctly
# Try running authentication manually:
node dist/index.js auth  # For felores/gdrive-mcp-server
```

### Permission Issues

**Problem:** "Insufficient authentication scopes"
```python
# Update SCOPES in upload_to_gdrive.py:
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

# Delete token and re-authenticate
rm credentials/token.pickle
python upload_to_gdrive.py
```

---

## Recommendations

**For Automated Workflows:**
→ Use Option 2 (Python API Direct Upload)
- Full control over uploads
- Easy to integrate with existing automation
- No additional services required

**For Claude Desktop Integration:**
→ Use Option 1 (MCP Server) with Simtheory or piotr-agier
- Seamless integration with Claude
- Natural language file operations
- May require paid subscription (Simtheory)

**For Quick One-Time Uploads:**
→ Use Option 3 (Manual Upload)
- No setup required
- Fastest for occasional use
- No authentication needed

---

## Next Steps

1. **Choose your integration method** based on workflow needs
2. **Set up credentials** following setup instructions above
3. **Test upload** with a single file
4. **Integrate into workflow** for automated uploads

---

**Last Updated:** November 10, 2025
**Google Drive Folder:** https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx
**Folder ID:** `1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx`
**Maintained By:** Boring Business AI Brand System
