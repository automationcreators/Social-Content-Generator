---
title: "I Built a Chrome Extension in One Weekend (No Coding Experience Required)"
topic: Building Prompt Vault - A Chrome extension for prompt management
variation_type: transformation
date: 2025-12-04
content_type: full_script
project: PromptSaver (Prompt Vault)
project_status: v1.0.0 Complete - Ready for Chrome Web Store
tech_stack: React 18, TypeScript, Vite, TailwindCSS, IndexedDB
---

# YouTube Script: I Built a Chrome Extension in One Weekend

## Strategic Reasoning
Transformation angle with clear before/after. Appeals to business owners and operators who want to build tools but think they need to hire developers. Demonstrates Claude Code's capabilities while staying accessible to non-technical audience.

---

## Hook (Kallaway's 4-Part Structure)

### Part 1: Context Lean (5-7 seconds)
"I was copying and pasting the same prompts into Claude and ChatGPT dozens of times a day. Context, instructions, formatting—the same 500 words, over and over."

### Part 2: Scroll Stop (3-5 seconds)
"So I decided to build something to fix it. Here's the thing—"

### Part 3: Contrarian Snapback (5-10 seconds)
"I'm not a developer. I can't write React from scratch. I don't know TypeScript. But I built a fully functional Chrome extension in one weekend using Claude Code—and I'm going to show you exactly how."

### Part 4: Credibility Enhancer (5-7 seconds)
"The extension now saves me 2+ hours a week on prompt management. It works across Claude, ChatGPT, Perplexity, Gemini, and Grok. And I've documented the entire build process so you can do the same thing for YOUR workflow."

**Visual Callouts:** ONE WEEKEND | NO CODING | 2+ HRS/WEEK SAVED | 6 PLATFORMS

---

## Body Section

### Point 1: WHY I Needed This (The Problem)

**WHY it matters:**
Let me paint the picture of my daily workflow before this tool:

**Morning routine:**
1. Open Claude
2. Copy my "content creator" system prompt from a Google Doc
3. Paste it
4. Add today's context
5. Start working

**When I switch platforms:**
1. Open ChatGPT
2. Go back to Google Doc
3. Find the slightly different version for ChatGPT
4. Copy, paste, add context
5. Repeat

**When I write emails:**
1. Open new Claude chat
2. Copy my "email writer" prompt from... wait, which doc was that?
3. Search through 3 folders
4. Find it, copy, paste
5. Finally start working

**[VISUAL: COPY-PASTE HELL | 500 WORDS × 20 TIMES/DAY]**

**WHAT this was costing me:**
Conservative math:
- 20 paste operations/day × 30 seconds each = 10 minutes/day
- 10 minutes × 5 days × 52 weeks = 43 hours/year
- 43 hours at my hourly rate = significant money wasted on copy-paste

And that's not counting the friction—the mental load of remembering which prompt, which doc, which version.

**HOW I knew the solution:**
I needed:
- One-click prompt capture from any LLM platform
- Quick access with a keyboard shortcut (like TextBlaze)
- Organization by folder, tags, and usage frequency
- Works across ALL platforms, not just one

