---
title: "How I Automated My Trading Edge (AI + Dealer Positioning)"
topic: Building an AI-powered trading setup detection system
variation_type: contrarian
date: 2025-12-04
content_type: full_script
project: Heatseeker
project_status: Planning Phase Complete - Ready for Phase 1 Development
---

# YouTube Script: How I Automated My Trading Edge

## Strategic Reasoning
This script positions you as a systems-thinker who applies business automation principles to trading. Appeals to traders frustrated with indicator overload and looking for an edge. Demonstrates technical credibility while staying accessible.

---

## Hook (Kallaway's 4-Part Structure)

### Part 1: Context Lean (5-7 seconds)
"Most traders are staring at 15 indicators, second-guessing every entry, and still losing money. I was that trader. Then I built something different."

### Part 2: Scroll Stop (3-5 seconds)
"But here's what changed everything—"

### Part 3: Contrarian Snapback (5-10 seconds)
"I stopped trying to predict price and started reading dealer intent. Specifically, I built an AI system that captures heatmap data, combines it with technical confirmation, and flags setups with 7/10 or higher probability—before I even look at a chart."

### Part 4: Credibility Enhancer (5-7 seconds)
"After 15 years building automation systems for portfolio companies, I applied the same compound leverage thinking to my trading. Today I'm going to show you exactly how this setup scout works—the tech stack, the logic, and the specific signals it's looking for."

**Visual Callouts:** DEALER INTENT | 7/10 PROBABILITY | SETUP SCOUT | ZERO INDICATOR OVERLOAD

---

## Body Section

### Point 1: WHY Most Trading Systems Fail

**WHY it matters:**
Here's the uncomfortable truth about trading systems: most of them are backwards.

They're trying to predict what price WILL do based on what price HAS done. Moving averages, RSI, MACD—they're all lagging indicators. You're essentially driving by looking in the rearview mirror.

What I learned from building business automation systems is that the best systems don't predict—they detect. They find patterns that are ALREADY happening, not patterns you hope will happen.

**[VISUAL: PREDICT vs. DETECT | LAGGING vs. LEADING]**

**WHAT I discovered:**
Dealers—market makers, options traders with serious capital—they don't hope. They position. And their positioning shows up in data most retail traders ignore.

GEX (Gamma Exposure) and VEX (Vanna Exposure) heatmaps show where dealers are positioned. These aren't predictions. These are CURRENT positions that create magnetic effects on price.

When price approaches a node where dealers have significant exposure, one of two things happens:
- **Bounce**: Price respects the level because dealers defend their position
- **Break**: Price blows through because the node is "unwinding"

The setup scout I built is designed to detect WHICH scenario is most likely—before I take a trade.

**HOW this changes the game:**
Instead of analyzing 10 indicators and still being uncertain, I get alerts like:

> "SPY at first-touch king node, GEX accumulating, EMA alignment confirmed, volume spike. Setup score: 8/10."

That's a trade I take. Everything else, I ignore.

**Pattern Break:** "Now, you might be thinking—this sounds complicated to build. But the tech stack is actually simpler than you'd expect. Let me show you exactly what's under the hood."

---

### Point 2: WHAT the Heatseeker System Actually Does

**WHY it matters:**
The system runs on a schedule—capturing data at specific market times when setup probability is highest:
- 9:30-10:00 AM: Early-day gatekeeper rejections
- 10:30 AM: First-hour consolidation
- 12:00 PM: Midday map status
- 3:30-4:00 PM: Power Hour dynamics

**[VISUAL: 4 CAPTURE WINDOWS | STRATEGIC TIMING]**

**WHAT it captures and analyzes:**

**Layer 1: Heatmap Capture**
- Puppeteer automates browser navigation to Skylit.ai
- Screenshots every ticker in my watchlist
- OCR extracts GEX/VEX values from the heatmap images
- All data logged to SQLite database with timestamps

**Layer 2: Technical Confirmation**
- yfinance pulls OHLCV chart data
- Pandas-TA calculates: EMA (9, 21, 50, 200), VWAP, volume profile, ATR
- System identifies supply/demand zones I've pre-defined
- Checks zone "freshness" (first touch vs. 3rd retest)

