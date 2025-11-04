#!/usr/bin/env python3
"""
Dynamic Pillar Content Generator
Generates NEW pillar ideas by combining:
1. RSS trending topics from Content tab
2. Real Claude Code projects
3. Skill-based script generation
"""

import json
from pathlib import Path
from datetime import datetime
import hashlib

class DynamicPillarGenerator:
    """Generates pillar content dynamically from trends + projects"""

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.project_data = self.load_project_data()
        self.rss_trends = self.load_rss_trends()
        self.frameworks = self.load_frameworks()

    def load_project_data(self):
        """Load real project analysis"""
        data_file = self.base_dir / "config" / "project_data_analysis.json"
        with open(data_file, 'r') as f:
            return json.load(f)

    def load_rss_trends(self):
        """Load RSS trends from Content tab data"""
        rss_file = self.base_dir / "scouts" / "rss_ideas_database.json"
        try:
            with open(rss_file, 'r') as f:
                data = json.load(f)
                return data.get('ideas', [])
        except:
            return []

    def load_frameworks(self):
        """Load Kallaway frameworks"""
        framework_file = self.base_dir / "config" / "content_frameworks" / "kallaway_hooks.json"
        with open(framework_file, 'r') as f:
            return json.load(f)

    def generate_new_pillar_ideas(self, count=3):
        """Generate NEW pillar ideas from trends + projects"""

        ideas = []

        # Get top RSS trends
        top_trends = self.rss_trends[:5] if self.rss_trends else []

        # Get real examples
        real_examples = self.project_data.get("real_examples", [])[:10]

        # Generate pillar ideas by fusing trends with projects
        for i, trend in enumerate(top_trends[:count]):
            # Pick different project examples for each pillar
            example_start = (i * 3) % len(real_examples)
            trend_examples = real_examples[example_start:example_start+3]

            # Create unique pillar ID
            pillar_id = hashlib.md5(
                f"{trend.get('title', '')}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:12]

            # Generate pillar title fusing trend + Claude Code angle
            pillar_title = self.generate_pillar_title(trend, trend_examples)

            idea = {
                "id": pillar_id,
                "title": pillar_title,
                "category": "use_cases",
                "hook_type": "transformation",
                "audience": "small_business_owners",
                "urgency": "high",
                "created_date": datetime.now().isoformat(),
                "trend_source": trend,
                "project_examples": trend_examples,
                "description": self.generate_description(trend, trend_examples)
            }

            ideas.append(idea)

        return ideas

    def generate_pillar_title(self, trend, examples):
        """Generate pillar title combining trend + Claude Code"""

        trend_topic = trend.get('title', '').split(':')[0].strip()

        if examples:
            example = examples[0]
            project_name = example.get('title', '').replace('How to: ', '')

            # Create fusion title
            templates = [
                f"How I used Claude Code to {trend_topic.lower()} in {project_name}",
                f"Building {project_name} with Claude Code: {trend_topic}",
                f"{trend_topic}: A real-world Claude Code implementation"
            ]

            return templates[0]

        return f"How I automated {trend_topic.lower()} with Claude Code"

    def generate_description(self, trend, examples):
        """Generate pillar description"""

        if examples:
            example = examples[0]
            business_value = example.get('business_value', 'automated workflow')

            return f"Real implementation: {business_value}. Built with Claude Code. Here's the complete workflow."

        return "Step-by-step guide using Claude Code. No coding required."

    def create_full_pillar(self, idea):
        """Create complete pillar content with scripts"""

        trend = idea.get('trend_source', {})
        examples = idea.get('project_examples', [])

        # Extract statistics from examples
        stats = self.extract_statistics(examples)

        # Build real_data structure
        real_data = {
            "examples": examples,
            "statistics": stats,
            "insights": self.project_data.get("insights", [])[:5]
        }

        pillar = {
            "id": f"pillar_{idea['id']}",
            "created_date": idea['created_date'],
            "idea": idea,
            "hook_framework": self.frameworks["hook_types"].get("transformation", {}),
            "real_data": real_data,
            "content": {}
        }

        # Generate content using skill-based approach
        pillar["content"]["youtube_script"] = self.create_youtube_script_skillbased(pillar)
        pillar["content"]["linkedin_article"] = self.create_linkedin_article(pillar)
        pillar["content"]["twitter_thread"] = self.create_twitter_thread(pillar)
        pillar["content"]["short_posts"] = self.create_short_posts(pillar)

        return pillar

    def extract_statistics(self, examples):
        """Extract statistics from project examples"""

        stats = []

        # Add aggregate stats
        if self.project_data.get("aggregate_stats"):
            agg = self.project_data["aggregate_stats"]

            stats.append({
                "stat": f"{agg.get('total_projects', 0)} active projects",
                "detail": "Managing diverse automation projects with Claude Code",
                "source": "Project Data"
            })

            if agg.get('automation_tools'):
                stats.append({
                    "stat": f"{agg['automation_tools']} automation tools",
                    "detail": "Built autonomous agents and workflows",
                    "source": "Project Analysis"
                })

        # Add example-specific stats
        for example in examples[:2]:
            if example.get('business_value'):
                stats.append({
                    "stat": example.get('title', 'Project'),
                    "detail": example['business_value'],
                    "source": "Real Implementation"
                })

        return stats[:5]

    def create_youtube_script_skillbased(self, pillar):
        """Create YouTube script using skill-based framework"""

        idea = pillar['idea']
        examples = pillar['real_data']['examples']
        stats = pillar['real_data']['statistics']

        # Build script using framework structure
        script = f"""# {idea['title']}

{idea['description']}

## The Reality Check

"""

        # Add statistics
        for stat in stats[:3]:
            script += f"- {stat['stat']}: {stat['detail']}\n"

        script += """

## What I've Built (Real Examples)

"""

        # Add project examples
        for i, example in enumerate(examples[:3], 1):
            script += f"""
### {example.get('title', f'Project {i}')}

**The Challenge**: {example.get('use_case', 'Business automation need')}

**The Solution**: {example.get('description', 'Built with Claude Code')}

**Business Impact**: {example.get('business_value', 'Saves time and increases efficiency')}

**Tech Stack**: {example.get('tech', 'Claude Code')}

---
"""

        script += """

## The Numbers Don't Lie

"""

        # Repeat key statistics
        for stat in stats:
            script += f"- **{stat['stat']}**: {stat['detail']}\n"

        script += """

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

Don't think "I need a Python script that..."
Think "I need a system that automatically handles..."

**Step 2: Describe It Like Delegating**

Talk to Claude like you're delegating to a capable assistant.

**Step 3: Iterate Based on Results**

The first version works. Then you refine based on actual use.

## Why This Matters

Big companies have unlimited dev resources.
Small businesses now have Claude Code.

It's not about competing. It's about having the same capabilities without the overhead.

## Start Here

Pick ONE task that wastes your time every week.
Describe it to Claude Code.
That's it.

## What Are You Automating?

Comment below with one task you want to automate and I'll help you structure the prompt.

#ClaudeCode #Automation #SmallBusiness
"""

        return script

    def create_linkedin_article(self, pillar):
        """Create LinkedIn article"""
        return pillar["content"]["youtube_script"]  # Same content, formatted for LinkedIn

    def create_twitter_thread(self, pillar):
        """Create Twitter thread"""

        idea = pillar['idea']
        examples = pillar['real_data']['examples']

        tweets = []

        # Opening tweet
        tweets.append({
            "text": f"{idea['title']}\n\nA thread 🧵👇"
        })

        # Stats tweet
        tweets.append({
            "text": f"Over the past year:\n\n✅ {len(examples)} projects built\n✅ Zero coding background\n\nJust learned to talk to AI effectively."
        })

        # Example tweets
        for i, ex in enumerate(examples[:3], 1):
            tweets.append({
                "text": f"Example {i}: {ex.get('title', 'Project')}\n\n{ex.get('description', '')}[:180]\n\nResult: {ex.get('business_value', 'Automated workflow')}"
            })

        # Closing CTA
        tweets.append({
            "text": "Reply with what you want to automate and I'll help you structure the prompt.\n\n#ClaudeCode #Automation"
        })

        return {
            "tweet_count": len(tweets),
            "tweets": tweets
        }

    def create_short_posts(self, pillar):
        """Create short posts for Instagram/Threads/Twitter"""

        idea = pillar['idea']
        examples = pillar['real_data']['examples']

        posts = []

        # Instagram post
        instagram_text = f"🚀 {idea['title']}\n\n"
        instagram_text += f"Built {len(examples)} projects with Claude Code this year.\n\n"
        if examples:
            instagram_text += f"Real example: {examples[0].get('title', '')}\n{examples[0].get('business_value', '')}\n\n"
        instagram_text += "#ClaudeCode #Automation #BuildingInPublic"

        posts.append({
            "platform": "Instagram",
            "post": instagram_text
        })

        # Threads post
        threads_text = f"💡 {idea['title']}\n\n{idea['description']}\n\nThis is the future of small business.\n\n#ClaudeCode #Automation"

        posts.append({
            "platform": "Threads",
            "post": threads_text
        })

        # Single tweet
        tweet_text = f"{idea['title']}\n\nBuilt {len(examples)} projects with Claude Code. No coding required.\n\n#ClaudeCode #Automation"

        posts.append({
            "platform": "Twitter",
            "post": tweet_text
        })

        return posts


def main():
    """Test the dynamic generator"""

    generator = DynamicPillarGenerator()

    # Generate 3 NEW pillar ideas
    print("Generating new pillar ideas...")
    ideas = generator.generate_new_pillar_ideas(count=3)

    print(f"\nGenerated {len(ideas)} new pillar ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"\n{i}. {idea['title']}")
        print(f"   Created: {idea['created_date']}")
        print(f"   Examples: {len(idea['project_examples'])}")

    # Create full pillar content for first idea
    print("\n\nCreating full pillar content for first idea...")
    pillar = generator.create_full_pillar(ideas[0])

    print(f"\n✅ Created pillar: {pillar['id']}")
    print(f"   YouTube script: {len(pillar['content']['youtube_script'])} chars")
    print(f"   Twitter thread: {pillar['content']['twitter_thread']['tweet_count']} tweets")
    print(f"   Short posts: {len(pillar['content']['short_posts'])} posts")


if __name__ == "__main__":
    main()
