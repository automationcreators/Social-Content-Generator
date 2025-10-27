#!/usr/bin/env python3
"""
Update Project Data for Pillar Content

Runs daily to scan active projects and update the project_data_analysis.json
used by the pillar content generator.
"""

import json
import sys
from pathlib import Path

# Add utils to path for agent_framework
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from project_data_collector import ProjectDataCollector

def main():
    print("\n" + "="*100)
    print("📊 PROJECT DATA COLLECTOR")
    print("="*100)

    print("\n🔍 Scanning active projects...")
    collector = ProjectDataCollector()

    # Collect all project data
    project_data = collector.collect_all_project_data()

    # Save to config directory
    config_dir = Path(__file__).parent.parent / 'config'
    output_file = config_dir / 'project_data_analysis.json'

    print(f"\n💾 Saving project data to: {output_file}")

    with open(output_file, 'w') as f:
        json.dump(project_data, f, indent=2)

    # Print summary
    print("\n" + "="*100)
    print("📊 PROJECT SCAN SUMMARY")
    print("="*100)

    stats = project_data['aggregate_stats']
    print(f"\n📁 Projects: {stats['total_projects']}")
    print(f"📄 Total files: {stats['total_files']}")
    print(f"🐍 Python files: {stats['total_python_files']}")
    print(f"📜 JS files: {stats['total_js_files']}")
    print(f"🤖 Projects with agents: {stats['projects_with_agents']}")
    print(f"⚙️  Automation tools: {stats['automation_tools']}")
    print(f"📊 Data processing tools: {stats['data_processing_tools']}")
    print(f"🌐 Web apps: {stats['web_apps']}")

    print(f"\n💡 Insights found: {len(project_data.get('insights', []))}")
    print(f"📝 Real examples: {len(project_data.get('real_examples', []))}")

    if project_data.get('insights'):
        print("\n🔍 Top Insights:")
        for insight in project_data['insights'][:5]:
            print(f"   • {insight.get('type', 'N/A')}: {insight.get('stat', 'N/A')}")

    print("\n" + "="*100)
    print("✅ PROJECT DATA UPDATED!")
    print("="*100)

    print(f"\n📊 This data will be used by the pillar content generator")
    print(f"   to create authentic content with real project examples.\n")

    return project_data


if __name__ == "__main__":
    main()
