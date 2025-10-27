#!/usr/bin/env python3
"""
Content Extractor - Deep dive into project files for rich content

Extracts:
- Key insights and learnings
- Step-by-step guides
- Tips and tricks
- Success stories
- Problem-solution narratives
- Technical breakthroughs
"""

import re
from pathlib import Path
from typing import Dict, List


class ContentExtractor:
    """Extracts rich content from project documentation"""

    def extract_from_project(self, project_dir: Path) -> Dict:
        """Extract all types of content from a project"""

        content = {
            "insights": [],
            "guides": [],
            "tips": [],
            "stories": [],
            "problems_solved": [],
            "tech_stack": [],
            "business_impact": []
        }

        # Read README
        readme = project_dir / "README.md"
        if readme.exists():
            readme_content = self._read_markdown(readme)
            content["insights"].extend(self._extract_insights(readme_content))
            content["guides"].extend(self._extract_guides(readme_content))
            content["tips"].extend(self._extract_tips(readme_content))
            content["stories"].extend(self._extract_stories(readme_content))
            content["problems_solved"].extend(self._extract_problems_solved(readme_content))
            content["business_impact"].extend(self._extract_business_impact(readme_content))

        # Read other markdown files
        for md_file in project_dir.rglob("*.md"):
            if md_file.name != "README.md" and not any(skip in str(md_file) for skip in ['node_modules', '.git', 'venv']):
                md_content = self._read_markdown(md_file)

                # Look for specific content types
                if any(word in md_file.name.lower() for word in ['guide', 'tutorial', 'how', 'setup']):
                    content["guides"].extend(self._extract_guides(md_content))

                if any(word in md_file.name.lower() for word in ['tip', 'trick', 'best', 'practice']):
                    content["tips"].extend(self._extract_tips(md_content))

                if any(word in md_file.name.lower() for word in ['story', 'case', 'example']):
                    content["stories"].extend(self._extract_stories(md_content))

        # Read CLAUDE.md for project context
        claude_md = project_dir / "CLAUDE.md"
        if claude_md.exists():
            claude_content = self._read_markdown(claude_md)
            content["insights"].extend(self._extract_insights(claude_content))
            content["tech_stack"].extend(self._extract_tech_stack(claude_content))

        # Read Python docstrings for insights
        for py_file in list(project_dir.rglob("*.py"))[:20]:  # Limit to first 20 files
            if not any(skip in str(py_file) for skip in ['node_modules', '.git', '__pycache__', 'venv']):
                py_content = self._read_file(py_file)
                content["insights"].extend(self._extract_from_docstrings(py_content))

        # Deduplicate and limit
        content["insights"] = self._deduplicate(content["insights"])[:10]
        content["guides"] = self._deduplicate(content["guides"])[:5]
        content["tips"] = self._deduplicate(content["tips"])[:10]
        content["stories"] = self._deduplicate(content["stories"])[:3]
        content["problems_solved"] = self._deduplicate(content["problems_solved"])[:5]
        content["business_impact"] = self._deduplicate(content["business_impact"])[:5]

        return content

    def _read_markdown(self, file_path: Path) -> str:
        """Read markdown file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

    def _read_file(self, file_path: Path) -> str:
        """Read any text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""

    def _extract_insights(self, content: str) -> List[str]:
        """Extract key insights"""
        insights = []

        # Look for patterns like "Key insight:", "Learned:", "Discovery:"
        patterns = [
            r"(?:key insight|learned|discovery|finding|realized):\s*(.+?)(?:\n|$)",
            r"##\s*(?:insights?|learnings?|discoveries)\s*\n(.+?)(?=\n##|\Z)",
            r"\*\*(?:insight|learning|discovery)\*\*:\s*(.+?)(?:\n|$)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                text = match.group(1).strip()
                if len(text) > 20 and len(text) < 300:
                    insights.append(text)

        # Extract bullet points under "Insights" sections
        insights_section = re.search(r"##\s*Insights?\s*\n((?:[-*]\s*.+\n)+)", content, re.IGNORECASE)
        if insights_section:
            bullets = re.findall(r"[-*]\s*(.+)", insights_section.group(1))
            insights.extend([b.strip() for b in bullets if len(b.strip()) > 20])

        return insights

    def _extract_guides(self, content: str) -> List[Dict]:
        """Extract step-by-step guides"""
        guides = []

        # Look for numbered steps
        step_patterns = [
            r"(?:step\s+\d+|^\d+\.)\s*[:\-]?\s*(.+?)(?=\n(?:step\s+\d+|\d+\.)|$)",
            r"##\s*(?:step\s+\d+|installation|setup)\s*\n(.+?)(?=\n##|\Z)",
        ]

        for pattern in step_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                text = match.group(1).strip()
                if len(text) > 30 and len(text) < 500:
                    guides.append({
                        "type": "step",
                        "content": text
                    })

        return guides

    def _extract_tips(self, content: str) -> List[str]:
        """Extract tips and tricks"""
        tips = []

        # Look for tip patterns
        tip_patterns = [
            r"(?:tip|trick|pro tip|protip|note|important):\s*(.+?)(?:\n|$)",
            r"💡\s*(.+?)(?:\n|$)",
            r"\*\*tip\*\*:\s*(.+?)(?:\n|$)",
        ]

        for pattern in tip_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                text = match.group(1).strip()
                if len(text) > 20 and len(text) < 200:
                    tips.append(text)

        return tips

    def _extract_stories(self, content: str) -> List[Dict]:
        """Extract success stories and narratives"""
        stories = []

        # Look for story patterns
        story_sections = re.finditer(
            r"##\s*(?:story|example|case study|success|journey)\s*\n(.+?)(?=\n##|\Z)",
            content,
            re.IGNORECASE | re.DOTALL
        )

        for match in story_sections:
            text = match.group(1).strip()
            if len(text) > 100 and len(text) < 1000:
                stories.append({
                    "type": "narrative",
                    "content": text[:500]  # Limit length
                })

        # Look for before/after patterns
        before_after = re.search(
            r"(?:before|problem):\s*(.+?)\s*(?:after|solution):\s*(.+?)(?:\n\n|$)",
            content,
            re.IGNORECASE | re.DOTALL
        )
        if before_after:
            stories.append({
                "type": "transformation",
                "before": before_after.group(1).strip(),
                "after": before_after.group(2).strip()
            })

        return stories

    def _extract_problems_solved(self, content: str) -> List[Dict]:
        """Extract problem-solution pairs"""
        problems = []

        # Look for problem patterns
        problem_patterns = [
            r"##\s*(?:problem|challenge|issue)\s*\n(.+?)\n##\s*(?:solution|resolution|fix)\s*\n(.+?)(?=\n##|\Z)",
            r"(?:problem|challenge):\s*(.+?)\s*(?:solution|fix):\s*(.+?)(?:\n\n|$)",
        ]

        for pattern in problem_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                problems.append({
                    "problem": match.group(1).strip()[:300],
                    "solution": match.group(2).strip()[:300]
                })

        return problems

    def _extract_business_impact(self, content: str) -> List[Dict]:
        """Extract business impact metrics"""
        impacts = []

        # Look for impact patterns
        impact_patterns = [
            r"(?:saved?|saving)\s+(\d+\s*(?:hours?|minutes?|days?))",
            r"(?:reduced|decreased)\s+(?:by\s+)?(\d+%)",
            r"(?:increased|improved)\s+(?:by\s+)?(\d+%)",
            r"\$(\d+(?:,\d+)*)\s*(?:saved|revenue|profit)",
        ]

        for pattern in impact_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                impacts.append({
                    "metric": match.group(0),
                    "value": match.group(1)
                })

        return impacts

    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract technology stack"""
        tech = []

        # Common tech keywords
        tech_keywords = [
            "Python", "JavaScript", "React", "Node.js", "Flask", "FastAPI",
            "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes",
            "AWS", "GCP", "Azure", "Supabase", "Firebase",
            "Claude", "GPT", "OpenAI", "AI", "ML"
        ]

        for keyword in tech_keywords:
            if re.search(rf"\b{keyword}\b", content, re.IGNORECASE):
                tech.append(keyword)

        return list(set(tech))

    def _extract_from_docstrings(self, content: str) -> List[str]:
        """Extract insights from Python docstrings"""
        insights = []

        # Find docstrings
        docstrings = re.findall(r'"""(.+?)"""', content, re.DOTALL)
        for docstring in docstrings:
            # Look for meaningful descriptions
            lines = [l.strip() for l in docstring.split('\n') if len(l.strip()) > 30]
            insights.extend(lines[:2])  # Take first 2 meaningful lines

        return insights

    def _deduplicate(self, items: List) -> List:
        """Remove duplicates while preserving order"""
        seen = set()
        result = []
        for item in items:
            # Convert to string for comparison
            item_str = str(item).lower()
            if item_str not in seen:
                seen.add(item_str)
                result.append(item)
        return result
