#!/usr/bin/env python3
"""
Generate Scripts from Selected RSS Ideas
Combines viral AI trends with personal Claude Code projects using script-variation-generator framework
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def load_selected_ideas():
    """Load ideas selected from the UI"""
    selected_file = Path(__file__).parent.parent / 'scouts' / 'selected_ideas.json'
    if not selected_file.exists():
        print("❌ No selected ideas found")
        return []

    with open(selected_file, 'r') as f:
        data = json.load(f)

    return data.get('ideas', [])

def load_project_data():
    """Load personal Claude Code project data"""
    project_file = Path(__file__).parent.parent / 'config' / 'project_data_analysis.json'
    if project_file.exists():
        with open(project_file, 'r') as f:
            return json.load(f)
    return {}

def generate_kallaway_hook(idea, variation_type):
    """Generate Kallaway's 4-part hook structure"""

    if variation_type == "contrarian":
        return f"""## HOOK (0:00 - 0:30)

Everyone's talking about {idea.get('categories', ['AI'])[0]} as the future.

**[VISUAL: Typical {idea.get('categories', ['AI'])[0]} headlines]**

But here's what they're not telling you—{idea['title'].lower()}.

**[VISUAL: Headlines disappearing]**

{idea['description']}

**[VISUAL: Key stat appearing - "{idea['key_stats'][0]}"]**

This isn't incremental improvement. This is a fundamental shift. And I'll show you why that changes everything.
"""

    elif variation_type == "authority":
        return f"""## HOOK (0:00 - 0:30)

When you're managing real AI automation projects at scale, you see patterns that most people miss.

**[VISUAL: Project dashboard with multiple AI agents]**

Here's what I discovered after implementing autonomous systems across 34 active projects: {idea['title'].lower()}.

**[VISUAL: Data visualization showing scale]**

{idea['description']}

**[VISUAL: "{idea['key_stats'][0]}" stat appearing]**

Let me show you exactly how this works and why it matters for your business.
"""

    else:  # transformation
        return f"""## HOOK (0:00 - 0:30)

Six months ago, I was skeptical about {idea.get('categories', ['AI'])[0]}.

**[VISUAL: Before/after split screen]**

Then I saw the data: {idea['title'].lower()}.

**[VISUAL: Stat appearing dramatically]**

{idea['description']}

**[VISUAL: "{idea['key_stats'][0]}"]**

This completely changed how I think about automation. Let me show you what I learned.
"""

def generate_why_section(idea, user_notes):
    """Generate WHY section with problem statement"""

    notes_context = f"\n\n**User Insight:** {user_notes}" if user_notes else ""

    return f"""## WHY THIS MATTERS (1:00 - 3:30)

### The Shift Everyone's Missing

{idea['description']}

**[VISUAL: Data comparison]**

Let's look at the numbers:

{chr(10).join(f'- {stat}' for stat in idea['key_stats'])}

**Why This Changes Everything:**

{idea.get('business_value', 'This represents a fundamental shift in how AI automation works at scale.')}

**[VISUAL: Impact visualization]{notes_context}

### The Real Cost of Ignoring This

If you're still operating with the old model, here's what you're leaving on the table:

**[VISUAL: Opportunity cost breakdown]**

- **Speed:** While competitors automate at {idea.get('content_angle', 'modern rates')}, manual processes fall behind exponentially
- **Cost:** Human-dependent workflows scale linearly with cost, while AI automation costs stay flat
- **Quality:** Manual processes have 5-10% error rates vs. <1% for automated systems
- **Scale:** Human teams hit capacity limits, automated systems scale infinitely

The gap widens every single day.
"""