I searched for existing tools. Found a few—but they were either:
- Platform-specific (only Claude or only ChatGPT)
- Overly complex (enterprise pricing, team features I don't need)
- Missing the quick-access feature I wanted most

So I decided to build it.

**Pattern Break:** "Now, if you're thinking 'I can't build a Chrome extension'—I thought the same thing. Then I discovered Claude Code."

---

### Point 2: WHAT I Built (The Solution)

**WHY it matters:**
Prompt Vault is a Chrome extension that does three things:
1. **Capture:** One-click save from any LLM platform
2. **Organize:** Folders, tags, favorites, usage analytics
3. **Access:** Type `;;` anywhere for instant prompt search

**[VISUAL: CAPTURE → ORGANIZE → ACCESS]**

**WHAT the extension includes:**

**Feature 1: Universal Capture**
A small button appears next to the input field on every supported platform:
- Claude
- ChatGPT
- Grok
- Perplexity
- Gemini
- Meta AI

Click it, and the current prompt is saved with:
- Platform detected automatically
- Timestamp
- Option to add tags/folder

**Feature 2: Quick Command**
This is the killer feature. Type `;;` anywhere on a supported site, and a search popup appears. Start typing—fuzzy search finds your prompt instantly. Hit Enter, and it pastes into the input field.

Time to access any prompt: < 2 seconds.

**Feature 3: Analytics Dashboard**
The extension tracks:
- Which prompts you use most
- When you last used each prompt
- Which platforms you use most
- Total time saved (calculated based on usage)

**[VISUAL: ;; QUICK COMMAND | <2 SECONDS ACCESS | USAGE ANALYTICS]**

**HOW it's built (technically):**

**Tech stack:**
- React 18 + TypeScript (I didn't write this from scratch—Claude Code did)
- Vite (fast build tool)
- TailwindCSS (styling)
- IndexedDB via Dexie.js (local database)
- Fuse.js (fuzzy search)
- Chrome Manifest V3 (latest extension format)

**Architecture:**
- Background service worker handles cross-tab communication
- Content scripts inject the capture button on each platform
- Popup UI shows your prompt library
- All data stored locally—no server, no account needed

**Closer:** "The tech sounds complex, but here's the truth: Claude Code wrote 95% of this. My job was describing what I wanted."

---

### Point 3: HOW I Built It With Claude Code (Step-by-Step)

**WHY it matters:**
This is the part most people skip—the actual process. I'm going to be specific so you can replicate this for YOUR tool idea.

**[VISUAL: THE ACTUAL PROCESS | REPLICATE THIS]**

**WHAT the build looked like:**

**Day 1: Saturday Morning (3 hours)**

**Hour 1: Project Setup**
I told Claude Code:
> "I want to build a Chrome extension that saves prompts from Claude, ChatGPT, and other AI platforms. The user should be able to capture prompts with one click and access them later with a keyboard shortcut."

Claude Code:
- Created the project structure
- Set up React + TypeScript + Vite
- Configured Chrome Manifest V3
- Built the basic popup UI

I didn't write a single line of code. I described what I wanted, Claude Code built it.

**Hour 2: Platform Detection**
I said:
> "The extension needs to detect which AI platform the user is on and show a capture button next to the input field."

Claude Code:
- Created platform detection logic (checking URLs, DOM elements)
- Built content scripts for each platform
- Injected the capture button with proper styling
- Added platform-specific selectors for the input fields

**Hour 3: Database Setup**
I explained:
> "Prompts should be stored locally with the ability to organize by folder and tags. Include analytics like usage count and last used date."

Claude Code:
- Set up IndexedDB via Dexie.js
- Created the data schema
- Built CRUD operations
- Added analytics tracking

**[VISUAL: HOUR 1 → HOUR 2 → HOUR 3 | DESCRIBE → BUILD → ITERATE]**

**Day 1: Saturday Afternoon (3 hours)**

**Hours 4-5: Quick Command Feature**
This was the hardest part. I wanted:
> "When the user types `;;` in any input field, a floating search popup should appear. They can type to search their prompts, and hitting Enter pastes the selected prompt."

This required:
- Keyboard event listeners
- Fuzzy search integration
- Floating UI positioning
- Focus management

Claude Code built it in two iterations. First version had bugs—the popup appeared in the wrong position on some sites. I described the issue, Claude Code fixed it.

**Hour 6: Testing and Polish**
I tested on each platform, found edge cases, described them to Claude Code:
- "The button doesn't appear on ChatGPT's new UI"
- "The popup is hidden behind Claude's sidebar"
- "Fuzzy search isn't finding partial matches"

Each fix took 5-10 minutes.

**Day 2: Sunday (4 hours)**

**Hours 7-8: Analytics Dashboard**
> "Add a stats view that shows most-used prompts, platform breakdown, and total time saved."

**Hours 9-10: Export and Polish**
> "Add JSON and CSV export. Make the UI match modern Chrome extensions—clean, minimal, dark mode support."

**[VISUAL: 10 HOURS TOTAL | SATURDAY + SUNDAY]**

**HOW to replicate this:**

1. **Start with the problem, not the solution**
   - What task are you doing repeatedly?
   - What would "one-click" look like?
   - Where does the friction live?

2. **Describe the MVP to Claude Code**
   - Don't over-engineer the first version
   - "I want to save X and access it with Y"
   - Let Claude Code suggest the architecture

3. **Iterate based on testing**
   - Use the tool yourself immediately
   - Describe bugs in plain language
   - Each fix compounds into a better product

4. **Document as you go**
   - Claude Code can generate README files
   - Capture your learnings for the next project
   - Build your own "playbook" for future tools

**Closer:** "10 hours. One weekend. Zero prior extension development experience. The barrier isn't skill—it's starting."

---

## Outro

**Value Summary:**
Here's the transformation: I went from copy-pasting 500-word prompts 20 times a day to accessing any prompt in under 2 seconds. Not by hiring a developer. Not by learning to code. By describing what I needed to Claude Code and iterating until it worked.

**Future Pacing:**
What's the tool YOU need? The thing you do manually 10 times a day that makes you think "there has to be a better way"? There probably isn't—yet. But you could build it. This weekend. With the same process I just showed you.

**Native Embed CTA:**
I've documented the complete build process—every prompt I gave Claude Code, every iteration, every bug fix. It's all in a guide I'll link in the description. Plus the extension itself if you want to use it.

**Engagement Request:**
I'm genuinely curious—what tool would YOU build if you knew you could do it in a weekend? Drop it in the comments. I'll tell you if Claude Code can handle it.

---

## Visual Callouts Summary
- ONE WEEKEND
- NO CODING
- 2+ HRS/WEEK SAVED
- 6 PLATFORMS
- COPY-PASTE HELL
- ;; QUICK COMMAND
- <2 SECONDS ACCESS
- 10 HOURS TOTAL
- DESCRIBE → BUILD → ITERATE

---

## Production Notes
- **Screen recording:** Show the extension in action
- **Before/After:** Side-by-side of old workflow vs. new
- **Claude Code demo:** Show actual prompts given to Claude Code
- **CTA:** Link to extension + build guide

---

## Key Project Details (For Reference)
- Project Location: /Documents/claudec/active/promptSaver/
- GitHub: github.com/automationcreators/promptSaver
- Version: 1.0.0
- Tech Stack: React 18, TypeScript, Vite, TailwindCSS, IndexedDB (Dexie.js), Fuse.js
- Platforms Supported: Claude, ChatGPT, Grok, Perplexity, Gemini, Meta AI
- Build Status: Clean - ready for Chrome Web Store
