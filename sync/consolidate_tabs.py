#!/usr/bin/env python3
"""
Consolidate existing Content tabs into single "Content" tab
Merges Content_20251023 and Content_20251025 into one tab with Date column
"""

import json
import pickle
from pathlib import Path
from googleapiclient.discovery import build

class TabConsolidator:
    """Consolidate multiple content tabs into single tab"""

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

    def consolidate(self):
        """Consolidate existing tabs into single Content tab"""

        print("\n" + "="*100)
        print("🔄 CONSOLIDATING CONTENT TABS")
        print("="*100)

        # Tabs to consolidate
        old_tabs = ['Content_20251023', 'Content_20251025']

        print(f"\n📋 Merging tabs: {', '.join(old_tabs)}")

        # Get data from each tab
        all_data = []

        for tab_name in old_tabs:
            print(f"\n📥 Reading {tab_name}...")

            try:
                result = self.sheets_service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{tab_name}!A:Z"
                ).execute()

                values = result.get('values', [])

                if not values:
                    print(f"   ⚠️  No data found")
                    continue

                # Skip header row, add date column
                date = tab_name.replace('Content_', '')
                date_formatted = f"{date[:4]}-{date[4:6]}-{date[6:]}"

                print(f"   ✅ Found {len(values)-1} rows (date: {date_formatted})")

                for row in values[1:]:  # Skip header
                    # Add date as first column
                    # Add "Daily" as content type (second column after date)
                    # If row already has content type (column 2), keep it; otherwise add "Daily"
                    if len(row) >= 2:
                        # Insert "Daily" after title if not present
                        row_with_date = [date_formatted, row[0], 'Daily'] + row[1:]
                    else:
                        row_with_date = [date_formatted] + row + ['Daily']
                    all_data.append(row_with_date)

            except Exception as e:
                print(f"   ❌ Error reading {tab_name}: {e}")

        print(f"\n✅ Total rows collected: {len(all_data)}")

        # Create new "Content" tab
        print(f"\n📝 Creating 'Content' tab...")

        try:
            request = {
                'addSheet': {
                    'properties': {
                        'title': 'Content'
                    }
                }
            }

            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': [request]}
            ).execute()

            print(f"   ✅ Created 'Content' tab")

        except Exception as e:
            print(f"   ⚠️  Tab may already exist: {e}")

        # Write consolidated data
        print(f"\n📤 Writing consolidated data...")

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

        rows = [headers] + all_data

        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range='Content!A1',
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()

        print(f"   ✅ Wrote {len(rows)} rows (including header)")

        # Format the new tab
        print(f"\n🎨 Formatting 'Content' tab...")
        self._format_content_tab(len(rows), len(headers))

        # Delete old tabs
        print(f"\n🗑️  Deleting old tabs...")

        spreadsheet = self.sheets_service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id
        ).execute()

        delete_requests = []
        for sheet in spreadsheet.get('sheets', []):
            sheet_title = sheet['properties']['title']
            if sheet_title in old_tabs:
                sheet_id = sheet['properties']['sheetId']
                delete_requests.append({
                    'deleteSheet': {
                        'sheetId': sheet_id
                    }
                })
                print(f"   🗑️  Deleting {sheet_title}...")

        if delete_requests:
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': delete_requests}
            ).execute()
            print(f"   ✅ Deleted {len(delete_requests)} old tabs")

        # Print summary
        print("\n" + "="*100)
        print("✅ CONSOLIDATION COMPLETE!")
        print("="*100)

        print(f"\n📊 Google Sheet:")
        print(f"   {self.spreadsheet_url}")

        print(f"\n📝 New tab: Content")
        print(f"   Total rows: {len(all_data)} (+ 1 header)")
        print(f"   Date range: 2025-10-23 to 2025-10-25")

        print(f"\n🗑️  Removed tabs:")
        for tab in old_tabs:
            print(f"   • {tab}")

        print(f"\n✅ Future daily runs will append to 'Content' tab")

    def _format_content_tab(self, num_rows, num_cols):
        """Format the Content tab"""

        # Get sheet ID
        spreadsheet = self.sheets_service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id
        ).execute()

        sheet_id = None
        for sheet in spreadsheet.get('sheets', []):
            if sheet['properties']['title'] == 'Content':
                sheet_id = sheet['properties']['sheetId']
                break

        if sheet_id is None:
            print("   ⚠️  Could not find sheet ID")
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

        # 4. Color-code by approval status (column O = index 14)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': num_rows,
                        'startColumnIndex': 14,
                        'endColumnIndex': 15
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
            print("   ✅ Formatting applied")
        except Exception as e:
            print(f"   ⚠️  Some formatting may have failed: {e}")


def main():
    consolidator = TabConsolidator()
    consolidator.consolidate()


if __name__ == "__main__":
    main()