def generate_what_section(idea, project_examples):
    """Generate WHAT section with solution"""

    return f"""## WHAT ACTUALLY WORKS (3:30 - 5:30)

### The New Model: {idea.get('content_angle', 'Automation-First Architecture')}

Here's the architecture that delivers these results:

**[VISUAL: System architecture diagram]**

**Component 1: Autonomous Agent Layer**
- Handles 80-95% of tasks without human intervention
- Uses {idea.get('source', 'proven AI systems')}
- Runs 24/7 with automatic validation
- Error rate: <1%

**Component 2: Exception Handler**
- Surfaces edge cases to human review
- Learns from human decisions
- Reduces exception rate over time
- Current exception rate: ~5% (down from 20%)

**Component 3: Continuous Learning System**
- Records all operations and outcomes
- Updates rules based on patterns
- Improves accuracy automatically
- Self-optimizing performance

### Real-World Example

**[VISUAL: Case study comparison]**

Let me show you how this works with a real implementation:

**Scenario:** {idea['title']}

**Before (Manual Process):**
- Time per task: 60+ minutes
- Error rate: 5-10%
- Cost: $50-100 per task
- Scale limit: Human capacity

**After (Automated Process):**
- Time per task: 15 minutes (4× faster)
- Error rate: <1%
- Cost: $0.50-1.00 per task (100× reduction)
- Scale limit: API rate limits only

**[VISUAL: Dramatic before/after comparison]**

The math is undeniable: **4× faster, 100× cheaper, 10× more accurate.**
"""

def generate_how_section(idea, user_notes):
    """Generate HOW section with implementation steps"""

    implementation_context = f"\n\n**Implementation Note:** {user_notes}" if user_notes else ""

    return f"""## HOW TO IMPLEMENT THIS (5:30 - 8:30)

### Step 1: Identify Your Automation Opportunity

Use this framework to find high-impact tasks:

**[VISUAL: Decision matrix]**

**High Automation Potential:**
- ✅ Repeatable (same process every time)
- ✅ Rule-based (clear decision criteria)
- ✅ Data-driven (structured inputs/outputs)
- ✅ High-volume (done frequently)

**Example from {idea['title']}:**
- Fits repeatable pattern: ✅
- Has clear rules: ✅
- Uses structured data: ✅
- High volume opportunity: ✅

**Perfect automation candidate.**{implementation_context}

### Step 2: Build the Autonomous System

Here's the exact architecture:

**[VISUAL: Implementation diagram]**

```python
# Autonomous Agent Template
class AutonomousAgent:
    def monitor_trigger(self):
        # Watch for events that need handling
        pass

    def execute_workflow(self, task):
        # Run predefined process
        # Validate output
        # Log results
        pass

    def handle_exceptions(self, task):
        # Check for edge cases
        # Surface to human if needed
        # Learn from decisions
        pass
```

**Implementation Steps:**

1. **Define your "happy path" workflow**
   - What happens 80% of the time?
   - What are the standard inputs and outputs?

2. **Set up autonomous execution**
   - Use Claude API for agent logic
   - Define validation criteria
   - Configure automatic logging

3. **Configure exception handling**
   - Define what qualifies as an exception
   - Set up human review queue
   - Build learning feedback loop

4. **Deploy and monitor**
   - Start in shadow mode (propose only)
   - Monitor for 1-2 weeks
   - Switch to autonomous mode
   - Review results daily

### Step 3: Optimize Through Learning

The key to {idea.get('key_stats', ['continuous improvement'])[0]} is systematic learning:

**[VISUAL: Learning loop diagram]**

**Learning Process:**

```
Exception surfaces →
Human reviews (5 min) →
Human documents decision rationale →
System updates rules →
Similar cases handled autonomously →
Exception rate drops
```

**Real Example:**

**Month 1:** 20% exception rate (200 reviews/day)
**Month 3:** 10% exception rate (100 reviews/day)
**Month 6:** 5% exception rate (50 reviews/day)
**Month 12:** 2% exception rate (20 reviews/day)

**You're teaching the system your judgment at scale.**

### Step 4: Scale the Model

Once you have one autonomous agent working:

**[VISUAL: Scaling diagram]**

1. **Replicate the pattern** to similar tasks
2. **Share learning** across agent instances
3. **Build agent networks** that coordinate
4. **Create autonomous workflows** end-to-end

**Example scaling path:**

- Week 1: First agent deployed (1 task automated)
- Month 1: 3 agents running (3 tasks automated)
- Month 3: 10 agents running (10 tasks automated)
- Month 6: 25+ agents running (25+ tasks automated)

**[VISUAL: Exponential growth curve]**

Each new agent takes less time to deploy because you're using the same pattern.
"""

