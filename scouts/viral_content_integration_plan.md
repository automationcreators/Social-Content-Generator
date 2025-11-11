# Viral Content Discovery - Automated Integration Plan

## Current State

**RSS Content Scout (scouts/rss_content_scout.py)**
- Source: ContentGen database (7,540 items)
- Problem: Data is 3+ weeks old (last update: Oct 13)
- Scoring: Relevance (30) + Brand Alignment (25) + Viral (20) + Trending (15) + Quality (10) = 100
- Output: `rss_ideas_database.json` (top 30 ideas)

**Manual Workaround**
- Currently using web search to find viral AI trends
- 5 ideas manually researched and added
- Not sustainable for daily operation

---

## Discovered n8n Viral Content Workflows

### 1. Reddit Content Research
**Location:** `/Users/elizabethknopf/Downloads/Reddit content research.json`

**What It Does:**
- Scrapes Reddit posts from target subreddits
- Filters by "hot" (viral) posts
- LLM extraction (using Grok):
  - Reddit Post Summary (1 sentence)
  - Theme (main idea)
  - Key Points (bullet points)
- LLM generates content ideas + themes
- Claude generates hooks and angles
- Saves to Google Sheets

**Subreddits to Target:**
- r/MarketingAutomation
- r/artificialintelligence
- r/ChatGPT
- r/ClaudeAI
- r/SaaS
- r/Entrepreneur
- r/smallbusiness

### 2. LinkedIn Insights Scraper
**Location:** `/Users/elizabethknopf/Downloads/automationcreators-workflows 2/...`

**What It Does:**
- Uses LinkedIn API (RapidAPI)
- Fetches posts you marked as "insightful"
- Filters last 7 days
- Extracts:
  - Title (from username)
  - Description (post text)
  - Source (URL)
- Saves to Airtable

**Why It's Valuable:**
- Your own curation (already filtered by your judgment)
- Recent (7 days)
- Proven to resonate (you found it insightful)

### 3. Hacker News Scraper
**Location:** `/Users/elizabethknopf/Documents/awesome-n8n-templates-main/AI_Research_RAG_and_Data_Analysis/`

**What It Does:**
- Scrapes HN frontpage
- Filters tech/AI stories
- Parses engagement (points, comments)
- Identifies trending topics

### 4. Instagram Top Trends Generator
**Location:** `/Users/elizabethknopf/Documents/awesome-n8n-templates-main/Instagram_Twitter_Social_Media/`

**What It Does:**
- Monitors Instagram trending topics
- Generates content ideas
- AI image generation

