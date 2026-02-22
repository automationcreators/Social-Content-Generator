---
title: "How I Found 246 Acquisition Targets in 2 Days (Without Paying for Data)"
topic: Building an automated acquisition target discovery system
variation_type: authority
date: 2025-12-04
content_type: full_script
project: OwnerScraper
project_status: Active - Multi-State Expansion (FL + GA)
results: 246 verified executives from 143 schools in Texas pilot
---

# YouTube Script: How I Found 246 Acquisition Targets in 2 Days

## Strategic Reasoning
This script leads with M&A credibility and specific results. Appeals to searchers, operators, and investors looking for deal flow without expensive data subscriptions. Demonstrates the intersection of automation + acquisition strategy.

---

## Hook (Kallaway's 4-Part Structure)

### Part 1: Context Lean (5-7 seconds)
"Finding acquisition targets is expensive. Data brokers charge $20,000+ for lists. LinkedIn Sales Navigator is $1,200/year. And most of the data is outdated anyway."

### Part 2: Scroll Stop (3-5 seconds)
"But here's what nobody tells you—"

### Part 3: Contrarian Snapback (5-10 seconds)
"The best acquisition data isn't for sale. It's sitting in public records—state registrars, business filings, licensing databases. And with the right automation, you can extract more qualified targets in 48 hours than most brokers compile in a month."

### Part 4: Credibility Enhancer (5-7 seconds)
"I've spent 15 years in M&A and SMB investing. Last quarter, I built a system that identified 246 verified executives from 143 private schools in Texas—complete with ownership structures, contact info, and acquisition suitability scores. Zero data subscriptions. Here's exactly how."

**Visual Callouts:** 246 EXECUTIVES | 143 TARGETS | 48 HOURS | $0 DATA COST

---

## Body Section

### Point 1: WHY Traditional Deal Sourcing is Broken

**WHY it matters:**
Let me tell you what deal sourcing looks like for most searchers and small PE firms:

1. Pay $15-20K for a "proprietary" list from a broker
2. Discover 40% of the contacts are outdated
3. Spend weeks qualifying leads manually
4. Compete with 10 other buyers who got the same list

The data is commoditized. Everyone's fishing in the same pond.

**[VISUAL: $20K LISTS | 40% OUTDATED | SAME POND]**

**WHAT I discovered from portfolio work:**
Across $500M in analyzed deals, I noticed something: the best acquisitions came from targets that weren't on anyone's list. They were sourced through:
- Direct outreach to owners found in public filings
- Relationships built before the business was "for sale"
- Proprietary research that competitors couldn't replicate

The common thread? Differentiated data.

**HOW I applied this to education acquisitions:**
Private education is a sector I know well. High fragmentation, aging owner demographics, and clear acquisition criteria (Title IV status, enrollment, profitability).

But the problem was scale. How do you research 1,600+ schools across Florida alone? Manually? Impossible.

So I built a system.

**Pattern Break:** "This first insight—that public data beats paid data—is just the starting point. What I'm about to show you is the automation that makes it actionable."

---

### Point 2: WHAT the OwnerScraper System Does

**WHY it matters:**
The system has one job: transform raw state licensing data into qualified acquisition targets with verified decision-maker contact information.

Here's the pipeline:

**[VISUAL: RAW DATA → QUALIFIED TARGETS | AUTOMATION PIPELINE]**

**WHAT the system processes:**

**Stage 1: Data Ingestion**
- Import: State licensing database (schools with operating permits)
- Enrich: Cross-reference with Title IV federal database
- Filter: Flag and exclude non-targets automatically

Exclusion criteria:
- `.edu` domains → Mark as "accredited" (different buyer profile)
- `.org` domains → Mark as "non-profit" (different deal structure)
- Contains "college" or "university" → Mark as "high probability Title IV"
- 90%+ fuzzy match on Title IV database → Mark as "Title IV confirmed"

This single filter eliminated 60% of the list immediately—saving weeks of manual research on schools that don't fit the acquisition criteria.

**Stage 2: Ownership Discovery**
For remaining targets, the system:
- Queries state registrar (Texas Comptroller, Florida Sunbiz, Georgia SOS)
- Extracts: Entity type, registered agent, officers, directors
- Validates: Cross-references business address with school address
- Scores: Ownership confidence (0-100%)

**Stage 3: Contact Enrichment**
- Discovers/validates website URLs
- Extracts phone numbers from websites
- Identifies emails (direct or info@)
- Verifies emails via bulk verification API

**[VISUAL: 3-STAGE PIPELINE | FILTER → DISCOVER → VERIFY]**