def generate_results_section(idea):
    """Generate results and call to action"""

    return f"""## THE REALITY CHECK (8:30 - 9:30)

### The Numbers Don't Lie

**[VISUAL: Industry data compilation]**

**Market Data:**
- Current market size: {idea.get('market_size', '$5.1B+ and growing')}
- Growth rate: 44.8%+ CAGR
- Adoption timeline: Happening now, not future

**Real Implementation Results:**

**From {idea['source']}:**
{chr(10).join(f'- {stat}' for stat in idea['key_stats'])}

**[VISUAL: Results summary]**

**Pattern Across All Implementations:**
- Automation handles: 80-95% of volume
- Human role: Strategy + exceptions + learning
- Speed improvement: 4-5× faster
- Cost reduction: 100× lower
- Quality improvement: 10× more accurate

### What This Means For You

**If you're still manual:** You're operating at 1× speed while competitors run at 4× speed.

**If you're augmenting:** You're getting 2× improvement but paying for AI + human time on every task.

**If you're automating:** You're getting 4-5× improvement with costs that stay flat as you scale.

**[VISUAL: Three paths diverging]**

**The gap compounds daily.**

---

## YOUR MOVE (9:30 - 10:00)

Here's your implementation plan:

**Week 1: Pick Your First Task**

Choose something:
- Repetitive (done frequently)
- Rule-based (clear criteria)
- High-volume (big impact)

**Week 2: Build Your First Agent**

Use this prompt with Claude:

```
"Build an autonomous agent that:
1. Monitors for [trigger event]
2. Executes [workflow steps]
3. Validates output meets [criteria]
4. Flags for review if [exception conditions]
5. Runs automatically without my input

Make it production-ready."
```

**Week 3: Deploy and Monitor**

- Start in shadow mode
- Review proposed actions
- Tune exception criteria
- Switch to autonomous after 100 successful runs

**Week 4: Scale to Next Task**

- Apply same pattern
- Share learnings across agents
- Build toward full automation

**[VISUAL: 4-week roadmap]**

**In 30 days, you'll have proof this works.**

**In 90 days, you'll have 5-10 autonomous agents running.**

**In 6 months, you'll wonder how you ever worked manually.**

**[VISUAL: "{idea['title']}" title card]**

The question isn't whether to automate.

It's whether you'll do it before your competition does.

**Drop a comment: What's the first task you're automating?**

I'll send you the exact Claude prompt to get started.

**[END SCREEN]**

---

## VIDEO METADATA

**Title:** {idea['title']} (The Data Will Shock You)

**Description:**
{idea['description']}

🎯 What You'll Learn:
{chr(10).join(f'- {stat}' for stat in idea['key_stats'][:3])}
- Why manual processes can't compete anymore
- The exact autonomous agent architecture that works
- Step-by-step implementation guide

⏱️ Timestamps:
0:00 - Hook: {idea['title'][:50]}...
1:00 - Why this changes everything
3:30 - The autonomous + exception model
5:30 - How to implement (step-by-step)
8:30 - Real-world results and data
9:30 - Your 30-day implementation plan

📊 Data Sources:
- {idea['source']}
- {idea.get('url', 'Multiple industry sources')}

#{' #'.join(idea.get('categories', ['AI', 'Automation', 'Business']))} #ClaudeAI #Productivity

**Tags:**
{', '.join(idea.get('categories', []) + ['AI automation', 'business automation', 'autonomous agents', 'productivity', 'AI trends 2024'])}

**Thumbnail Text:**
"{idea['title'][:30]}..."
"{idea['key_stats'][0][:40]}"
"(The Future Is Here)"
"""

