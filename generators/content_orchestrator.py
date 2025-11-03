#!/usr/bin/env python3
"""
Content Orchestrator
Coordinates all content generation agents:
- RSS Content Scout
- Research Data Agent
- Contrarian Angle Generator
- Personal Project Data
- Kallaway Frameworks

Outputs final content ready for Google Sheets
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class ContentOrchestrator:
    """Orchestrate multi-agent content generation pipeline"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent

        # Agent scripts
        self.rss_scout = self.agents_dir.parent / 'scouts' / 'rss_content_scout.py'
        self.research_agent = self.agents_dir.parent / 'research' / 'research_data_agent.py'
        self.angle_generator = self.agents_dir / 'contrarian_angle_generator.py'

        # Data files
        self.pillar_content = self.agents_dir.parent / 'config' / 'pillar_content_library.json'
        self.project_data = self.agents_dir.parent / 'config' / 'project_data_analysis.json'
        self.frameworks_file = self.agents_dir / 'content_frameworks' / 'kallaway_hooks.json'

        # Output files from agents
        self.rss_ideas_file = self.agents_dir.parent / 'scouts' / 'rss_ideas_database.json'
        self.research_file = self.agents_dir.parent / 'data' / 'research_results_quick.json'
        self.angles_file = self.agents_dir.parent / 'data' / 'contrarian_angles.json'

    def run_pipeline(self, mode='balanced', auto_approve=True):
        """
        Run complete content generation pipeline

        Args:
            mode: 'professional', 'spicy', or 'balanced'
            auto_approve: Auto-approve content with high confidence scores
        """

        print("\n" + "="*100)
        print("🎬 CONTENT ORCHESTRATOR - STARTING PIPELINE")
        print("="*100)

        print(f"\n⚙️  Configuration:")
        print(f"   Mode: {mode}")
        print(f"   Auto-approve: {auto_approve}")

        # Step 1: Run RSS Content Scout (skip if fresh data exists)
        print("\n" + "-"*100)
        print("📡 STEP 1: Scanning RSS Feeds")
        print("-"*100)

        # Check if RSS data already exists and is recent (within 1 hour)
        rss_data_fresh = False
        if self.rss_ideas_file.exists():
            try:
                from datetime import datetime as dt
                mod_time = dt.fromtimestamp(self.rss_ideas_file.stat().st_mtime)
                age = dt.now() - mod_time
                if age.total_seconds() < 3600:  # Less than 1 hour old
                    with open(self.rss_ideas_file, 'r') as f:
                        data = json.load(f)
                        if data.get('ideas') and len(data['ideas']) > 0:
                            rss_data_fresh = True
                            print(f"   ✅ Using existing RSS data ({len(data['ideas'])} ideas, {int(age.total_seconds()/60)} minutes old)")
            except Exception as e:
                print(f"   ⚠️  Could not check RSS data freshness: {e}")

        if not rss_data_fresh:
            self._run_agent('rss_scout', ['scan', '30', '10'])

        # Step 2: Run Research Agent
        print("\n" + "-"*100)
        print("📚 STEP 2: Researching Data")
        print("-"*100)

        self._run_agent('research', ['batch', 'quick'])

        # Step 3: Run Angle Generator
        print("\n" + "-"*100)
        print("🎭 STEP 3: Generating Angles")
        print("-"*100)

        self._run_agent('angles', ['batch'])

        # Step 4: Load all data
        print("\n" + "-"*100)
        print("📥 STEP 4: Loading All Data")
        print("-"*100)

        data = self._load_all_data()

        # Step 5: Create fusion content
        print("\n" + "-"*100)
        print("🔗 STEP 5: Creating Fusion Content")
        print("-"*100)

        fusion_content = self._create_fusion_content(data, mode)

        # Step 6: Score and rank
        print("\n" + "-"*100)
        print("🎯 STEP 6: Scoring Content")
        print("-"*100)

        scored_content = self._score_content(fusion_content, auto_approve)

        # Step 7: Format for output
        print("\n" + "-"*100)
        print("📤 STEP 7: Formatting Output")
        print("-"*100)

        final_output = self._format_final_output(scored_content, mode, auto_approve)

        # Save output
        output_file = self.agents_dir / 'final_content_output.json'
        with open(output_file, 'w') as f:
            json.dump(final_output, f, indent=2)

        # Print summary
        self._print_summary(final_output)

        print(f"\n✅ Pipeline complete! Output saved to: {output_file}")

        return final_output

    def _run_agent(self, agent_name, args):
        """Run an agent script"""

        agent_map = {
            'rss_scout': self.rss_scout,
            'research': self.research_agent,
            'angles': self.angle_generator
        }

        script = agent_map.get(agent_name)

        if not script.exists():
            print(f"⚠️  Agent script not found: {script}")
            return

        cmd = ['python3', str(script)] + args
        subprocess.run(cmd, cwd=self.agents_dir)

    def _load_all_data(self) -> Dict:
        """Load data from all sources"""

        data = {}

        # RSS ideas
        if self.rss_ideas_file.exists():
            with open(self.rss_ideas_file, 'r') as f:
                data['rss_ideas'] = json.load(f)
            print(f"   ✅ Loaded {len(data['rss_ideas'].get('ideas', []))} RSS ideas")

        # Research results
        if self.research_file.exists():
            with open(self.research_file, 'r') as f:
                data['research'] = json.load(f)
            print(f"   ✅ Loaded research for {len(data['research'].get('results', []))} ideas")

        # Contrarian angles
        if self.angles_file.exists():
            with open(self.angles_file, 'r') as f:
                data['angles'] = json.load(f)
            print(f"   ✅ Loaded {len(data['angles'].get('angles', []))} angle sets")

        # Personal pillars
        if self.pillar_content.exists():
            with open(self.pillar_content, 'r') as f:
                data['pillars'] = json.load(f)
            print(f"   ✅ Loaded {len(data['pillars'].get('pillars', []))} personal pillars")

        # Project data
        if self.project_data.exists():
            with open(self.project_data, 'r') as f:
                data['projects'] = json.load(f)
            print(f"   ✅ Loaded project data")

        return data

    def _create_fusion_content(self, data: Dict, mode: str) -> List[Dict]:
        """
        Create fusion content combining:
        - Trending RSS ideas
        - Personal project examples
        - Research data
        - Contrarian angles
        """

        fusion_pieces = []

        rss_ideas = data.get('rss_ideas', {}).get('ideas', [])
        angles_data = data.get('angles', {}).get('angles', [])
        research_data = data.get('research', {}).get('results', [])
        pillars = data.get('pillars', {}).get('pillars', [])

        print(f"\n   🔗 Creating fusion content from:")
        print(f"      • {len(rss_ideas)} trending ideas")
        print(f"      • {len(pillars)} personal pillars")
        print(f"      • {len(angles_data)} angle variations")

        # For each RSS idea, create fusion with personal content
        for piece_index, rss_idea in enumerate(rss_ideas):
            # Find matching angles
            angles = None
            for a in angles_data:
                if a.get('idea_id') == rss_idea.get('id'):
                    angles = a
                    break

            # Find matching research
            research = None
            for r in research_data:
                if r.get('idea_id') == rss_idea.get('id'):
                    research = r.get('research')
                    break

            # Determine fusion potential
            fusion_level = rss_idea.get('fusion_potential', 'low')

            if fusion_level in ['high', 'medium']:
                # Find related personal pillar
                related_pillar = self._find_related_pillar(rss_idea, pillars)

                # Create fusion piece with piece_index for rotation
                fusion = self._build_fusion_piece(
                    rss_idea=rss_idea,
                    angles=angles,
                    research=research,
                    pillar=related_pillar,
                    mode=mode,
                    piece_index=piece_index  # Add index for variation
                )

                fusion_pieces.append(fusion)

        print(f"\n   ✅ Created {len(fusion_pieces)} fusion content pieces")

        return fusion_pieces

    def _find_related_pillar(self, rss_idea: Dict, pillars: List[Dict]) -> Optional[Dict]:
        """Find personal pillar related to RSS idea - with rotation"""

        # Simple keyword matching for now
        rss_title = rss_idea.get('title', '').lower()

        keywords = ['automation', 'workflow', 'tool', 'productivity', 'ai agent']

        # Try to match by keywords
        for pillar in pillars:
            pillar_title = pillar.get('idea', {}).get('title', '').lower()

            # Check for keyword overlap
            for keyword in keywords:
                if keyword in rss_title and keyword in pillar_title:
                    return pillar

        # Rotate through pillars instead of always using first one
        # Use hash of title to get consistent but varied selection
        pillar_index = hash(rss_title) % len(pillars) if pillars else 0
        return pillars[pillar_index] if pillars else None

    def _build_fusion_piece(self, rss_idea: Dict, angles: Dict, research: Dict, pillar: Dict, mode: str, piece_index: int = 0) -> Dict:
        """Build a complete fusion content piece with variation"""

        # Select angle based on mode
        if mode == 'professional':
            selected_angles = angles.get('professional', {}).get('angles', []) if angles else []
        elif mode == 'spicy':
            selected_angles = angles.get('spicy', {}).get('angles', []) if angles else []
        else:  # balanced
            selected_angles = angles.get('balanced', {}).get('angles', []) if angles else []

        # Rotate through angles for variety (not always the same 2)
        if len(selected_angles) >= 2:
            start_idx = (piece_index * 2) % len(selected_angles)
            angle_pair = [
                selected_angles[start_idx % len(selected_angles)],
                selected_angles[(start_idx + 1) % len(selected_angles)]
            ]
        else:
            angle_pair = selected_angles[:2]

        # Get statistics and rotate them
        stats = research.get('statistics', []) if research else []
        if len(stats) >= 3:
            stat_start = piece_index % len(stats)
            rotated_stats = [
                stats[stat_start % len(stats)],
                stats[(stat_start + 1) % len(stats)],
                stats[(stat_start + 2) % len(stats)]
            ]
        else:
            rotated_stats = stats[:3]

        # Build fusion piece
        fusion = {
            'type': 'fusion',
            'trend_source': {
                'title': rss_idea.get('title'),
                'source': rss_idea.get('source'),
                'url': rss_idea.get('url'),
                'opportunity_type': rss_idea.get('opportunity_type')
            },
            'personal_example': None,
            'angles': angle_pair,  # Now rotates per piece
            'statistics': rotated_stats if rotated_stats else [],  # Rotates per piece
            'framework': rss_idea.get('suggested_framework', 'benefit_driven'),
            'platforms': rss_idea.get('suggested_platforms', ['LinkedIn', 'Twitter']),
            'fusion_strength': self._calculate_fusion_strength(rss_idea, pillar),
            'variation_style': self._get_variation_style(rss_idea)  # Story vs How-to
        }

        # Add personal example if pillar exists - with rotation
        if pillar:
            examples = pillar.get('real_data', {}).get('examples', [])

            # Rotate which examples to use based on opportunity type
            opp_type = rss_idea.get('opportunity_type', 'educational')

            if opp_type == 'tutorial':
                # For tutorials, use 1 example in detail
                fusion['personal_example'] = {
                    'title': pillar.get('idea', {}).get('title'),
                    'category': pillar.get('idea', {}).get('category'),
                    'examples': examples[:1] if examples else [],  # Just 1 example
                    'format': 'how_to'
                }
            elif opp_type in ['case_study', 'productivity']:
                # For case studies, use story format
                fusion['personal_example'] = {
                    'title': pillar.get('idea', {}).get('title'),
                    'category': pillar.get('idea', {}).get('category'),
                    'examples': examples[:1] if examples else [],  # Just 1 example
                    'format': 'story'
                }
            else:
                # For others, use 2 examples
                fusion['personal_example'] = {
                    'title': pillar.get('idea', {}).get('title'),
                    'category': pillar.get('idea', {}).get('category'),
                    'examples': examples[:2] if examples else [],
                    'format': 'standard'
                }

        return fusion

    def _get_variation_style(self, rss_idea: Dict) -> str:
        """Determine variation style based on opportunity type"""
        opp_type = rss_idea.get('opportunity_type', 'educational')

        style_map = {
            'tutorial': 'how_to_guide',
            'case_study': 'story_narrative',
            'comparison': 'analytical',
            'tool_review': 'practical_demo',
            'productivity': 'transformation_story',
            'trend': 'insight_analysis'
        }

        return style_map.get(opp_type, 'standard')

    def _calculate_fusion_strength(self, rss_idea: Dict, pillar: Dict) -> str:
        """Calculate how strong the fusion is between trend and personal content"""

        if not pillar:
            return 'standalone'

        fusion_potential = rss_idea.get('fusion_potential', 'low')

        if fusion_potential == 'high':
            return 'strong'
        elif fusion_potential == 'medium':
            return 'moderate'
        else:
            return 'weak'

    def _score_content(self, fusion_pieces: List[Dict], auto_approve: bool) -> List[Dict]:
        """Score content pieces for quality and confidence"""

        print(f"\n   🎯 Scoring {len(fusion_pieces)} content pieces...")

        for piece in fusion_pieces:
            score = self._calculate_content_score(piece)
            piece['quality_score'] = score

            # Determine if auto-approved
            if auto_approve:
                piece['auto_approved'] = score['total'] >= 70
                piece['requires_review'] = score['total'] < 70
            else:
                piece['auto_approved'] = False
                piece['requires_review'] = True

        # Sort by total score
        fusion_pieces.sort(key=lambda x: x['quality_score']['total'], reverse=True)

        return fusion_pieces

    def _calculate_content_score(self, piece: Dict) -> Dict:
        """Calculate quality score for content piece"""

        # Components: fusion_strength, data_quality, angle_quality, platform_fit
        scores = {
            'fusion_strength': 0,
            'data_quality': 0,
            'angle_quality': 0,
            'platform_fit': 0,
            'total': 0
        }

        # Fusion strength (0-30)
        fusion_map = {'strong': 30, 'moderate': 20, 'weak': 10, 'standalone': 5}
        scores['fusion_strength'] = fusion_map.get(piece.get('fusion_strength', 'weak'), 10)

        # Data quality (0-30) - based on statistics count and credibility
        stats = piece.get('statistics', [])
        if stats:
            avg_credibility = sum(s.get('credibility', 5) for s in stats) / len(stats)
            scores['data_quality'] = min(30, len(stats) * 5 + avg_credibility)

        # Angle quality (0-25) - based on number and variety
        angles = piece.get('angles', [])
        scores['angle_quality'] = min(25, len(angles) * 12.5)

        # Platform fit (0-15) - based on platform count
        platforms = piece.get('platforms', [])
        scores['platform_fit'] = min(15, len(platforms) * 5)

        # Total
        scores['total'] = round(sum([
            scores['fusion_strength'],
            scores['data_quality'],
            scores['angle_quality'],
            scores['platform_fit']
        ]))

        return scores

    def _format_final_output(self, scored_content: List[Dict], mode: str, auto_approve: bool) -> Dict:
        """Format final output for Google Sheets integration"""

        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'mode': mode,
                'auto_approve_enabled': auto_approve,
                'total_pieces': len(scored_content),
                'auto_approved': sum(1 for p in scored_content if p.get('auto_approved', False)),
                'requires_review': sum(1 for p in scored_content if p.get('requires_review', True))
            },
            'content_ready_for_sheets': scored_content,
            'sheet_columns': [
                'Title',
                'Trend Source',
                'Personal Example',
                'Hook Option 1',
                'Hook Option 2',
                'Stat 1',
                'Stat 2',
                'Stat 3',
                'Framework',
                'Platforms',
                'Fusion Strength',
                'Quality Score',
                'Auto Approved',
                'Status'
            ]
        }

    def _print_summary(self, output: Dict):
        """Print pipeline summary"""

        print("\n" + "="*100)
        print("📊 PIPELINE SUMMARY")
        print("="*100)

        metadata = output['metadata']

        print(f"\n🎯 Content Generated:")
        print(f"   Total pieces: {metadata['total_pieces']}")
        print(f"   Auto-approved: {metadata['auto_approved']}")
        print(f"   Requires review: {metadata['requires_review']}")

        print(f"\n🔥 Top 5 Content Pieces:")

        for i, piece in enumerate(output['content_ready_for_sheets'][:5], 1):
            print(f"\n   {i}. {piece['trend_source']['title'][:60]}...")
            print(f"      Quality Score: {piece['quality_score']['total']}/100")
            print(f"      Fusion: {piece['fusion_strength']}")
            print(f"      Platforms: {', '.join(piece['platforms'])}")
            print(f"      Auto-approved: {'✅' if piece.get('auto_approved') else '❌'}")

        print("\n" + "="*100)