**HOW results compound:**
Texas pilot results:
- **Input:** 627 private schools
- **After Title IV filter:** 143 schools (77% eliminated)
- **Verified executives:** 246 (1.7 contacts per target)
- **Email verification rate:** 89%
- **Time invested:** 48 hours (mostly automation running)

Compare that to manual research: 627 schools × 30 minutes each = 313 hours.

The system delivered 6.5x efficiency—and the data is BETTER because it's sourced directly from public filings, not recycled databases.

**Pattern Break:** "Now here's where this gets interesting for YOUR deal flow. Let me show you how to build your own version—even if you're not technical."

---

### Point 3: HOW to Build Your Own Acquisition Research System

**WHY it matters:**
The specific tech stack matters less than the framework. Whether you're targeting schools, healthcare practices, home services, or manufacturing—the pattern is the same:

1. Find the public data source for your sector
2. Build filters that eliminate non-targets early
3. Automate ownership discovery from state registrars
4. Verify and enrich contact information
5. Output to CRM for outreach

**[VISUAL: 5-STEP FRAMEWORK | SECTOR-AGNOSTIC]**

**WHAT you need for each sector:**

**Education:**
- State licensing databases (each state publishes online)
- Title IV Institution Campus database (federal, free)
- State registrar API or scraper

**Healthcare:**
- State medical board license lookups
- CMS provider databases (federal, free)
- State corporation filings

**Home Services:**
- State contractor licensing databases
- Better Business Bureau data
- State business registrations

**Manufacturing:**
- Industry association directories
- State manufacturer registries
- EPA facility databases (public)

**HOW I built the tech stack:**

**Tools (all free or low-cost):**
- **Scraping:** Puppeteer/Playwright (free, handles dynamic sites)
- **Fuzzy matching:** RapidFuzz or fuzzywuzzy (Python, free)
- **Data processing:** Pandas (Python, free)
- **Email verification:** EmailBulkVerify (~$50/10K verifications)
- **LLM enrichment:** Perplexity API (for edge cases needing web research)
- **Database:** SQLite or Supabase (free tier sufficient)

**Rate limiting strategy:**
- State registrar sites have anti-bot measures
- 1-2 second delays between requests
- Residential proxies if needed (Apify, ScrapingBee)
- Respect robots.txt and terms of service

**Output schema:**
Every target gets a standardized record:
- School/company name
- Classification (private, non-profit, Title IV, etc.)
- Entity type (LLC, Corp, etc.)
- Officers and directors (JSON array)
- Registered agent
- Verified contact info
- Ownership confidence score
- Research date and source

**Closer:** "This system isn't magic. It's just the boring work of data research—automated and systematized. The advantage isn't the technology. It's that most buyers won't build this."

---

## Outro

**Value Summary:**
Here's the bottom line: 246 qualified targets in 48 hours. Zero data subscription costs. All sourced from public records that anyone can access—but almost nobody automates.

**Future Pacing:**
Imagine having a pipeline that continuously identifies acquisition targets in your sector—filtered to your criteria, enriched with ownership data, verified contact info ready for outreach. Not buying stale lists. Building proprietary deal flow that your competitors can't replicate.

**Native Embed CTA:**
If you want the implementation roadmap—including the state registrar queries, the filtering logic, and the output schema—I'm putting together a more detailed breakdown. Drop "ACQUIRE" in the comments and I'll send you early access.

**Engagement Request:**
What sector are you focused on for acquisitions? I'm curious where else this framework would create the most value. Drop it in the comments.

---

## Visual Callouts Summary
- 246 EXECUTIVES
- 143 TARGETS
- 48 HOURS
- $0 DATA COST
- $20K LISTS → FREE PUBLIC DATA
- 6.5x EFFICIENCY
- 3-STAGE PIPELINE
- 5-STEP FRAMEWORK

---

## Production Notes
- **Anonymize:** No specific school names or executive names in video
- **B-Roll:** Screen recording of state registrar interface
- **Data viz:** Show funnel from 627 → 143 → 246
- **CTA:** Comment trigger for waitlist

---

## Key Project Details (For Reference)
- Project Location: /Documents/claudec/active/OwnerScraper/
- Current Scope: Florida (1,611 schools) + Georgia (2,148 schools)
- Texas Results: 246 executives from 143 non-Title IV schools
- Tech Stack: Node.js, Puppeteer, Python, Pandas, SQLite
- State Sources: Sunbiz (FL), ecorp.sos.ga.gov (GA), Texas Comptroller (TX)
