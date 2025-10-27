# Content Frameworks

This directory contains content generation frameworks for social media posts.

## Framework Structure

Each framework is a JSON file with the following structure:

```json
{
  "framework_name": "Name of the framework",
  "framework_type": "engagement_hooks | storytelling | platform_specific",
  "description": "What this framework does",
  "applies_to": {
    "platforms": ["twitter", "linkedin"],
    "categories": ["progress_updates", "learning_moments"]
  },
  "hook_types": {
    "hook_name": {
      "description": "When to use this hook",
      "power_words": ["word1", "word2"],
      "templates": [...]
    }
  }
}
```

## Available Frameworks

### kallaway_hooks.json
- **6 Power Words Framework**
- **3-Step Hook Formula**
- Hook types: contrarian_snapback, benefit_driven, transformation, how_to

## Adding New Frameworks

### From Local Files
1. Create a new JSON file in this directory
2. Follow the structure above
3. Framework will be automatically loaded

### From Google Drive
1. Upload framework JSON to your Google Drive folder
2. Run: `python3 framework_loader.py sync`
3. Frameworks will be downloaded and cached locally

## Framework Matching Logic

The FrameworkManager selects frameworks based on:
1. **Content Category** (progress_updates, learning_moments, etc.)
2. **Platform** (twitter, linkedin, instagram)
3. **Context Triggers** (agent files, testing, documentation, etc.)

## Google Drive Setup

Set your Google Drive folder ID in `framework_loader.py`:
```python
GDRIVE_FOLDER_ID = "your_folder_id_here"
```

Folder structure in Google Drive:
```
Content Frameworks/
├── kallaway_hooks.json
├── storytelling_frameworks.json
├── platform_templates.json
└── custom_frameworks/
    ├── aida_framework.json
    └── pas_framework.json
```

## Example: Creating a Storytelling Framework

```json
{
  "framework_name": "Story Arc Framework",
  "framework_type": "storytelling",
  "hook_types": {
    "hero_journey": {
      "description": "Classic hero's journey narrative",
      "templates": [
        {
          "pattern": "I faced {problem}. Here's how I {solution}",
          "variables": ["problem", "solution", "outcome"]
        }
      ]
    }
  }
}
```

## Testing Frameworks

Run the framework tester:
```bash
python3 framework_loader.py test --framework kallaway_hooks
```

This will show sample hooks generated from each template.
