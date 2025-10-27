#!/usr/bin/env python3
"""
Agent Framework - Base system for autonomous project management agents
Provides communication, coordination, and execution infrastructure for workflow agents
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import threading
import time
import uuid

@dataclass
class AgentMessage:
    """Message format for agent communication"""
    id: str
    sender: str
    recipient: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: str
    priority: int = 5  # 1-10, higher = more important
    requires_response: bool = False
    correlation_id: Optional[str] = None

@dataclass
class AgentTask:
    """Task assigned to an agent"""
    id: str
    agent_id: str
    task_type: str
    parameters: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    priority: int = 5

class BaseAgent(ABC):
    """Base class for all project management agents"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.status = "initialized"  # initialized, running, paused, stopped
        self.last_activity = datetime.now().isoformat()
        
        # Agent configuration
        self.config = self.load_config()
        self.capabilities = self.get_capabilities()
        
        # Communication setup
        self.message_bus = AgentMessageBus()
        self.task_queue = AgentTaskQueue()
        
        # Agent state
        self.state = {}
        self.metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "uptime_seconds": 0
        }
        
        self.running = False
        self.thread = None
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    @abstractmethod
    def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process a specific task assigned to this agent"""
        pass
    
    def load_config(self) -> Dict:
        """Load agent-specific configuration"""
        config_path = Path("/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents/config") / f"{self.agent_id}.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        default_config = {
            "enabled": True,
            "execution_interval": 300,  # 5 minutes
            "max_concurrent_tasks": 3,
            "retry_attempts": 3,
            "timeout_seconds": 300,
            "log_level": "info"
        }
        
        # Save default config
        os.makedirs(config_path.parent, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def start(self):
        """Start the agent in a separate thread"""
        if self.running:
            return
        
        self.running = True
        self.status = "running"
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        self.log(f"Agent {self.name} started")
    
    def stop(self):
        """Stop the agent"""
        self.running = False
        self.status = "stopped"
        
        if self.thread:
            self.thread.join(timeout=5)
        
        self.log(f"Agent {self.name} stopped")
    
    def pause(self):
        """Pause agent execution"""
        self.status = "paused"
        self.log(f"Agent {self.name} paused")
    
    def resume(self):
        """Resume agent execution"""
        self.status = "running"
        self.log(f"Agent {self.name} resumed")
    
    def _run_loop(self):
        """Main execution loop for the agent"""
        start_time = datetime.now()
        
        while self.running:
            try:
                if self.status == "running" and self.config.get("enabled", True):
                    # Process pending tasks
                    self._process_pending_tasks()
                    
                    # Process incoming messages
                    self._process_messages()
                    
                    # Perform periodic work
                    self._perform_periodic_work()
                    
                    # Update metrics
                    self.metrics["uptime_seconds"] = (datetime.now() - start_time).total_seconds()
                    self.last_activity = datetime.now().isoformat()
                
                # Sleep for execution interval
                time.sleep(self.config.get("execution_interval", 300))
                
            except Exception as e:
                self.log(f"Error in agent loop: {e}", level="error")
                time.sleep(60)  # Wait before retrying
    
    def _process_pending_tasks(self):
        """Process tasks from the task queue"""
        max_tasks = self.config.get("max_concurrent_tasks", 3)
        pending_tasks = self.task_queue.get_pending_tasks(self.agent_id, limit=max_tasks)
        
        for task in pending_tasks:
            try:
                self.log(f"Processing task {task.id}: {task.task_type}")
                
                # Mark task as running
                task.status = "running"
                task.started_at = datetime.now().isoformat()
                self.task_queue.update_task(task)
                
                # Process the task
                result = self.process_task(task)
                
                # Mark as completed
                task.status = "completed"
                task.completed_at = datetime.now().isoformat()
                task.result = result
                self.task_queue.update_task(task)
                
                self.metrics["tasks_completed"] += 1
                self.log(f"Task {task.id} completed successfully")
                
            except Exception as e:
                # Mark as failed
                task.status = "failed"
                task.completed_at = datetime.now().isoformat()
                task.error = str(e)
                self.task_queue.update_task(task)
                
                self.metrics["tasks_failed"] += 1
                self.log(f"Task {task.id} failed: {e}", level="error")
    
    def _process_messages(self):
        """Process incoming messages"""
        messages = self.message_bus.get_messages_for_agent(self.agent_id)
        
        for message in messages:
            try:
                self.handle_message(message)
                self.metrics["messages_received"] += 1
            except Exception as e:
                self.log(f"Error processing message {message.id}: {e}", level="error")
    
    def _perform_periodic_work(self):
        """Override this method for agent-specific periodic work"""
        pass
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages - override for agent-specific logic"""
        self.log(f"Received message from {message.sender}: {message.message_type}")
        
        if message.requires_response:
            # Send acknowledgment
            response = AgentMessage(
                id=str(uuid.uuid4()),
                sender=self.agent_id,
                recipient=message.sender,
                message_type="acknowledgment",
                payload={"original_message_id": message.id},
                timestamp=datetime.now().isoformat(),
                correlation_id=message.correlation_id
            )
            self.send_message(response)
    
    def send_message(self, message: AgentMessage):
        """Send message to another agent"""
        self.message_bus.send_message(message)
        self.metrics["messages_sent"] += 1
        self.log(f"Sent message to {message.recipient}: {message.message_type}")
    
    def assign_task(self, agent_id: str, task_type: str, parameters: Dict[str, Any], 
                   priority: int = 5) -> str:
        """Assign a task to another agent"""
        task = AgentTask(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            task_type=task_type,
            parameters=parameters,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        
        self.task_queue.add_task(task)
        self.log(f"Assigned task {task.id} to agent {agent_id}")
        return task.id
    
    def log(self, message: str, level: str = "info"):
        """Log agent activity"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {self.agent_id} ({level.upper()}): {message}"
        
        # Print to console
        print(log_entry)
        
        # Save to log file
        log_dir = Path("/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{self.agent_id}.log"
        with open(log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "last_activity": self.last_activity,
            "capabilities": self.capabilities,
            "metrics": self.metrics,
            "config": self.config
        }

class AgentMessageBus:
    """Message bus for agent communication"""
    
    def __init__(self):
        self.message_dir = Path("/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents/messages")
        self.message_dir.mkdir(parents=True, exist_ok=True)
    
    def send_message(self, message: AgentMessage):
        """Send message to recipient agent"""
        message_file = self.message_dir / f"{message.recipient}_inbox.json"
        
        # Load existing messages
        messages = []
        if message_file.exists():
            with open(message_file, 'r') as f:
                messages = json.load(f)
        
        # Add new message
        messages.append(asdict(message))
        
        # Save messages
        with open(message_file, 'w') as f:
            json.dump(messages, f, indent=2)
    
    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """Get and clear messages for an agent"""
        message_file = self.message_dir / f"{agent_id}_inbox.json"
        
        if not message_file.exists():
            return []
        
        # Load messages
        with open(message_file, 'r') as f:
            message_data = json.load(f)
        
        messages = [AgentMessage(**msg) for msg in message_data]
        
        # Clear inbox
        message_file.unlink()
        
        return messages

class AgentTaskQueue:
    """Task queue for agent coordination"""
    
    def __init__(self):
        self.queue_file = Path("/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents/task-queue.json")
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
    
    def add_task(self, task: AgentTask):
        """Add task to queue"""
        tasks = self._load_tasks()
        tasks.append(asdict(task))
        self._save_tasks(tasks)
    
    def get_pending_tasks(self, agent_id: str, limit: int = 10) -> List[AgentTask]:
        """Get pending tasks for an agent"""
        tasks = self._load_tasks()
        
        # Filter pending tasks for this agent
        pending_tasks = [
            AgentTask(**task) for task in tasks 
            if task.get("agent_id") == agent_id and task.get("status") == "pending"
        ]
        
        # Sort by priority and creation time
        pending_tasks.sort(key=lambda t: (-t.priority, t.created_at))
        
        return pending_tasks[:limit]
    
    def update_task(self, task: AgentTask):
        """Update task status"""
        tasks = self._load_tasks()
        
        # Find and update task
        for i, t in enumerate(tasks):
            if t.get("id") == task.id:
                tasks[i] = asdict(task)
                break
        
        self._save_tasks(tasks)
    
    def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        """Get task by ID"""
        tasks = self._load_tasks()
        
        for task_data in tasks:
            if task_data.get("id") == task_id:
                return AgentTask(**task_data)
        
        return None
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from file"""
        if not self.queue_file.exists():
            return []
        
        with open(self.queue_file, 'r') as f:
            return json.load(f)
    
    def _save_tasks(self, tasks: List[Dict]):
        """Save tasks to file"""
        with open(self.queue_file, 'w') as f:
            json.dump(tasks, f, indent=2, default=str)

class AgentOrchestrator:
    """Orchestrates multiple agents and coordinates their work"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_bus = AgentMessageBus()
        self.task_queue = AgentTaskQueue()
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        agent.log(f"Registered with orchestrator")
    
    def start_agent(self, agent_id: str):
        """Start a specific agent"""
        if agent_id in self.agents:
            self.agents[agent_id].start()
    
    def stop_agent(self, agent_id: str):
        """Stop a specific agent"""
        if agent_id in self.agents:
            self.agents[agent_id].stop()
    
    def start_all_agents(self):
        """Start all registered agents"""
        for agent in self.agents.values():
            agent.start()
    
    def stop_all_agents(self):
        """Stop all registered agents"""
        for agent in self.agents.values():
            agent.stop()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "agents": {agent_id: agent.get_status() for agent_id, agent in self.agents.items()},
            "total_agents": len(self.agents),
            "running_agents": len([a for a in self.agents.values() if a.status == "running"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def broadcast_message(self, sender_id: str, message_type: str, payload: Dict[str, Any]):
        """Broadcast message to all agents except sender"""
        for agent_id in self.agents:
            if agent_id != sender_id:
                message = AgentMessage(
                    id=str(uuid.uuid4()),
                    sender=sender_id,
                    recipient=agent_id,
                    message_type=message_type,
                    payload=payload,
                    timestamp=datetime.now().isoformat()
                )
                self.message_bus.send_message(message)

def main():
    """CLI interface for agent framework management"""
    import sys
    
    orchestrator = AgentOrchestrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "status":
            status = orchestrator.get_system_status()
            print("🤖 Agent System Status:")
            print(f"Total agents: {status['total_agents']}")
            print(f"Running agents: {status['running_agents']}")
            
            for agent_id, agent_status in status['agents'].items():
                print(f"\n  {agent_status['name']} ({agent_id}):")
                print(f"    Status: {agent_status['status']}")
                print(f"    Tasks completed: {agent_status['metrics']['tasks_completed']}")
                print(f"    Last activity: {agent_status['last_activity']}")
        
        elif command == "logs":
            log_dir = Path("/Users/elizabethknopf/Documents/claudec/active/Personal-OS/agents/logs")
            if log_dir.exists():
                print("📝 Recent agent logs:")
                for log_file in log_dir.glob("*.log"):
                    print(f"\n=== {log_file.stem} ===")
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        # Show last 10 lines
                        for line in lines[-10:]:
                            print(line.strip())
            else:
                print("No logs found")
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: status, logs")
    else:
        print("Agent Framework Management")
        print("Commands:")
        print("  status - Show agent system status")
        print("  logs   - Show recent agent logs")

if __name__ == "__main__":
    main()