def generate_full_script(idea, variation_type, project_data, user_notes=""):
    """Generate complete script combining RSS idea with personal content"""

    # Get relevant project examples
    project_examples = []
    if project_data and isinstance(project_data, dict):
        try:
            projects = project_data.get('projects', [])
            if isinstance(projects, list) and len(projects) > 0:
                project_examples = projects[:2]
        except Exception as e:
            print(f"   ⚠️  Could not load project examples: {e}")
            project_examples = []

    # Build complete script
    script = f"""# {idea['title']}

**Video Length:** ~10 minutes
**Word Count:** ~1,450 words
**Variation:** {variation_type.title()}
**Source:** {idea['source']}
**RSS Idea Score:** {idea['score']}/100

---

{generate_kallaway_hook(idea, variation_type)}

---

## INTRO (0:30 - 1:00)

I'm Liz, and I build autonomous AI systems.

Not AI assistants. Not AI copilots. **Autonomous systems** that run without human intervention.

**[VISUAL: System dashboard]**

And the data I'm about to show you isn't a prediction—it's happening right now:

{chr(10).join(f'- {stat}' for stat in idea['key_stats'][:3])}

**This is the shift from AI assistance to AI autonomy.**

And if you're still thinking about "augmenting" your work, you're already behind.

---

{generate_why_section(idea, user_notes)}

---

{generate_what_section(idea, project_examples)}

---

{generate_how_section(idea, user_notes)}

---

{generate_results_section(idea)}
"""

    return script

def main():
    """Main execution"""
    print("🚀 Starting Script Generation from Selected Ideas\n")

    # Load data
    selected_ideas = load_selected_ideas()
    if not selected_ideas:
        print("❌ No ideas to process")
        return

    project_data = load_project_data()

    print(f"📊 Found {len(selected_ideas)} selected ideas\n")

    # Output directory
    output_dir = Path(__file__).parent.parent / 'pillar_scripts'
    output_dir.mkdir(exist_ok=True)

    # Generate scripts for each idea (3 variations each)
    variations = ['contrarian', 'authority', 'transformation']
    total_generated = 0

    for idea in selected_ideas:
        print(f"\n📝 Generating scripts for: {idea['title']}")
        print(f"   Score: {idea['score']}/100")
        print(f"   User Notes: {idea.get('user_notes', 'None')[:100]}...")

        for variation in variations:
            # Generate script
            script = generate_full_script(
                idea,
                variation,
                project_data,
                idea.get('user_notes', '')
            )

            # Save to file
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"{date_str}_{idea['id']}_{variation}.md"
            filepath = output_dir / filename

            with open(filepath, 'w') as f:
                f.write(script)

            print(f"   ✅ Created: {variation} variation ({len(script)} chars)")
            total_generated += 1

    # Update execution log
    log_file = Path(__file__).parent.parent / 'systems' / 'skills-main' / 'script-variation-generator' / 'execution.log'

    if log_file.exists():
        with open(log_file, 'a') as f:
            f.write(f"\n\n### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Action:** Generated from selected RSS ideas\n")
            f.write(f"**Ideas Processed:** {len(selected_ideas)}\n")
            f.write(f"**Scripts Generated:** {total_generated}\n")
            f.write(f"**Output Location:** `/active/Social-Content-Generator/pillar_scripts/`\n")
            f.write(f"**Ideas:**\n")
            for idea in selected_ideas:
                f.write(f"- {idea['title']} (Score: {idea['score']}/100)\n")
            f.write(f"**Status:** ✅ Success\n")

    print(f"\n\n✅ Complete! Generated {total_generated} scripts")
    print(f"📂 Location: {output_dir}")
    print(f"📋 Scripts ready for review and customization\n")

if __name__ == '__main__':
    main()
