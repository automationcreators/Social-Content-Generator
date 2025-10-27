#!/usr/bin/env python3
"""
Sync Pillar Content to Google Sheets
Generates pillar content and syncs to Google Sheets with date column
"""

import json
import pickle
import re
import sys
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build

# Add parent directory to path to import from generators
sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.pillar_content_generator import PillarContentGenerator

def remove_emojis(text):
    """Remove all emojis from text"""
    if not text:
        return text

    # Remove emojis using regex
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "]+",
        flags=re.UNICODE
    )

    # Common text emojis to remove
    text_emojis = ['✅', '❌', '🎯', '📊', '🔥', '💡', '⚡', '🚀', '✨', '📝', '🎉', '🎬', '📡', '📋', '📈', '🔗', '🎨', '🗑️', '⏳', '⚠️', '🧵', '👇']

    text = emoji_pattern.sub('', text)
    for emoji in text_emojis:
        text = text.replace(emoji, '')

    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


class PillarContentSyncer:
    """Generate and sync pillar content to Google Sheets"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent
        self.token_file = self.agents_dir / 'google_token.pickle'

        # Load credentials
        with open(self.token_file, 'rb') as token:
            self.creds = pickle.load(token)

        # Initialize services
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)

        # Load Google Sheets results to get spreadsheet ID
        results_file = self.agents_dir / 'google_sheets_results.json'
        with open(results_file, 'r') as f:
            results = json.load(f)
            self.spreadsheet_id = results['spreadsheet_id']
            self.spreadsheet_url = results['spreadsheet_url']

    def generate_and_sync(self):
        """Generate pillar content and sync to Google Sheets"""

        print("\n" + "="*100)
        print("PILLAR CONTENT GENERATOR & SYNC")
        print("="*100)

        # Generate pillar content
        print("\n1. Generating pillar content...")
        generator = PillarContentGenerator()

        # Get business-focused ideas
        business_ideas = [idea for idea in generator.content_ideas["content_ideas"]
                         if idea.get("audience") == "small_business_owners"]

        pillars = []
        for i, idea in enumerate(business_ideas[:3], 1):
            print(f"   Generating pillar #{i}: {idea['title'][:60]}...")
            pillar = generator.create_pillar_content(idea['id'])
            pillars.append(pillar)

        print(f"   ✅ Generated {len(pillars)} pillars")

        # Save to JSON for reference
        output_file = self.agents_dir / "pillar_content_library.json"
        with open(output_file, 'w') as f:
            json.dump({"pillars": pillars, "created": datetime.now().isoformat()}, f, indent=2)

        # Sync to Google Sheets
        print("\n2. Syncing to Google Sheets...")
        result = self._sync_to_sheets(pillars)

        print("\n" + "="*100)
        print("✅ PILLAR CONTENT SYNC COMPLETE!")
        print("="*100)

        print(f"\n📊 Google Sheet:")
        print(f"   {self.spreadsheet_url}")

        print(f"\n📝 Tab: Pillar Content")
        print(f"   Date: {result['date']}")
        print(f"   Pillars added: {result['rows_written']}")
        print(f"   Total rows: {result['total_rows']}")

        return result

    def _sync_to_sheets(self, pillars):
        """Sync pillar content to Google Sheets - Single 'Pillar Content' tab"""

        tab_name = "Pillar Content"
        today = datetime.now().strftime('%Y-%m-%d')

        # Check if tab exists
        sheet_exists = self._check_sheet_exists(tab_name)

        if not sheet_exists:
            print(f"   Creating 'Pillar Content' tab (first time)...")
            try:
                self._create_sheet_tab(tab_name)
            except Exception as e:
                print(f"   ⚠️  Could not create tab: {e}")

        # Prepare headers - match daily content format
        headers = [
            'Date',
            'Title',
            'Content Type',
            'YouTube Doc Link',
            'Personal Example',
            'Hook Option 1',
            'Hook Option 2',
            'Stat 1',
            'Stat 2',
            'Stat 3',
            'Framework',
            'Platforms',
            'Category',
            'Content Preview',
            'Examples Count',
            'Status'
        ]

        # Get existing data
        existing_data = self._get_existing_data(tab_name)

        if not existing_data or len(existing_data) == 0:
            # First time - add headers
            rows = [headers]
            print(f"   ✅ First run - adding headers")
        else:
            # Append mode - no headers
            rows = []
            print(f"   ✅ Appending to existing {len(existing_data)-1} rows")

        # Format pillar data into rows
        for pillar in pillars:
            row = self._format_pillar_row(pillar, today)
            rows.append(row)

        # Write to sheet
        if not existing_data or len(existing_data) == 0:
            # First time - write from A1
            range_name = f"{tab_name}!A1"
        else:
            # Append - start after existing data
            next_row = len(existing_data) + 1
            range_name = f"{tab_name}!A{next_row}"

        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()

        total_rows = (len(existing_data) if existing_data else 0) + len(rows)
        print(f"   ✅ Wrote {len(rows)} new rows (total: {total_rows} rows)")

        # Format the sheet (only on first run)
        if not existing_data or len(existing_data) == 0:
            print(f"   🎨 Formatting sheet...")
            self._format_sheet(tab_name, total_rows, len(headers))

        return {
            'spreadsheet_url': self.spreadsheet_url,
            'tab_name': tab_name,
            'date': today,
            'rows_written': len(rows),
            'total_rows': total_rows
        }

    def _format_pillar_row(self, pillar, date):
        """Format a pillar into a sheet row - matches daily content format"""

        idea = pillar['idea']
        content = pillar['content']
        real_data = pillar['real_data']

        # Extract hooks
        hook1 = idea.get('description', '')  # Main description as Hook 1

        # Extract Hook 2 from Twitter thread first tweet
        twitter_thread = content.get('twitter_thread', {})
        tweets = twitter_thread.get('tweets', [])
        hook2 = tweets[0].get('text', '')[:200] if tweets else idea.get('title', '')

        # Extract statistics (format to match daily content)
        stats = real_data.get('statistics', [])
        stat1 = f"{stats[0].get('stat', '')}: {stats[0].get('detail', '')} ({stats[0].get('source', '')})" if len(stats) > 0 else ''
        stat2 = f"{stats[1].get('stat', '')}: {stats[1].get('detail', '')} ({stats[1].get('source', '')})" if len(stats) > 1 else ''
        stat3 = f"{stats[2].get('stat', '')}: {stats[2].get('detail', '')} ({stats[2].get('source', '')})" if len(stats) > 2 else ''

        # Extract personal examples
        examples = real_data.get('examples', [])
        examples_count = len(examples)

        # Format first example similar to daily content
        personal_text = ''
        if examples:
            ex = examples[0]
            personal_text = f"{idea['title']}\n\nExample: {ex.get('title', '')}\n{ex.get('description', '')[:200]}"

        # Get content preview (first 200 chars of YouTube script)
        youtube_script = content.get('youtube_script', '')
        content_preview = youtube_script[:200].replace('\n', ' ').strip() + '...' if len(youtube_script) > 200 else youtube_script.replace('\n', ' ').strip()

        # YouTube doc link - this would be set by the generator
        youtube_link = pillar.get('youtube_doc_url', 'To be created')

        # Get platforms (default for pillar content)
        platforms = 'YouTube, LinkedIn, Twitter, Instagram'

        return [
            date,
            remove_emojis(idea['title']),
            'Pillar',  # Content Type
            remove_emojis(youtube_link),
            remove_emojis(personal_text),
            remove_emojis(hook1),
            remove_emojis(hook2),
            remove_emojis(stat1),
            remove_emojis(stat2),
            remove_emojis(stat3),
            remove_emojis(idea.get('hook_type', '')),
            platforms,
            remove_emojis(idea.get('category', '')),
            remove_emojis(content_preview),
            str(examples_count),
            'Ready'
        ]

    def _create_sheet_tab(self, tab_name):
        """Create a new sheet tab"""

        request = {
            'addSheet': {
                'properties': {
                    'title': tab_name
                }
            }
        }

        self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={'requests': [request]}
        ).execute()

    def _check_sheet_exists(self, tab_name):
        """Check if a sheet tab exists"""
        try:
            spreadsheet = self.sheets_service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == tab_name:
                    return True
            return False
        except Exception as e:
            print(f"   ⚠️  Error checking sheet: {e}")
            return False

    def _get_existing_data(self, tab_name):
        """Get existing data from sheet"""
        try:
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{tab_name}!A:Z"
            ).execute()
            return result.get('values', [])
        except Exception as e:
            return []

    def _format_sheet(self, tab_name, num_rows, num_cols):
        """Format the sheet for better readability"""

        # Get sheet ID
        spreadsheet = self.sheets_service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id
        ).execute()

        sheet_id = None
        for sheet in spreadsheet.get('sheets', []):
            if sheet['properties']['title'] == tab_name:
                sheet_id = sheet['properties']['sheetId']
                break

        if sheet_id is None:
            print("   ⚠️  Could not find sheet ID for formatting")
            return

        requests = []

        # 1. Freeze header row
        requests.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        })

        # 2. Bold header row
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
                        'textFormat': {
                            'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                            'fontSize': 10,
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        })

        # 3. Auto-resize columns
        requests.append({
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': num_cols
                }
            }
        })

        try:
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': requests}
            ).execute()
            print("   ✅ Sheet formatted successfully")
        except Exception as e:
            print(f"   ⚠️  Some formatting may have failed: {e}")


def main():
    syncer = PillarContentSyncer()
    result = syncer.generate_and_sync()

    print("\n" + "="*100)
    print("🎉 READY TO USE!")
    print("="*100)

    print(f"\n📊 Open your Google Sheet:")
    print(f"   {result['spreadsheet_url']}")

    print(f"\n✅ Next steps:")
    print(f"   1. Review pillar content in 'Pillar Content' tab")
    print(f"   2. Copy scripts to your content calendar")
    print(f"   3. Schedule long-form content creation")

    print("\n💡 Tip: Run weekly for fresh pillar content ideas")


if __name__ == "__main__":
    main()
