#!/usr/bin/env python3
"""
Contrarian Angle Generator
Creates professional and spicy/contrarian variations of content ideas
Generates unique perspectives and tension points
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class ContrarianAngleGenerator:
    """Generate contrarian and unique angles for content"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent

        # Contrarian frameworks
        self.frameworks = {
            'inversion': {
                'name': 'Inversion Framework',
                'pattern': 'Everyone says X. But the truth is Y.',
                'examples': [
                    'Everyone says you need developers → Truth: You need clear thinking',
                    'Everyone says scale requires people → Truth: Scale requires systems'
                ]
            },
            'scale_surprise': {
                'name': 'Scale Surprise',
                'pattern': 'X seems small. But at scale, it becomes Y.',
                'examples': [
                    '5 minutes saved → Across 250 work days = 20 hours/year',
                    '$10/month tool → Across team of 10 = $1,200/year wasted'
                ]
            },
            'time_shift': {
                'name': 'Time Shift',
                'pattern': 'What used to take X now takes Y.',
                'examples': [
                    'Hiring a dev (6 months) → Claude Code (45 minutes)',
                    'Building a tool (weeks) → Describing it (1 hour)'
                ]
            },
            'hidden_cost': {
                'name': 'Hidden Cost',
                'pattern': 'You think it costs X. The real cost is Y.',
                'examples': [
                    'Think: $50/month subscription → Real: 10 hours learning + maintenance',
                    'Think: Free tool → Real: Your time debugging'
                ]
            },
            'paradox': {
                'name': 'Paradox',
                'pattern': 'The more X you do, the less Y you get.',
                'examples': [
                    'More tools → Less productivity',
                    'More automation → More manual setup'
                ]
            }
        }

    def generate_professional(self, idea: Dict, research: Dict = None) -> Dict:
        """
        Generate professional angle
        - Data-driven
        - Credible
        - Educational tone
        """

        title = idea.get('title', '')
        description = idea.get('description', '')

        # Extract key concept
        key_concept = self._extract_key_concept(title)

        # Build professional angle
        professional = {
            'variation_type': 'professional',
            'tone': 'educational',
            'hook_style': 'data_first',
            'angles': []
        }

        # Angle 1: Statistical Authority
        if research and research.get('statistics'):
            top_stat = research['statistics'][0]
            professional['angles'].append({
                'type': 'statistical_authority',
                'hook': f"{top_stat['stat']} {top_stat['detail']}.",
                'bridge': f"This is why {key_concept} matters more than ever.",
                'promise': f"Here's how to leverage {key_concept} effectively:",
                'framework': 'benefit_driven'
            })

        # Angle 2: Industry Expert
        professional['angles'].append({
            'type': 'industry_expert',
            'hook': f"After analyzing {key_concept} across multiple projects, I've identified a clear pattern.",
            'bridge': "Most people miss this critical insight.",
            'promise': f"Here's what actually works:",
            'framework': 'how_to'
        })

        # Angle 3: Practical Guide
        professional['angles'].append({
            'type': 'practical_guide',
            'hook': f"A complete guide to {key_concept} for non-technical professionals.",
            'bridge': f"No coding required. No complex setup. Just results.",
            'promise': f"3 steps to implement {key_concept} today:",
            'framework': 'how_to'
        })

        return professional

    def generate_spicy(self, idea: Dict, research: Dict = None) -> Dict:
        """
        Generate spicy/contrarian angle
        - Challenges assumptions
        - Provocative
        - Memorable
        """

        title = idea.get('title', '')
        description = idea.get('description', '')

        key_concept = self._extract_key_concept(title)

        spicy = {
            'variation_type': 'spicy',
            'tone': 'contrarian',
            'hook_style': 'challenge_belief',
            'angles': []
        }

        # Angle 1: Inversion (Challenge common belief)
        spicy['angles'].append({
            'type': 'inversion',
            'framework_used': 'inversion',
            'hook': f"Everyone's doing {key_concept} wrong.",
            'contrast': f"They think it requires expensive tools and technical expertise.",
            'reality': f"I've proven you can do it in 45 minutes with zero code.",
            'tension': "Why are experts making this so complicated?",
            'cta': f"Here's the simple truth about {key_concept}:"
        })

        # Angle 2: Scale Surprise
        if research and research.get('statistics'):
            stat = research['statistics'][0]
            spicy['angles'].append({
                'type': 'scale_surprise',
                'framework_used': 'scale_surprise',
                'hook': f"{stat['stat']} sounds impressive.",
                'contrast': f"But here's what they don't tell you:",
                'reality': f"That's hours of your life you'll never get back. Unless you automate.",
                'tension': "Small inefficiencies compound into massive waste.",
                'cta': f"Stop the bleeding. Here's how:"
            })

        # Angle 3: Time Shift (Then vs Now)
        spicy['angles'].append({
            'type': 'time_shift',
            'framework_used': 'time_shift',
            'hook': f"A year ago, {key_concept} took weeks and cost thousands.",
            'contrast': f"Today, it takes 30 minutes and costs nothing.",
            'reality': f"Yet 80% of people are still doing it the old way.",
            'tension': "Why are you still paying for last decade's solutions?",
            'cta': f"Wake up. Here's the new playbook:"
        })

        # Angle 4: Hidden Cost
        spicy['angles'].append({
            'type': 'hidden_cost',
            'framework_used': 'hidden_cost',
            'hook': f"That $50/month tool for {key_concept}?",
            'contrast': f"You think you're saving time.",
            'reality': f"But you spent 10 hours learning it, 5 hours maintaining it, and it only saves 2 hours/month.",
            'tension': "The subscription model is robbing you blind.",
            'cta': f"Here's the real calculation:"
        })

        # Angle 5: Paradox
        spicy['angles'].append({
            'type': 'paradox',
            'framework_used': 'paradox',
            'hook': f"The more tools you add, the less productive you become.",
            'contrast': f"Everyone chases the next {key_concept} solution.",
            'reality': f"I replaced 3 tools with 1 simple automation. Results: 10x better.",
            'tension': "Tool fatigue is killing your productivity.",
            'cta': f"Less is more. Here's proof:"
        })

        return spicy

    def generate_balanced(self, idea: Dict, research: Dict = None) -> Dict:
        """
        Generate balanced angle
        - Professional credibility + memorable edge
        - Data-backed + personality
        """

        title = idea.get('title', '')
        key_concept = self._extract_key_concept(title)

        balanced = {
            'variation_type': 'balanced',
            'tone': 'confident_educator',
            'hook_style': 'data_with_edge',
            'angles': []
        }

        # Angle 1: Personal + Statistical
        if research and research.get('statistics'):
            stat = research['statistics'][0]
            balanced['angles'].append({
                'type': 'personal_statistical',
                'hook': f"I tested {key_concept} across 32 projects.",
                'stat_line': f"Result: {stat['stat']} {stat['detail']}",
                'tension': f"Most people waste time on the wrong approach.",
                'promise': f"Here's what actually works:",
                'framework': 'transformation'
            })

        # Angle 2: Myth-busting with proof
        balanced['angles'].append({
            'type': 'myth_busting',
            'hook': f"Myth: {key_concept} requires technical expertise.",
            'reality': f"Truth: I built {key_concept} solutions without writing a single line of code.",
            'proof': f"32 working projects. 40 autonomous agents. Zero programming.",
            'promise': f"Here's my framework:",
            'framework': 'contrarian_snapback'
        })

        return balanced

    def _extract_key_concept(self, title: str) -> str:
        """Extract the main concept from title"""

        # Remove common filler words
        fillers = ['how to', 'why', 'what', 'when', 'the', 'a', 'an', 'best', 'top', '2025', '2024']

        title_lower = title.lower()
        for filler in fillers:
            title_lower = title_lower.replace(filler, '')

        # Take first meaningful phrase (3-5 words)
        words = title_lower.split()[:5]
        return ' '.join(words).strip()

    def generate_all_angles(self, idea: Dict, research: Dict = None) -> Dict:
        """Generate all angle variations for an idea"""

        return {
            'idea_id': idea.get('id'),
            'idea_title': idea.get('title'),
            'professional': self.generate_professional(idea, research),
            'spicy': self.generate_spicy(idea, research),
            'balanced': self.generate_balanced(idea, research),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_angles': 3,  # professional, spicy, balanced
                'has_research': research is not None
            }
        }

    def batch_generate(self, ideas: List[Dict], research_data: Dict = None) -> Dict:
        """Generate angles for multiple ideas"""

        print("\n" + "="*100)
        print("🎭 CONTRARIAN ANGLE GENERATOR")
        print("="*100)

        print(f"\n🔄 Generating angles for {len(ideas)} ideas...")

        results = []

        for i, idea in enumerate(ideas, 1):
            print(f"\n   [{i}/{len(ideas)}] {idea.get('title', '')[:60]}...")

            # Find matching research
            research = None
            if research_data:
                for r in research_data.get('results', []):
                    if r.get('idea_id') == idea.get('id'):
                        research = r.get('research')
                        break

            angles = self.generate_all_angles(idea, research)
            results.append(angles)

        # Save results
        output_file = self.agents_dir / 'contrarian_angles.json'

        output = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'ideas_processed': len(ideas),
                'total_variations': len(results) * 3
            },
            'angles': results
        }

        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✅ Angles generated! Saved to: {output_file}")

        # Summary
        print("\n" + "="*100)
        print("📊 ANGLE GENERATION SUMMARY")
        print("="*100)

        print(f"\n🎯 Generated {len(results) * 3} total angle variations:")
        print(f"   • {len(results)} Professional angles")
        print(f"   • {len(results)} Spicy/Contrarian angles")
        print(f"   • {len(results)} Balanced angles")

        print(f"\n🔥 Sample Spicy Angles:")
        for i, result in enumerate(results[:3], 1):
            spicy_angle = result['spicy']['angles'][0]
            print(f"\n   {i}. {result['idea_title'][:50]}...")
            print(f"      Hook: {spicy_angle['hook']}")
            print(f"      Type: {spicy_angle['type']}")

        print("\n" + "="*100)

        return output


