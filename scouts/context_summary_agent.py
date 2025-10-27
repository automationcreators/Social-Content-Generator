#!/usr/bin/env python3
"""
Context Summary & Chat Log Agent - Creates context summaries and maintains chat logs
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import argparse
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.agent_framework import BaseAgent


class ContextSummaryAgent(BaseAgent):
    """Agent for creating context summaries and maintaining chat logs"""
    
    def __init__(self):
        super().__init__(
            "context_summary_agent",
            "Context Summary & Chat Log Agent",
            "Creates context summaries and maintains chat logs for Claude Code sessions"
        )
        
        # Configuration
        self.context_checkpoint_interval = 50  # Messages between context summaries
        self.max_log_size_mb = 10  # Maximum log file size before rotation
        
        # File patterns
        self.log_filename = "log.md"
        self.context_filename = "context.md"
        
        # Setup logging
        self.logger = logging.getLogger("context_summary")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(name)s (%(levelname)s): %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.info("Context Summary Agent initialized")
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        return [
            "context_summarization",
            "chat_log_management",
            "session_tracking",
            "checkpoint_creation",
            "log_rotation",
            "context_extraction"
        ]
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task request"""
        task_type = task.get("type", "create_checkpoint")
        project_path = task.get("project_path", os.getcwd())
        
        if task_type == "create_checkpoint":
            return self.create_context_checkpoint(
                project_path,
                task.get("conversation_text", ""),
                task.get("force", False)
            )
        elif task_type == "append_to_log":
            return self.append_to_chat_log(
                project_path,
                task.get("entry", ""),
                task.get("entry_type", "message")
            )
        elif task_type == "summarize_session":
            return self.summarize_session(project_path)
        elif task_type == "rotate_logs":
            return self.rotate_logs(project_path)
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    def create_context_checkpoint(self, project_path: str, conversation_text: str = "", 
                                force: bool = False) -> Dict[str, Any]:
        """Create a context summary checkpoint"""
        project_dir = Path(project_path)
        if not project_dir.exists():
            return {"error": f"Project path does not exist: {project_path}"}
        
        context_file = project_dir / self.context_filename
        log_file = project_dir / self.log_filename
        
        self.logger.info(f"Creating context checkpoint for {project_dir.name}")
        
        # Check if checkpoint is needed
        if not force and not self._should_create_checkpoint(log_file):
            return {
                "checkpoint_created": False,
                "reason": "Not enough new content since last checkpoint"
            }
        
        # Gather context information
        context_data = self._gather_context_information(project_dir, conversation_text)
        
        # Generate context summary
        context_summary = self._generate_context_summary(context_data)
        
        # Save context summary
        try:
            with open(context_file, 'w') as f:
                f.write(context_summary)
            
            # Update log with checkpoint marker
            self._add_checkpoint_marker(log_file)
            
            self.logger.info(f"Context checkpoint created: {context_file}")
            
            return {
                "checkpoint_created": True,
                "context_file": str(context_file),
                "timestamp": datetime.now().isoformat(),
                "summary_length": len(context_summary)
            }
            
        except Exception as e:
            self.logger.error(f"Error creating context checkpoint: {e}")
            return {"error": str(e)}
    
    def append_to_chat_log(self, project_path: str, entry: str, 
                          entry_type: str = "message") -> Dict[str, Any]:
        """Append entry to chat log"""
        project_dir = Path(project_path)
        log_file = project_dir / self.log_filename
        
        if not entry.strip():
            return {"error": "Entry content is required"}
        
        # Create log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = self._format_log_entry(timestamp, entry_type, entry)
        
        try:
            # Check if log rotation is needed
            if log_file.exists() and self._should_rotate_log(log_file):
                self.rotate_logs(project_path)
            
            # Append to log
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return {
                "success": True,
                "log_file": str(log_file),
                "entry_type": entry_type,
                "timestamp": timestamp
            }
            
        except Exception as e:
            self.logger.error(f"Error appending to chat log: {e}")
            return {"error": str(e)}
    
    def summarize_session(self, project_path: str) -> Dict[str, Any]:
        """Summarize the current session"""
        project_dir = Path(project_path)
        log_file = project_dir / self.log_filename
        
        if not log_file.exists():
            return {"error": "No log file found"}
        
        self.logger.info(f"Summarizing session for {project_dir.name}")
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            # Parse session data
            session_data = self._parse_session_data(log_content)
            
            # Generate session summary
            session_summary = self._generate_session_summary(session_data)
            
            return {
                "success": True,
                "session_summary": session_summary,
                "session_data": session_data
            }
            
        except Exception as e:
            self.logger.error(f"Error summarizing session: {e}")
            return {"error": str(e)}
    
    def rotate_logs(self, project_path: str) -> Dict[str, Any]:
        """Rotate log files when they get too large"""
        project_dir = Path(project_path)
        log_file = project_dir / self.log_filename
        
        if not log_file.exists():
            return {"error": "No log file to rotate"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_name = f"log_archived_{timestamp}.md"
        archived_file = project_dir / archived_name
        
        try:
            # Move current log to archived
            log_file.rename(archived_file)
            
            # Create new log with header
            self._create_new_log(log_file, project_dir.name)
            
            self.logger.info(f"Log rotated: {archived_file}")
            
            return {
                "success": True,
                "archived_file": str(archived_file),
                "new_log_file": str(log_file)
            }
            
        except Exception as e:
            self.logger.error(f"Error rotating logs: {e}")
            return {"error": str(e)}
    
    def _should_create_checkpoint(self, log_file: Path) -> bool:
        """Check if a context checkpoint should be created"""
        if not log_file.exists():
            return False
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count messages since last checkpoint
            lines = content.split('\n')
            messages_since_checkpoint = 0
            found_checkpoint = False
            
            for line in reversed(lines):
                if '## Context Checkpoint' in line:
                    found_checkpoint = True
                    break
                elif line.startswith('**[') or line.startswith('**User') or line.startswith('**Assistant'):
                    messages_since_checkpoint += 1
            
            # Create checkpoint if enough messages or no checkpoint found
            return messages_since_checkpoint >= self.context_checkpoint_interval or not found_checkpoint
            
        except Exception as e:
            self.logger.warning(f"Error checking checkpoint need: {e}")
            return False
    
    def _should_rotate_log(self, log_file: Path) -> bool:
        """Check if log file should be rotated"""
        try:
            size_mb = log_file.stat().st_size / (1024 * 1024)
            return size_mb >= self.max_log_size_mb
        except:
            return False
    
    def _gather_context_information(self, project_dir: Path, conversation_text: str = "") -> Dict[str, Any]:
        """Gather all relevant context information"""
        context_data = {
            "project_name": project_dir.name,
            "project_path": str(project_dir),
            "timestamp": datetime.now().isoformat(),
            "conversation_text": conversation_text,
            "project_files": {},
            "recent_changes": [],
            "localhost_config": {},
            "project_status": {}
        }
        
        # Gather key project files
        key_files = ["CLAUDE.md", "TODO.md", "README.md", "package.json", "requirements.txt"]
        for filename in key_files:
            file_path = project_dir / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context_data["project_files"][filename] = f.read()[:2000]  # First 2000 chars
                except:
                    context_data["project_files"][filename] = "[File exists but could not read]"
        
        # Get recent file changes
        context_data["recent_changes"] = self._get_recent_file_changes(project_dir)
        
        # Get localhost configuration
        context_data["localhost_config"] = self._extract_localhost_info(context_data["project_files"])
        
        return context_data
    
    def _get_recent_file_changes(self, project_dir: Path) -> List[Dict[str, Any]]:
        """Get recently modified files"""
        recent_changes = []
        cutoff_time = datetime.now() - timedelta(hours=24)  # Last 24 hours
        
        try:
            for file_path in project_dir.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mod_time > cutoff_time:
                        recent_changes.append({
                            "file": str(file_path.relative_to(project_dir)),
                            "modified": mod_time.isoformat(),
                            "size": file_path.stat().st_size
                        })
        except Exception as e:
            self.logger.warning(f"Error getting recent changes: {e}")
        
        return sorted(recent_changes, key=lambda x: x["modified"], reverse=True)[:10]
    
    def _extract_localhost_info(self, project_files: Dict[str, str]) -> Dict[str, Any]:
        """Extract localhost configuration from project files"""
        localhost_info = {}
        
        claude_content = project_files.get("CLAUDE.md", "")
        if claude_content:
            # Extract localhost URLs
            url_matches = re.findall(r'http://localhost:(\d+)', claude_content)
            if url_matches:
                localhost_info["ports"] = [int(port) for port in url_matches]
                localhost_info["primary_port"] = int(url_matches[0])
                localhost_info["primary_url"] = f"http://localhost:{url_matches[0]}"
        
        return localhost_info
    
    def _generate_context_summary(self, context_data: Dict[str, Any]) -> str:
        """Generate comprehensive context summary"""
        project_name = context_data["project_name"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""# {project_name} - Context Summary

*Generated: {timestamp}*

## Project Overview
- **Name**: {project_name}
- **Path**: {context_data["project_path"]}
- **Last Updated**: {timestamp}

## Current Status
"""
        
        # Add localhost information
        localhost_config = context_data.get("localhost_config", {})
        if localhost_config:
            summary += f"""
### Localhost Configuration
- **Primary URL**: {localhost_config.get("primary_url", "Not configured")}
- **Assigned Ports**: {localhost_config.get("ports", [])}
"""
        
        # Add project files summary
        summary += "\n### Key Files Status\n"
        for filename, content in context_data.get("project_files", {}).items():
            status = "✅ Present" if content and content != "[File exists but could not read]" else "❌ Missing/Unreadable"
            summary += f"- **{filename}**: {status}\n"
        
        # Add recent changes
        recent_changes = context_data.get("recent_changes", [])
        if recent_changes:
            summary += f"\n### Recent Activity ({len(recent_changes)} files)\n"
            for change in recent_changes[:5]:
                mod_time = datetime.fromisoformat(change["modified"]).strftime("%m/%d %H:%M")
                summary += f"- `{change['file']}` (Modified: {mod_time})\n"
        
        # Add conversation context if provided
        conversation_text = context_data.get("conversation_text", "")
        if conversation_text:
            # Extract key topics and decisions
            key_topics = self._extract_key_topics(conversation_text)
            if key_topics:
                summary += "\n### Key Topics & Decisions\n"
                for topic in key_topics:
                    summary += f"- {topic}\n"
        
        # Add file contents for important files
        claude_content = context_data.get("project_files", {}).get("CLAUDE.md", "")
        if claude_content and len(claude_content) > 50:
            summary += f"\n### CLAUDE.md Overview\n"
            # Extract purpose and key sections
            lines = claude_content.split('\n')
            for line in lines[:20]:  # First 20 lines
                if '**Purpose**:' in line or '**Category**:' in line or '**Phase**:' in line:
                    summary += f"- {line.strip()}\n"
        
        summary += f"""

## Context Checkpoint Details
- **Checkpoint ID**: {hashlib.md5(timestamp.encode()).hexdigest()[:8]}
- **Session Time**: {timestamp}
- **Files Analyzed**: {len(context_data.get("project_files", {}))}
- **Recent Changes**: {len(recent_changes)}

---
*Generated by Context Summary Agent v1.0*
"""
        
        return summary
    
    def _extract_key_topics(self, conversation_text: str) -> List[str]:
        """Extract key topics from conversation text"""
        if not conversation_text:
            return []
        
        key_topics = []
        
        # Look for common patterns that indicate important topics
        patterns = [
            r'(?:implement|create|build|add)\s+(.{10,50})',
            r'(?:fix|resolve|solve)\s+(.{10,50})',
            r'(?:configure|setup|install)\s+(.{10,50})',
            r'(?:integrate|connect|link)\s+(.{10,50})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, conversation_text, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 per pattern
                topic = match.strip().rstrip('.!?').title()
                if len(topic) > 10 and topic not in key_topics:
                    key_topics.append(topic)
        
        return key_topics[:10]  # Limit total topics
    
    def _format_log_entry(self, timestamp: str, entry_type: str, content: str) -> str:
        """Format a log entry"""
        entry_types = {
            "message": "💬",
            "command": "⚡",
            "error": "❌",
            "success": "✅",
            "info": "ℹ️",
            "checkpoint": "🔄"
        }
        
        icon = entry_types.get(entry_type, "📝")
        
        return f"""
**[{timestamp}] {icon} {entry_type.title()}**
{content}

---
"""
    
    def _add_checkpoint_marker(self, log_file: Path):
        """Add checkpoint marker to log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        checkpoint_entry = f"""
## Context Checkpoint Created
**Timestamp**: {timestamp}  
**Status**: Context summary updated in `context.md`

---
"""
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(checkpoint_entry)
        except Exception as e:
            self.logger.warning(f"Error adding checkpoint marker: {e}")
    
    def _create_new_log(self, log_file: Path, project_name: str):
        """Create new log file with header"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""# {project_name} - Chat Log

*Session started: {timestamp}*

This file contains the conversation history for Claude Code sessions in this project.

- **Context summaries**: See `context.md` for periodic context summaries
- **Log rotation**: Previous logs are archived when files get large

---

"""
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    def _parse_session_data(self, log_content: str) -> Dict[str, Any]:
        """Parse session data from log content"""
        lines = log_content.split('\n')
        
        session_data = {
            "total_entries": 0,
            "entry_types": {},
            "session_duration": None,
            "key_activities": []
        }
        
        # Count entries by type
        for line in lines:
            if '**[' in line and ']' in line:
                session_data["total_entries"] += 1
                # Extract entry type
                if '💬' in line:
                    session_data["entry_types"]["message"] = session_data["entry_types"].get("message", 0) + 1
                elif '⚡' in line:
                    session_data["entry_types"]["command"] = session_data["entry_types"].get("command", 0) + 1
                elif '❌' in line:
                    session_data["entry_types"]["error"] = session_data["entry_types"].get("error", 0) + 1
                elif '✅' in line:
                    session_data["entry_types"]["success"] = session_data["entry_types"].get("success", 0) + 1
        
        return session_data
    
    def _generate_session_summary(self, session_data: Dict[str, Any]) -> str:
        """Generate session summary"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""## Session Summary - {timestamp}

### Activity Overview
- **Total Entries**: {session_data["total_entries"]}

### Entry Breakdown
"""
        
        for entry_type, count in session_data.get("entry_types", {}).items():
            percentage = (count / session_data["total_entries"]) * 100 if session_data["total_entries"] > 0 else 0
            summary += f"- **{entry_type.title()}**: {count} ({percentage:.1f}%)\n"
        
        return summary
    
    def monitor_project(self, project_path: str, conversation_text: str = "") -> Dict[str, Any]:
        """Monitor project and create checkpoint/log entries as needed"""
        results = {
            "project_path": project_path,
            "actions_taken": []
        }
        
        # Create chat log entry
        if conversation_text:
            log_result = self.append_to_chat_log(project_path, conversation_text, "message")
            if log_result.get("success"):
                results["actions_taken"].append("chat_log_updated")
        
        # Check if context checkpoint is needed
        checkpoint_result = self.create_context_checkpoint(project_path, conversation_text)
        if checkpoint_result.get("checkpoint_created"):
            results["actions_taken"].append("context_checkpoint_created")
        
        return results


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Context Summary & Chat Log Agent")
    parser.add_argument("command", choices=["checkpoint", "log", "summarize", "rotate", "monitor"], 
                       help="Command to execute")
    parser.add_argument("--project", help="Project path", default=os.getcwd())
    parser.add_argument("--text", help="Conversation text or log entry")
    parser.add_argument("--type", default="message", help="Entry type for log")
    parser.add_argument("--force", action="store_true", help="Force checkpoint creation")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ContextSummaryAgent()
    
    if args.command == "checkpoint":
        result = agent.create_context_checkpoint(args.project, args.text or "", args.force)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get("checkpoint_created"):
                print(f"✅ Context checkpoint created: {result['context_file']}")
                print(f"   Summary length: {result['summary_length']} characters")
            else:
                print(f"ℹ️  No checkpoint created: {result.get('reason', 'Unknown reason')}")
    
    elif args.command == "log":
        if not args.text:
            print("❌ Text content required for log entry")
            return
        
        result = agent.append_to_chat_log(args.project, args.text, args.type)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"✅ Log entry added: {result['entry_type']} at {result['timestamp']}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == "summarize":
        result = agent.summarize_session(args.project)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print("📊 Session Summary:")
                print(result["session_summary"])
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == "rotate":
        result = agent.rotate_logs(args.project)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get("success"):
                print(f"🔄 Logs rotated:")
                print(f"   Archived: {Path(result['archived_file']).name}")
                print(f"   New log: {Path(result['new_log_file']).name}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    elif args.command == "monitor":
        result = agent.monitor_project(args.project, args.text or "")
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"👁️  Monitoring project: {Path(args.project).name}")
            print(f"   Actions taken: {', '.join(result['actions_taken']) or 'None'}")


if __name__ == "__main__":
    main()