### 5. Twitter/X Scraping
**Potential Sources:**
- Trending hashtags (#AI, #automation)
- Top AI influencer tweets
- Viral threads

---

## Proposed Multi-Source Viral Content Pipeline

### Architecture

```
Daily Viral Content Scout (Runs at 6 AM)
│
├─ Source 1: Reddit Hot Posts
│  ├─ r/artificialintelligence (limit: 10)
│  ├─ r/ChatGPT (limit: 10)
│  ├─ r/ClaudeAI (limit: 5)
│  ├─ r/MarketingAutomation (limit: 5)
│  └─ r/Entrepreneur (limit: 5)
│  └─> Extract themes, points, viral potential
│
├─ Source 2: LinkedIn Insights (Your Likes)
│  ├─ Fetch "insightful" reactions (last 7 days)
│  └─> Already pre-filtered by your judgment
│
├─ Source 3: Hacker News Frontpage
│  ├─ Top 10 AI/tech stories
│  └─> Extract engagement metrics
│
├─ Source 4: ContentGen RSS Database
│  ├─ If updated in last 7 days: Use it
│  └─> Fallback to web search if stale
│
└─ Source 5: Twitter/X Trending (Optional)
   ├─ #AI hashtag top posts
   └─> Viral threads from AI influencers
```

### Aggregation & Scoring

```python
# Combine all sources
all_ideas = []
all_ideas.extend(reddit_ideas)      # ~35 ideas
all_ideas.extend(linkedin_ideas)    # ~10 ideas
all_ideas.extend(hackernews_ideas)  # ~10 ideas
all_ideas.extend(contentgen_ideas)  # ~20 ideas (if fresh)
all_ideas.extend(twitter_ideas)     # ~10 ideas (optional)

# Total: ~75-85 raw ideas

# Enhanced Scoring System
for idea in all_ideas:
    score = calculate_enhanced_score(idea)
    # Relevance (0-25): AI/automation/business keywords
    # Brand Alignment (0-20): Claude/no-code/small business
    # Viral Potential (0-25): Engagement metrics (upvotes, likes, comments)
    # Recency (0-15): Posted in last 7 days = full score
    # Authority (0-10): Source reputation (HN > Reddit > Twitter)
    # Personal Resonance (0-5): From LinkedIn likes = bonus

# Filter & Deduplicate
qualified_ideas = [idea for idea in all_ideas if idea.score >= 30]
deduplicated = remove_duplicates(qualified_ideas)

# Sort by score
top_ideas = sorted(deduplicated, key=lambda x: x.score, reverse=True)[:30]

# Save to rss_ideas_database.json
save_to_database(top_ideas)
```

### Data Flow

```
Multi-Source Scout → rss_ideas_database.json (30 ideas)
                              ↓
                  UI (http://localhost:8888)
                              ↓
                  User selects 3-5 ideas + adds notes
                              ↓
                  selected_ideas.json
                              ↓
            Script Generator (generate_from_selected.py)
                              ↓
              3 variations per idea × 3-5 ideas = 9-15 scripts
                              ↓
                  pillar_scripts/
                              ↓
                  Google Sheets sync
```

---

## Implementation Plan

### Phase 1: Reddit Integration (Highest ROI)

**File:** `scouts/reddit_viral_scout.py`

```python
class RedditViralScout:
    """
    Scrapes Reddit hot posts from AI/business subreddits
    Uses Reddit API (requires Reddit app credentials)
    """

    subreddits = [
        {"name": "artificialintelligence", "limit": 10},
        {"name": "ChatGPT", "limit": 10},
        {"name": "ClaudeAI", "limit": 5},
        {"name": "MarketingAutomation", "limit": 5},
        {"name": "Entrepreneur", "limit": 5},
    ]

    def scrape_hot_posts(self, subreddit, limit=10):
        """Fetch hot posts from subreddit"""
        # Use PRAW (Python Reddit API Wrapper)
        pass

    def extract_viral_signals(self, post):
        """Extract engagement metrics"""
        return {
            'upvotes': post.score,
            'comments': post.num_comments,
            'upvote_ratio': post.upvote_ratio,
            'awards': post.total_awards_received
        }

    def score_idea(self, post):
        """Enhanced scoring with viral signals"""
        viral_score = (
            (post.score / 1000) * 10 +  # Upvotes
            (post.num_comments / 100) * 5 +  # Comments
            post.upvote_ratio * 5 +  # Quality
            post.total_awards_received * 2  # Awards
        )
        return min(viral_score, 25)  # Cap at 25
```

### Phase 2: LinkedIn Integration

**File:** `scouts/linkedin_insights_scout.py`

```python
class LinkedInInsightsScout:
    """
    Fetches LinkedIn posts you marked as 'insightful'
    Uses RapidAPI LinkedIn scraper
    """

    def fetch_insightful_likes(self, username, days_back=7):
        """Get your LinkedIn 'insightful' reactions"""
        # HTTP request to RapidAPI
        pass

    def filter_recent(self, likes, days=7):
        """Only last 7 days"""
        cutoff = datetime.now() - timedelta(days=days)
        return [like for like in likes if like.posted_date >= cutoff]

    def format_as_idea(self, post):
        """Convert LinkedIn post to idea format"""
        return {
            'id': generate_id(post.url),
            'title': f"LinkedIn Insight: {post.author}",
            'description': post.text,
            'source': 'LinkedIn (Your Likes)',
            'url': post.url,
            'score': 85,  # Pre-scored high (your curation)
            'personal_resonance': True  # Bonus flag
        }
```

### Phase 3: Unified Scout Orchestrator

**File:** `scouts/unified_viral_scout.py`

```python
class UnifiedViralScout:
    """
    Orchestrates all viral content sources
    Aggregates, scores, deduplicates, saves
    """

    def __init__(self):
        self.reddit_scout = RedditViralScout()
        self.linkedin_scout = LinkedInInsightsScout()
        self.contentgen_scout = RSSContentScout()

    def run_daily_scan(self):
        """Main orchestrator"""

        print("🔍 Starting Multi-Source Viral Content Scan...")

        # Collect from all sources
        ideas = []

        # Source 1: Reddit
        print("📡 Scanning Reddit...")
        reddit_ideas = self.reddit_scout.scan()
        ideas.extend(reddit_ideas)
        print(f"   ✅ Found {len(reddit_ideas)} Reddit ideas")

        # Source 2: LinkedIn
        print("📡 Scanning LinkedIn insights...")
        linkedin_ideas = self.linkedin_scout.scan()
        ideas.extend(linkedin_ideas)
        print(f"   ✅ Found {len(linkedin_ideas)} LinkedIn ideas")

        # Source 3: ContentGen (if fresh)
        print("📡 Checking ContentGen database...")
        if self.contentgen_scout.is_fresh(days=7):
            contentgen_ideas = self.contentgen_scout.scan()
            ideas.extend(contentgen_ideas)
            print(f"   ✅ Found {len(contentgen_ideas)} ContentGen ideas")
        else:
            print("   ⚠️  ContentGen data stale (>7 days), skipping")

        print(f"\n📊 Total raw ideas collected: {len(ideas)}")

        # Score all ideas
        scored_ideas = [self.score_idea(idea) for idea in ideas]

        # Filter by threshold
        qualified = [i for i in scored_ideas if i['score'] >= 30]
        print(f"   ✅ {len(qualified)} ideas scored above 30")

        # Deduplicate
        unique = self.deduplicate(qualified)
        print(f"   ✅ {len(unique)} unique ideas after deduplication")

        # Sort by score
        top_ideas = sorted(unique, key=lambda x: x['score'], reverse=True)[:30]

        # Save to database
        output_data = {
            'metadata': {
                'scan_date': datetime.now().isoformat(),
                'sources': ['Reddit', 'LinkedIn', 'ContentGen'],
                'total_raw_ideas': len(ideas),
                'qualified_ideas': len(top_ideas),
                'min_score_threshold': 30
            },
            'ideas': top_ideas
        }

        output_file = Path(__file__).parent / 'rss_ideas_database.json'
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✅ Saved {len(top_ideas)} top ideas to rss_ideas_database.json")
        return output_data

    def deduplicate(self, ideas):
        """Remove duplicate ideas by title similarity"""
        # Use fuzzy matching to detect similar titles
        seen = set()
        unique = []
        for idea in ideas:
            # Simple title normalization
            normalized = idea['title'].lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique.append(idea)
        return unique

    def score_idea(self, idea):
        """Enhanced scoring with viral signals"""
        # Use existing scoring logic + viral bonuses
        base_score = idea.get('score', 0)

        # Bonuses
        if idea.get('personal_resonance'):
            base_score += 5  # LinkedIn likes bonus
        if idea.get('upvotes', 0) > 500:
            base_score += 10  # High Reddit engagement
        if idea.get('comments', 0) > 100:
            base_score += 5  # High discussion

        idea['score'] = min(base_score, 100)
        return idea
```

---

## Automation Integration

### Update `automation/daily_content_generator.py`

```python
# Replace current RSS scout call with unified scout
from scouts.unified_viral_scout import UnifiedViralScout

def run_daily_scan():
    """Daily content generation workflow"""

    # Step 1: Multi-source viral content scan
    scout = UnifiedViralScout()
    viral_ideas = scout.run_daily_scan()

    # Step 2: UI available at http://localhost:8888
    # (User selects ideas manually during day)

    # Step 3: Evening run generates scripts from selections
    # (Triggered by daily-evening.sh)

    return viral_ideas
```

### Add to `systems/daily-morning.sh`

```bash
# Morning: Scan viral content
echo "🔍 Scanning viral content sources..."
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator
python3 scouts/unified_viral_scout.py

# Start UI server for idea selection
echo "🚀 Starting RSS Idea Selector UI..."
python3 ui/api_server.py &

echo "📊 UI available at: http://localhost:8888"
echo "Select ideas during the day, scripts generated at 6 PM"
```

---

## Benefits of Multi-Source Approach

### 1. **Freshness**
- Reddit: Real-time hot posts (last 24 hours)
- LinkedIn: Your curated insights (last 7 days)
- Eliminates stale ContentGen dependency

### 2. **Diversity**
- Reddit: Community-validated trends
- LinkedIn: Professional insights
- HN: Tech/startup focus
- Multiple perspectives on same trends

### 3. **Quality Signals**
- Reddit upvotes/comments = viral potential
- LinkedIn "insightful" = your pre-filter
- HN frontpage = authority

### 4. **Volume**
- 75-85 raw ideas daily
- Filter to top 30
- User selects 3-5
- Generate 9-15 scripts

### 5. **Relevance**
- Brand alignment scoring
- AI/automation focus
- Small business angle

---

## Required Setup

### Reddit API
```bash
# Create Reddit app: https://www.reddit.com/prefs/apps
# Get: client_id, client_secret, user_agent

# Install PRAW
pip3 install praw
```

### LinkedIn API (RapidAPI)
```bash
# Sign up: https://rapidapi.com/rockapis-rockapis-default/api/linkedin-api8
# Get: X-RapidAPI-Key

# Free tier: 500 requests/month
```

### Credentials File
```python
# scouts/credentials.json
{
  "reddit": {
    "client_id": "...",
    "client_secret": "...",
    "user_agent": "Social-Content-Generator v1.0"
  },
  "linkedin_rapidapi": {
    "api_key": "...",
    "username": "your-linkedin-username"
  }
}
```

---

## Testing Plan

### Week 1: Reddit Only
```bash
python3 scouts/reddit_viral_scout.py
# Expected: 35 Reddit ideas
# Validate: Scores, deduplication, relevance
```

### Week 2: Add LinkedIn
```bash
python3 scouts/unified_viral_scout.py
# Expected: 45 combined ideas
# Validate: Personal resonance bonus working
```

### Week 3: Full Integration
```bash
# Morning run (automated)
bash systems/daily-morning.sh

# Check UI
open http://localhost:8888

# Select 3 ideas + add notes

# Evening run (automated)
bash systems/daily-evening.sh

# Verify: Scripts generated in pillar_scripts/
```

---

## Next Steps

1. **Create Reddit scout** (`scouts/reddit_viral_scout.py`)
2. **Create LinkedIn scout** (`scouts/linkedin_insights_scout.py`)
3. **Create unified orchestrator** (`scouts/unified_viral_scout.py`)
4. **Set up Reddit API credentials**
5. **Set up LinkedIn RapidAPI credentials**
6. **Test each source individually**
7. **Test combined pipeline**
8. **Integrate with daily automation**

---

## Estimated Timeline

- **Reddit Scout**: 2 hours
- **LinkedIn Scout**: 1 hour
- **Unified Orchestrator**: 2 hours
- **Testing & Debugging**: 2 hours
- **Integration with daily automation**: 1 hour
- **Total**: ~8 hours (1 working day)

---

## Success Metrics

**Before (Manual):**
- 5 manually researched ideas
- 1-2 hours research time
- Inconsistent quality

**After (Automated):**
- 30 algorithmically scored ideas
- 5 minutes selection time (via UI)
- 9-15 scripts generated automatically
- Fresh daily content from 3-5 sources
- Viral potential validated by engagement metrics
