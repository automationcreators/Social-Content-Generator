#!/usr/bin/env python3
"""
Framework Manager - Loads and manages content generation frameworks
Supports local files and Google Drive sync
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("framework_manager")


class FrameworkManager:
    """Manages content generation frameworks from local and Google Drive sources"""

    def __init__(self, frameworks_dir: Optional[Path] = None):
        """
        Initialize the FrameworkManager

        Args:
            frameworks_dir: Path to local frameworks directory
        """
        if frameworks_dir is None:
            frameworks_dir = Path(__file__).parent

        self.frameworks_dir = Path(frameworks_dir)
        self.frameworks = {}
        self.gdrive_folder_id = None  # Set this for Google Drive sync

        # Load all local frameworks
        self.load_local_frameworks()

    def load_local_frameworks(self):
        """Load all JSON frameworks from the local directory"""
        logger.info(f"Loading frameworks from {self.frameworks_dir}")

        for framework_file in self.frameworks_dir.glob("*.json"):
            try:
                with open(framework_file, 'r') as f:
                    framework_data = json.load(f)
                    framework_name = framework_data.get("framework_name", framework_file.stem)
                    self.frameworks[framework_name] = framework_data
                    logger.info(f"Loaded framework: {framework_name}")
            except Exception as e:
                logger.error(f"Error loading {framework_file}: {e}")

        logger.info(f"Total frameworks loaded: {len(self.frameworks)}")

    def get_applicable_frameworks(self, category: str, platform: str = None) -> List[Dict]:
        """
        Get frameworks applicable to a category and platform

        Args:
            category: Content category (progress_updates, learning_moments, etc.)
            platform: Social media platform (twitter, linkedin, etc.)

        Returns:
            List of applicable framework dictionaries
        """
        applicable = []

        for framework_name, framework in self.frameworks.items():
            applies_to = framework.get("applies_to", {})

            # Check category match
            categories = applies_to.get("categories", [])
            if category not in categories:
                continue

            # Check platform match (if specified)
            if platform:
                platforms = applies_to.get("platforms", [])
                if platforms and platform not in platforms:
                    continue

            applicable.append(framework)

        return applicable

    def select_hook_template(self,
                            framework_name: str,
                            category: str,
                            context: Dict[str, Any]) -> Optional[Dict]:
        """
        Select the best hook template based on category and context

        Args:
            framework_name: Name of the framework to use
            category: Content category
            context: Context data (file_count, has_agents, has_tests, etc.)

        Returns:
            Selected hook template dictionary or None
        """
        if framework_name not in self.frameworks:
            logger.warning(f"Framework not found: {framework_name}")
            return None

        framework = self.frameworks[framework_name]
        hook_types_data = framework.get("hook_types", {})
        matching_rules = framework.get("matching_rules", {})

        # Get category-specific rules
        category_rules = matching_rules.get(category, {})
        preferred_hooks = category_rules.get("preferred_hooks", list(hook_types_data.keys()))

        # Check context triggers to narrow down hook type
        context_triggers = category_rules.get("context_triggers", {})
        selected_hook_type = None

        for trigger, hook_type in context_triggers.items():
            if context.get(trigger, False):
                selected_hook_type = hook_type
                break

        # If no specific trigger, randomly choose from preferred hooks
        if not selected_hook_type:
            selected_hook_type = random.choice(preferred_hooks) if preferred_hooks else None

        if not selected_hook_type or selected_hook_type not in hook_types_data:
            return None

        # Get templates for the selected hook type
        hook_type_info = hook_types_data[selected_hook_type]
        templates = hook_type_info.get("templates", [])

        if not templates:
            return None

        # Randomly select a template
        template = random.choice(templates)

        return {
            "hook_type": selected_hook_type,
            "template": template,
            "power_words": hook_type_info.get("power_words", []),
            "description": hook_type_info.get("description", "")
        }

    def generate_hook(self,
                     framework_name: str,
                     category: str,
                     context: Dict[str, Any],
                     variables: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """
        Generate a complete hook using a framework template

        Args:
            framework_name: Name of the framework to use
            category: Content category
            context: Context for template selection
            variables: Variables to fill in the template

        Returns:
            Dictionary with 'title', 'description', 'hook_type' or None
        """
        # Select appropriate template
        hook_data = self.select_hook_template(framework_name, category, context)

        if not hook_data:
            return None

        template = hook_data["template"]
        hook_type = hook_data["hook_type"]

        # Fill in the title template
        title_pattern = template.get("pattern", "")
        title = title_pattern
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in title:
                title = title.replace(placeholder, str(var_value))

        # Fill in the description template
        desc_pattern = template.get("description_pattern", "")
        description = desc_pattern
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            if placeholder in description:
                description = description.replace(placeholder, str(var_value))

        return {
            "title": title,
            "description": description,
            "hook_type": hook_type
        }

    def sync_from_gdrive(self):
        """
        Sync frameworks from Google Drive
        TODO: Implement Google Drive API integration
        """
        if not self.gdrive_folder_id:
            logger.warning("Google Drive folder ID not configured")
            return False

        logger.info("Google Drive sync not yet implemented")
        # This will be implemented with Google Drive API
        return False

    def list_frameworks(self) -> Dict[str, Any]:
        """Get summary of all loaded frameworks"""
        summary = {}
        for name, framework in self.frameworks.items():
            summary[name] = {
                "description": framework.get("description", ""),
                "type": framework.get("framework_type", ""),
                "categories": framework.get("applies_to", {}).get("categories", []),
                "platforms": framework.get("applies_to", {}).get("platforms", []),
                "hook_types": list(framework.get("hook_types", {}).keys())
            }
        return summary


def main():
    """CLI interface for framework manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Content Framework Manager")
    parser.add_argument("command", choices=["list", "test", "sync"],
                       help="Command to execute")
    parser.add_argument("--framework", help="Framework name for testing")
    parser.add_argument("--category", default="progress_updates",
                       help="Content category for testing")

    args = parser.parse_args()

    manager = FrameworkManager()

    if args.command == "list":
        print("\n📚 Available Frameworks:\n")
        for name, info in manager.list_frameworks().items():
            print(f"✨ {name}")
            print(f"   Description: {info['description']}")
            print(f"   Type: {info['type']}")
            print(f"   Categories: {', '.join(info['categories'])}")
            print(f"   Platforms: {', '.join(info['platforms'])}")
            print(f"   Hook Types: {', '.join(info['hook_types'])}")
            print()

    elif args.command == "test":
        if not args.framework:
            print("❌ --framework required for testing")
            return

        print(f"\n🧪 Testing Framework: {args.framework}\n")

        # Test hook generation
        context = {
            "high_file_count": True,
            "agent_files": True,
            "testing_focus": False
        }

        variables = {
            "project": "TestProject",
            "file_count": 10,
            "time_saved": "5 hours",
            "common_mistake": "write monolithic code",
            "better_approach": "break into specialized agents"
        }

        hook = manager.generate_hook(
            args.framework,
            args.category,
            context,
            variables
        )

        if hook:
            print(f"✅ Generated Hook:")
            print(f"   Title: {hook['title']}")
            print(f"   Description: {hook['description']}")
            print(f"   Hook Type: {hook['hook_type']}")
        else:
            print("❌ Failed to generate hook")

    elif args.command == "sync":
        print("\n🔄 Syncing frameworks from Google Drive...")
        success = manager.sync_from_gdrive()
        if success:
            print("✅ Sync complete")
        else:
            print("❌ Sync failed or not configured")


if __name__ == "__main__":
    main()
