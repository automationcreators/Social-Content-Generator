#!/usr/bin/env python3
"""
Generate pillar content using Kallaway frameworks + real project data
"""

import json
from pathlib import Path
from datetime import datetime

class PillarContentGenerator:
    """Creates pillar content from frameworks and real data"""

    def __init__(self):
        self.frameworks = self.load_kallaway_frameworks()
        self.project_data = self.load_project_data()
        self.content_ideas = self.load_content_ideas()

    def load_kallaway_frameworks(self):
        """Load Kallaway hook frameworks"""
        framework_file = Path(__file__).parent / "content_frameworks" / "kallaway_hooks.json"
        with open(framework_file, 'r') as f:
            return json.load(f)

    def load_project_data(self):
        """Load real project analysis"""
        data_file = Path(__file__).parent / "project_data_analysis.json"
        with open(data_file, 'r') as f:
            return json.load(f)

    def load_content_ideas(self):
        """Load content ideas"""
        ideas_file = Path(__file__).parent / "social_media_content_database.json"
        with open(ideas_file, 'r') as f:
            return json.load(f)

    def create_pillar_content(self, content_idea_id):
        """Create full pillar content for an idea using real data"""

        # Find the content idea
        idea = None
        for ci in self.content_ideas["content_ideas"]:
            if ci["id"] == content_idea_id:
                idea = ci
                break

        if not idea:
            return {"error": "Idea not found"}

        # Get real examples that match this idea
        matching_examples = self.find_matching_examples(idea)

        # Get relevant insights
        relevant_insights = self.get_relevant_insights(idea)

        # Build pillar content using Kallaway structure
        pillar = {
            "id": f"pillar_{idea['id']}",
            "created_date": datetime.now().isoformat(),
            "idea": idea,
            "hook_framework": self.frameworks["hook_types"].get(idea.get("hook_type", "benefit_driven")),
            "real_data": {
                "examples": matching_examples,
                "insights": relevant_insights,
                "statistics": self.extract_statistics(matching_examples, relevant_insights)
            },
            "content": {}
        }

        # Create YouTube/Long-form script
        pillar["content"]["youtube_script"] = self.create_youtube_script(pillar)

        # Create LinkedIn article
        pillar["content"]["linkedin_article"] = self.create_linkedin_article(pillar)

        # Create Twitter thread
        pillar["content"]["twitter_thread"] = self.create_twitter_thread(pillar)

        # Create short-form posts
        pillar["content"]["short_posts"] = self.create_short_posts(pillar)

        return pillar

    def find_matching_examples(self, idea):
        """Find real project examples that match the content idea"""
        category = idea["category"]
        examples = []

        for example in self.project_data.get("real_examples", []):
            if example.get("category") == category or category in ["use_cases", "tips_and_tricks"]:
                examples.append(example)

        return examples

    def get_relevant_insights(self, idea):
        """Get insights relevant to the idea"""
        category = idea["category"]
        insights = []

        for insight in self.project_data.get("insights", []):
            # Match insights to categories
            if category == "architecture_insights" and insight["type"] in ["automation", "versatility"]:
                insights.append(insight)
            elif category == "feature_demos" and insight["type"] == "data_viz":
                insights.append(insight)
            elif category == "use_cases":
                insights.append(insight)
            elif category == "progress_updates" and insight["type"] == "scale":
                insights.append(insight)

        return insights[:2]  # Limit to top 2

    def extract_statistics(self, examples, insights):
        """Extract compelling statistics from data"""
        stats = []

        # From insights
        for insight in insights:
            stats.append({
                "stat": insight["stat"],
                "context": insight["detail"]
            })

        # From project data aggregates
        total_projects = self.project_data["aggregate_stats"]["total_projects"]
        stats.append({
            "stat": f"{total_projects} active projects",
            "context": "All built and managed with Claude Code"
        })

        # Agent count
        agent_insights = [i for i in self.project_data["insights"] if i.get("type") == "automation"]
        if agent_insights:
            stats.append({
                "stat": agent_insights[0]["stat"],
                "context": "Autonomous agents handling business operations"
            })

        return stats

    def create_youtube_script(self, pillar):
        """Create YouTube/long-form video script using Kallaway framework"""
        idea = pillar["idea"]
        examples = pillar["real_data"]["examples"]
        stats = pillar["real_data"]["statistics"]

        script = f"""
# {idea['title']}

## HOOK (First 5 seconds)
{idea['description']}

## PROBLEM SETUP (15 seconds)
Most small business owners waste hours on repetitive tasks. Manual reporting, data entry, customer follow-ups—it all adds up. I was spending 15-20 hours per week on tasks that didn't grow my business.

## CREDIBILITY (10 seconds)
Over the past year, I've built {self.project_data['aggregate_stats']['total_projects']} different automation projects using Claude Code. No coding background. Just learned to talk to AI effectively.

## THE TRANSFORMATION (Main Content)

### What I Built:

"""
        # Add real examples
        for i, example in enumerate(examples[:3], 1):
            script += f"""
**Example {i}: {example['title']}**
- **The Problem**: {self._extract_problem(example)}
- **The Solution**: {example['description']}
- **Business Impact**: {example['business_value']}
- **Time to Build**: 45 minutes to 2 hours with Claude Code

"""

        script += f"""
### The Numbers (Show on screen):

"""
        for stat in stats[:4]:
            script += f"- {stat['stat']} - {stat['context']}\n"

        script += f"""

## THE FRAMEWORK (How You Can Do This)

I use a simple 3-step process:

**Step 1: Describe What You Do Manually**
Write out your current process like you're explaining it to an assistant. Be specific about inputs, outputs, and edge cases.

**Step 2: Talk to Claude Code Like a Human**
No coding jargon needed. I literally say: "Build me a system that [does the thing]."

Example: "Build me a quote generator that takes my pricing list, creates professional PDFs, and emails them to customers."

**Step 3: Test and Refine**
Claude builds it. You test it. You tell Claude what to fix. Repeat until it's perfect.

## REAL EXAMPLE WALKTHROUGH

Let me show you exactly how I built {examples[0]['title'] if examples else 'a recent project'}...

[Screen recording showing the actual conversation with Claude Code]

## PROOF (Show the Results)

Here's the actual tool running: [Demo the real project]

This replaced:
- {self._extract_replaced_tool(examples[0]) if examples else 'Manual processes'}
- Saving me {self._extract_time_savings(examples[0]) if examples else '10+ hours per week'}
- One-time setup, runs forever

## CONTRARIAN TAKE

Everyone thinks you need to:
- Learn to code
- Hire developers
- Use expensive SaaS tools

Wrong. You need:
- Clear idea of what you want
- Ability to explain it to Claude
- 30-60 minutes of setup time

## CALL TO ACTION

Start with ONE repetitive task. The thing that annoys you most. Describe it to Claude Code. See what happens.

Drop a comment with what you want to automate and I'll help you structure the prompt.

## END SCREEN
- Link to my other Claude Code tutorials
- Subscribe for more automation content
- Join my newsletter for the exact prompts I use

---
**Estimated Length**: 8-12 minutes
**Key Visuals**: Screen recordings of actual projects, before/after comparisons, statistics overlays
"""

        return script

    def create_linkedin_article(self, pillar):
        """Create LinkedIn article"""
        idea = pillar["idea"]
        examples = pillar["real_data"]["examples"]
        stats = pillar["real_data"]["statistics"]

        article = f"""# {idea['title']}

{idea['description']}

## The Reality Check

I manage {self.project_data['aggregate_stats']['total_projects']} active projects.
I'm not a professional developer.
I don't have a dev team.

What I have: Claude Code and a clear understanding of what I need.

## What I've Built (Real Examples)

"""

        for example in examples[:3]:
            article += f"""### {example['title']}

**The Challenge**: {self._extract_problem(example)}

**The Solution**: {example['description']}

**Business Impact**: {example['business_value']}

**Tech Stack**: {example.get('tech', 'Python/JavaScript')}

**Build Time**: Less than 2 hours from idea to working prototype

---

"""

        article += f"""## The Numbers Don't Lie

"""
        for stat in stats[:4]:
            article += f"- **{stat['stat']}**: {stat['context']}\n"

        article += f"""

## How This Changes Everything

Traditional approach:
1. Define requirements (weeks)
2. Find/hire developers (months)
3. Development (months)
4. Testing and iteration (weeks)
5. Maintenance costs (ongoing)

My approach with Claude Code:
1. Describe what I need (5 minutes)
2. Let Claude build it (30-60 minutes)
3. Test and refine (15 minutes)
4. Run it (forever, for free)

## The Framework I Use

**Step 1: Think in Outcomes, Not Code**

I don't think "I need a Python script that..."

I think "I need a system that emails me when customers haven't ordered in 30 days."

**Step 2: Describe It Like Delegating**

Talk to Claude like you're delegating to a very capable assistant:

"Build me a dashboard that shows:
- Today's sales vs. last week
- Top 5 customers by revenue
- Products that need reordering
- Pull data from my Google Sheet
- Update every hour"

Claude knows how to translate that into code.

**Step 3: Iterate Based on Results**

The first version works. But you'll want tweaks:
- "Add email alerts when sales drop 20%"
- "Make the chart show last 30 days instead of 7"
- "Export to PDF for my weekly meeting"

Just tell Claude. It adjusts.

## Why This Matters for Small Business

Big companies have advantages:
- Unlimited dev resources
- Custom software for everything
- Automation at scale

Small businesses now have Claude Code:
- Build anything you can describe
- No coding required
- No monthly subscriptions
- Runs 24/7

It's not about competing. It's about having the same capabilities without the overhead.

## Start Here

Pick ONE task that wastes your time every week:
- Weekly reporting
- Customer follow-ups
- Data entry
- Inventory tracking
- Quote generation

Describe it to Claude Code.

That's it.

## What Are You Automating?

I'm documenting my entire journey building with Claude Code.

Comment below with one task you want to automate and I'll help you structure the prompt to get started.

---

**Building in public with Claude Code.**

#ClaudeCode #SmallBusiness #Automation #AI #Productivity #BuildingInPublic
"""

        return article

    def create_twitter_thread(self, pillar):
        """Create Twitter thread"""
        idea = pillar["idea"]
        examples = pillar["real_data"]["examples"]
        stats = pillar["real_data"]["statistics"]

        thread = []

        # Tweet 1: Hook
        thread.append({
            "text": f"{idea['title']}\n\n{idea['description'][:180]}\n\nA thread:",
            "number": 1
        })

        # Tweet 2: Problem
        thread.append({
            "text": f"Most small business owners waste 15-20 hrs/week on:\n• Manual reporting\n• Data entry\n• Customer follow-ups\n• Quote generation\n\nI did too. Until I learned to automate everything with Claude Code.",
            "number": 2
        })

        # Tweet 3: Credibility
        thread.append({
            "text": f"Over the past year:\n\n• {self.project_data['aggregate_stats']['total_projects']} automation projects\n• {stats[1]['stat'] if len(stats) > 1 else '80+ autonomous agents'}\n• Zero coding background\n\nJust learned to talk to AI effectively.",
            "number": 3
        })

        # Tweets 4-6: Real Examples
        for i, example in enumerate(examples[:3], 4):
            thread.append({
                "text": f"Example {i-3}: {example['title']}\n\n{example['description'][:150]}\n\nResult: {example['business_value']}\n\nBuild time: <2 hours",
                "number": i
            })

        # Tweet: Framework
        thread.append({
            "text": "My 3-step framework:\n\n1. Describe what you do manually\n2. Tell Claude Code to build it (like delegating to an assistant)\n3. Test and refine\n\nThat's it. No coding knowledge needed.",
            "number": len(thread) + 1
        })

        # Tweet: Contrarian take
        thread.append({
            "text": "Everyone says you need:\n• To learn coding\n• Hire developers\n• Expensive SaaS\n\nActually you need:\n• Clear idea of what you want\n• Ability to explain it\n• 30-60 minutes\n\nClaude Code handles the rest.",
            "number": len(thread) + 1
        })

        # Tweet: CTA
        thread.append({
            "text": "Start with ONE repetitive task.\n\nThe thing that annoys you most.\n\nDescribe it to Claude Code.\n\nReply with what you want to automate and I'll help you structure the prompt.\n\n#ClaudeCode #Automation #SmallBusiness",
            "number": len(thread) + 1
        })

        return {"thread": thread, "tweet_count": len(thread)}

    def create_short_posts(self, pillar):
        """Create various short-form posts"""
        idea = pillar["idea"]
        examples = pillar["real_data"]["examples"]
        stats = pillar["real_data"]["statistics"]

        posts = {}

        # Single tweet version
        posts["single_tweet"] = f"{idea['title']}\n\n{idea['description'][:150]}\n\nBuilt {stats[0]['stat']} with Claude Code. No coding required.\n\n#ClaudeCode #Automation"

        # Instagram caption
        posts["instagram"] = f"""{idea['title']}

{idea['description']}

I've built {self.project_data['aggregate_stats']['total_projects']} automation projects this year using Claude Code.

No coding background. Just learned to describe what I need in plain English.

Real examples:
{chr(10).join([f'• {ex["title"]} - {ex["business_value"]}' for ex in examples[:3]])}

The future of small business isn't hiring developers. It's learning to communicate with AI.

What would you automate if you could?

#ClaudeCode #SmallBusiness #Automation #AI #Productivity #BuildingInPublic #Entrepreneur #BusinessAutomation
"""

        # Threads post
        posts["threads"] = f"""{idea['title']}

{idea['description']}

Over the past year, I've built {self.project_data['aggregate_stats']['total_projects']} automation projects with Claude Code.

Real example: {examples[0]['title'] if examples else 'Custom automation'}

{examples[0]['description'] if examples else ''}

Business impact: {examples[0]['business_value'] if examples else 'Significant time savings'}

No coding required. Just describe what you need.

This is the future of small business.

#ClaudeCode #Automation #BuildingInPublic
"""

        return posts

    def _extract_problem(self, example):
        """Extract the problem from an example"""
        problem_map = {
            "vendor-quote-tool": "Manual quote creation was taking hours and looked unprofessional",
            "Personal-OS": "Managing multiple business operations manually led to inconsistencies and missed tasks",
            "legiscraper": "Researching legislative data across multiple states was time-consuming and error-prone",
            "UsageDash": "No visibility into usage patterns and metrics without expensive analytics tools"
        }
        return problem_map.get(example["project"], "Manual processes were inefficient and time-consuming")

    def _extract_replaced_tool(self, example):
        """Extract what tool this replaced"""
        if "vendor-quote-tool" in example["project"]:
            return "Manual Word docs and email"
        elif "UsageDash" in example["project"]:
            return "$150/month analytics subscription"
        elif "Personal-OS" in example["project"]:
            return "Multiple task managers and monitoring tools"
        return "Manual processes"

    def _extract_time_savings(self, example):
        """Extract time savings from example"""
        if "vendor-quote-tool" in example["project"]:
            return "5 hours/week"
        elif "Personal-OS" in example["project"]:
            return "20 hours/week"
        return "10 hours/week"


