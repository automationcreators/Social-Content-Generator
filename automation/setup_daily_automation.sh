#!/bin/bash
# Setup Daily Content Generation Automation
# Runs every day at 9 AM

echo "🔧 Setting up daily content generation automation"
echo ""

SCG_DIR="/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator"

# Create cron job entry
CRON_COMMAND="0 9 * * * cd $SCG_DIR && /opt/homebrew/bin/python3 automation/daily_content_generator.py --mode balanced >> automation/daily_run.log 2>&1"

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
    echo "   Log: $SCG_DIR/daily_run.log"
    echo ""
    echo "🔍 To verify cron job:"
    echo "   crontab -l | grep daily_content"
    echo ""
    echo "📝 To view logs:"
    echo "   tail -f $SCG_DIR/daily_run.log"
    echo ""
    echo "🗑️  To remove automation:"
    echo "   crontab -e"
    echo "   (Delete the line with daily_content_generator.py)"
fi
