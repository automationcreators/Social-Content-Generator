# Social Content Generator

**AI-powered social media content generation pipeline that fuses trending topics with personal projects**

Automatically generates daily content for LinkedIn, Twitter, YouTube, and Threads by combining:
- RSS trend scanning (AI/business focus)
- Data-driven research
- Contrarian angle generation
- Personal project examples
- Long-form pillar content

## 🎯 What It Does

1. **Scans RSS feeds** for trending AI/business topics from ContentGen database
2. **Researches supporting data** - finds statistics, reports, and credibility markers
3. **Generates multiple angles** - professional, spicy/contrarian, and balanced variations
4. **Fuses with personal projects** - connects trends to your real work examples
5. **Syncs to Google Sheets** - ready-to-post content with date tracking
6. **Creates pillar content** - long-form scripts for YouTube and LinkedIn articles

## 📊 Output

**Daily Content Tab:**
- 4 content pieces per day
- Auto-approved based on quality scoring
- Platform suggestions (LinkedIn, Twitter, YouTube, Threads)
- Emoji-free, clean formatting
- Date column for tracking

**Pillar Content Tab:**
- 3 long-form content pieces
- YouTube scripts (8-12 minutes)
- LinkedIn articles (1500+ words)
- Twitter threads (8-10 tweets)
- Instagram/Threads posts
- Date column for tracking

## 🚀 Quick Start

### Prerequisites

1. **ContentGen database** - RSS feed aggregator
2. **Google OAuth credentials** - for Sheets sync
3. **Python 3.9+**

### Installation

```bash
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator
pip install -r requirements.txt
```

### Configuration

1. **Set up Google OAuth:**
   - Place `google_token.pickle` in `data/` directory

2. **Configure ContentGen path:**
   - Update database path in `scouts/rss_content_scout.py`
   - Default: `/Users/elizabethknopf/Documents/claudec/active/ContentGen/data/database.db`

### Daily Generation

```bash
# Run once daily (recommended: 9 AM)
python3 automation/daily_content_generator.py --mode balanced
```

**Modes:**
- `professional` - Data-driven, educational, credible
- `spicy` - Contrarian, provocative, memorable
- `balanced` - Mix of credibility + edge (recommended)

### Automated Daily Runs

```bash
# Set up cron job for 9 AM daily
bash automation/setup_daily_automation.sh
```

## 📁 Repository Structure

```
Social-Content-Generator/
├── scouts/                    # RSS and trend scanning
│   └── rss_content_scout.py
├── research/                  # Data research agents
│   └── research_data_agent.py
├── generators/               # Content generation
│   ├── contrarian_angle_generator.py
│   ├── content_orchestrator.py
│   └── pillar_content_generator.py
├── sync/                     # Google Sheets integration
│   ├── sync_to_google_sheets.py
│   ├── pillar_content_sync.py
│   └── consolidate_tabs.py
├── config/                   # Configuration files
│   ├── content_frameworks/
│   ├── project_data_analysis.json
│   └── social_media_content_database.json
├── data/                     # Generated data & credentials
│   ├── google_token.pickle
│   ├── rss_ideas_database.json
│   ├── final_content_output.json
│   └── pillar_content_library.json
├── automation/              # Daily automation
│   ├── daily_content_generator.py
│   ├── setup_daily_automation.sh
│   └── webhook_server.py
└── utils/                   # Utilities
    └── remove_emojis.py
```

## 🔄 How It Works

### Pipeline Flow

```
ContentGen DB → RSS Scout → Research Agent → Angle Generator → Orchestrator → Google Sheets
                                                                      ↓
                                                              Pillar Generator
```

### 1. RSS Content Scout
- Scans ContentGen database for AI/business articles (last 14 days)
- Scores by relevance, brand alignment, viral potential
- Ensures source diversity (max 3 from same source)
- Categorizes by opportunity type (trend, tutorial, comparison, etc.)

### 2. Research Data Agent
- Finds supporting statistics and data
- Adds credibility markers
- Sources: industry reports, studies, benchmarks

### 3. Contrarian Angle Generator
- Creates 3 variations per idea:
  - Professional (data-driven)
  - Spicy/Contrarian (provocative)
  - Balanced (mix of both)
- Uses Kallaway hook frameworks

### 4. Content Orchestrator
- Fuses trending topics with personal project examples
- Rotates through pillar content (automation projects)
- Varies format based on content type:
  - Tutorials: 1 example (how-to format)
  - Case studies: 1 example (story format)
  - Trends: 2 examples (standard format)
