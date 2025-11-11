# Google Drive Upload Instructions

## Quick Upload

**Target Folder:**
https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx

**Folder ID:** `1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx`

## Manual Upload Steps

1. **Open Folder**
   - Click the link above
   - Or navigate to "Content Scripts" folder in Google Drive

2. **Select Files**
   - Navigate to `pillar_scripts/` folder locally
   - Select the files to upload:
     - `social_media_scripts_YYYY-MM-DD.md`
     - `SCRIPTS_SUMMARY_YYYY-MM-DD.md`
     - Any other recent scripts

3. **Upload**
   - Drag and drop files into Google Drive folder
   - Or click "New" → "File upload" and select files
   - Maintain original filenames

4. **Verify**
   - Check files uploaded successfully
   - Verify they're readable in Drive
   - Confirm dates match local versions

## Files to Upload After Generation

When new social media scripts are generated, upload:

✅ **Primary Files:**
- `social_media_scripts_[DATE].md`
- `SCRIPTS_SUMMARY_[DATE].md`

✅ **Optional Files:**
- Variation scripts
- Topic-specific scripts
- Research documents

❌ **Do NOT Upload:**
- Test files
- Temporary outputs
- System files (.DS_Store, etc.)

## Automation (Coming Soon)

### Planned Features

**Automatic Upload After Generation:**
- Script generates → auto-saves to pillar_scripts/ → auto-uploads to Drive
- Version control with timestamps
- Sync status notifications

**Google Drive MCP Integration:**
- Direct Drive API access
- Two-way sync capability
- Conflict resolution
- Version history

**Current Status:**
- Manual upload required (use steps above)
- MCP integration planned for future release

## Command Line Upload (Advanced)

### Using gdrive CLI

If you have `gdrive` installed:

```bash
# Navigate to pillar_scripts
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts

# Upload specific file
gdrive upload --parent 1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx social_media_scripts_2025-11-09.md

# Upload all recent .md files (last 7 days)
find . -name "*.md" -mtime -7 -exec gdrive upload --parent 1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx {} \;
```

### Using rclone

If you have `rclone` configured:

```bash
# Sync entire folder
rclone copy /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts \
  gdrive:Content-Scripts/ \
  --include "*.md" \
  --exclude "test_*" \
  --update
```

## Verification

After uploading, verify:

1. ✅ Files appear in Google Drive folder
2. ✅ Filenames match local versions
3. ✅ Content is readable (not corrupted)
4. ✅ Dates are correct
5. ✅ Markdown formatting preserved

## Troubleshooting

### Issue: Upload fails

**Solutions:**
- Check internet connection
- Verify Google Drive storage space
- Try uploading one file at a time
- Clear browser cache if using web interface

### Issue: File appears corrupted

**Solutions:**
- Re-upload the file
- Verify local file isn't corrupted
- Try different upload method (drag-drop vs file upload button)

### Issue: Can't access folder

**Solutions:**
- Verify folder link is correct
- Check Google account permissions
- Request access if needed
- Verify you're logged into correct account

## Contact

For automatic upload setup or issues:
- Check `CONFIG.md` for skill configuration
- Review `README.md` for pillar_scripts documentation
- See brand skill docs for generation settings

---

**Last Updated:** November 10, 2025
**Google Drive Folder:** https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx
**Folder ID:** `1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx`
**Status:** Manual upload (automation planned)
