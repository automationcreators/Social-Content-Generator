# Social-Content-Generator - Claude Context

## Project Overview
- **Purpose**: AI-powered social content generation from real project activity
- **Category**: content, automation
- **Priority**: high
- **Phase**: active

## Parent Context
**IMPORTANT**: For content generation, reference the parent CLAUDE.md at `/Users/elizabethknopf/Documents/claudec/CLAUDE.md` for:
- Full project portfolio (40+ projects)
- Real metrics and examples
- Daily activity logs (LOG.md, CONTEXT.md)

## Content Pipeline

### Input Sources
1. `../../LOG.md` - Daily activity (what was built/fixed)
2. `../../CONTEXT.md` - Current decisions and focus
3. `../../project-registry.json` - All project metadata
4. `../../active/*/CLAUDE.md` - Individual project context

### Output Location
`./generated_content/` - All generated social content

### Key Files in generated_content/
- `social-content-all-100.json` - Master file (100 posts combined)
- `social-content-complete-100.csv` - Airtable/Sheets import format
- `SOCIAL-CONTENT-README.md` - Documentation

## Content Types Generated
- X single posts (40)
- X threads (30)
- LinkedIn posts (30)
- Threads posts (planned)

## Hook Frameworks
Located in `/.claude/skills/`:
- `/viral-hook-generator` - Contrarian, Transformation, How-To, Benefit-Driven
- `/platform-voice-adapter` - X, LinkedIn, Threads, Instagram formatting

## Development
- **Primary URL**: N/A (CLI-based)
- **Dependencies**: Python 3.9+, Google OAuth (for Sheets sync)

## Commands
```bash
# View generated content
ls generated_content/

# Check content count
python3 -c "import json; d=json.load(open('generated_content/social-content-all-100.json')); print(f'{len(d[\"posts\"])} posts')"

# Run content generators
python generators/daily_content_gen.py
```

## Related Projects
- `ContentGen/` - RSS feed aggregation
- `Personal-OS/` - Main source of project examples
- `YouTubeRAG/` - Technical deep-dive examples

---
*Reference parent CLAUDE.md for full portfolio context*

---

## Mandatory Workflow Gates

**BEFORE building any new feature (non-negotiable design gate):**
1. Invoke `superpowers:brainstorming` — write a design doc, get explicit user approval
2. Only then proceed: `writing-plans` → `executing-plans`
3. Skipping this is the #1 cause of wasted work

**BEFORE claiming any work is done:**
- Run `superpowers:verification-before-completion`

**WHEN starting work on any existing project:**
- Invoke `remembering-conversations` skill to search episodic memory for prior decisions

## Parallel Orchestration

**When you have 3+ independent tasks**, use `driving-claude-code-sessions` skill to fan out to parallel Claude worker sessions via tmux.
