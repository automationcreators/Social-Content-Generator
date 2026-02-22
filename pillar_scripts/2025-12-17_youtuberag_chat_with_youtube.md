---
title: "I Built a Tool That Lets Me Chat With Any YouTube Video"
topic: Building a RAG system for YouTube content
variation_type: transformation
date: 2025-12-17
content_type: full_script
project: YouTubeRAG
project_status: Production-ready
tech_stack: FastAPI, ChromaDB, OpenAI, SQLite
---

# YouTube Script: Chat With Any YouTube Video

## Strategic Reasoning
Transformation angle showing the before/after of content research. Appeals to content creators, researchers, and anyone who consumes YouTube for learning. Demonstrates practical AI application beyond chatbots.

---

## Hook (Kallaway's 4-Part Structure)

### Part 1: Context Lean (5-7 seconds)
"I watch 10-15 hours of YouTube content every week for research. Podcasts, tutorials, industry analysis. The problem? I could never find that ONE insight I remembered hearing—somewhere in a 3-hour video."

### Part 2: Scroll Stop (3-5 seconds)
"So I built something to fix it. And here's what surprised me—"

### Part 3: Contrarian Snapback (5-10 seconds)
"The hardest part wasn't the AI. It was figuring out how to chunk a 3-hour transcript so the AI could actually find relevant moments. Once I solved that, I could literally have a conversation with any YouTube video—and it would tell me EXACTLY where in the video to go."

### Part 4: Credibility Enhancer (5-7 seconds)
"The system now has over 100 videos indexed, with timestamped source links for every answer. I'll show you exactly how it works, the tech stack, and how you could build your own version for under $25 a month."

**Visual Callouts:** 10-15 HRS/WEEK | CHAT WITH VIDEOS | TIMESTAMPED SOURCES | <$25/MONTH

---

## Body Section

### Point 1: WHY Regular Search Fails for Video Content

**WHY it matters:**
YouTube's search is designed to find VIDEOS, not moments within videos.

When I'm researching a topic, I don't need another video. I need the specific 2-minute segment where an expert explained the concept I'm trying to understand.

**[VISUAL: VIDEO SEARCH vs. MOMENT SEARCH]**

**WHAT the problem looks like:**
Example: I'm writing a script about AI agents. I know I watched a video where someone explained the difference between agents and assistants brilliantly. But:
- Was it on Lex Fridman? AI Explained? The podcast with the CEO?
- Was it 20 minutes in or 2 hours in?
- What were the exact words they used?

Without timestamps, I'm scrubbing through hours of content manually. That's not research—that's archaeology.

**HOW traditional solutions fail:**
- **YouTube search:** Finds videos, not moments
- **Transcript downloads:** I'd have to read 50,000 words to find one paragraph
- **Note-taking apps:** Only works if I took notes in the first place
- **Memory:** Unreliable at best

I needed a system that could search INSIDE videos the way Google searches the web.

**Pattern Break:** "That's when I realized—this is exactly what RAG systems are designed to do. Let me show you how I built it."

---

### Point 2: WHAT the YouTubeRAG System Does

**WHY it matters:**
YouTubeRAG is a Retrieval-Augmented Generation system specifically designed for YouTube content. You give it a video URL, it processes the transcript, and then you can have a conversation with that content.

**[VISUAL: URL → PROCESS → CHAT]**

**WHAT happens when you process a video:**

**Step 1: Transcript Extraction**
The system pulls the transcript using YouTube's API—including timestamps for every sentence. No manual transcription needed.

**Step 2: Semantic Chunking**
This is where most people get it wrong. You can't just dump a 50,000-word transcript into an AI. You need to break it into meaningful chunks.