def main():
    import sys

    orchestrator = ContentOrchestrator()

    mode = 'balanced'
    auto_approve = True

    if len(sys.argv) > 1:
        if sys.argv[1] == '--mode':
            mode = sys.argv[2] if len(sys.argv) > 2 else 'balanced'
        elif sys.argv[1] == '--no-auto-approve':
            auto_approve = False
        elif sys.argv[1] == '--help':
            print("""
Content Orchestrator

Usage:
  python3 content_orchestrator.py                           # Run with defaults (balanced, auto-approve)
  python3 content_orchestrator.py --mode [mode]             # Specify mode
  python3 content_orchestrator.py --no-auto-approve         # Disable auto-approval

Modes:
  professional - Data-driven, educational tone
  spicy        - Contrarian, provocative angles
  balanced     - Mix of credibility + edge (recommended)

Pipeline Steps:
  1. Scan RSS feeds (AI/business focus)
  2. Research supporting data
  3. Generate angle variations
  4. Load personal project data
  5. Create fusion content (trends + personal)
  6. Score and rank content
  7. Format for Google Sheets

Output:
  • final_content_output.json - Ready for Google Sheets
  • Auto-approved content (score >= 70)
  • Content requiring review (score < 70)

Daily Usage:
  Run once per day to generate 1-2 posts per channel
            """)
            return

    orchestrator.run_pipeline(mode=mode, auto_approve=auto_approve)


if __name__ == "__main__":
    main()