- Quality scoring and auto-approval

### 5. Pillar Content Generator
- Creates long-form content:
  - YouTube scripts (8-12 minutes)
  - LinkedIn articles (1500+ words)
  - Twitter threads (8-10 tweets)
  - Instagram/Threads posts
- Includes real project examples
- Statistics and credibility markers

### 6. Google Sheets Sync
- Single "Content" tab with date column
- Single "Pillar Content" tab with date column
- Appends daily (no new tabs)
- Emoji-free formatting
- Auto-approval status

## 🎨 Content Quality

### Scoring System (0-100)

- **Relevance** (0-30): Match to focus areas
- **Brand Alignment** (0-25): Personal brand keywords
- **Viral Potential** (0-20): Engagement signals
- **Trending** (0-15): Current momentum
- **Quality** (0-10): Content depth

**Auto-approval threshold:** 70+

### Source Diversity

- Maximum 3 ideas from same source
- Deduplication (no duplicate titles)
- Varied opportunity types (trends, tutorials, comparisons)

### Personal Fusion

- **High fusion:** Direct automation/Claude/workflow connection
- **Medium fusion:** Tangentially related (AI, tools, efficiency)
- **Low fusion:** Standalone topic

## 🔧 Configuration

### Project Data (`config/project_data_analysis.json`)

Define your personal projects and examples:

```json
{
  "real_examples": [
    {
      "title": "Vendor Quote Automation",
      "project": "vendor-quote-tool",
      "category": "automation",
      "description": "...",
      "business_value": "Saves 5 hours/week"
    }
  ]
}
```

### Content Frameworks (`config/content_frameworks/`)

Kallaway hook frameworks for engagement:
- Transformation
- Contrarian Snapback
- Benefit-Driven
- How-To

## 📊 Google Sheets Output

### Content Tab Columns:
1. Date
2. Title
3. Trend Source
4. Trend URL
5. Personal Example
6. Hook Option 1
7. Hook Option 2
8. Stat 1, 2, 3
9. Framework
10. Platforms
11. Fusion Strength
12. Quality Score
13. Auto Approved
14. Status

### Pillar Content Tab Columns:
1. Date
2. Title
3. Category
4. Audience
5. Hook Type
6. YouTube Script (chars)
7. LinkedIn Article (chars)
8. Twitter Thread (tweets)
9. Short Posts (count)
10. Real Examples Used
11. Statistics Count
12. Status

## 🐛 Troubleshooting

### No Fresh Content / Same Articles Repeating

**Problem:** ContentGen database is stale

**Solution:**
```bash
cd /Users/elizabethknopf/Documents/claudec/active/ContentGen
python3 backend/app.py
# Access http://localhost:5000 to trigger RSS collection
```

### Emojis in Content

**Problem:** Emojis appearing in pillar content

**Solution:** Fixed in pillar_content_generator.py (Oct 26 update)

### Cron Job Not Running

**Problem:** Wrong Python path

**Solution:** Verify Python path in setup_daily_automation.sh
```bash
which python3  # Should be /usr/bin/python3
```

## 📝 Documentation

- **FIXES_APPLIED.md** - Content variety and example rotation fixes
- **ISSUE_SUMMARY_OCT26.md** - Troubleshooting guide for Oct 26 issues

## 🤝 Integration with Personal-OS

While this is a standalone system, it integrates with:
- **ContentGen** - RSS feed aggregation and storage
- **Personal-OS** - Project data and automation infrastructure

## 📅 Recommended Schedule

- **Daily content:** 1-2 posts per platform
- **LinkedIn:** 1 post/day (professional/balanced)
- **Twitter:** 1-2 posts/day (mix of professional + spicy)
- **YouTube:** 1 post/week (deep-dive from pillar content)
- **Threads:** 1 post/day (balanced/spicy)

## 🔐 Security

- Google OAuth credentials stored securely in `data/`
- `.gitignore` excludes sensitive files
- No API keys in code

## 📦 Dependencies

```
feedparser
beautifulsoup4
requests
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

## 🚀 Future Enhancements

- [ ] Image generation for posts
- [ ] Scheduling integration (Buffer, Hootsuite)
- [ ] A/B testing for hooks
- [ ] Performance analytics
- [ ] Multi-language support

## 📄 License

Private - Personal use only

## 🤖 Built With Claude Code

This entire system was built using Claude Code for automated content generation at scale.

---

**Last Updated:** October 26, 2025
**Version:** 1.0
