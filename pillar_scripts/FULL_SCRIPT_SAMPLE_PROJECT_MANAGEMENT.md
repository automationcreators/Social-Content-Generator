# How I Built a Self-Managing Project System That Cut My Planning Time by 80%

**Video Length:** ~10 minutes
**Word Count:** ~1,450 words
**Variation:** Transformation (Before/After Story)

---

## HOOK (0:00 - 0:30)

Every Monday, I used to spend 2 hours planning projects. Updating spreadsheets. Checking statuses. Remembering what I was working on.

**[VISUAL: Screen recording of cluttered spreadsheet, multiple browser tabs]**

Then I stopped trying to be a better project manager.

**[VISUAL: Close spreadsheet, pull up terminal]**

Instead, I built a project manager. An autonomous system that scans projects, aggregates todos, syncs with GitHub, and updates dashboards automatically. Now I wake up to completed tasks.

**[VISUAL: Dashboard showing 34 projects, all auto-updated]**

My planning time went from 2 hours to 24 minutes. That's 80% of my Monday morning back. And I'll walk you through the exact 3-system architecture that makes it possible.

**[VISUAL: "3 SYSTEMS" text overlay]**

---

## INTRO (0:30 - 1:00)

I'm Liz, and I manage 34 active projects simultaneously. That's not a flex—it's actually a problem. Or at least it was, until I stopped managing them manually.

**[VISUAL: Split screen - left side shows old workflow, right shows new]**

See, most productivity advice tells you to get better at project management. Better tools. Better discipline. Better templates.

But that's backwards.

The solution isn't becoming a better project manager. It's not needing one at all.

And I'm going to show you exactly how I built a system that eliminated 94% of my project management overhead—and how you can do the same thing, even if you've never written a line of code.

---

## WHY THIS MATTERS (1:00 - 3:30)

### The Real Cost of Manual Project Management

Let me show you what my Mondays used to look like.

**[VISUAL: Time breakdown graphic]**

**9:00 AM:** Open spreadsheet. Try to remember what I worked on last week across 34 projects.

**9:30 AM:** Check each project folder individually. What's done? What's stuck? What needs attention?

**10:15 AM:** Update status in spreadsheet. Copy-paste project names. Update progress bars.

**10:45 AM:** Check GitHub for each project. What needs to be committed? What PRs are open?

**11:00 AM:** Finally done with "planning." Completely exhausted. Haven't built anything yet.

**Two hours. Every single Monday.**

But here's what I didn't realize until I actually tracked it:

**[VISUAL: Full weekly breakdown]**

- **Monday planning:** 2 hours
- **Daily status checks:** 10 hours/week (30 minutes per project, rotating through them)
- **Manual git operations:** 3 hours/week (commits, PRs, merging across projects)
- **New project setup:** 2 hours every time I start something new

**That's 17+ hours per week on project overhead.**

Do the math with me: 17 hours × 52 weeks = **884 hours per year**.

That's over **5 weeks of full-time work** spent NOT building, just tracking what I'm building.

**[VISUAL: "5 WEEKS LOST" in big text]**

### The Scaling Problem

And here's the killer: The more successful you are, the worse it gets.

Every new project adds another 30-60 minutes of weekly overhead. You hit a ceiling where you literally can't take on new work because you're drowning in project admin.

I hit that ceiling at 34 projects. I couldn't add a 35th. Not because I lacked time to build it—but because I lacked time to track it.

**[VISUAL: Graph showing overhead increasing with project count]**

That's when I realized: I don't need better project management skills. I need to eliminate project management entirely.

---

## WHAT YOU ACTUALLY NEED (3:30 - 5:00)

Not another Notion template. Not another Trello board. Not another "system."

You need a **self-managing system** that:

**[VISUAL: Animated checklist appearing item by item]**

1. **Knows what exists** - Automatically discovers and tracks all your projects without you logging anything

2. **Monitors changes** - Detects what you're working on by analyzing your actual files, not by asking you to update a status

3. **Aggregates context** - Pulls todos, priorities, and deadlines from wherever you actually write them (CLAUDE.md files, code comments, git commits)

4. **Syncs automatically** - Commits your code, creates pull requests, monitors CI/CD, sends you alerts only when something breaks

5. **Generates reports** - Builds a dashboard that answers "what's the status?" without you ever touching a spreadsheet

**[VISUAL: Dashboard demo - real-time project data]**

### The Key Difference

Traditional PM tools work like this:
**You** → **Input data manually** → **Tool displays it**

This system works like this:
**System** → **Extracts data from your work** → **You review 5-minute summary**

It's the difference between being the project manager and having one.

