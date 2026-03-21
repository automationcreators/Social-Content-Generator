# Social Posts — Workflow Audit Session
*Generated: 2026-03-20 | Source: Claude Code skills audit session*

---

## X / Twitter Posts

### Post 1 — Transformation / Confession
```
I had 160+ Claude Code skills installed.

Was using maybe 8 of them.

Did a full audit. Found 5 gaps costing me time daily:

→ Skipping design gate before coding
→ Not recalling episodic memory between sessions
→ Working sequential on parallel-capable tasks
→ No security hook on git commits
→ Couldn't name half my tools, let alone use them

Fixed all 5 in one session.

The bottleneck was never the AI.
```
**Hook type:** Contrarian snapback + transformation
**Best time:** Tue/Wed 9-11am

---

### Post 2 — How-To / Dev
```
Set up a hook that scans staged files before every git commit.

Detects:
• .env and .key files
• AWS access keys (AKIA*)
• GitHub tokens (ghp_*)
• OpenAI keys (sk-*)
• Private keys (BEGIN PRIVATE KEY)

Blocks the commit with a clear message.

3 lines in settings.json.
One script in ~/.claude/hooks/

Fired twice this week. Both would've been real problems.
```
**Hook type:** How-To + proof point
**Best time:** Thu/Fri 8-10am (dev audience active)

---

### Post 3 — Insight / Big Picture
```
The problem with AI coding tools isn't the AI.

Most people:
• Skip design → build the wrong thing
• Skip verification → ship broken work
• Re-explain context every session → no continuity
• Run tasks sequentially → ignoring parallel capacity
• Install 160 tools → use 8

The tool is capable.

The operator just hasn't set up the workflow.

And workflow problems have workflow solutions.
```
**Hook type:** Contrarian reframe
**Best time:** Mon 7-9am (week-start mindset)

---

## LinkedIn Post

### Post — Full Workflow Audit Story
```
I spent an hour auditing how I'm actually using Claude Code.

The gap was bigger than I expected.

Here's what I found — and what I fixed:

**Gap 1: Skipping the design gate**

Every time I said "build X," coding would start immediately.

There's a skill called superpowers:brainstorming that forces a design doc + user approval before any code gets written.

I wasn't using it.

This is the #1 cause of wasted dev work. You build the wrong thing, then rebuild it.

---

**Gap 2: Episodic memory installed, not in workflow**

The episodic-memory plugin indexes every Claude Code conversation and makes it semantically searchable.

I had 286 conversations indexed.

I was re-explaining context at the start of every session.

Fixed with one SessionStart hook that reminds me to search before I ask.

---

**Gap 3: 160 skills, using ~8**

I had industry-scanner, signal-detection-pipeline, competitor-intel, content-repurposer, and 150+ others just sitting there.

I couldn't name most of them.

Built a use-case cheat sheet. Now I actually reach for them.

---

**Gap 4: No security hooks**

No automated check before git commits.

Added a PreToolUse hook that scans staged files for .env files, API key patterns, private keys. Blocks the commit with a clear message.

It's fired twice since I set it up. Both would've been actual incidents.

---

**Gap 5: Sequential work on parallel tasks**

The claude-session-driver plugin lets Claude spawn parallel worker sessions via tmux.

I had it installed for months.

Never used it once.

---

The fix took one session.

3 hook scripts. 2 rules in CLAUDE.md. One skills reference guide.

**The bottleneck isn't the AI. It's the operator knowing how to use it.**

---

What does your Claude Code setup look like?
Are you using hooks? Running workflows? Or just prompting?
```
**Hook type:** Benefit-driven + confession + how-to hybrid
**Format:** Long-form with section headers — performs well in LinkedIn feed
**Best time:** Tue/Wed 8-10am

---

## Content Notes
- All posts sourced from real session work — authentic, specific, verifiable
- Short 2 (security hook) has the highest viral potential — dev audience shares tools
- LinkedIn post is the anchor piece — X posts are excerpts from it
- Pair Short 1 thumbnail with Post 1 for cross-platform reinforcement