def main():
    generator = PillarContentGenerator()

    # Get business-focused ideas
    business_ideas = [idea for idea in generator.content_ideas["content_ideas"]
                     if idea.get("audience") == "small_business_owners"]

    print("=" * 80)
    print("PILLAR CONTENT GENERATOR")
    print("=" * 80)
    print(f"\nGenerating pillar content for top business ideas...\n")

    # Generate pillar content for top 3 business ideas
    pillars = []
    for i, idea in enumerate(business_ideas[:3], 1):
        print(f"\n{'='*80}")
        print(f"PILLAR #{i}: {idea['title']}")
        print(f"{'='*80}")

        pillar = generator.create_pillar_content(idea['id'])
        pillars.append(pillar)

        print(f"\n✅ Generated pillar content with:")
        print(f"   - YouTube script ({len(pillar['content']['youtube_script'])} characters)")
        print(f"   - LinkedIn article ({len(pillar['content']['linkedin_article'])} characters)")
        print(f"   - Twitter thread ({pillar['content']['twitter_thread']['tweet_count']} tweets)")
        print(f"   - {len(pillar['content']['short_posts'])} short-form posts")

        print(f"\n📊 Using {len(pillar['real_data']['examples'])} real examples:")
        for example in pillar['real_data']['examples']:
            print(f"   • {example['title']} ({example['project']})")

        print(f"\n📈 Statistics included:")
        for stat in pillar['real_data']['statistics'][:3]:
            print(f"   • {stat['stat']}")

    # Save all pillars
    output_file = Path(__file__).parent / "pillar_content_library.json"
    with open(output_file, 'w') as f:
        json.dump({"pillars": pillars, "created": datetime.now().isoformat()}, f, indent=2)

    print(f"\n\n{'='*80}")
    print(f"✅ Pillar content saved to: {output_file}")
    print(f"📚 Total pillars generated: {len(pillars)}")
    print(f"{'='*80}")

    # Show preview of first pillar's YouTube script
    print(f"\n\n{'='*80}")
    print("PREVIEW: YouTube Script for Pillar #1")
    print(f"{'='*80}")
    print(pillars[0]['content']['youtube_script'][:1500])
    print("\n[... full script continues ...]")

if __name__ == "__main__":
    main()
