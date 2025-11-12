#!/usr/bin/env python3
"""
Visual Prompt Generator for B-Roll and Shot Planning
Extracts visual markers from scripts and generates AI prompts for different tools
"""

import json
import re
from pathlib import Path
from datetime import datetime

class VisualPromptGenerator:
    """Generate B-roll prompts from script visual markers"""

    def __init__(self):
        self.scripts_dir = Path(__file__).parent.parent / 'pillar_scripts'
        self.output_dir = Path(__file__).parent.parent / 'visual_prompts'
        self.output_dir.mkdir(exist_ok=True)

    def parse_script(self, script_path):
        """Extract visual markers and metadata from a script"""
        with open(script_path, 'r') as f:
            content = f.read()

        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else script_path.stem

        # Extract metadata
        variation_match = re.search(r'\*\*Variation:\*\* (.+)$', content, re.MULTILINE)
        variation = variation_match.group(1) if variation_match else 'Unknown'

        # Extract visual markers with their sections
        visuals = []
        current_section = None
        current_timestamp = None

        # Split into lines for processing
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Track current section
            section_match = re.match(r'^## (.+) \((\d+:\d+) - (\d+:\d+)\)', line)
            if section_match:
                current_section = section_match.group(1)
                current_timestamp = f"{section_match.group(2)}-{section_match.group(3)}"

            # Extract visual markers
            visual_match = re.search(r'\*\*\[VISUAL: (.+?)\]\*\*', line)
            if visual_match:
                visual_desc = visual_match.group(1)

                # Get surrounding context (previous 2 lines for context)
                context_lines = []
                for j in range(max(0, i-2), i):
                    context_line = lines[j].strip()
                    if context_line and not context_line.startswith('#') and not context_line.startswith('**[VISUAL'):
                        context_lines.append(context_line)

                context = ' '.join(context_lines[-2:]) if context_lines else ''

                visuals.append({
                    'section': current_section or 'Unknown',
                    'timestamp': current_timestamp or '0:00-0:00',
                    'description': visual_desc,
                    'context': context
                })

        return {
            'title': title,
            'variation': variation,
            'script_file': script_path.name,
            'total_visuals': len(visuals),
            'visuals': visuals
        }

    def generate_runway_prompt(self, visual, context):
        """Generate Runway Gen-4 prompt (cinematic, high-quality)"""
        base_desc = visual['description']

        # Runway excels at: Cinematic quality, smooth motion, realistic lighting
        prompt_variations = {
            'data_viz': f"Professional data visualization: {base_desc}. Clean minimalist design, subtle animations, corporate aesthetic, 4K quality, smooth transitions",

            'dashboard': f"Sleek digital dashboard: {base_desc}. Modern UI, glowing elements, dark theme, cinematic lighting, shallow depth of field",

            'system': f"High-tech system visualization: {base_desc}. Futuristic interface, holographic elements, blue/purple color palette, cinematic camera movement",

            'comparison': f"Split-screen comparison: {base_desc}. Before/after dramatic reveal, cinematic lighting, professional color grading, smooth transition",

            'abstract': f"Abstract concept visualization: {base_desc}. Particle effects, fluid dynamics, volumetric lighting, cinematic composition",

            'default': f"Cinematic b-roll: {base_desc}. Professional lighting, smooth camera movement, 4K quality, color graded"
        }

        # Detect visual type
        desc_lower = base_desc.lower()
        if 'data' in desc_lower or 'chart' in desc_lower or 'graph' in desc_lower:
            prompt_type = 'data_viz'
        elif 'dashboard' in desc_lower or 'screen' in desc_lower:
            prompt_type = 'dashboard'
        elif 'system' in desc_lower or 'architecture' in desc_lower or 'diagram' in desc_lower:
            prompt_type = 'system'
        elif 'comparison' in desc_lower or 'before' in desc_lower or 'vs' in desc_lower:
            prompt_type = 'comparison'
        elif 'concept' in desc_lower or 'idea' in desc_lower or 'abstract' in desc_lower:
            prompt_type = 'abstract'
        else:
            prompt_type = 'default'

        return {
            'tool': 'Runway Gen-4',
            'prompt': prompt_variations[prompt_type],
            'duration': '10s',
            'settings': 'Gen-4 Turbo, 1080p, auto-camera movement',
            'cost_estimate': '$1.25'
        }

    def generate_kling_prompt(self, visual, context):
        """Generate Kling AI 2.0 prompt (photorealistic, dynamic motion)"""
        base_desc = visual['description']

        # Kling excels at: Photorealism, dynamic motion, complex scenes
        prompt_variations = {
            'data_viz': f"Photorealistic 3D data visualization: {base_desc}. Physical objects representing data, dynamic camera rotation, professional studio lighting",

            'dashboard': f"Realistic tech environment: {base_desc}. Modern office setting, actual screens displaying data, natural lighting, professional workspace",

            'system': f"Industrial tech setting: {base_desc}. Server room aesthetic, real hardware, blue LED lighting, cinematic dolly shot",

            'comparison': f"Side-by-side real-world comparison: {base_desc}. Two parallel scenes, synchronized motion, photorealistic details, smooth transition",

            'abstract': f"Physical representation of concept: {base_desc}. Tangible objects, natural physics, studio lighting, macro photography style",

            'default': f"Photorealistic scene: {base_desc}. Natural lighting, camera movement, high detail, cinematic framing"
        }

        # Detect visual type
        desc_lower = base_desc.lower()
        if 'data' in desc_lower or 'chart' in desc_lower or 'metric' in desc_lower:
            prompt_type = 'data_viz'
        elif 'dashboard' in desc_lower or 'screen' in desc_lower or 'interface' in desc_lower:
            prompt_type = 'dashboard'
        elif 'system' in desc_lower or 'architecture' in desc_lower or 'server' in desc_lower:
            prompt_type = 'system'
        elif 'comparison' in desc_lower or 'before' in desc_lower or 'vs' in desc_lower:
            prompt_type = 'comparison'
        elif 'concept' in desc_lower or 'idea' in desc_lower:
            prompt_type = 'abstract'
        else:
            prompt_type = 'default'

        return {
            'tool': 'Kling AI 2.0',
            'prompt': prompt_variations[prompt_type],
            'duration': '10s',
            'settings': 'Professional Mode, 1080p, dynamic camera',
            'cost_estimate': '$0.30'
        }

    def generate_pika_prompt(self, visual, context):
        """Generate Pika Labs 2.5 prompt (fast, social media style)"""
        base_desc = visual['description']

        # Pika excels at: Quick iterations, social media style, punchy visuals
        prompt_variations = {
            'data_viz': f"Bold data visualization: {base_desc}. High contrast colors, quick animations, social media ready, attention-grabbing",

            'dashboard': f"Modern app interface: {base_desc}. Vibrant colors, fast transitions, mobile-first design, eye-catching",

            'system': f"Tech visualization: {base_desc}. Neon accents, quick cuts, digital aesthetic, high energy",

            'comparison': f"Fast-paced comparison: {base_desc}. Quick reveal, bold typography, high contrast, social media optimized",

            'abstract': f"Stylized concept: {base_desc}. Bold colors, geometric shapes, fast motion, scroll-stopping visual",

            'default': f"Punchy b-roll: {base_desc}. High energy, vibrant colors, quick motion, social media optimized"
        }

        # Detect visual type
        desc_lower = base_desc.lower()
        if 'data' in desc_lower or 'stat' in desc_lower or 'number' in desc_lower:
            prompt_type = 'data_viz'
        elif 'dashboard' in desc_lower or 'app' in desc_lower or 'screen' in desc_lower:
            prompt_type = 'dashboard'
        elif 'system' in desc_lower or 'tech' in desc_lower:
            prompt_type = 'system'
        elif 'comparison' in desc_lower or 'vs' in desc_lower:
            prompt_type = 'comparison'
        elif 'concept' in desc_lower or 'idea' in desc_lower:
            prompt_type = 'abstract'
        else:
            prompt_type = 'default'

        return {
            'tool': 'Pika Labs 2.5',
            'prompt': prompt_variations[prompt_type],
            'duration': '5s',
            'settings': 'Fast mode, 1080p, dynamic motion',
            'cost_estimate': '$0.20'
        }

    def generate_real_shot_suggestion(self, visual, context):
        """Generate suggestions for real-life footage"""
        base_desc = visual['description']
        desc_lower = base_desc.lower()

        # Categorize by what works best with real footage
        if 'person' in desc_lower or 'presenter' in desc_lower or 'speaking' in desc_lower:
            return {
                'type': 'Real Footage - Required',
                'shot_type': 'Medium shot, talking head',
                'setup': 'Well-lit background, professional framing',
                'equipment': 'Camera/smartphone, lavalier mic, key + fill lighting',
                'duration': '5-10s',
                'notes': 'Essential for credibility and personal connection'
            }

        elif 'dashboard' in desc_lower or 'screen' in desc_lower or 'interface' in desc_lower:
            return {
                'type': 'Real Footage - Screen Recording',
                'shot_type': 'Screen capture with cursor movement',
                'setup': 'Clean desktop, relevant app/dashboard open',
                'equipment': 'Screen recording software (Descript, OBS)',
                'duration': '5-8s',
                'notes': 'Shows actual working system, builds trust'
            }

        elif 'workspace' in desc_lower or 'office' in desc_lower or 'desk' in desc_lower:
            return {
                'type': 'Real Footage - Environmental',
                'shot_type': 'Wide/establishing shot of workspace',
                'setup': 'Clean, organized workspace with tech elements',
                'equipment': 'Camera/smartphone, natural + practical lighting',
                'duration': '3-5s',
                'notes': 'Authentic, relatable, shows real work environment'
            }

        elif 'hands' in desc_lower or 'typing' in desc_lower or 'working' in desc_lower:
            return {
                'type': 'Real Footage - Detail Shot',
                'shot_type': 'Close-up of hands on keyboard/mouse',
                'setup': 'Clean desk surface, keyboard in focus',
                'equipment': 'Camera/smartphone macro mode, overhead angle',
                'duration': '3-5s',
                'notes': 'Shows action, engaging detail shot'
            }

        else:
            return {
                'type': 'AI Recommended',
                'shot_type': 'Better suited for AI generation',
                'setup': 'Use Runway/Kling for this visual',
                'equipment': 'N/A',
                'duration': '5-10s',
                'notes': f"Abstract concept '{base_desc}' works better with AI visualization"
            }

    def generate_heygen_suggestion(self, visual, context, variation):
        """Generate HeyGen avatar suggestions"""
        base_desc = visual['description']

        # HeyGen works best for presenter/talking head shots
        if 'speaking' in base_desc.lower() or 'presenter' in base_desc.lower():
            avatar_style = 'Professional'
        elif variation.lower() == 'authority':
            avatar_style = 'Executive/Expert'
        elif variation.lower() == 'contrarian':
            avatar_style = 'Confident/Direct'
        else:  # transformation
            avatar_style = 'Friendly/Approachable'

        return {
            'tool': 'HeyGen',
            'avatar_style': avatar_style,
            'script_text': context[:200] if context else 'To be scripted',
            'background': 'Modern office with subtle blur',
            'duration': '10-15s',
            'cost_estimate': '$0.50',
            'notes': 'Use for intro, key points, transitions'
        }

    def generate_all_prompts(self, visual, context, variation):
        """Generate all prompt types for a visual"""
        return {
            'visual_id': f"{visual['section']}_{visual['timestamp'].replace(':', '').replace('-', '_')}",
            'section': visual['section'],
            'timestamp': visual['timestamp'],
            'description': visual['description'],
            'context': context,
            'prompts': {
                'runway': self.generate_runway_prompt(visual, context),
                'kling': self.generate_kling_prompt(visual, context),
                'pika': self.generate_pika_prompt(visual, context),
                'real_footage': self.generate_real_shot_suggestion(visual, context),
                'heygen': self.generate_heygen_suggestion(visual, context, variation)
            },
            'recommended_approach': self.recommend_approach(visual, context)
        }

    def recommend_approach(self, visual, context):
        """Recommend best approach for this specific visual"""
        desc_lower = visual['description'].lower()

        # Real footage priorities
        if any(word in desc_lower for word in ['person', 'presenter', 'speaking', 'you']):
            return {
                'primary': 'Real Footage or HeyGen Avatar',
                'secondary': 'AI B-roll for backgrounds',
                'reasoning': 'Human presence builds credibility and connection'
            }

        # Screen recording priorities
        if any(word in desc_lower for word in ['dashboard', 'screen', 'interface', 'app', 'system']):
            return {
                'primary': 'Screen Recording (real)',
                'secondary': 'Kling for stylized version',
                'reasoning': 'Actual working systems demonstrate proof'
            }

        # Abstract concepts = AI
        if any(word in desc_lower for word in ['concept', 'idea', 'visualization', 'abstract', 'diagram']):
            return {
                'primary': 'Runway Gen-4',
                'secondary': 'Kling for alternate angle',
                'reasoning': 'AI excels at visualizing abstract concepts'
            }

        # Data visualizations
        if any(word in desc_lower for word in ['data', 'chart', 'graph', 'metric', 'stat']):
            return {
                'primary': 'Pika (fast iteration)',
                'secondary': 'Runway (if high-quality needed)',
                'reasoning': 'Quick social media-ready data viz'
            }

        # Default: Hybrid
        return {
            'primary': 'Kling AI (photorealistic)',
            'secondary': 'Real footage if easily filmable',
            'reasoning': 'Balanced approach for general B-roll'
        }

    def process_script(self, script_path):
        """Process a single script and generate all visual prompts"""
        print(f"\n📄 Processing: {script_path.name}")

        # Parse script
        script_data = self.parse_script(script_path)
        print(f"   Found {script_data['total_visuals']} visual markers")

        # Generate prompts for each visual
        visual_prompts = []
        total_cost_runway = 0
        total_cost_kling = 0
        total_cost_pika = 0
        total_cost_heygen = 0

        for visual in script_data['visuals']:
            prompt_data = self.generate_all_prompts(
                visual,
                visual['context'],
                script_data['variation']
            )
            visual_prompts.append(prompt_data)

            # Calculate costs
            total_cost_runway += float(prompt_data['prompts']['runway']['cost_estimate'].replace('$', ''))
            total_cost_kling += float(prompt_data['prompts']['kling']['cost_estimate'].replace('$', ''))
            total_cost_pika += float(prompt_data['prompts']['pika']['cost_estimate'].replace('$', ''))
            total_cost_heygen += float(prompt_data['prompts']['heygen']['cost_estimate'].replace('$', ''))

        # Compile output
        output = {
            'metadata': {
                'script_title': script_data['title'],
                'variation': script_data['variation'],
                'script_file': script_data['script_file'],
                'generated_date': datetime.now().isoformat(),
                'total_visuals': script_data['total_visuals']
            },
            'cost_estimates': {
                'runway_all_ai': f"${total_cost_runway:.2f}",
                'kling_all_ai': f"${total_cost_kling:.2f}",
                'pika_all_ai': f"${total_cost_pika:.2f}",
                'heygen_all': f"${total_cost_heygen:.2f}",
                'hybrid_recommended': f"${(total_cost_kling * 0.6 + total_cost_heygen * 0.2):.2f}"
            },
            'production_estimates': {
                'pure_ai_runway': f"{len(visual_prompts) * 2} minutes (+ render time)",
                'pure_ai_kling': f"{len(visual_prompts) * 1.5} minutes (+ render time)",
                'hybrid_approach': f"2-3 hours (filming + AI generation)",
                'heygen_avatar': f"1-2 hours (scripting + generation)"
            },
            'visual_prompts': visual_prompts
        }

        # Save to JSON
        output_file = self.output_dir / f"{script_path.stem}_visual_prompts.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"   ✅ Generated {len(visual_prompts)} visual prompt sets")
        print(f"   💰 Cost estimates: Runway ${total_cost_runway:.2f} | Kling ${total_cost_kling:.2f} | Pika ${total_cost_pika:.2f}")
        print(f"   📁 Saved: {output_file.name}")

        return output

    def process_all_scripts(self):
        """Process all scripts in pillar_scripts directory"""
        print("🎬 Visual Prompt Generator Starting...\n")

        # Find all markdown scripts
        script_files = list(self.scripts_dir.glob('*.md'))

        if not script_files:
            print("❌ No scripts found in pillar_scripts/")
            return

        print(f"📊 Found {len(script_files)} scripts to process\n")

        # Process each script
        results = []
        for script_file in sorted(script_files):
            try:
                result = self.process_script(script_file)
                results.append(result)
            except Exception as e:
                print(f"   ❌ Error processing {script_file.name}: {e}")

        # Generate summary report
        self.generate_summary_report(results)

        print(f"\n\n✅ Complete! Processed {len(results)}/{len(script_files)} scripts")
        print(f"📂 Visual prompts saved to: {self.output_dir}")

    def generate_summary_report(self, results):
        """Generate a summary report across all scripts"""
        if not results:
            return

        total_visuals = sum(r['metadata']['total_visuals'] for r in results)

        # Calculate average costs
        avg_runway = sum(float(r['cost_estimates']['runway_all_ai'].replace('$', '')) for r in results) / len(results)
        avg_kling = sum(float(r['cost_estimates']['kling_all_ai'].replace('$', '')) for r in results) / len(results)
        avg_pika = sum(float(r['cost_estimates']['pika_all_ai'].replace('$', '')) for r in results) / len(results)
        avg_heygen = sum(float(r['cost_estimates']['heygen_all'].replace('$', '')) for r in results) / len(results)

        summary = {
            'generated_date': datetime.now().isoformat(),
            'total_scripts_processed': len(results),
            'total_visual_moments': total_visuals,
            'average_visuals_per_script': total_visuals / len(results),
            'average_costs_per_script': {
                'runway_pure_ai': f"${avg_runway:.2f}",
                'kling_pure_ai': f"${avg_kling:.2f}",
                'pika_pure_ai': f"${avg_pika:.2f}",
                'heygen_pure_ai': f"${avg_heygen:.2f}",
                'hybrid_recommended': f"${(avg_kling * 0.6 + avg_heygen * 0.2):.2f}"
            },
            'total_costs_all_scripts': {
                'runway_approach': f"${avg_runway * len(results):.2f}",
                'kling_approach': f"${avg_kling * len(results):.2f}",
                'pika_approach': f"${avg_pika * len(results):.2f}",
                'hybrid_approach': f"${(avg_kling * 0.6 + avg_heygen * 0.2) * len(results):.2f}"
            },
            'recommended_workflow': {
                'approach': 'Hybrid: Kling AI (60%) + HeyGen Avatar (20%) + Real Footage (20%)',
                'total_cost': f"${(avg_kling * 0.6 + avg_heygen * 0.2) * len(results):.2f}",
                'production_time': f"{len(results) * 3}-{len(results) * 4} hours total",
                'reasoning': 'Best balance of cost, quality, and authenticity'
            },
            'scripts_breakdown': [
                {
                    'script': r['metadata']['script_file'],
                    'variation': r['metadata']['variation'],
                    'visuals': r['metadata']['total_visuals'],
                    'recommended_cost': r['cost_estimates']['hybrid_recommended']
                }
                for r in results
            ]
        }

        # Save summary
        summary_file = self.output_dir / '_SUMMARY_REPORT.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n\n📊 SUMMARY REPORT")
        print(f"   Total Scripts: {len(results)}")
        print(f"   Total Visual Moments: {total_visuals}")
        print(f"   Average per Script: {total_visuals / len(results):.1f} visuals")
        print(f"\n   💰 COST ESTIMATES (All {len(results)} Scripts):")
        print(f"   • Pure Runway: ${avg_runway * len(results):.2f}")
        print(f"   • Pure Kling: ${avg_kling * len(results):.2f}")
        print(f"   • Pure Pika: ${avg_pika * len(results):.2f}")
        print(f"   • Hybrid (Recommended): ${(avg_kling * 0.6 + avg_heygen * 0.2) * len(results):.2f}")
        print(f"\n   📁 Summary saved: {summary_file.name}")


def main():
    """Main execution"""
    generator = VisualPromptGenerator()
    generator.process_all_scripts()


if __name__ == '__main__':
    main()
