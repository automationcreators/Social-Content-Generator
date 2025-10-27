#!/usr/bin/env python3
"""
Collect real project data, statistics, and stories for social media content
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.agent_framework import BaseAgent
from scouts.content_extractor import ContentExtractor

class ProjectDataCollector(BaseAgent):
    """Collects real data from projects for authentic social media content"""

    def __init__(self):
        super().__init__(
            "project_data_collector",
            "Project Data Collector",
            "Collects real statistics, examples, and stories from projects"
        )
        self.active_dir = Path("/Users/elizabethknopf/Documents/claudec/active")
        self.content_extractor = ContentExtractor()

    def get_capabilities(self):
        """Return list of agent capabilities"""
        return ["project_analysis", "statistics_collection", "example_extraction"]

    def process_task(self, task):
        """Process a task request"""
        task_type = task.get("type", "collect_all")
        if task_type == "collect_all":
            return self.collect_all_project_data()
        return {"error": "Unknown task type"}

    def collect_all_project_data(self):
        """Collect comprehensive data from all projects"""
        all_data = {
            "collection_date": datetime.now().isoformat(),
            "projects": {},
            "aggregate_stats": {
                "total_projects": 0,
                "total_files": 0,
                "total_python_files": 0,
                "total_js_files": 0,
                "projects_with_agents": 0,
                "automation_tools": 0,
                "data_processing_tools": 0,
                "web_apps": 0
            },
            "interesting_findings": [],
            "stories": [],
            "workflows": [],
            "time_savings": [],
            "automation_examples": []
        }

        # Scan each project
        for project_dir in self.active_dir.iterdir():
            if not project_dir.is_dir() or project_dir.name.startswith('.'):
                continue

            project_data = self.analyze_project(project_dir)
            all_data["projects"][project_dir.name] = project_data
            all_data["aggregate_stats"]["total_projects"] += 1

        # Generate insights
        all_data["insights"] = self.generate_insights(all_data)
        all_data["real_examples"] = self.extract_real_examples(all_data)

        return all_data

    def analyze_project(self, project_dir):
        """Analyze a single project for interesting data"""
        data = {
            "name": project_dir.name,
            "path": str(project_dir),
            "file_count": 0,
            "file_types": {},
            "has_agents": False,
            "has_automation": False,
            "has_api": False,
            "has_dashboard": False,
            "tech_stack": [],
            "purpose": "",
            "interesting_files": [],
            "recent_activity": None,
            "estimated_complexity": "simple"
        }

        try:
            # Count files and analyze structure
            for file_path in project_dir.rglob("*"):
                if file_path.is_file() and not any(skip in str(file_path) for skip in ['node_modules', '.git', '__pycache__', 'venv']):
                    data["file_count"] += 1
                    ext = file_path.suffix.lower()
                    data["file_types"][ext] = data["file_types"].get(ext, 0) + 1

                    # Check for agent patterns
                    if 'agent' in file_path.name.lower():
                        data["has_agents"] = True
                        data["interesting_files"].append({
                            "file": file_path.name,
                            "type": "agent"
                        })

                    # Check for automation
                    if any(word in file_path.name.lower() for word in ['automation', 'scheduler', 'cron', 'background']):
                        data["has_automation"] = True
                        data["interesting_files"].append({
                            "file": file_path.name,
                            "type": "automation"
                        })

                    # Check for API
                    if 'api' in file_path.name.lower():
                        data["has_api"] = True

                    # Check for dashboard
                    if 'dashboard' in file_path.name.lower():
                        data["has_dashboard"] = True

            # Determine tech stack
            if '.py' in data["file_types"]:
                data["tech_stack"].append("Python")
            if any(ext in data["file_types"] for ext in ['.js', '.jsx', '.ts', '.tsx']):
                data["tech_stack"].append("JavaScript/React")
            if '.html' in data["file_types"]:
                data["tech_stack"].append("Web")

            # Estimate complexity
            if data["file_count"] > 100:
                data["estimated_complexity"] = "complex"
            elif data["file_count"] > 20:
                data["estimated_complexity"] = "moderate"

            # Extract rich content using ContentExtractor
            try:
                rich_content = self.content_extractor.extract_from_project(project_dir)
                data["rich_content"] = rich_content

                # Get purpose from README or first insight
                readme_path = project_dir / "README.md"
                if readme_path.exists():
                    try:
                        with open(readme_path, 'r') as f:
                            first_line = f.readline().strip()
                            data["purpose"] = first_line.replace('#', '').strip() if first_line else ""
                    except:
                        pass

                # Use insights as alternative purpose
                if not data["purpose"] and rich_content.get("insights"):
                    data["purpose"] = rich_content["insights"][0][:100]
            except Exception as extract_error:
                data["rich_content"] = {
                    "insights": [],
                    "guides": [],
                    "tips": [],
                    "stories": [],
                    "problems_solved": [],
                    "tech_stack": [],
                    "business_impact": []
                }
                data["extract_error"] = str(extract_error)

        except Exception as e:
            data["error"] = str(e)

        return data

    def generate_insights(self, all_data):
        """Generate insights from collected data"""
        insights = []

        projects = all_data["projects"]

        # Calculate totals
        total_files = sum(p["file_count"] for p in projects.values())
        agent_projects = [p for p in projects.values() if p["has_agents"]]
        automation_projects = [p for p in projects.values() if p["has_automation"]]
        dashboard_projects = [p for p in projects.values() if p["has_dashboard"]]

        insights.append({
            "type": "scale",
            "title": "Building at Scale",
            "stat": f"{len(projects)} active projects",
            "detail": f"Managing {total_files:,} files across diverse projects",
            "hook": f"How I manage {len(projects)} projects simultaneously with Claude Code"
        })

        if agent_projects:
            insights.append({
                "type": "automation",
                "title": "Agent-Driven Architecture",
                "stat": f"{len(agent_projects)} projects with autonomous agents",
                "detail": f"Built {sum(len([f for f in p.get('interesting_files', []) if f.get('type') == 'agent']) for p in agent_projects)} custom agents",
                "examples": [p["name"] for p in agent_projects[:3]],
                "hook": "Why I replaced scripts with autonomous agents"
            })

        if automation_projects:
            insights.append({
                "type": "automation",
                "title": "Automation Infrastructure",
                "stat": f"{len(automation_projects)} automated workflows",
                "detail": "Schedulers, background tasks, and automated processing",
                "examples": [p["name"] for p in automation_projects[:3]],
                "hook": "The automation stack that saves me 20 hours/week"
            })

        if dashboard_projects:
            insights.append({
                "type": "data_viz",
                "title": "Data Visualization",
                "stat": f"{len(dashboard_projects)} custom dashboards",
                "detail": "Real-time monitoring and business intelligence",
                "examples": [p["name"] for p in dashboard_projects[:3]],
                "hook": "Building custom dashboards without hiring a dev team"
            })

        # Tech stack diversity
        all_tech = set()
        for p in projects.values():
            all_tech.update(p["tech_stack"])

        insights.append({
            "type": "versatility",
            "title": "Multi-Stack Development",
            "stat": f"{len(all_tech)} technology stacks",
            "detail": f"Working across {', '.join(all_tech)}",
            "hook": "How Claude Code lets me code in any language"
        })

        return insights

    def extract_real_examples(self, all_data):
        """Extract concrete, real examples for content using rich content from projects"""
        examples = []

        projects = all_data["projects"]

        # Extract examples from all projects with rich content
        for project_name, project_data in projects.items():
            rich_content = project_data.get("rich_content", {})

            # Skip projects with no rich content or errors
            if not rich_content or project_data.get("extract_error"):
                continue

            # Extract from stories
            for story in rich_content.get("stories", [])[:2]:  # Max 2 stories per project
                if isinstance(story, dict):
                    examples.append({
                        "project": project_name,
                        "title": project_data.get("purpose", project_name)[:60],
                        "use_case": story.get("type", "project_story"),
                        "description": story.get("content", "")[:300] if isinstance(story.get("content"), str) else str(story)[:300],
                        "tech": ", ".join(project_data["tech_stack"]),
                        "category": "stories",
                        "business_value": "See description"
                    })

            # Extract from problem-solution pairs
            for problem in rich_content.get("problems_solved", [])[:2]:  # Max 2 problems per project
                if isinstance(problem, dict):
                    examples.append({
                        "project": project_name,
                        "title": f"{project_name} - Problem Solved",
                        "use_case": "Problem-Solution",
                        "description": f"Problem: {problem.get('problem', '')[:150]}\nSolution: {problem.get('solution', '')[:150]}",
                        "tech": ", ".join(project_data["tech_stack"]),
                        "category": "problem_solving",
                        "business_value": "Problem solved efficiently"
                    })

            # Extract from business impact
            for impact in rich_content.get("business_impact", [])[:2]:  # Max 2 impacts per project
                if isinstance(impact, dict):
                    examples.append({
                        "project": project_name,
                        "title": f"{project_name} - {impact.get('metric', 'Impact')}",
                        "use_case": "Business Impact",
                        "description": f"Achieved: {impact.get('metric', '')}",
                        "tech": ", ".join(project_data["tech_stack"]),
                        "category": "business_results",
                        "business_value": impact.get('value', 'Measurable impact')
                    })

            # Extract from guides (show how-to)
            for guide in rich_content.get("guides", [])[:1]:  # Max 1 guide per project
                if isinstance(guide, dict):
                    examples.append({
                        "project": project_name,
                        "title": f"How to: {project_name}",
                        "use_case": guide.get("type", "guide"),
                        "description": guide.get("content", "")[:300] if isinstance(guide.get("content"), str) else str(guide)[:300],
                        "tech": ", ".join(project_data["tech_stack"]),
                        "category": "how_to_guides",
                        "business_value": "Step-by-step implementation"
                    })

        # If no examples extracted from rich content, fall back to basic project info
        if not examples:
            for project_name, project_data in list(projects.items())[:5]:  # Top 5 projects
                if project_data.get("file_count", 0) > 5:  # Only non-trivial projects
                    examples.append({
                        "project": project_name,
                        "title": project_data.get("purpose", project_name)[:60],
                        "use_case": "Automation project",
                        "description": f"Built with {project_data['file_count']} files using {', '.join(project_data['tech_stack'])}",
                        "tech": ", ".join(project_data["tech_stack"]),
                        "category": "project_overview",
                        "business_value": "Custom automation solution"
                    })

        return examples[:15]  # Limit to 15 examples total

def main():
    collector = ProjectDataCollector()
    data = collector.collect_all_project_data()

    # Save to file
    output_file = Path(__file__).parent / "project_data_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print("=" * 80)
    print("PROJECT DATA COLLECTION COMPLETE")
    print("=" * 80)
    print(f"\n📊 Total Projects Analyzed: {data['aggregate_stats']['total_projects']}")
    print(f"📁 Total Files: {sum(p['file_count'] for p in data['projects'].values()):,}")

    print("\n\n🔍 KEY INSIGHTS:")
    print("=" * 80)
    for insight in data["insights"]:
        print(f"\n💡 {insight['title']}")
        print(f"   📈 {insight['stat']}")
        print(f"   📝 {insight['detail']}")
        print(f"   🎯 Hook: \"{insight['hook']}\"")
        if 'examples' in insight:
            print(f"   📂 Examples: {', '.join(insight['examples'])}")

    print("\n\n🎬 REAL EXAMPLES FOR CONTENT:")
    print("=" * 80)
    for i, example in enumerate(data["real_examples"][:10], 1):  # Show first 10
        print(f"\n{i}. {example['title']} ({example['project']})")
        print(f"   Use Case: {example['use_case']}")
        print(f"   Description: {example['description'][:150]}...")
        print(f"   Business Value: {example['business_value']}")
        print(f"   Category: {example['category']}")

    print(f"\n   ... and {len(data['real_examples']) - 10} more examples" if len(data["real_examples"]) > 10 else "")

    # Show rich content statistics
    print("\n\n📚 RICH CONTENT EXTRACTED:")
    print("=" * 80)
    total_insights = sum(len(p.get("rich_content", {}).get("insights", [])) for p in data["projects"].values())
    total_guides = sum(len(p.get("rich_content", {}).get("guides", [])) for p in data["projects"].values())
    total_tips = sum(len(p.get("rich_content", {}).get("tips", [])) for p in data["projects"].values())
    total_stories = sum(len(p.get("rich_content", {}).get("stories", [])) for p in data["projects"].values())
    total_problems = sum(len(p.get("rich_content", {}).get("problems_solved", [])) for p in data["projects"].values())

    print(f"💡 {total_insights} Insights")
    print(f"📖 {total_guides} Guides")
    print(f"💎 {total_tips} Tips")
    print(f"📚 {total_stories} Stories")
    print(f"🔧 {total_problems} Problems Solved")

    print(f"\n\n✅ Full data saved to: {output_file}")
    return data

if __name__ == "__main__":
    main()