**Layer 3: Setup Scoring**
The magic is in the scoring logic. Here's the actual framework:

```
Heatseeker Signals (max 10 points):
- First-touch node: +3
- Node accumulating: +2
- Price at range edge: +2
- Multi-index aligned (SPX + SPY + QQQ): +2
- Gatekeeper rejection: +1

Technical Confirmation (bonus):
- Price at supply/demand zone: +1
- EMAs aligned: +1
- Fresh candle pattern: +1
- Volume confirms: +1

Alert threshold: 7/10 or higher
```

**[VISUAL: SCORING LOGIC | 7/10 THRESHOLD]**

**HOW alerts work:**
When a setup scores 7/10 or higher, I get a Discord notification with:
- Ticker and current price
- Setup type (gatekeeper rejection, king node bounce, etc.)
- Confidence score
- Supporting data points

I don't have to hunt for setups. The setups find me.

**Pattern Break:** "But here's the part that separates this from a typical trading indicator—the system learns. Let me show you the feedback loop."

---

### Point 3: HOW the System Compounds Over Time

**WHY it matters:**
Most trading tools are static. You download them, you use them, and they never get better.

Heatseeker is designed to compound—exactly like the business systems I build for portfolio companies.

Every trade I take, win or lose, gets logged back into the database. Over time, the system builds a record of:
- Which setup types perform best
- Which time windows have highest hit rate
- Which confluence combinations are most reliable
- Where my own biases cause deviation

**[VISUAL: FEEDBACK LOOP | COMPOUNDS OVER TIME]**

**WHAT this enables:**

**Backtesting with real data:**
After 3 months of logging, I can run queries like:
- "Show me all gatekeeper rejections before 10 AM with GEX accumulating"
- "What's my win rate on first-touch king nodes vs. second retests?"
- "Which days of the week have highest setup quality?"

**Algorithm refinement:**
The scoring weights aren't fixed. As data accumulates, I can adjust:
- Maybe first-touch nodes are worth +4, not +3
- Maybe multi-index alignment is less predictive than I thought
- Maybe Power Hour setups have lower hit rates

**HOW to build your own version:**

The tech stack is entirely free/open source:
- **Automation:** Puppeteer + Node.js
- **Data:** yfinance (Python)
- **Indicators:** Pandas-TA
- **OCR:** Tesseract
- **Database:** SQLite
- **Alerts:** Discord webhooks

I'll link the GitHub repo in the description with the full implementation roadmap.

**Closer:** "This isn't about having more indicators. It's about having a SYSTEM that does the pattern recognition for you—and gets smarter every week."

---

## Outro

**Value Summary:**
Here's what 15 years of building automation systems taught me: the best systems don't just execute—they compound. Heatseeker applies that same principle to trading. One system that captures data, confirms with technicals, scores probability, alerts me to setups, and learns from outcomes.

**Future Pacing:**
Imagine opening your trading platform tomorrow and instead of scanning 50 charts, you check one Discord channel. Three alerts waiting. Each one scored 7/10 or higher with supporting data. You take the best setup, manage the trade, log the outcome—and the system gets smarter.

**Native Embed CTA:**
If you want the full technical breakdown—the Puppeteer scripts, the scoring logic, the database schema—I'll link the GitHub repo and implementation roadmap in the description.

**Engagement Request:**
I'm curious—what's the ONE thing you wish you could automate in your trading workflow? Drop it in the comments. I might build it next.

---

## Visual Callouts Summary
- DEALER INTENT
- 7/10 PROBABILITY
- PREDICT vs. DETECT
- 4 CAPTURE WINDOWS
- SCORING LOGIC
- FEEDBACK LOOP
- COMPOUNDS OVER TIME

---

## Production Notes
- **B-Roll:** Screen recording of Skylit.ai heatmaps
- **Demo:** Show actual alert examples (anonymized)
- **Code snippets:** Display scoring logic pseudocode
- **CTA:** GitHub repo link in description

---

## Key Project Details (For Reference)
- Project Location: /Documents/claudec/active/heatseeker/
- Tech Stack: Puppeteer, yfinance, Pandas-TA, Tesseract, SQLite, Discord
- Status: Planning Complete - Ready for Phase 1 Development
- GitHub: https://github.com/automationcreators/heatseeker
