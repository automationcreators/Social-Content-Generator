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
        self.token_file = self.agents_dir.parent / 'data' / 'google_token.pickle'

        # Load credentials
        with open(self.token_file, 'rb') as token:
            self.creds = pickle.load(token)

        # Initialize services
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

        # Load Google Sheets results to get spreadsheet ID
        results_file = self.agents_dir.parent / 'data' / 'google_sheets_results.json'
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

        # Prepare headers - EXACT structure from rows 1-4
        headers = [
            'Pillar ID',
            'Title',
            'Category',
            'Hook Type',
            'Audience',
            'Urgency',
            'Created Date',
            'Real Examples (Projects)',
            'Key Statistics',
            'YouTube Script',  # Google Doc link
            'LinkedIn Article',
            'Twitter Thread',
            'Instagram Post',
            'Threads Post',
            'Single Tweet',
            'Business Value',
            'Time Savings',
            'Tech Stack',
            'Status',
            'Notes',
            'Hook Variation A (Stats Lead)',
            'Hook Variation B (Contrarian)',
            'Hook Variation C (Story)',
            'Hook Variation D (Question)',
            'Hook Variation E (Outcome)',
            'Contrasting Idea 1',
            'Contrasting Idea 2',
            'Contrasting Idea 3',
            'Statistical Variant 1',
            'Statistical Variant 2',
            'Statistical Variant 3',
            'Personal Story 1',
            'Personal Story 2',
            'Hook Format Reference'
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

    def _create_youtube_doc(self, pillar):
        """Create a Google Doc with the YouTube script and return the URL"""

        idea = pillar['idea']
        content = pillar['content']
        youtube_script = content.get('youtube_script', '')

        # Create the document
        doc_title = f"YouTube Script - {idea.get('title', 'Untitled')}"
        doc = self.docs_service.documents().create(body={'title': doc_title}).execute()
        doc_id = doc.get('documentId')

        # Add content to the document
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': youtube_script
                }
            }
        ]

        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        # Make it publicly viewable (optional - adjust permissions as needed)
        self.drive_service.permissions().create(
            fileId=doc_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        doc_url = f"https://docs.google.com/document/d/{doc_id}"
        return doc_url

    def _format_pillar_row(self, pillar, date):
        """Format a pillar into a sheet row - EXACT 34-column structure"""

        idea = pillar['idea']
        content = pillar['content']
        real_data = pillar['real_data']
        hook_framework = pillar.get('hook_framework', {})

        # Create Google Doc with YouTube script
        print(f"      Creating Google Doc for YouTube script...")
        youtube_doc_url = self._create_youtube_doc(pillar)

        # Get content
        linkedin_article = remove_emojis(content.get('linkedin_article', ''))

        # Format Twitter thread
        twitter_thread = content.get('twitter_thread', {})
        tweets = twitter_thread.get('tweets', [])
        if isinstance(tweets, list):
            thread_text = '\n\n'.join([f"Tweet {i+1}: {remove_emojis(tweet.get('text', ''))}" for i, tweet in enumerate(tweets)])
        else:
            thread_text = remove_emojis(str(tweets))

        # Get individual posts
        short_posts = content.get('short_posts', [])
        instagram_post = ''
        threads_post = ''
        single_tweet = ''

        if isinstance(short_posts, list):
            for post in short_posts:
                if isinstance(post, dict):
                    platform = post.get('platform', '').lower()
                    text = remove_emojis(post.get('post', ''))
                    if 'instagram' in platform:
                        instagram_post = text
                    elif 'threads' in platform:
                        threads_post = text
                    elif 'twitter' in platform or 'tweet' in platform:
                        single_tweet = text

        # Format examples
        examples = real_data.get('examples', [])
        examples_text = ", ".join([ex.get('title', '') for ex in examples if isinstance(ex, dict)])

        # Format statistics
        stats = real_data.get('statistics', [])
        stats_text = " | ".join([f"{s.get('stat', '')}" for s in stats if isinstance(s, dict)])[:200]

        # Extract business value and time savings from examples
        business_value = " | ".join([ex.get('business_value', '') for ex in examples if isinstance(ex, dict) and ex.get('business_value')])[:200]
        time_savings = examples[0].get('business_value', '') if examples else ''

        # Tech stack
        tech_stack = ", ".join(set([ex.get('tech', '') for ex in examples if isinstance(ex, dict) and ex.get('tech')]))

        # Generate hook variations (5 variations)
        title = idea.get('title', '')
        description = idea.get('description', '')

        hook_a = f"{len(examples)} projects. {len(stats)} key stats. {idea.get('category', '')}.\n\n{title}\n\nNumbers → Contrast → Promise"
        hook_b = f"Everyone says you need developers to build software.\n\nI've built {len(examples)} projects with zero coding experience.\n\n{title}"
        hook_c = f"A year ago, I was spending 20 hours/week on manual tasks.\n\nToday, automation handles everything.\n\nHere's what changed:"
        hook_d = f"What if you could automate your entire business without hiring a single developer?\n\nI did it.\n\n{title}"
        hook_e = f"Save {time_savings}. Replace $300/month in subscriptions. Build in 45 minutes.\n\n{title}"

        # Contrasting ideas (3)
        contrast_1 = "❌ Most people think automation requires: Coding skills, Developer team, Expensive tools\n✅ What actually works: Plain English descriptions, Claude Code, Zero monthly costs"
        contrast_2 = "❌ Traditional approach: Hire developers (months), Build custom ($$), Maintain forever\n✅ Claude Code approach: Describe what you need (minutes), Built in 1 hour, Runs automatically"
        contrast_3 = "❌ They say: \"You need a CS degree\", \"Learn Python first\", \"Understand databases\"\n✅ I proved: No degree needed, No code written, No database knowledge"

        # Statistical variants (3)
        stat_var_1 = f"ROI Focus: Built {len(examples)} tools that save {business_value}"
        stat_var_2 = f"Scale Focus: Managing {len(examples)} projects with automation"
        stat_var_3 = f"Speed Focus: From idea to working tool in 45 minutes"

        # Personal stories (2)
        story_1 = description[:200] if description else ''
        story_2 = examples[0].get('description', '')[:200] if examples else ''

        # Hook format reference
        hook_ref = hook_framework.get('description', 'Transformation story')

        return [
            pillar.get('id', ''),  # Pillar ID
            remove_emojis(title),
            remove_emojis(idea.get('category', '')),
            remove_emojis(idea.get('hook_type', '')),
            remove_emojis(idea.get('audience', '')),
            remove_emojis(idea.get('urgency', '')),
            idea.get('created_date', date),
            remove_emojis(examples_text),
            remove_emojis(stats_text),
            youtube_doc_url,  # Google Doc URL!
            linkedin_article,
            thread_text,
            instagram_post,
            threads_post,
            single_tweet,
            remove_emojis(business_value),
            remove_emojis(time_savings),
            remove_emojis(tech_stack),
            'Ready',
            '',  # Notes
            remove_emojis(hook_a),
            remove_emojis(hook_b),
            remove_emojis(hook_c),
            remove_emojis(hook_d),
            remove_emojis(hook_e),
            remove_emojis(contrast_1),
            remove_emojis(contrast_2),
            remove_emojis(contrast_3),
            remove_emojis(stat_var_1),
            remove_emojis(stat_var_2),
            remove_emojis(stat_var_3),
            remove_emojis(story_1),
            remove_emojis(story_2),
            remove_emojis(hook_ref)
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
