#!/usr/bin/env python3
"""
Test Script for Script Variation Generator
Uses Project Management context to generate 3 hook variations
Following Kallaway's 4-part structure
"""

import json
from datetime import datetime

class ScriptVariationTester:
    """Test the script-variation-generator framework"""

    def __init__(self):
        self.context = {
            "topic": "Project Management Automation",
            "pain_point": "Spending 17+ hours/week on manual project overhead",
            "transformation": "From 2 hours of planning to 24 minutes with autonomous system",
            "credibility": "Managing 34 active projects, saved 16 hours/week",
            "roi": "94% reduction in project overhead",
            "projects": [
                "Project Discovery Service (autonomous scanning)",
                "Todo Aggregation Engine (cross-project todos)",
                "GitHub Sync Agent (automatic commits)"
            ]
        }

    def generate_hook_variation_1_contrarian(self):
        """Variation 1: Contrarian angle - challenges conventional wisdom"""

        return {
            "type": "Contrarian",
            "strategic_angle": "Challenges the idea that better PM skills are the solution",
            "hook_parts": {
                "part_1_context_lean": {
                    "text": "Everyone thinks they need better project management skills. Better tools. Better templates. Better discipline.",
                    "duration": "5-7 seconds",
                    "technique": "Short, staccato sentences stating common belief"
                },
                "part_2_scroll_stop": {
                    "text": "But here's what nobody tells you—that's not actually the problem.",
                    "duration": "3-5 seconds",
                    "technique": "Cognitive dissonance with 'but'"
                },
                "part_3_contrarian_snapback": {
                    "text": "The problem isn't your skills. It's that you're trying to BE a project manager instead of BUILDING one. I'll show you how to create a system that manages 34 projects while you sleep.",
                    "duration": "5-10 seconds",
                    "technique": "Redirect to unexpected solution"
                },
                "part_4_credibility": {
                    "text": "I know this works because I cut my project planning from 2 hours to 24 minutes—a 94% reduction. And I'll break down the exact 3-part system I use.",
                    "duration": "5-7 seconds",
                    "technique": "Specific numbers + structure preview"
                }
            },
            "visual_callouts": ["BETTER SKILLS", "NOT THE PROBLEM", "BUILDING ONE", "24 MINUTES", "94% REDUCTION"],
            "total_duration": "20-30 seconds",
            "full_hook": "Everyone thinks they need better project management skills. Better tools. Better templates. Better discipline.\n\nBut here's what nobody tells you—that's not actually the problem.\n\nThe problem isn't your skills. It's that you're trying to BE a project manager instead of BUILDING one. I'll show you how to create a system that manages 34 projects while you sleep.\n\nI know this works because I cut my project planning from 2 hours to 24 minutes—a 94% reduction. And I'll break down the exact 3-part system I use."
        }

    def generate_hook_variation_2_authority(self):
        """Variation 2: Authority positioning - leverages unique experience"""

        return {
            "type": "Authority",
            "strategic_angle": "Positions speaker as expert through scale and results",
            "hook_parts": {
                "part_1_context_lean": {
                    "text": "When you're managing 34 active projects simultaneously, manual status updates become impossible. You either automate or you drown.",
                    "duration": "5-7 seconds",
                    "technique": "State extreme scenario that establishes authority"
                },
                "part_2_scroll_stop": {
                    "text": "Here's what I discovered after burning 17 hours every single week on admin work.",
                    "duration": "3-5 seconds",
                    "technique": "Tease unique insight from experience"
                },
                "part_3_contrarian_snapback": {
                    "text": "You don't need better project management. You need a self-managing system. One that updates itself, tracks everything, and only alerts you when something actually needs your attention.",
                    "duration": "5-10 seconds",
                    "technique": "Offer solution based on authority"
                },
                "part_4_credibility": {
                    "text": "This system now saves me 16 hours per week. Zero manual updates. Zero spreadsheet work. Just 24 minutes of review time. Let me show you the 3 components that make it work.",
                    "duration": "5-7 seconds",
                    "technique": "Multiple proof points + preview"
                }
            },
            "visual_callouts": ["34 PROJECTS", "17 HOURS", "SELF-MANAGING", "16 HOURS SAVED", "24 MINUTES"],
            "total_duration": "20-30 seconds",
            "full_hook": "When you're managing 34 active projects simultaneously, manual status updates become impossible. You either automate or you drown.\n\nHere's what I discovered after burning 17 hours every single week on admin work.\n\nYou don't need better project management. You need a self-managing system. One that updates itself, tracks everything, and only alerts you when something actually needs your attention.\n\nThis system now saves me 16 hours per week. Zero manual updates. Zero spreadsheet work. Just 24 minutes of review time. Let me show you the 3 components that make it work."
        }

    def generate_hook_variation_3_transformation(self):
        """Variation 3: Transformation promise - emphasizes outcome over process"""

        return {
            "type": "Transformation",
            "strategic_angle": "Focuses on before/after transformation story",
            "hook_parts": {
                "part_1_context_lean": {
                    "text": "Every Monday, I used to spend 2 hours planning projects. Updating spreadsheets. Checking statuses. Remembering what I was working on.",
                    "duration": "5-7 seconds",
                    "technique": "Paint relatable 'before' picture"
                },
                "part_2_scroll_stop": {
                    "text": "Then I stopped trying to be a better project manager.",
                    "duration": "3-5 seconds",
                    "technique": "Unexpected decision that contradicts Part 1"
                },
                "part_3_contrarian_snapback": {
                    "text": "Instead, I built a project manager. An autonomous system that scans projects, aggregates todos, syncs with GitHub, and updates dashboards automatically. Now I wake up to completed tasks.",
                    "duration": "5-10 seconds",
                    "technique": "Reveal transformation mechanism"
                },
                "part_4_credibility": {
                    "text": "My planning time went from 2 hours to 24 minutes. That's 80% of my Monday morning back. And I'll walk you through the exact 3-system architecture that makes it possible.",
                    "duration": "5-7 seconds",
                    "technique": "Specific transformation + structure"
                }
            },
            "visual_callouts": ["2 HOURS", "STOPPED TRYING", "BUILT A PROJECT MANAGER", "24 MINUTES", "80% BACK"],
            "total_duration": "20-30 seconds",
            "full_hook": "Every Monday, I used to spend 2 hours planning projects. Updating spreadsheets. Checking statuses. Remembering what I was working on.\n\nThen I stopped trying to be a better project manager.\n\nInstead, I built a project manager. An autonomous system that scans projects, aggregates todos, syncs with GitHub, and updates dashboards automatically. Now I wake up to completed tasks.\n\nMy planning time went from 2 hours to 24 minutes. That's 80% of my Monday morning back. And I'll walk you through the exact 3-system architecture that makes it possible."
        }

    def generate_why_what_how_body(self):
        """Generate script body using WHY-WHAT-HOW framework"""

        return {
            "why_section": {
                "problem_statement": "Manual project management creates massive overhead",
                "cost_of_inaction": "17+ hours per week on admin tasks. That's 884 hours per year—over 5 weeks of full-time work just tracking what you're doing.",
                "pain_amplification": "The more projects you manage, the worse it gets. Each new project adds 30-60 minutes of weekly overhead.",
                "content": """## Why This Matters

Manual project management isn't just inefficient—it's unsustainable.

**The Real Cost:**
- 2 hours/week: Project planning
- 10 hours/week: Status updates across projects
- 3 hours/week: Git operations and syncing
- 2 hours/week: Setting up new projects

**That's 17 hours per week. 884 hours per year.**

That's 5+ weeks of full-time work spent NOT building, just tracking what you're building.

And here's the killer: the more successful you are, the worse it gets. Every new project adds another 30-60 minutes of weekly overhead.

You hit a ceiling where you literally can't take on new work because you're drowning in project admin."""
            },
            "what_section": {
                "solution_overview": "Self-managing system with 3 core components",
                "differentiation": "Unlike traditional PM tools that require manual input, this system extracts data automatically from your actual work",
                "content": """## What You Actually Need

Not another project management tool. Not better discipline. Not more training.

You need a **self-managing system** that:

1. **Knows what exists** - Automatically discovers and tracks all projects
2. **Monitors changes** - Detects updates without you logging anything
3. **Aggregates context** - Pulls todos, status, and priorities into one view
4. **Syncs automatically** - Commits code, creates PRs, monitors deployments
5. **Alerts intelligently** - Only bothers you when intervention is needed

**The Key Difference:**

Traditional PM tools → You feed them information
This system → Extracts information from your actual work

It's the difference between being the project manager and having one."""
            },
            "how_section": {
                "step_by_step": "3 autonomous systems working together",
                "implementation": "Built with Claude Code using Python, APIs, and daily schedulers",
                "content": """## How to Build It

### System 1: Project Discovery Service

**What it does:**
- Scans workspace daily at 9 AM
- Parses CLAUDE.md files in every project
- Extracts todos, priorities, and status
- Builds unified project registry

**Business impact:** 10 hours/week saved on manual tracking

**How to build:**
```
Prompt Claude: "Build a Python script that scans a directory tree, finds all CLAUDE.md files, extracts structured data (todos, status, phase), and outputs to JSON. Run it daily via cron."
```

---

### System 2: Template Generator

**What it does:**
- Creates new project structure in one command
- Auto-generates CLAUDE.md with context
- Assigns unique localhost ports
- Sets up security defaults

**Business impact:** 2 hours → 5 minutes per project (96% reduction)

**How to build:**
```
Prompt Claude: "Create a project template generator that accepts a project name, creates directory structure, generates CLAUDE.md from template, assigns available port from range 3000-9000, and initializes git repo."
```

---

### System 3: GitHub Sync Agent

**What it does:**
- Auto-commits changes daily
- Creates pull requests with summaries
- Monitors CI/CD status
- Sends failure notifications

**Business impact:** Zero manual git operations across 34 projects

**How to build:**
```
Prompt Claude: "Build an agent that runs daily, checks for uncommitted changes in a list of project directories, creates meaningful commit messages based on file changes, commits and pushes, and creates PRs when on feature branches."
```

---

### Connecting the Systems

All three run via a daily scheduler:
- 9:00 AM: Project discovery scans everything
- 9:05 AM: Todo aggregation compiles cross-project tasks
- 9:10 AM: GitHub sync commits and pushes changes
- 9:15 AM: Dashboard updates with latest data

You wake up to a complete project status report. No manual work required."""
            }
        }

    def generate_complete_test_output(self):
        """Generate complete test output with all 3 variations"""

        print("=" * 100)
        print("SCRIPT VARIATION GENERATOR - TEST OUTPUT")
        print("=" * 100)
        print(f"\nTopic: {self.context['topic']}")
        print(f"Generated: {datetime.now().isoformat()}\n")

        # Generate 3 hook variations
        variation_1 = self.generate_hook_variation_1_contrarian()
        variation_2 = self.generate_hook_variation_2_authority()
        variation_3 = self.generate_hook_variation_3_transformation()

        # Generate body
        body = self.generate_why_what_how_body()

        output = {
            "pillar_id": "test_pm_001",
            "title": "How I Built a Self-Managing Project System That Cut My Planning Time by 80%",
            "created_date": datetime.now().isoformat(),
            "hook_variations": {
                "variation_1_contrarian": variation_1,
                "variation_2_authority": variation_2,
                "variation_3_transformation": variation_3
            },
            "body_framework": body,
            "google_sheet_format": {
                "Hook Variation A (Stats Lead)": "I manage 34 projects simultaneously. Zero manual status updates. This autonomous system saves me 16 hours every single week.",
                "Hook Variation B (Contrarian)": variation_1["full_hook"],
                "Hook Variation C (Story)": variation_3["full_hook"],
                "Hook Variation D (Question)": "What if your projects managed themselves? No status meetings. No spreadsheet updates. Just a system that works while you sleep. Here's how I built it.",
                "Hook Variation E (Outcome)": variation_2["full_hook"]
            }
        }

        # Print each variation
        print("\n" + "=" * 100)
        print("VARIATION 1: CONTRARIAN ANGLE")
        print("=" * 100)
        print(f"\nStrategic Angle: {variation_1['strategic_angle']}\n")

        for part, content in variation_1["hook_parts"].items():
            print(f"\n### {part.upper().replace('_', ' ')}")
            print(f"Duration: {content['duration']}")
            print(f"Technique: {content['technique']}")
            print(f"\nText:\n{content['text']}")

        print(f"\n### VISUAL CALLOUTS")
        print(", ".join(variation_1["visual_callouts"]))

        print(f"\n### FULL HOOK")
        print("-" * 100)
        print(variation_1["full_hook"])
        print("-" * 100)

        print("\n" + "=" * 100)
        print("VARIATION 2: AUTHORITY POSITIONING")
        print("=" * 100)
        print(f"\nStrategic Angle: {variation_2['strategic_angle']}\n")

        for part, content in variation_2["hook_parts"].items():
            print(f"\n### {part.upper().replace('_', ' ')}")
            print(f"Duration: {content['duration']}")
            print(f"Technique: {content['technique']}")
            print(f"\nText:\n{content['text']}")

        print(f"\n### VISUAL CALLOUTS")
        print(", ".join(variation_2["visual_callouts"]))

        print(f"\n### FULL HOOK")
        print("-" * 100)
        print(variation_2["full_hook"])
        print("-" * 100)

        print("\n" + "=" * 100)
        print("VARIATION 3: TRANSFORMATION PROMISE")
        print("=" * 100)
        print(f"\nStrategic Angle: {variation_3['strategic_angle']}\n")

        for part, content in variation_3["hook_parts"].items():
            print(f"\n### {part.upper().replace('_', ' ')}")
            print(f"Duration: {content['duration']}")
            print(f"Technique: {content['technique']}")
            print(f"\nText:\n{content['text']}")

        print(f"\n### VISUAL CALLOUTS")
        print(", ".join(variation_3["visual_callouts"]))

        print(f"\n### FULL HOOK")
        print("-" * 100)
        print(variation_3["full_hook"])
        print("-" * 100)

        print("\n" + "=" * 100)
        print("BODY FRAMEWORK: WHY-WHAT-HOW")
        print("=" * 100)

        print("\n### WHY SECTION")
        print(body["why_section"]["content"])

        print("\n### WHAT SECTION")
        print(body["what_section"]["content"])

        print("\n### HOW SECTION")
        print(body["how_section"]["content"])

        print("\n" + "=" * 100)
        print("GOOGLE SHEET FORMAT")
        print("=" * 100)

        for column, content in output["google_sheet_format"].items():
            print(f"\n### {column}")
            print("-" * 100)
            print(content)

        # Save to JSON
        output_file = "/Users/elizabethknopf/Documents/claudec/systems/skills-main/script-variation-generator/test_output.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print("\n" + "=" * 100)
        print(f"✅ Test output saved to: {output_file}")
        print("=" * 100)

        return output


def main():
    tester = ScriptVariationTester()
    tester.generate_complete_test_output()


if __name__ == "__main__":
    main()
