---
title: "How I Find Content Ideas Before They're Trending (246+ Sources Automated)"
topic: Building a cross-platform trend detection system
variation_type: contrarian
date: 2025-12-17
content_type: full_script
project: ContentGen
project_status: Production - Active
tech_stack: Flask, SQLite, Apify, YouTube API, RSS
sources: 246+ RSS feeds, YouTube channels, Twitter/X accounts
---

# YouTube Script: Find Trends Before They're Trending

## Strategic Reasoning
Contrarian angle challenging the "react to trends" approach most creators take. Appeals to content creators tired of being late to trends. Demonstrates compound leverage through automated intelligence gathering.

---

## Hook (Kallaway's 4-Part Structure)

### Part 1: Context Lean (5-7 seconds)
"Most content creators find out about trends the same way—they scroll Twitter until they see something blowing up, then scramble to make a video about it."

### Part 2: Scroll Stop (3-5 seconds)
"But here's the problem with that approach—"

### Part 3: Contrarian Snapback (5-10 seconds)
"By the time something is trending on your feed, it's already too late. The algorithm has already shown it to millions of people. You're not riding the wave—you're swimming in the wake. What if you could see trends BEFORE they hit the mainstream?"

### Part 4: Credibility Enhancer (5-7 seconds)
"I built a system that monitors 246 RSS feeds, dozens of YouTube channels, and Twitter accounts around the clock. It detects patterns, flags emerging topics, and tells me what to create BEFORE everyone else catches on. Let me show you exactly how it works."

**Visual Callouts:** 246+ SOURCES | BEFORE MAINSTREAM | PATTERN DETECTION | AUTOMATED INTELLIGENCE

---

## Body Section

### Point 1: WHY Reactive Content Creation Fails

**WHY it matters:**
Let me show you the math on reactive content creation.

**The typical creator workflow:**
1. Monday: See trending topic on Twitter
2. Tuesday: Research and outline
3. Wednesday: Record and edit
4. Thursday: Upload and optimize
5. Friday: Video goes live

By Friday, the trend is 5 days old. Every major creator has already published. The algorithm is saturated with content on that topic.

**[VISUAL: 5-DAY LAG | SATURATED ALGORITHM]**

**WHAT the data shows:**
- First-mover content gets 3-5x more impressions
- "Me too" content competes against established videos
- YouTube's algorithm favors fresh takes on emerging topics
- By day 3 of a trend, CTR drops by 40%

**HOW most creators try to solve this:**
- Doom-scroll Twitter more
- Join Discord servers for "hot tips"
- Follow trend alert accounts
- Set up Google Alerts

The problem? These are all REACTIVE. You're waiting for someone else to tell you what's trending.

I wanted to be the one who SEES it first.

**Pattern Break:** "That's when I started building ContentGen—a system that doesn't wait for trends to surface. It watches the sources where trends BEGIN."

---

### Point 2: WHAT the ContentGen System Does

**WHY it matters:**
ContentGen is a cross-platform content intelligence system. It aggregates, analyzes, and surfaces emerging topics from 246+ sources before they hit mainstream feeds.

**[VISUAL: 246+ SOURCES → ANALYSIS → EARLY SIGNALS]**

**WHAT it monitors:**

**Layer 1: RSS Aggregation (246+ feeds)**
- Industry newsletters (AI, business, tech)
- Niche blogs that break stories early
- Press release feeds (product launches)
- Academic publications (research drops)
- Government databases (policy changes)

These sources are UPSTREAM of Twitter. By the time something hits social media, it's usually been in an RSS feed for 12-48 hours.

**Layer 2: YouTube Intelligence**
- Channel monitoring (competitors, thought leaders)
- Transcript analysis (what topics are they covering?)
- Velocity detection (sudden increase in videos about X topic)
- Comment sentiment (what are viewers asking for?)

**Layer 3: Twitter/X Collection**
- Specific accounts (early signal accounts, not mainstream)
- Personal archive import (your own engagement data)
- Apify live collection (~$0.40/1000 tweets)
- Keyword tracking with velocity alerts

**[VISUAL: RSS → YOUTUBE → TWITTER | UPSTREAM INTELLIGENCE]**

**HOW analysis works:**

**Trend Detection Algorithm:**
1. **Keyword Frequency:** Track mention counts across all sources
2. **Velocity Scoring:** How fast is mention rate increasing?
3. **Cross-Platform Correlation:** Is the topic appearing in multiple source types?
4. **Freshness Weighting:** Recent mentions score higher
5. **Authority Weighting:** Mentions from high-authority sources score higher

When a topic scores above threshold on velocity + cross-platform + freshness, it gets flagged as an emerging trend.

**HOW I use it:**

Every morning, I check the ContentGen dashboard:
- **Trending Topics:** Sorted by velocity score
- **Content Gaps:** Topics with high interest, low coverage
- **Competitor Analysis:** What are they publishing about?
- **Idea Bank:** AI-generated content angles for each trend