**[VISUAL: Side-by-side comparison]**

---

## HOW TO BUILD IT (5:00 - 9:00)

Here's the architecture. Three autonomous systems that work together.

**[VISUAL: Architecture diagram with 3 boxes]**

### System 1: Project Discovery Service (5:00 - 6:15)

**What it does:**

Every morning at 9 AM, this system:
- Scans my entire workspace directory
- Finds every project (looks for git repos or CLAUDE.md files)
- Parses the CLAUDE.md in each project
- Extracts: project name, status, phase, todos, priority, tech stack
- Outputs everything to a JSON file

**[VISUAL: Screen recording of script running, showing output]**

**Business impact:** 10 hours per week saved. I never manually check project status anymore.

**How I built it:**

I gave Claude this exact prompt:

> "Build a Python script that scans /Users/elizabethknopf/Documents/claudec/active/ recursively, finds all CLAUDE.md files, extracts structured data using regex (todos under ## Progress Tracking, status under ## Current Status, phase field), and outputs to projects.json. Run daily via cron at 9 AM."

**[VISUAL: Show the prompt on screen]**

Claude built it in 3 minutes. I tested it. It worked. Done.

The script is 200 lines of Python. I didn't write a single line myself.

**Key files it creates:**
- `dashboard-projects-data.json` - All project data
- `aggregated-todos.json` - Cross-project todo list
- `project-discovery.log` - What changed since yesterday

**[VISUAL: Show actual JSON output]**

### System 2: Template Generator (6:15 - 7:15)

**What it does:**

When I start a new project, I run one command:

```bash
python3 template-generator.py "New Project Name"
```

**[VISUAL: Terminal showing command execution]**

And it:
1. Creates directory structure (src, tests, docs folders)
2. Generates CLAUDE.md with all sections pre-filled
3. Assigns a unique localhost port (range 3000-9000)
4. Initializes git repository
5. Creates .gitignore with security defaults
6. Logs the project to the registry

Total time: **5 minutes** from idea to working project structure.

**[VISUAL: Before/after - empty folder → complete project structure]**

**Old way:** 2 hours (manual folder creation, copy-paste templates, configure everything)

**New way:** 5 minutes (one command)

**Time savings:** 96%

**How I built it:**

Another Claude prompt:

> "Create a project template generator that: 1) Takes project name as argument, 2) Creates standardized folder structure, 3) Generates CLAUDE.md from template with project-specific fields auto-filled, 4) Finds next available port in range 3000-9000 by checking all existing CLAUDE.md files, 5) Initializes git repo with initial commit, 6) Outputs success message with project path and assigned port."

**[VISUAL: Show the generated CLAUDE.md file]**

The template includes:
- Project category (auto-detected from name)
- Port assignment (auto-selected)
- Setup commands (based on detected tech)
- Standard sections (Success Criteria, Next Actions, Progress Tracking)

### System 3: GitHub Sync Agent (7:15 - 8:30)

**What it does:**

Every morning at 9:10 AM (right after project discovery), this agent:

**[VISUAL: Flowchart of the process]**

1. **Checks for uncommitted changes** in all 34 projects
2. **Analyzes file changes** to create meaningful commit messages (not "update files")
3. **Commits and pushes** to remote branches
4. **Creates pull requests** if on feature branches (includes summary of changes)
5. **Monitors CI/CD status** for all active PRs
6. **Sends me notifications** only if tests fail or deployments break

**Business impact:** Zero manual git operations across 34 projects. Zero commits forgotten. Zero PRs missed.

**[VISUAL: GitHub showing automated commits and PRs]**

**How I built it:**

You guessed it—Claude:

> "Build a GitHub sync agent that: 1) Scans project list from projects.json, 2) Checks git status in each, 3) For uncommitted changes: analyze diffs and generate commit message describing actual changes, commit with message, push to remote, 4) For feature branches: create PR with detailed summary using gh CLI, 5) For open PRs: check CI status and log failures, 6) Output daily summary of all git operations."

**[VISUAL: Show the daily summary log]**

The agent generates commit messages like:
- "Add authentication flow to user dashboard" (not "update files")
- "Fix API rate limiting in data sync module" (not "bug fix")
- "Refactor database queries for 3x performance improvement" (not "changes")

It reads the diffs and understands context.

---

## THE COMPOUND EFFECT (8:30 - 9:00)

### How These Systems Work Together

**[VISUAL: Timeline of a typical morning]**

**9:00 AM:** Project Discovery runs
- Scans 34 projects
- Updates status for all
- Flags 3 projects with blocking issues

**9:05 AM:** Todo Aggregator runs
- Compiles cross-project todos
- Prioritizes by urgency
- Sends me consolidated list

