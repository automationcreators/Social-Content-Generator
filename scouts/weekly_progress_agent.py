#!/usr/bin/env python3
"""
Weekly Progress Summary Agent - Tracks and summarizes weekly progress across all projects
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import argparse
import hashlib

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from utils.agent_framework import BaseAgent
from context_summary_agent import ContextSummaryAgent
from planning_analysis_agent import PlanningAnalysisAgent
from social_media_content_agent import SocialMediaContentAgent


class WeeklyProgressAgent(BaseAgent):
    """Agent for tracking and summarizing weekly progress"""
    
    def __init__(self):
        super().__init__(
            "weekly_progress_agent",
            "Weekly Progress Summary Agent",
            "Tracks and summarizes weekly progress across all projects and agents"
        )
        
        # Progress tracking configuration
        self.tracking_categories = {
            "code_development": {
                "weight": 0.3,
                "indicators": ["new files", "code changes", "commits"],
                "icon": "💻"
            },
            "project_setup": {
                "weight": 0.2,
                "indicators": ["new projects", "configuration", "templates"],
                "icon": "🔧"
            },
            "documentation": {
                "weight": 0.15,
                "indicators": ["markdown files", "README updates", "context files"],
                "icon": "📝"
            },
            "agent_development": {
                "weight": 0.25,
                "indicators": ["agent files", "automation", "intelligence"],
                "icon": "🤖"
            },
            "dashboard_features": {
                "weight": 0.1,
                "indicators": ["dashboard updates", "visualizations", "integrations"],
                "icon": "📊"
            }
        }
        
        # Progress storage
        self.progress_database_file = Path(__file__).parent / "weekly_progress_database.json"
        
        # Initialize other agents
        self.context_agent = ContextSummaryAgent()
        self.planning_agent = PlanningAnalysisAgent()
        self.content_agent = SocialMediaContentAgent()
        
        # Setup logging
        self.logger = logging.getLogger("weekly_progress")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(name)s (%(levelname)s): %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # Load progress database
        self.progress_database = self.load_progress_database()
        
        self.logger.info("Weekly Progress Agent initialized")
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return [
            "weekly_progress_tracking",
            "accomplishment_summarization",
            "project_portfolio_analysis",
            "productivity_metrics",
            "achievement_highlighting",
            "trend_analysis"
        ]
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task request"""
        task_type = task.get("type", "generate_summary")
        
        if task_type == "generate_summary":
            return self.generate_weekly_summary(
                task.get("week_offset", 0)
            )
        elif task_type == "track_progress":
            return self.track_current_progress()
        elif task_type == "analyze_trends":
            return self.analyze_productivity_trends(
                task.get("weeks_back", 4)
            )
        elif task_type == "get_accomplishments":
            return self.get_major_accomplishments(
                task.get("time_period", "week")
            )
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    def load_progress_database(self) -> Dict[str, Any]:
        """Load existing progress database"""
        if self.progress_database_file.exists():
            try:
                with open(self.progress_database_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading progress database: {e}")
        
        # Initialize empty database
        return {
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            },
            "weekly_summaries": {},
            "daily_progress": {},
            "milestones": [],
            "productivity_metrics": {}
        }
    
    def save_progress_database(self):
        """Save progress database to file"""
        self.progress_database["metadata"]["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.progress_database_file, 'w') as f:
                json.dump(self.progress_database, f, indent=2)
            self.logger.info(f"Progress database saved with {len(self.progress_database['weekly_summaries'])} weekly summaries")
        except Exception as e:
            self.logger.error(f"Error saving progress database: {e}")
    
    def generate_weekly_summary(self, week_offset: int = 0) -> Dict[str, Any]:
        """Generate comprehensive weekly progress summary"""
        # Calculate target week
        target_date = datetime.now() - timedelta(weeks=week_offset)
        week_start = target_date - timedelta(days=target_date.weekday())
        week_end = week_start + timedelta(days=6)
        
        week_key = week_start.strftime("%Y-W%U")
        
        self.logger.info(f"Generating weekly summary for week {week_key} ({week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')})")
        
        # Gather comprehensive progress data
        weekly_data = {
            "week_key": week_key,
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "generated_at": datetime.now().isoformat(),
            "summary_type": "comprehensive"
        }
        
        # Analyze project portfolio
        weekly_data["portfolio_analysis"] = self._analyze_portfolio_progress(week_start, week_end)
        
        # Analyze agent system development
        weekly_data["agent_development"] = self._analyze_agent_progress(week_start, week_end)
        
        # Track major accomplishments
        weekly_data["major_accomplishments"] = self._identify_major_accomplishments(week_start, week_end)
        
        # Calculate productivity metrics
        weekly_data["productivity_metrics"] = self._calculate_productivity_metrics(week_start, week_end)
        
        # Generate content and insights
        weekly_data["content_insights"] = self._analyze_content_generation(week_start, week_end)
        
        # Create executive summary
        weekly_data["executive_summary"] = self._generate_executive_summary(weekly_data)
        
        # Calculate overall progress score
        weekly_data["progress_score"] = self._calculate_weekly_progress_score(weekly_data)
        
        # Store in database
        self.progress_database["weekly_summaries"][week_key] = weekly_data
        self.save_progress_database()
        
        return weekly_data
    
    def _analyze_portfolio_progress(self, week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """Analyze progress across project portfolio"""
        active_dir = Path("/Users/elizabethknopf/Documents/claudec/active")
        project_paths = [str(p) for p in active_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]
        
        portfolio_analysis = {
            "total_projects": len(project_paths),
            "active_projects": 0,
            "new_projects": 0,
            "major_updates": [],
            "file_changes_summary": {},
            "localhost_improvements": 0
        }
        
        for project_path in project_paths:
            project_dir = Path(project_path)
            project_analysis = self._analyze_single_project_progress(project_dir, week_start, week_end)
            
            if project_analysis["has_activity"]:
                portfolio_analysis["active_projects"] += 1
                
                if project_analysis["is_new_project"]:
                    portfolio_analysis["new_projects"] += 1
                
                if project_analysis["major_changes"] > 10:
                    portfolio_analysis["major_updates"].append({
                        "project": project_dir.name,
                        "changes": project_analysis["major_changes"],
                        "highlights": project_analysis["highlights"]
                    })
                
                # Aggregate file changes
                for file_type, count in project_analysis["file_changes"].items():
                    portfolio_analysis["file_changes_summary"][file_type] = \
                        portfolio_analysis["file_changes_summary"].get(file_type, 0) + count
        
        return portfolio_analysis
    
    def _analyze_single_project_progress(self, project_dir: Path, week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """Analyze progress for a single project"""
        analysis = {
            "project_name": project_dir.name,
            "has_activity": False,
            "is_new_project": False,
            "major_changes": 0,
            "file_changes": {},
            "highlights": []
        }
        
        # Check if project was created this week
        try:
            creation_time = datetime.fromtimestamp(project_dir.stat().st_ctime)
            if week_start <= creation_time <= week_end:
                analysis["is_new_project"] = True
                analysis["has_activity"] = True
                analysis["highlights"].append("New project created")
        except:
            pass
        
        # Analyze file changes during the week
        file_changes = {}
        try:
            for file_path in project_dir.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if week_start <= mod_time <= week_end:
                        analysis["has_activity"] = True
                        ext = file_path.suffix or "no_extension"
                        file_changes[ext] = file_changes.get(ext, 0) + 1
                        analysis["major_changes"] += 1
        except Exception as e:
            self.logger.warning(f"Error analyzing {project_dir.name}: {e}")
        
        analysis["file_changes"] = file_changes
        
        # Check for specific achievements
        if analysis["has_activity"]:
            # Check for CLAUDE.md creation
            claude_file = project_dir / "CLAUDE.md"
            if claude_file.exists():
                try:
                    claude_mod_time = datetime.fromtimestamp(claude_file.stat().st_mtime)
                    if week_start <= claude_mod_time <= week_end:
                        analysis["highlights"].append("CLAUDE.md context file added")
                except:
                    pass
            
            # Check for agent development
            if any('agent' in str(f).lower() for f in project_dir.rglob("*.py")):
                analysis["highlights"].append("Agent development activity")
        
        return analysis
    
    def _analyze_agent_progress(self, week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """Analyze agent system development progress"""
        agents_dir = Path(__file__).parent
        
        agent_progress = {
            "new_agents": [],
            "agent_updates": [],
            "total_agent_files": 0,
            "new_capabilities": [],
            "system_improvements": []
        }
        
        # Find all agent files
        for agent_file in agents_dir.glob("*agent*.py"):
            try:
                mod_time = datetime.fromtimestamp(agent_file.stat().st_mtime)
                creation_time = datetime.fromtimestamp(agent_file.stat().st_ctime)
                
                agent_progress["total_agent_files"] += 1
                
                # Check if new agent created this week
                if week_start <= creation_time <= week_end:
                    agent_progress["new_agents"].append({
                        "name": agent_file.stem,
                        "created": creation_time.isoformat()
                    })
                
                # Check if agent updated this week
                elif week_start <= mod_time <= week_end:
                    agent_progress["agent_updates"].append({
                        "name": agent_file.stem,
                        "updated": mod_time.isoformat()
                    })
                
            except Exception as e:
                self.logger.warning(f"Error analyzing agent file {agent_file}: {e}")
        
        # Analyze system improvements
        config_files = list(agents_dir.glob("*.json")) + list(agents_dir.glob("*.md"))
        for config_file in config_files:
            try:
                mod_time = datetime.fromtimestamp(config_file.stat().st_mtime)
                if week_start <= mod_time <= week_end:
                    agent_progress["system_improvements"].append({
                        "file": config_file.name,
                        "updated": mod_time.isoformat()
                    })
            except:
                pass
        
        return agent_progress
    
    def _identify_major_accomplishments(self, week_start: datetime, week_end: datetime) -> List[Dict[str, Any]]:
        """Identify major accomplishments during the week"""
        accomplishments = []
        
        # Check for new agent creation (major accomplishment)
        agents_dir = Path(__file__).parent
        for agent_file in agents_dir.glob("*agent*.py"):
            try:
                creation_time = datetime.fromtimestamp(agent_file.stat().st_ctime)
                if week_start <= creation_time <= week_end:
                    accomplishments.append({
                        "type": "agent_creation",
                        "title": f"Created {agent_file.stem.replace('_', ' ').title()}",
                        "description": f"Developed new autonomous agent for enhanced workflow automation",
                        "impact": "high",
                        "category": "agent_development",
                        "date": creation_time.isoformat()
                    })
            except:
                pass
        
        # Check for major project milestones
        active_dir = Path("/Users/elizabethknopf/Documents/claudec/active")
        for project_dir in active_dir.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                # Check if project was set up with complete configuration this week
                claude_file = project_dir / "CLAUDE.md"
                todo_file = project_dir / "TODO.md"
                
                if claude_file.exists() and todo_file.exists():
                    try:
                        claude_mod = datetime.fromtimestamp(claude_file.stat().st_mtime)
                        todo_mod = datetime.fromtimestamp(todo_file.stat().st_mtime)
                        
                        if (week_start <= claude_mod <= week_end) and (week_start <= todo_mod <= week_end):
                            accomplishments.append({
                                "type": "project_standardization",
                                "title": f"Standardized {project_dir.name} Project",
                                "description": "Added complete project configuration with CLAUDE.md and TODO.md",
                                "impact": "medium",
                                "category": "project_setup",
                                "date": max(claude_mod, todo_mod).isoformat()
                            })
                    except:
                        pass
        
        # Check for dashboard/localhost integration milestones
        dashboard_dir = Path("/Users/elizabethknopf/Documents/claudec/active/Project Management/dashboard")
        if dashboard_dir.exists():
            for file_path in dashboard_dir.glob("localhost*"):
                try:
                    creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    if week_start <= creation_time <= week_end:
                        accomplishments.append({
                            "type": "dashboard_integration",
                            "title": "Localhost Dashboard Integration Complete",
                            "description": "Integrated localhost URLs into Project Management dashboard",
                            "impact": "high",
                            "category": "dashboard_features",
                            "date": creation_time.isoformat()
                        })
                        break
                except:
                    pass
        
        return sorted(accomplishments, key=lambda x: x["date"], reverse=True)
    
    def _calculate_productivity_metrics(self, week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """Calculate productivity metrics for the week"""
        metrics = {
            "total_files_modified": 0,
            "total_files_created": 0,
            "projects_touched": 0,
            "agent_development_score": 0,
            "documentation_score": 0,
            "automation_improvements": 0
        }
        
        # Count file modifications across all projects
        active_dir = Path("/Users/elizabethknopf/Documents/claudec/active")
        projects_with_activity = set()
        
        for project_dir in active_dir.iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                project_has_activity = False
                
                try:
                    for file_path in project_dir.rglob("*"):
                        if file_path.is_file() and not file_path.name.startswith('.'):
                            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                            
                            if week_start <= mod_time <= week_end:
                                metrics["total_files_modified"] += 1
                                project_has_activity = True
                            
                            if week_start <= creation_time <= week_end:
                                metrics["total_files_created"] += 1
                                project_has_activity = True
                                
                                # Score different file types
                                if file_path.suffix == '.py' and 'agent' in file_path.name:
                                    metrics["agent_development_score"] += 10
                                elif file_path.suffix == '.md':
                                    metrics["documentation_score"] += 5
                
                    if project_has_activity:
                        projects_with_activity.add(project_dir.name)
                        
                except Exception as e:
                    self.logger.warning(f"Error calculating metrics for {project_dir.name}: {e}")
        
        metrics["projects_touched"] = len(projects_with_activity)
        
        # Calculate overall productivity score (0-100)
        base_score = min(metrics["total_files_created"] * 2, 40)  # Max 40 for file creation
        agent_bonus = min(metrics["agent_development_score"], 30)  # Max 30 for agent work
        doc_bonus = min(metrics["documentation_score"], 20)  # Max 20 for documentation
        project_bonus = min(metrics["projects_touched"] * 2, 10)  # Max 10 for project diversity
        
        metrics["overall_productivity_score"] = base_score + agent_bonus + doc_bonus + project_bonus
        
        return metrics
    
    def _analyze_content_generation(self, week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """Analyze content generation and insights for the week"""
        content_analysis = {
            "content_ideas_generated": 0,
            "social_media_posts": 0,
            "technical_insights": 0,
            "documentation_improvements": 0
        }
        
        # Check if content agent database exists and analyze
        content_db_file = Path(__file__).parent / "social_media_content_database.json"
        if content_db_file.exists():
            try:
                with open(content_db_file, 'r') as f:
                    content_db = json.load(f)
                
                # Count content ideas generated this week
                for idea in content_db.get("content_ideas", []):
                    try:
                        idea_date = datetime.fromisoformat(idea["created_date"])
                        if week_start <= idea_date <= week_end:
                            content_analysis["content_ideas_generated"] += 1
                    except:
                        pass
                
                # Count posts created this week
                for post in content_db.get("published_posts", []):
                    try:
                        post_date = datetime.fromisoformat(post["created_date"])
                        if week_start <= post_date <= week_end:
                            content_analysis["social_media_posts"] += 1
                    except:
                        pass
                        
            except Exception as e:
                self.logger.warning(f"Error analyzing content database: {e}")
        
        return content_analysis
    
    def _generate_executive_summary(self, weekly_data: Dict[str, Any]) -> str:
        """Generate executive summary of the week"""
        portfolio = weekly_data["portfolio_analysis"]
        agents = weekly_data["agent_development"]
        accomplishments = weekly_data["major_accomplishments"]
        metrics = weekly_data["productivity_metrics"]
        
        # Generate dynamic summary based on actual data
        summary_parts = []
        
        # Portfolio progress
        if portfolio["active_projects"] > 0:
            summary_parts.append(f"Made progress on {portfolio['active_projects']} projects")
            
            if portfolio["new_projects"] > 0:
                summary_parts.append(f"created {portfolio['new_projects']} new projects")
        
        # Agent development
        if agents["new_agents"]:
            agent_names = [agent["name"].replace("_", " ").title() for agent in agents["new_agents"]]
            summary_parts.append(f"developed {len(agent_names)} new agents: {', '.join(agent_names)}")
        
        # Major accomplishments
        high_impact_accomplishments = [acc for acc in accomplishments if acc["impact"] == "high"]
        if high_impact_accomplishments:
            summary_parts.append(f"achieved {len(high_impact_accomplishments)} major milestones")
        
        # File activity
        if metrics["total_files_created"] > 0:
            summary_parts.append(f"created {metrics['total_files_created']} new files")
        
        # Combine into executive summary
        if summary_parts:
            summary = f"This week I {', '.join(summary_parts)}."
        else:
            summary = "This was a maintenance week with system optimization and planning."
        
        # Add productivity score context
        productivity_score = metrics["overall_productivity_score"]
        if productivity_score >= 80:
            summary += " Exceptional productivity week with high-impact deliverables."
        elif productivity_score >= 60:
            summary += " Strong productivity with solid progress across multiple areas."
        elif productivity_score >= 40:
            summary += " Good steady progress with focus on quality improvements."
        else:
            summary += " Planning and preparation week setting foundation for future development."
        
        return summary
    
    def _calculate_weekly_progress_score(self, weekly_data: Dict[str, Any]) -> int:
        """Calculate overall weekly progress score (0-100)"""
        weights = self.tracking_categories
        
        portfolio = weekly_data["portfolio_analysis"]
        agents = weekly_data["agent_development"]
        metrics = weekly_data["productivity_metrics"]
        accomplishments = weekly_data["major_accomplishments"]
        
        # Calculate category scores
        scores = {}
        
        # Code development score
        code_score = min(metrics["total_files_created"] * 3 + metrics["total_files_modified"], 100)
        scores["code_development"] = code_score * weights["code_development"]["weight"]
        
        # Project setup score
        setup_score = min(portfolio["new_projects"] * 20 + portfolio["active_projects"] * 5, 100)
        scores["project_setup"] = setup_score * weights["project_setup"]["weight"]
        
        # Documentation score  
        doc_score = min(metrics["documentation_score"] * 5, 100)
        scores["documentation"] = doc_score * weights["documentation"]["weight"]
        
        # Agent development score
        agent_score = len(agents["new_agents"]) * 30 + len(agents["agent_updates"]) * 15
        agent_score = min(agent_score, 100)
        scores["agent_development"] = agent_score * weights["agent_development"]["weight"]
        
        # Dashboard features score
        dashboard_accomplishments = [acc for acc in accomplishments if acc["category"] == "dashboard_features"]
        dashboard_score = len(dashboard_accomplishments) * 25
        dashboard_score = min(dashboard_score, 100)
        scores["dashboard_features"] = dashboard_score * weights["dashboard_features"]["weight"]
        
        # Calculate weighted total
        total_score = sum(scores.values())
        
        return min(int(total_score), 100)
    
    def track_current_progress(self) -> Dict[str, Any]:
        """Track current progress (real-time)"""
        current_week_summary = self.generate_weekly_summary(0)  # Current week
        
        tracking_data = {
            "timestamp": datetime.now().isoformat(),
            "current_week_progress": current_week_summary["progress_score"],
            "active_projects": current_week_summary["portfolio_analysis"]["active_projects"],
            "recent_accomplishments": current_week_summary["major_accomplishments"][:3],
            "productivity_trend": self._get_productivity_trend()
        }
        
        return tracking_data
    
    def _get_productivity_trend(self) -> str:
        """Get productivity trend compared to previous weeks"""
        if len(self.progress_database["weekly_summaries"]) < 2:
            return "establishing_baseline"
        
        # Get last two weeks' scores
        sorted_weeks = sorted(self.progress_database["weekly_summaries"].keys(), reverse=True)
        
        if len(sorted_weeks) >= 2:
            current_score = self.progress_database["weekly_summaries"][sorted_weeks[0]]["progress_score"]
            previous_score = self.progress_database["weekly_summaries"][sorted_weeks[1]]["progress_score"]
            
            diff = current_score - previous_score
            
            if diff > 10:
                return "strongly_increasing"
            elif diff > 5:
                return "increasing"
            elif diff > -5:
                return "stable"
            elif diff > -10:
                return "decreasing"
            else:
                return "strongly_decreasing"
        
        return "stable"
    
    def analyze_productivity_trends(self, weeks_back: int = 4) -> Dict[str, Any]:
        """Analyze productivity trends over multiple weeks"""
        trend_analysis = {
            "analysis_period_weeks": weeks_back,
            "weekly_scores": [],
            "average_score": 0,
            "trend_direction": "stable",
            "insights": [],
            "recommendations": []
        }
        
        # Get weekly scores
        sorted_weeks = sorted(self.progress_database["weekly_summaries"].keys(), reverse=True)
        
        scores = []
        for week_key in sorted_weeks[:weeks_back]:
            week_data = self.progress_database["weekly_summaries"][week_key]
            scores.append({
                "week": week_key,
                "score": week_data["progress_score"],
                "date": week_data["week_start"][:10]
            })
        
        trend_analysis["weekly_scores"] = scores
        
        if scores:
            trend_analysis["average_score"] = sum(s["score"] for s in scores) / len(scores)
            
            # Calculate trend
            if len(scores) >= 2:
                recent_avg = sum(s["score"] for s in scores[:2]) / 2
                older_avg = sum(s["score"] for s in scores[-2:]) / 2
                
                if recent_avg > older_avg + 10:
                    trend_analysis["trend_direction"] = "improving"
                elif recent_avg < older_avg - 10:
                    trend_analysis["trend_direction"] = "declining"
                else:
                    trend_analysis["trend_direction"] = "stable"
        
        # Generate insights and recommendations
        trend_analysis["insights"] = self._generate_productivity_insights(scores)
        trend_analysis["recommendations"] = self._generate_productivity_recommendations(trend_analysis)
        
        return trend_analysis
    
    def _generate_productivity_insights(self, scores: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from productivity scores"""
        insights = []
        
        if not scores:
            return ["Not enough data for insights"]
        
        avg_score = sum(s["score"] for s in scores) / len(scores)
        
        if avg_score >= 80:
            insights.append("Consistently high productivity with exceptional output")
        elif avg_score >= 60:
            insights.append("Strong steady productivity with regular achievements")
        elif avg_score >= 40:
            insights.append("Moderate productivity with room for optimization")
        else:
            insights.append("Lower productivity period - may indicate planning or learning phase")
        
        # Check for consistency
        if len(scores) >= 3:
            score_variance = max(s["score"] for s in scores) - min(s["score"] for s in scores)
            if score_variance < 20:
                insights.append("Highly consistent productivity patterns")
            elif score_variance > 40:
                insights.append("Variable productivity - may indicate project-dependent work cycles")
        
        return insights
    
    def _generate_productivity_recommendations(self, trend_analysis: Dict[str, Any]) -> List[str]:
        """Generate productivity recommendations"""
        recommendations = []
        
        avg_score = trend_analysis["average_score"]
        trend = trend_analysis["trend_direction"]
        
        if trend == "declining":
            recommendations.append("Consider analyzing what changed in high-productivity weeks")
            recommendations.append("Review agent automation to reduce manual work")
        
        if avg_score < 50:
            recommendations.append("Focus on high-impact agent development projects")
            recommendations.append("Increase documentation and standardization efforts")
        
        if trend == "improving":
            recommendations.append("Continue current successful patterns")
            recommendations.append("Document successful workflows for replication")
        
        # Always suggest automation
        recommendations.append("Leverage agent system for increased automation")
        
        return recommendations
    
    def get_major_accomplishments(self, time_period: str = "week") -> Dict[str, Any]:
        """Get major accomplishments for specified time period"""
        if time_period == "week":
            weeks_back = 1
        elif time_period == "month":
            weeks_back = 4
        elif time_period == "quarter":
            weeks_back = 12
        else:
            weeks_back = 1
        
        all_accomplishments = []
        
        # Gather accomplishments from recent weeks
        sorted_weeks = sorted(self.progress_database["weekly_summaries"].keys(), reverse=True)
        
        for week_key in sorted_weeks[:weeks_back]:
            week_data = self.progress_database["weekly_summaries"][week_key]
            accomplishments = week_data.get("major_accomplishments", [])
            all_accomplishments.extend(accomplishments)
        
        # Sort by impact and date
        high_impact = [acc for acc in all_accomplishments if acc["impact"] == "high"]
        medium_impact = [acc for acc in all_accomplishments if acc["impact"] == "medium"]
        
        return {
            "time_period": time_period,
            "total_accomplishments": len(all_accomplishments),
            "high_impact_count": len(high_impact),
            "medium_impact_count": len(medium_impact),
            "top_accomplishments": sorted(high_impact + medium_impact, 
                                        key=lambda x: (x["impact"] == "high", x["date"]), 
                                        reverse=True)[:10]
        }


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Weekly Progress Agent - Track and summarize weekly progress")
    parser.add_argument("command", choices=["summary", "track", "trends", "accomplishments"], 
                       help="Command to execute")
    parser.add_argument("--week-offset", type=int, default=0, help="Weeks back to analyze (0=current)")
    parser.add_argument("--weeks-back", type=int, default=4, help="Number of weeks for trend analysis")
    parser.add_argument("--period", default="week", choices=["week", "month", "quarter"], 
                       help="Time period for accomplishments")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = WeeklyProgressAgent()
    
    if args.command == "summary":
        result = agent.generate_weekly_summary(args.week_offset)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            week_start = datetime.fromisoformat(result["week_start"]).strftime("%Y-%m-%d")
            week_end = datetime.fromisoformat(result["week_end"]).strftime("%Y-%m-%d")
            
            print(f"📊 Weekly Progress Summary")
            print(f"   Week: {result['week_key']} ({week_start} to {week_end})")
            print(f"   Progress Score: {result['progress_score']}/100")
            print()
            
            print("🎯 Executive Summary:")
            print(f"   {result['executive_summary']}")
            print()
            
            portfolio = result["portfolio_analysis"]
            print(f"📁 Portfolio Progress:")
            print(f"   Active Projects: {portfolio['active_projects']}/{portfolio['total_projects']}")
            if portfolio["new_projects"]:
                print(f"   New Projects: {portfolio['new_projects']}")
            print()
            
            agents = result["agent_development"]
            print(f"🤖 Agent Development:")
            print(f"   Total Agent Files: {agents['total_agent_files']}")
            if agents["new_agents"]:
                new_agent_names = [agent["name"] for agent in agents["new_agents"]]
                print(f"   New Agents: {', '.join(new_agent_names)}")
            if agents["agent_updates"]:
                print(f"   Updated Agents: {len(agents['agent_updates'])}")
            print()
            
            accomplishments = result["major_accomplishments"]
            if accomplishments:
                print(f"🏆 Major Accomplishments ({len(accomplishments)}):")
                for acc in accomplishments[:3]:
                    impact_icon = "🔥" if acc["impact"] == "high" else "✨"
                    print(f"   {impact_icon} {acc['title']}")
                print()
            
            metrics = result["productivity_metrics"]
            print(f"📈 Productivity Metrics:")
            print(f"   Files Created: {metrics['total_files_created']}")
            print(f"   Files Modified: {metrics['total_files_modified']}")
            print(f"   Projects Touched: {metrics['projects_touched']}")
            print(f"   Overall Score: {metrics['overall_productivity_score']}/100")
    
    elif args.command == "track":
        result = agent.track_current_progress()
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"⏱️ Current Progress Tracking")
            print(f"   Week Progress Score: {result['current_week_progress']}/100")
            print(f"   Active Projects: {result['active_projects']}")
            print(f"   Productivity Trend: {result['productivity_trend'].replace('_', ' ').title()}")
            print()
            
            if result['recent_accomplishments']:
                print(f"🎯 Recent Accomplishments:")
                for acc in result['recent_accomplishments']:
                    impact_icon = "🔥" if acc["impact"] == "high" else "✨"
                    print(f"   {impact_icon} {acc['title']}")
    
    elif args.command == "trends":
        result = agent.analyze_productivity_trends(args.weeks_back)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"📈 Productivity Trends ({args.weeks_back} weeks)")
            print(f"   Average Score: {result['average_score']:.1f}/100")
            print(f"   Trend Direction: {result['trend_direction'].replace('_', ' ').title()}")
            print()
            
            print("📊 Weekly Scores:")
            for score_data in result['weekly_scores']:
                print(f"   Week {score_data['week']}: {score_data['score']}/100 ({score_data['date']})")
            print()
            
            if result['insights']:
                print("💡 Insights:")
                for insight in result['insights']:
                    print(f"   • {insight}")
                print()
            
            if result['recommendations']:
                print("🎯 Recommendations:")
                for rec in result['recommendations']:
                    print(f"   • {rec}")
    
    elif args.command == "accomplishments":
        result = agent.get_major_accomplishments(args.period)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"🏆 Major Accomplishments ({args.period})")
            print(f"   Total: {result['total_accomplishments']}")
            print(f"   High Impact: {result['high_impact_count']}")
            print(f"   Medium Impact: {result['medium_impact_count']}")
            print()
            
            for acc in result['top_accomplishments'][:5]:
                impact_icon = "🔥" if acc["impact"] == "high" else "✨"
                category_icons = {
                    "agent_development": "🤖",
                    "project_setup": "🔧", 
                    "dashboard_features": "📊",
                    "code_development": "💻"
                }
                category_icon = category_icons.get(acc["category"], "📝")
                
                date_str = datetime.fromisoformat(acc["date"]).strftime("%m/%d")
                print(f"{impact_icon} {category_icon} {acc['title']} ({date_str})")
                print(f"    {acc['description']}")
                print()


if __name__ == "__main__":
    main()