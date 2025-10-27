#!/usr/bin/env python3
"""
Daily Content Generator
One-command daily content generation workflow

Runs:
1. RSS Content Scout
2. Research Data Agent
3. Contrarian Angle Generator
4. Content Orchestrator
5. Google Sheets Sync
6. Pillar Content Generator (optional, default: enabled)

Usage:
    python3 daily_content_generator.py                    # Balanced mode (default) + pillar content
    python3 daily_content_generator.py --mode professional # Professional mode
    python3 daily_content_generator.py --mode spicy       # Spicy/contrarian mode
    python3 daily_content_generator.py --skip-pillar      # Skip pillar content generation
"""

import subprocess
from pathlib import Path
import sys

class DailyContentGenerator:
    """One-command daily content generation"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent

    def run_daily_workflow(self, mode='balanced', include_pillar=True):
        """Run complete daily content generation workflow"""

        print("\n" + "="*100)
        print("🚀 DAILY CONTENT GENERATOR")
        print("="*100)
        print(f"\nMode: {mode.upper()}")
        if include_pillar:
            print("Pillar Content: ENABLED")
        else:
            print("Pillar Content: SKIPPED")
        print("Running complete content pipeline...\n")

        # Step 1: Run orchestrator (which runs all agents)
        print("🎬 Running Content Orchestrator...")
        print("-"*100)

        subprocess.run([
            'python3',
            str(self.agents_dir / 'content_orchestrator.py'),
            '--mode', mode
        ], cwd=self.agents_dir)

        # Step 2: Sync to Google Sheets
        print("\n📊 Syncing to Google Sheets...")
        print("-"*100)

        subprocess.run([
            'python3',
            str(self.agents_dir / 'sync_to_google_sheets.py')
        ], cwd=self.agents_dir)

        # Step 3: Generate and sync pillar content (if enabled)
        if include_pillar:
            print("\n📚 Generating Pillar Content...")
            print("-"*100)

            subprocess.run([
                'python3',
                str(self.agents_dir / 'pillar_content_sync.py')
            ], cwd=self.agents_dir)

        print("\n" + "="*100)
        print("✅ DAILY WORKFLOW COMPLETE!")
        print("="*100)

        print("\n📊 Your content is ready in Google Sheets!")
        print("🎯 Daily content: 4 pieces generated")
        if include_pillar:
            print("🎯 Pillar content: 3 pieces generated")
        print("⏰ Estimated time to post: 1-2 posts per day across all platforms")

        print("\n💡 Schedule:")
        print("   • LinkedIn: 1 post/day (professional/balanced)")
        print("   • Twitter: 1-2 posts/day (mix of professional + spicy)")
        print("   • YouTube: 1 post/week (deep-dive tutorials)")
        print("   • Threads: 1 post/day (balanced/spicy)")
        if include_pillar:
            print("   • Long-form content: Use pillar content for YouTube/LinkedIn articles")

        print("\n🔄 Next run: Tomorrow at same time")


def main():
    generator = DailyContentGenerator()

    mode = 'balanced'
    include_pillar = True

    # Parse arguments
    if len(sys.argv) > 1:
        if '--mode' in sys.argv:
            mode_index = sys.argv.index('--mode') + 1
            if mode_index < len(sys.argv):
                mode = sys.argv[mode_index]
        if '--skip-pillar' in sys.argv:
            include_pillar = False
        if '--help' in sys.argv:
            print("""
Daily Content Generator

Runs complete content generation pipeline:
  1. Scans RSS feeds (AI/business focus)
  2. Researches supporting data
  3. Generates angle variations
  4. Creates fusion content (trends + personal projects)
  5. Syncs to Google Sheets
  6. Generates pillar content (long-form scripts/articles)

Usage:
  python3 daily_content_generator.py                    # Balanced mode (default) + pillar content
  python3 daily_content_generator.py --mode professional # Professional mode
  python3 daily_content_generator.py --mode spicy       # Spicy/contrarian mode
  python3 daily_content_generator.py --skip-pillar      # Skip pillar content generation

Modes:
  professional - Data-driven, educational, credible tone
  spicy        - Contrarian, provocative, memorable angles
  balanced     - Mix of credibility + edge (RECOMMENDED)

Output:
  • Content tab: 4 daily content pieces
  • Pillar Content tab: 3 long-form scripts/articles (with date column)
  • Auto-approved content (score >= 70)
  • Suggested platforms for each piece

Recommended Schedule:
  Run once per day, ideally morning
  Posts 1-2 pieces per platform daily
  Remixes ideas across different platforms

Automation:
  Add to cron: 0 9 * * * cd /path/to/agents && python3 daily_content_generator.py
            """)
            return

    generator.run_daily_workflow(mode=mode, include_pillar=include_pillar)


if __name__ == "__main__":
    main()