Instead of "what should I create today?" I ask "which of these 5 emerging topics do I want to own?"

**Pattern Break:** "But the real power isn't just seeing trends early—it's in the compound leverage of having a historical database."

---

### Point 3: HOW the System Compounds Over Time

**WHY it matters:**
Most trend tools are point-in-time. ContentGen is historical. Every piece of content ever collected stays in the database.

**[VISUAL: POINT-IN-TIME vs. HISTORICAL]**

**WHAT this enables:**

**Pattern Recognition:**
After 6 months, I can see:
- Which topics cycle every quarter
- Which sources are consistently early
- Which content formats perform best for which topics
- Seasonal patterns I would have missed

**Content Archaeology:**
When a trend resurfaces, I can instantly find:
- Every article written about it in the last year
- What angles have already been covered
- What the common misconceptions were
- What questions audiences asked last time

**Predictive Intelligence:**
The system starts to predict trends before they even emerge:
- "Topic X had a spike last October. Watch list for this October."
- "Source Y was 48 hours early on the last 3 trends. Prioritize their content."
- "Keyword Z correlates with keyword W 80% of the time. If Z spikes, watch W."

**HOW I built it (simplified):**

**Tech Stack:**
- **Backend:** Flask (Python)
- **Database:** SQLite (5 tables for trend analysis)
- **RSS:** FeedParser library (free)
- **YouTube:** YouTube Data API (free tier: 10k units/day)
- **Twitter:** Apify ($0.40/1000 tweets)
- **Analysis:** Python + pandas + simple velocity calculations

**Data Schema:**
- Content Ideas (main repository)
- Trend Keywords (with velocity scores)
- Keyword Correlations (cross-topic patterns)
- Source Performance (which feeds are most reliable)
- Collections (organized content groups)

**Daily Operation:**
- RSS pulls run every 4 hours
- YouTube scans run daily
- Twitter collection runs on-demand or scheduled
- Dashboard updates in real-time

**[VISUAL: TECH STACK | DAILY RHYTHM]**

**HOW to start your own:**

**Week 1: RSS Foundation**
1. Identify 20-30 upstream sources in your niche
2. Set up FeedParser with SQLite storage
3. Create simple frequency tracking
4. Check daily for emerging patterns

**Week 2: Add YouTube**
1. Identify 10-20 channels in your space
2. Use YouTube API to track recent uploads
3. Cross-reference with RSS topics

**Week 3: Add Twitter/X**
1. Import your own archive (free, valuable)
2. Add Apify for live collection ($5-10/month)
3. Connect to trend analysis

**Week 4: Build Dashboard**
1. Simple Flask app to visualize
2. Sort by velocity score
3. Flag cross-platform mentions
4. Export ideas to your content calendar

**Closer:** "The goal isn't to react faster. It's to see the wave forming while everyone else is looking at their feet."

---

## Outro

**Value Summary:**
Here's the shift: I stopped asking "what's trending?" and started asking "what's about to trend?" The difference is 246 upstream sources, automated collection, and velocity analysis that surfaces emerging topics days before they hit mainstream feeds.

**Future Pacing:**
Imagine checking your dashboard tomorrow morning and seeing three topics that are about to blow up—with cross-platform data proving they're emerging, not just noise. You choose the one that fits your expertise. You publish first. The algorithm rewards you.

**Native Embed CTA:**
I'm putting together a list of the RSS feeds I monitor—organized by niche and reliability. If you want early access, drop "UPSTREAM" in the comments and I'll send it over.

**Engagement Request:**
What's your current process for finding content ideas? Manual scrolling? Newsletters? Curiosity streams? I want to know what's working—and what's frustrating.

---

## Visual Callouts Summary
- 246+ SOURCES
- BEFORE MAINSTREAM
- PATTERN DETECTION
- 5-DAY LAG
- SATURATED ALGORITHM
- RSS → YOUTUBE → TWITTER
- UPSTREAM INTELLIGENCE
- POINT-IN-TIME vs. HISTORICAL
- SEE THE WAVE FORMING

---

## Production Notes
- **Screen recording:** Show dashboard with velocity scores
- **Before/After:** Reactive scrolling vs. dashboard check
- **Data viz:** Show trend emergence timeline (upstream → mainstream)
- **CTA:** RSS feed list download

---

## Key Project Details (For Reference)
- Project Location: /Documents/claudec/active/ContentGen/
- Tech Stack: Flask, SQLite, YouTube API, Apify, RSS (FeedParser)
- Sources: 246+ RSS feeds, YouTube channels, Twitter accounts
- Features: RSS aggregation, YouTube transcript analysis, X.com integration, trend analysis, collections
- Twitter Cost: $0.40/1000 tweets via Apify
- Status: Production - actively used
