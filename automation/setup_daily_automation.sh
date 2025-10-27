#!/bin/bash
# Setup Daily Content Generation Automation
# Runs every day at 9 AM

echo "🔧 Setting up daily content generation automation"
echo ""

AGENTS_DIR="/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents"

# Create cron job entry
CRON_COMMAND="0 9 * * * cd $AGENTS_DIR && /usr/local/bin/python3 daily_content_generator.py --mode balanced >> $AGENTS_DIR/daily_run.log 2>&1"

echo "📋 This will add the following cron job:"
echo "$CRON_COMMAND"
echo ""
echo "Translation: Run daily content generator every day at 9:00 AM"
echo ""

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -q "daily_content_generator.py") && ALREADY_EXISTS=1 || ALREADY_EXISTS=0

if [ $ALREADY_EXISTS -eq 1 ]; then
    echo "⚠️  Cron job already exists!"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep daily_content_generator
    echo ""
    echo "To remove and re-add:"
    echo "  crontab -e"
    echo "  (Delete the line with daily_content_generator.py)"
    echo "  (Then run this script again)"
else
    echo "✅ Adding cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

    echo ""
    echo "✅ Automation setup complete!"
    echo ""
    echo "📅 Daily schedule:"
    echo "   Time: 9:00 AM every day"
    echo "   Action: Generate 6 content pieces"
    echo "   Output: New Google Sheets tab (Content_YYYYMMDD)"
    echo "   Log: $AGENTS_DIR/daily_run.log"
    echo ""
    echo "🔍 To verify cron job:"
    echo "   crontab -l | grep daily_content"
    echo ""
    echo "📝 To view logs:"
    echo "   tail -f $AGENTS_DIR/daily_run.log"
    echo ""
    echo "🗑️  To remove automation:"
    echo "   crontab -e"
    echo "   (Delete the line with daily_content_generator.py)"
fi