My system uses "semantic chunking":
- 300 tokens per chunk (about a paragraph)
- 50-token overlap between chunks (so context isn't lost)
- Sentence boundary detection (never cuts mid-thought)
- Coherence scoring (flags low-quality chunks)

**Step 3: Vector Embedding**
Each chunk gets converted into a vector—a mathematical representation of its meaning. These vectors go into ChromaDB, a vector database optimized for similarity search.

**Step 4: Chat Interface**
Now here's the magic. When I ask a question:
1. My question gets converted to a vector
2. ChromaDB finds the 8 most similar chunks
3. Those chunks become context for GPT-4
4. The AI answers WITH timestamped sources

**[VISUAL: QUESTION → SIMILAR CHUNKS → ANSWER + TIMESTAMPS]**

**HOW the output looks:**

When I ask: "What did they say about AI agent architectures?"

I get:
```
Based on the transcript, the speaker discussed three main agent
architectures: ReAct, Chain-of-Thought, and Function-Calling...

Sources:
[1] 23:45 - "The ReAct pattern is fundamentally about..."
[2] 28:12 - "Where this breaks down is when you need..."
[3] 31:08 - "The function-calling approach solves this by..."
```

Each source is a clickable link that takes me to that exact moment in the video.

**Pattern Break:** "But single videos are just the beginning. The real power is when you query across your entire library."

---

### Point 3: HOW to Build Your Own Version

**WHY it matters:**
The tech stack is entirely open source or pay-as-you-go. No expensive subscriptions. No vendor lock-in.

**[VISUAL: OPEN SOURCE STACK | PAY-AS-YOU-GO]**

**WHAT you need:**

**Backend:**
- **FastAPI** (Python) - Handles all the API endpoints
- **SQLite** - Stores video metadata and conversation history
- **ChromaDB** - Vector database for embeddings
- **youtube-transcript-api** - Free transcript extraction
- **OpenAI API** - Embeddings + chat responses

**Frontend:**
- Vanilla JavaScript + TailwindCSS
- Simple chat interface with source attribution
- Video library management

**HOW processing works (actual architecture):**

```
User submits URL
    ↓
Extract video ID → Fetch metadata → Fetch transcript
    ↓
Semantic chunking (300 tokens, 50 overlap)
    ↓
Generate embeddings (text-embedding-3-small)
    ↓
Store in ChromaDB with metadata
    ↓
Ready for queries
```

**HOW search works:**

```
User asks question
    ↓
Generate query embedding
    ↓
ChromaDB similarity search (cosine distance)
    ↓
Rerank results (coherence, recency, relevance)
    ↓
Build context from top 8 chunks
    ↓
GPT-4 generates response with source attribution
    ↓
Return answer + timestamped links
```

**WHAT this costs:**

| Component | Monthly Cost |
|-----------|-------------|
| Processing (50 videos) | $0.015 |
| Queries (500/month) | $22.50 |
| Storage (ChromaDB) | $0 (local) |
| **Total** | **~$23/month** |

The expensive part is queries, not processing. If you're doing heavy research, budget $40-50. Light usage is under $10.

**HOW to get started:**

1. Clone the repo (I'll link in description)
2. Add your OpenAI API key
3. Run `python app.py`
4. Submit your first video URL
5. Wait 30 seconds for processing
6. Start chatting

**Closer:** "I've processed over 100 videos now. Every insight I've ever heard is now searchable, quotable, and timestamped."

---

## Outro

**Value Summary:**
Here's the transformation: I went from scrubbing through hours of video to asking a question and getting the exact timestamp in seconds. Not by paying for expensive tools. By building a system that understands video content the way I need it to.

**Future Pacing:**
Imagine having every podcast, every tutorial, every industry talk you've ever watched—fully searchable. You remember hearing something brilliant about pricing strategy? Ask the system. It tells you which video, which minute, and exactly what was said.

**Native Embed CTA:**
The full codebase is on GitHub—including the chunking logic, the reranking algorithm, and the chat interface. I'll link it in the description along with a setup guide.

**Engagement Request:**
What YouTube content would you index first? Drop a channel or topic in the comments—I'm curious what research rabbit holes you'd go down with a system like this.

---

## Visual Callouts Summary
- 10-15 HRS/WEEK
- CHAT WITH VIDEOS
- TIMESTAMPED SOURCES
- VIDEO SEARCH vs. MOMENT SEARCH
- URL → PROCESS → CHAT
- QUESTION → CHUNKS → ANSWER
- <$25/MONTH

---

## Production Notes
- **Screen recording:** Show actual chat with real video
- **Demo:** Process a video live, show chunking happening
- **Before/After:** Manual scrubbing vs. instant answer
- **CTA:** GitHub repo link

---

## Key Project Details (For Reference)
- Project Location: /Documents/claudec/active/YouTubeRAG/
- Tech Stack: FastAPI, ChromaDB, SQLite, OpenAI, youtube-transcript-api
- API Port: 3011
- Status: Production-ready
- Cost: ~$0.045 per query, ~$0.0003 per video processed
