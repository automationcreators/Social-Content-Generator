#!/usr/bin/env python3
"""
RSS Content Scout Agent
Scans ContentGen feeds for trending AI/business ideas
Scores by relevance, viral potential, and alignment with personal brand
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import re

class RSSContentScout:
    """Scout RSS feeds for content opportunities"""

    def __init__(self):
        self.agents_dir = Path(__file__).parent
        self.contentgen_db = Path("/Users/elizabethknopf/Documents/claudec/active/ContentGen/data/database.db")

        # Focus areas based on user requirements
        self.focus_categories = [
            "ai", "artificial intelligence", "machine learning",
            "business", "automation", "productivity",
            "claude", "agents", "no-code", "small business"
        ]

        # Personal brand keywords for alignment
        self.brand_keywords = [
            "automation", "claude", "no-code", "small business",
            "efficiency", "productivity", "tools", "workflow",
            "non-technical", "beginner", "practical", "real-world"
        ]

    def connect_db(self):
        """Connect to ContentGen database"""
        return sqlite3.connect(self.contentgen_db)

    def scan_recent_content(self, days_back=7, limit=50):
        """Scan recent content from AI/business feeds"""

        conn = self.connect_db()
        cursor = conn.cursor()

        # Get recent content from AI/business categories
        cutoff_date = datetime.now() - timedelta(days=days_back)

        query = """
            SELECT
                ci.id,
                ci.title,
                ci.description,
                ci.source_name,
                ci.url,
                ci.content,
                ci.category,
                ci.tags,
                ci.created_at,
                ci.engagement_score,
                cs.viral_score,
                cs.trending_score,
                cs.quality_score
            FROM content_ideas ci
            LEFT JOIN content_scores cs ON ci.id = cs.content_id
            WHERE (
                ci.category LIKE '%ai%' OR
                ci.category LIKE '%business%' OR
                ci.category LIKE '%automation%' OR
                ci.category LIKE '%productivity%'
            )
            AND ci.created_at >= ?
            ORDER BY ci.created_at DESC
            LIMIT ?
        """

        cursor.execute(query, (cutoff_date.isoformat(), limit))
        results = cursor.fetchall()

        conn.close()

        return results

    def score_idea(self, idea):
        """
        Score an idea based on:
        - Relevance to focus areas
        - Viral potential
        - Alignment with personal brand
        - Trending signals
        """

        title = idea[1].lower() if idea[1] else ""
        description = idea[2].lower() if idea[2] else ""
        content = idea[5].lower() if idea[5] else ""
        tags = idea[7].lower() if idea[7] else ""

        combined_text = f"{title} {description} {content} {tags}"

        # 1. Relevance Score (0-30)
        relevance = 0
        for keyword in self.focus_categories:
            if keyword in combined_text:
                relevance += 3
        relevance = min(relevance, 30)

        # 2. Brand Alignment Score (0-25)
        alignment = 0
        for keyword in self.brand_keywords:
            if keyword in combined_text:
                alignment += 2.5
        alignment = min(alignment, 25)

        # 3. Viral Score from database (0-20)
        viral_score = (idea[10] or 0) * 2 if idea[10] else 0
        viral_score = min(viral_score, 20)

        # 4. Trending Score from database (0-15)
        trending_score = (idea[11] or 0) * 1.5 if idea[11] else 0
        trending_score = min(trending_score, 15)

        # 5. Quality Score from database (0-10)
        quality_score = (idea[12] or 0) if idea[12] else 0
        quality_score = min(quality_score, 10)

        # Total score
        total_score = relevance + alignment + viral_score + trending_score + quality_score

        return {
            'total_score': round(total_score, 2),
            'relevance': round(relevance, 2),
            'brand_alignment': round(alignment, 2),
            'viral_potential': round(viral_score, 2),
            'trending': round(trending_score, 2),
            'quality': round(quality_score, 2)
        }

    def extract_keywords(self, ideas):
        """Extract trending keywords from ideas"""

        all_words = []

        for idea in ideas:
            title = idea[1] or ""
            description = idea[2] or ""
            content = idea[5] or ""

            combined = f"{title} {description} {content}"

            # Extract meaningful words (3+ chars, not common words)
            words = re.findall(r'\b[a-z]{3,}\b', combined.lower())
            all_words.extend(words)

        # Common words to filter out
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'with',
            'this', 'that', 'from', 'have', 'has', 'been', 'will',
            'can', 'could', 'would', 'should', 'may', 'might', 'must'
        }

        filtered_words = [w for w in all_words if w not in stop_words]

        # Count frequency
        word_counts = Counter(filtered_words)

        return word_counts.most_common(20)

    def categorize_opportunity(self, idea, score):
        """Categorize content opportunity type"""

        title = idea[1].lower() if idea[1] else ""
        description = idea[2].lower() if idea[2] else ""

        combined = f"{title} {description}"

        # Determine opportunity type
        if any(word in combined for word in ['how to', 'guide', 'tutorial', 'step by step']):
            return 'tutorial'
        elif any(word in combined for word in ['trend', 'future', '2025', '2024', 'new']):
            return 'trend'
        elif any(word in combined for word in ['vs', 'compare', 'better than', 'alternative']):
            return 'comparison'
        elif any(word in combined for word in ['tool', 'software', 'app', 'platform']):
            return 'tool_review'
        elif any(word in combined for word in ['save', 'automate', 'productivity', 'efficiency']):
            return 'productivity'
        elif any(word in combined for word in ['case study', 'example', 'real world']):
            return 'case_study'
        else:
            return 'educational'

    def format_idea_for_output(self, idea, score, opportunity_type):
        """Format idea for JSON output"""

        return {
            'id': idea[0],
            'title': idea[1],
            'description': idea[2],
            'source': idea[3],
            'url': idea[4],
            'category': idea[6],
            'created_at': idea[8],
            'opportunity_type': opportunity_type,
            'scores': score,
            'suggested_platforms': self.suggest_platforms(score, opportunity_type),
            'suggested_framework': self.suggest_framework(opportunity_type),
            'fusion_potential': self.assess_fusion_potential(idea)
        }

    def suggest_platforms(self, score, opportunity_type):
        """Suggest best platforms based on content type and score"""

        platforms = []

        # High-quality, in-depth content → LinkedIn, YouTube
        if score['quality'] >= 7 or opportunity_type in ['tutorial', 'case_study']:
            platforms.append('YouTube')
            platforms.append('LinkedIn')

        # Trending, viral potential → Twitter, Threads
        if score['viral_potential'] >= 10 or score['trending'] >= 10:
            platforms.append('Twitter')
            platforms.append('Threads')

        # Quick tips, comparisons → Twitter, LinkedIn
        if opportunity_type in ['tool_review', 'comparison', 'productivity']:
            platforms.append('Twitter')
            platforms.append('LinkedIn')

        # Always include at least one platform
        if not platforms:
            platforms = ['LinkedIn', 'Twitter']

        return list(set(platforms))  # Remove duplicates

    def suggest_framework(self, opportunity_type):
        """Suggest Kallaway framework based on opportunity type"""

        framework_map = {
            'tutorial': 'how_to',
            'trend': 'transformation',
            'comparison': 'contrarian_snapback',
            'tool_review': 'benefit_driven',
            'productivity': 'benefit_driven',
            'case_study': 'transformation',
            'educational': 'how_to'
        }

        return framework_map.get(opportunity_type, 'benefit_driven')

    def assess_fusion_potential(self, idea):
        """
        Assess if this idea can be fused with personal projects
        High = directly relates to automation/Claude/workflows
        Medium = tangentially related
        Low = standalone topic
        """

        title = idea[1].lower() if idea[1] else ""
        description = idea[2].lower() if idea[2] else ""

        combined = f"{title} {description}"

        # High fusion keywords
        high_fusion = ['automation', 'claude', 'workflow', 'no-code', 'ai agent',
                      'productivity tool', 'business automation']

        # Medium fusion keywords
        medium_fusion = ['ai', 'business', 'tool', 'software', 'efficiency',
                        'save time', 'small business']

        if any(kw in combined for kw in high_fusion):
            return 'high'
        elif any(kw in combined for kw in medium_fusion):
            return 'medium'
        else:
            return 'low'

    def scan(self, days_back=7, min_score=30, output_file=None):
        """
        Main scan function
        """

        print("\n" + "="*100)
        print("🔍 RSS CONTENT SCOUT - SCANNING FEEDS")
        print("="*100)

        print(f"\n📡 Scanning ContentGen database...")
        print(f"   Focus: AI, Business, Automation channels")
        print(f"   Time window: Last {days_back} days")

        # Scan recent content
        raw_ideas = self.scan_recent_content(days_back=days_back, limit=100)

        print(f"   ✅ Found {len(raw_ideas)} raw ideas")

        # Score and filter ideas
        print(f"\n🎯 Scoring ideas...")

        scored_ideas = []
        seen_titles = set()  # Deduplication

        for idea in raw_ideas:
            # Skip duplicates
            title = idea[1].lower() if idea[1] else ""
            if title in seen_titles:
                continue
            seen_titles.add(title)

            score = self.score_idea(idea)

            if score['total_score'] >= min_score:
                opportunity_type = self.categorize_opportunity(idea, score)
                formatted = self.format_idea_for_output(idea, score, opportunity_type)
                scored_ideas.append(formatted)

        # Ensure source diversity - limit to max 3 from same source
        scored_ideas = self._ensure_source_diversity(scored_ideas)

        # Sort by total score
        scored_ideas.sort(key=lambda x: x['scores']['total_score'], reverse=True)

        print(f"   ✅ {len(scored_ideas)} unique ideas scored above {min_score}")

        # Extract trending keywords
        print(f"\n📊 Analyzing trends...")
        keywords = self.extract_keywords(raw_ideas)

        # Categorize by opportunity type
        type_counts = Counter([idea['opportunity_type'] for idea in scored_ideas])

        # Categorize by fusion potential
        fusion_counts = Counter([idea['fusion_potential'] for idea in scored_ideas])

        # Output summary
        output_data = {
            'metadata': {
                'scan_date': datetime.now().isoformat(),
                'days_scanned': days_back,
                'total_raw_ideas': len(raw_ideas),
                'qualified_ideas': len(scored_ideas),
                'min_score_threshold': min_score
            },
            'trending_keywords': [
                {'keyword': kw, 'frequency': count}
                for kw, count in keywords
            ],
            'opportunity_breakdown': dict(type_counts),
            'fusion_potential_breakdown': dict(fusion_counts),
            'ideas': scored_ideas[:30]  # Top 30 ideas
        }

        # Save to file
        if output_file is None:
            output_file = self.agents_dir / 'rss_ideas_database.json'

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✅ Saved to: {output_file}")

        # Print summary
        print("\n" + "="*100)
        print("📋 SCAN SUMMARY")
        print("="*100)

        print(f"\n🎯 Top Opportunities:")
        for i, idea in enumerate(scored_ideas[:10], 1):
            print(f"\n   {i}. {idea['title'][:70]}...")
            print(f"      Score: {idea['scores']['total_score']}")
            print(f"      Type: {idea['opportunity_type']}")
            print(f"      Platforms: {', '.join(idea['suggested_platforms'])}")
            print(f"      Framework: {idea['suggested_framework']}")
            print(f"      Fusion potential: {idea['fusion_potential']}")

        print(f"\n📊 Trending Keywords:")
        for kw, count in keywords[:10]:
            print(f"   • {kw}: {count}")

        print(f"\n📈 Opportunity Types:")
        for opp_type, count in type_counts.most_common():
            print(f"   • {opp_type}: {count}")

        print(f"\n🔗 Fusion Potential:")
        for fusion, count in fusion_counts.most_common():
            print(f"   • {fusion}: {count}")

        print("\n" + "="*100)

        return output_data

    def _ensure_source_diversity(self, ideas):
        """Ensure we don't have too many ideas from the same source"""
        from collections import defaultdict

        source_count = defaultdict(int)
        diverse_ideas = []
        max_per_source = 3

        # First pass: take up to max_per_source from each source
        for idea in ideas:
            source = idea['source']
            if source_count[source] < max_per_source:
                diverse_ideas.append(idea)
                source_count[source] += 1

        print(f"   🎨 Source diversity: {len(set(i['source'] for i in diverse_ideas))} different sources")

        return diverse_ideas


def main():
    import sys

    scout = RSSContentScout()

    # Parse command line args
    days_back = 7
    min_score = 30

    if len(sys.argv) > 1:
        if sys.argv[1] == 'scan':
            days_back = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            min_score = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        elif sys.argv[1] == '--help':
            print("""
RSS Content Scout Agent

Usage:
  python3 rss_content_scout.py scan [days_back] [min_score]

Examples:
  python3 rss_content_scout.py scan                 # Scan last 7 days, min score 30
  python3 rss_content_scout.py scan 14              # Scan last 14 days
  python3 rss_content_scout.py scan 7 40            # Last 7 days, min score 40

Webhook endpoint: /scan-rss
            """)
            return

    # Run scan
    scout.scan(days_back=days_back, min_score=min_score)


if __name__ == "__main__":
    main()
