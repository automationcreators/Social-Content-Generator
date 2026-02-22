# Quick Start: Unified YouTube Script Generator

**TL;DR:** One command generates scripts informed by your entire past script database, automatically uploads to Google Drive, and prevents duplication.

## Install & Setup (One-Time)

```bash
# Done already! OAuth is configured, Gemini API key is stored
# Just verify you have the credentials folder:
ls ~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/
# Should show: google-drive-credentials.json, token.pickle, .env
```

## Generate Your First Script

### Option 1: Full Workflow (Recommended)
```bash
cd ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts
python3 unified_gemini_youtube_generator.py --topic "Your topic here" --full
```

Example:
```bash
python3 unified_gemini_youtube_generator.py --topic "Building AI agents that actually work" --full
```

### What You Get
```
✅ Searches your past 50+ scripts for related content
✅ Generates 3 hook variations (contrarian, authority, transformation)
✅ Creates WHY-WHAT-HOW body structure
✅ Adds 3-step implementation framework
✅ Saves locally with timestamp
✅ Uploads to Google Drive automatically
✅ Returns shareable link instantly
```

### Example Output
```
🔍 Searching for similar existing scripts...
✅ Found 4 related scripts:
   - youtube_scripts_2025-11-12_claude_skills_vs_traditional_automation_tools.md
   - youtube_scripts_2025-11-14_avoiding_the_95%_ai_implementation_failure_rate.md
   - youtube_scripts_2025-11-11_ai_automation_for_small_business_owners.md

📚 Script generated with 3 hook variations and proven frameworks

✅ Uploaded to Drive: https://drive.google.com/file/d/xxxxx/view

⏱️ Total time: 12 seconds
💰 Cost: < $0.01 (Gemini API)
```

## Other Commands

### Just Search for Ideas
```bash
python3 unified_gemini_youtube_generator.py --search-similar "Claude Skills"
```

Shows which existing scripts are related and what frameworks were used.

### Upload Unsynced Scripts
```bash
python3 unified_gemini_youtube_generator.py --sync-drive
```

Finds any local scripts not yet on Google Drive and uploads them.

### Check Status
```bash
python3 unified_gemini_youtube_generator.py
```

Shows:
- How many scripts are in Google Drive
- How many local scripts aren't synced
- When was the last sync

## Features You're Getting

✅ **Smart Context Search**
- Finds related past scripts automatically
- No manual database searching
- Prevents repeating frameworks

✅ **Never Duplicate Files**
- Tracks which files are synced via file hashing
- Safe to run multiple times
- Automatic update detection

✅ **Secure OAuth**
- Uses desktop OAuth credentials (never stored in code)
- Token auto-refreshes when expired
- No API keys in .gitignore tracked files

✅ **Instant Sharing**
- Get Google Drive link immediately after upload
- Direct shareable URL for team access
- Files organized in one Drive folder

✅ **Proven Frameworks**
- Kallaway's 4-part hook structure
- WHY-WHAT-HOW body format
- Authority positioning
- Transformation narrative arc

## File Locations

```
Generated Scripts:
~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/youtube_scripts_*.md

Script Code:
~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/unified_gemini_youtube_generator.py

Credentials (Secure):
~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/

Sync Tracking:
~/Documents/claudec/systems/skills-main/boring-business-brand/credentials/.sync_state.json
```

## Troubleshooting

**Q: "Credentials file not found"**
A: Run OAuth setup once:
```bash
python3 ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts/upload_to_gdrive.py
```

**Q: Script doesn't find related scripts**
A: Normal on first runs. Once you have 5+ scripts, search gets better automatically.

**Q: Want to change Google Drive folder?**
A: Edit the script, find `self.folder_id = '...'` and change to your folder ID.

**Q: How much does this cost?**
A: ~$0.01 per script generation (Gemini API). Google Drive storage is free for .md files.

## Advanced: Batch Generation

```bash
#!/bin/bash
# Save as: batch_generate.sh
# Run with: bash batch_generate.sh

topics=(
  "Building Compound Leverage with AI"
  "The 95% Failure Rate Truth"
  "Workflow Redesign Framework"
  "Claude Skills vs Traditional Tools"
  "ROI-Focused AI Implementation"
)

for topic in "${topics[@]}"; do
  echo ""
  echo "==============================================="
  echo "Generating: $topic"
  echo "==============================================="
  python3 unified_gemini_youtube_generator.py --topic "$topic" --full
  sleep 2  # Rate limit between requests
done

echo ""
echo "✅ Batch generation complete!"
echo "Check Google Drive folder for all generated scripts"
```

## Next Steps

1. **Generate your first script:**
   ```bash
   python3 unified_gemini_youtube_generator.py --topic "Your topic" --full
   ```

2. **Check Google Drive** for the uploaded file and shareable link

3. **Review the README** for advanced options:
   ```bash
   cat UNIFIED_GENERATOR_README.md
   ```

4. **Set up batch generation** for multiple topics at once

## Support

- Full documentation: `UNIFIED_GENERATOR_README.md`
- Gemini API docs: https://aistudio.google.com/
- Google Drive integration: Handled via OAuth (see `credentials/SECURITY_SETUP.md`)

---

**You're now using a production-ready unified system that combines:**
- Semantic search across 50+ past scripts
- AI-powered generation with proven frameworks
- Automatic Google Drive sync with duplication prevention
- Secure OAuth authentication
- Zero manual data management

🚀 **Let's go generate some viral YouTube scripts!**