**9:10 AM:** GitHub Sync runs
- Commits changes from yesterday
- Pushes to 12 active projects
- Creates 2 pull requests
- Reports 1 failed CI test

**9:15 AM:** Dashboard updates
- Pulls all new data
- Generates project health scores
- Displays everything in one view

**[VISUAL: Final dashboard with all data]**

**9:20 AM:** I open my computer

I see:
- ✅ All 34 projects: current status
- ✅ 15 todos prioritized across projects
- ✅ 12 commits pushed automatically
- ✅ 2 PRs ready for review
- ⚠️ 1 project needs attention (CI failure)

Total review time: **24 minutes**

**[VISUAL: "24 MINUTES" in large text]**

I spend those 24 minutes on the one thing that actually needs me: fixing that CI failure.

Everything else? Already done.

---

## RESULTS (9:00 - 9:30)

### Before vs After

**Before:**
- 2 hours: Monday planning
- 10 hours: Weekly status checks
- 3 hours: Git operations
- 2 hours: New project setup (each time)
- **Total: 17+ hours/week of overhead**

**After:**
- 24 minutes: Monday review
- 0 hours: Status checks (automated)
- 0 hours: Git operations (automated)
- 5 minutes: New project setup (templated)
- **Total: ~1 hour/week**

**Time saved: 16 hours per week**

**[VISUAL: Bar chart showing dramatic difference]**

That's 832 hours per year. Over 20 full work weeks. An entire quarter returned to me.

### What I Do With That Time

Not more projects. Better projects.

Instead of managing 34 things poorly, I can actually focus on the 3 that matter.

**[VISUAL: Focus vs. fragmentation graphic]**

---

## YOUR TURN (9:30 - 10:00)

You don't need to manage 34 projects to benefit from this.

Even if you have 3 projects, you're probably spending 5+ hours a week on overhead.

**Start with one system:**

**If you're drowning in status updates** → Build Project Discovery
**If new projects take forever to set up** → Build Template Generator
**If you're forgetting to commit code** → Build GitHub Sync

Pick one. Give Claude the prompt. Build it today.

**[VISUAL: Three options with arrows pointing to prompt examples]**

### The Prompt Template

Here's the framework:

> "Build a [system name] that: 1) [Input source], 2) [Processing logic], 3) [Output format], 4) [Automation schedule]. Make it production-ready with error handling and logging."

That's it. Claude does the rest.

**[VISUAL: Prompt template on screen]**

---

## FINAL THOUGHT (10:00)

Two years ago, I thought I needed to get better at project management.

I bought courses. I read books. I tried every productivity system.

Nothing worked—because the problem wasn't my skills.

The problem was that I was doing work a computer should do.

**[VISUAL: Person at desk → Autonomous system running]**

Now I wake up to 34 projects managed without me touching them.

Not because I'm good at project management.

Because I eliminated the need for it entirely.

**Your turn.**

What's one task you do every single week that a system could do better?

Drop it in the comments. I'll help you structure the Claude prompt.

And if you want to see the actual code for these three systems, I've linked the GitHub repo below. Everything's open source.

**[VISUAL: GitHub link overlay]**

See you in the next one.

**[END SCREEN: Subscribe + Related Videos]**

---

## VIDEO METADATA

**Title:** How I Cut Project Planning from 2 Hours to 24 Minutes (Autonomous System)

**Description:**
I manage 34 projects simultaneously without manual status updates. Here's the 3-system architecture that eliminated 94% of my project management overhead.

🎯 What You'll Learn:
- Why better PM skills won't solve the problem
- The 3 autonomous systems that manage projects for you
- How to build each system with Claude Code (no coding required)
- Exact prompts I used to create everything

⏱️ Timestamps:
0:00 - Hook: From 2 hours to 24 minutes
0:30 - The real cost of manual PM
3:30 - What you actually need
5:00 - System 1: Project Discovery
6:15 - System 2: Template Generator
7:15 - System 3: GitHub Sync Agent
8:30 - How they work together
9:30 - How to build yours

🔗 Resources:
- GitHub Repo: [link]
- Project Discovery Script: [link]
- Template Generator: [link]
- GitHub Sync Agent: [link]

#ProjectManagement #Automation #ClaudeCode #Productivity #BuildInPublic

**Tags:**
project management, automation, Claude Code, productivity, business automation, software development, autonomous systems, AI automation, no code, project tracking, GitHub automation, developer tools, time management, small business, solopreneur

**Thumbnail Text:**
"2 HOURS → 24 MIN"
"34 Projects"
"0 Manual Updates"
