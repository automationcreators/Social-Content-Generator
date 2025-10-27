#!/usr/bin/env python3
"""
Sync to Google Sheets
Takes final_content_output.json and syncs to Google Sheets
Uses existing Google OAuth credentials
"""

import json
import pickle
import re
from pathlib import Path
from googleapiclient.discovery import build
from datetime import datetime

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
    text_emojis = ['✅', '❌', '🎯', '📊', '🔥', '💡', '⚡', '🚀', '✨', '📝', '🎉', '🎬', '📡', '📋', '📈', '🔗', '🎨', '🗑️', '⏳', '⚠️']

    text = emoji_pattern.sub('', text)
    for emoji in text_emojis:
        text = text.replace(emoji, '')

    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class GoogleSheetsSyncer:
    """Sync content to Google Sheets"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent
        self.token_file = self.agents_dir / 'google_token.pickle'

        # Load credentials
        with open(self.token_file, 'rb') as token:
            self.creds = pickle.load(token)

        # Initialize services
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)

        # Load Google Sheets results to get spreadsheet ID
        results_file = self.agents_dir / 'google_sheets_results.json'
        with open(results_file, 'r') as f:
            results = json.load(f)
            self.spreadsheet_id = results['spreadsheet_id']
            self.spreadsheet_url = results['spreadsheet_url']

    def sync_content(self, content_file=None):
        """Sync content from final_content_output.json to Google Sheets - Single Content tab"""

        print("\n" + "="*100)
        print("📊 SYNCING CONTENT TO GOOGLE SHEETS")
        print("="*100)

        # Load content
        if content_file is None:
            content_file = self.agents_dir / 'final_content_output.json'

        with open(content_file, 'r') as f:
            content_data = json.load(f)

        print(f"\n📥 Loading content from: {content_file}")

        metadata = content_data['metadata']
        content_pieces = content_data['content_ready_for_sheets']

        print(f"   Total pieces: {metadata['total_pieces']}")
        print(f"   Auto-approved: {metadata['auto_approved']}")
        print(f"   Mode: {metadata['mode']}")

        # Use single "Content" tab
        tab_name = "Content"
        today = datetime.now().strftime('%Y-%m-%d')

        # Check if Content tab exists
        sheet_exists = self._check_sheet_exists(tab_name)

        if not sheet_exists:
            print(f"\n📝 Creating 'Content' tab (first time)...")
            try:
                self._create_sheet_tab(tab_name)
            except Exception as e:
                print(f"   ⚠️  Could not create tab: {e}")

        # Prepare rows for sheet
        print(f"\n🔄 Preparing {len(content_pieces)} rows for {today}...")

        headers = [
            'Date',
            'Title',
            'Content Type',
            'Trend Source',
            'Trend URL',
            'Personal Example',
            'Hook Option 1',
            'Hook Option 2',
            'Stat 1',
            'Stat 2',
            'Stat 3',
            'Framework',
            'Platforms',
            'Fusion Strength',
            'Quality Score',
            'Auto Approved',
            'Status'
        ]

        # Get existing row count to append
        existing_data = self._get_existing_data(tab_name)

        if not existing_data or len(existing_data) == 0:
            # First time - add headers
            rows = [headers]
            print(f"   ✅ First run - adding headers")
        else:
            # Append mode - no headers
            rows = []
            print(f"   ✅ Appending to existing {len(existing_data)-1} rows")

        for piece in content_pieces:
            row = self._format_row(piece, today)
            rows.append(row)

        # Write to sheet
        print(f"\n📤 Writing to Google Sheets...")

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

        # Format the sheet (only on first run or when needed)
        if not existing_data or len(existing_data) == 0:
            print(f"\n🎨 Formatting sheet...")
            self._format_sheet(tab_name, total_rows, len(headers))

        # Print summary
        print("\n" + "="*100)
        print("✅ SYNC COMPLETE!")
        print("="*100)

        print(f"\n📊 Google Sheet:")
        print(f"   {self.spreadsheet_url}")

        print(f"\n📝 Tab: {tab_name}")
        print(f"   Date: {today}")
        print(f"   New rows added: {len(rows)}")
        print(f"   Total rows: {total_rows}")

        print(f"\n🎯 Content Status:")
        auto_approved = sum(1 for p in content_pieces if p.get('auto_approved'))
        print(f"   Auto-approved: {auto_approved}")
        print(f"   Needs review: {len(content_pieces) - auto_approved}")

        return {
            'spreadsheet_url': self.spreadsheet_url,
            'tab_name': tab_name,
            'date': today,
            'rows_written': len(rows),
            'total_rows': total_rows,
            'auto_approved': auto_approved
        }

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

    def _format_row(self, piece, date):
        """Format a content piece into a sheet row"""

        trend = piece.get('trend_source', {})
        personal = piece.get('personal_example', {})
        angles = piece.get('angles', [])
        stats = piece.get('statistics', [])
        score = piece.get('quality_score', {})

        # Format hooks
        hook1 = angles[0].get('hook', '') if len(angles) > 0 else ''
        hook2 = angles[1].get('hook', '') if len(angles) > 1 else ''

        # Format stats
        stat1 = f"{stats[0]['stat']}: {stats[0]['detail']} ({stats[0]['source']})" if len(stats) > 0 else ''
        stat2 = f"{stats[1]['stat']}: {stats[1]['detail']} ({stats[1]['source']})" if len(stats) > 1 else ''
        stat3 = f"{stats[2]['stat']}: {stats[2]['detail']} ({stats[2]['source']})" if len(stats) > 2 else ''

        # Format personal example
        personal_text = ''
        if personal:
            examples = personal.get('examples', [])
            if examples:
                ex = examples[0]
                personal_text = f"{personal['title']}\n\nExample: {ex['title']}\n{ex['description']}"

        return [
            date,  # Date column first
            remove_emojis(trend.get('title', '')),
            'Daily',  # Content Type
            remove_emojis(trend.get('source', '')),
            remove_emojis(trend.get('url', '')),
            remove_emojis(personal_text),
            remove_emojis(hook1),
            remove_emojis(hook2),
            remove_emojis(stat1),
            remove_emojis(stat2),
            remove_emojis(stat3),
            remove_emojis(piece.get('framework', '')),
            remove_emojis(', '.join(piece.get('platforms', []))),
            remove_emojis(piece.get('fusion_strength', '')),
            f"{score.get('total', 0)}/100",
            'YES' if piece.get('auto_approved') else 'NO',
            'Ready' if piece.get('auto_approved') else 'Review'
        ]

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

        # 4. Color-code by approval status
        # Green for auto-approved (column M = index 13)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 13,
                        'endColumnIndex': 14
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_CONTAINS',
                            'values': [{'userEnteredValue': '✅'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 1, 'blue': 0.85}
                        }
                    }
                },
                'index': 0
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
    import sys

    syncer = GoogleSheetsSyncer()

    content_file = None
    if len(sys.argv) > 1:
        content_file = Path(sys.argv[1])

    result = syncer.sync_content(content_file)

    print("\n" + "="*100)
    print("🎉 READY TO POST!")
    print("="*100)

    print(f"\n📊 Open your Google Sheet:")
    print(f"   {result['spreadsheet_url']}")

    print(f"\n✅ Next steps:")
    print(f"   1. Review content in tab: {result['tab_name']}")
    print(f"   2. {result['auto_approved']} pieces ready to post immediately")
    print(f"   3. Edit or approve remaining pieces")
    print(f"   4. Schedule posts across platforms")

    print("\n💡 Tip: Run daily for fresh content (1-2 posts/day/platform)")


if __name__ == "__main__":
    main()