def main():
    import sys

    generator = ContrarianAngleGenerator()

    if len(sys.argv) > 1 and sys.argv[1] == 'batch':
        # Load ideas from RSS scout
        ideas_file = generator.agents_dir / 'rss_ideas_database.json'
        research_file = generator.agents_dir / 'research_results_quick.json'

        if not ideas_file.exists():
            print("❌ No ideas file found. Run RSS Content Scout first.")
            return

        with open(ideas_file, 'r') as f:
            ideas_data = json.load(f)

        ideas = ideas_data.get('ideas', [])[:10]

        # Load research if available
        research_data = None
        if research_file.exists():
            with open(research_file, 'r') as f:
                research_data = json.load(f)

        generator.batch_generate(ideas, research_data)

    elif len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Contrarian Angle Generator

Usage:
  python3 contrarian_angle_generator.py batch    # Generate angles for RSS ideas

Generates:
  • Professional angles (data-driven, educational)
  • Spicy/Contrarian angles (provocative, challenging)
  • Balanced angles (credible + edge)

Frameworks used:
  1. Inversion - Challenge common beliefs
  2. Scale Surprise - Show compound effects
  3. Time Shift - Then vs now comparison
  4. Hidden Cost - Real cost analysis
  5. Paradox - Counterintuitive truths

Examples of spicy angles:
  • "Everyone's doing X wrong"
  • "That $50/month tool is robbing you blind"
  • "The more tools you add, the less productive you become"

Webhook endpoint: /generate-angles
        """)
    else:
        print("Use --help for usage information")


if __name__ == "__main__":
    main()
