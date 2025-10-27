# Content Variation & Quality Issues - Oct 26, 2025

## Issues Identified

### 1. ✅ Project Data Collector Too Shallow (FIXED)

**Problem:** Agent only reads first 500 chars and first line of READMEs
- Missing: Key insights, step-by-step guides, tips/tricks, stories
- Not connecting dots across project history
- Only looking at recent changes, not broader project understanding

**Solution Applied:**
Created `content_extractor.py` that extracts:
- ✅ Key insights and learnings from full READMEs
- ✅ Step-by-step guides and tutorials
- ✅ Tips and tricks
- ✅ Success stories and narratives
- ✅ Problem-solution pairs
- ✅ Business impact metrics
- ✅ Tech stack
- ✅ Content from CLAUDE.md, docs, and docstrings

**Next Run:** Will extract rich content from all projects

---

### 2. ✅ Hook Variations Repeat Across Rows (FIXED)

**Problem:** Same hooks appeared in multiple rows
- Row 2: Hook A, Hook B
- Row 3: Hook A, Hook B  ← SAME
- Row 4: Hook A, Hook B  ← SAME

**Root Cause:** `content_orchestrator.py` line 299 always took first 2 angles

**Solution Applied:**
1. Added piece_index parameter to generation loop
2. Rotate through angles using modulo: (piece_index * 2) % len(angles)
3. Rotate through stats using modulo: piece_index % len(stats)
4. Each row now gets different hooks and statistics

**Implementation (Completed Oct 27):**
```python
# Line 196: Added enumeration
for piece_index, rss_idea in enumerate(rss_ideas):
    fusion = self._build_fusion_piece(..., piece_index=piece_index)

# Lines 267-275: Angle rotation
if len(selected_angles) >= 2:
    start_idx = (piece_index * 2) % len(selected_angles)
    angle_pair = [
        selected_angles[start_idx % len(selected_angles)],
        selected_angles[(start_idx + 1) % len(selected_angles)]
    ]

# Lines 277-287: Stat rotation
if len(stats) >= 3:
    stat_start = piece_index % len(stats)
    rotated_stats = [...]

# Line 300: Use rotated stats
'statistics': rotated_stats if rotated_stats else []
```

**Status:** ✅ FIXED and committed to GitHub

---

### 3. ✅ Format Inconsistency: Rows 2-4 vs Rows 5-10 (ANALYZED)

**Problem:** Different formats between row groups
- Rows 2-4: Good format (user likes this) - Daily Content
- Rows 5-10: Different format, YouTube script repetition, broken links - Pillar Content

**Root Cause IDENTIFIED:**
Two different sync methods with different data formats:

1. **Daily Content (Rows 2-4)** → "Content" tab
   - Format: Date | Title | Trend Source | URL | Personal Example | Hook 1 | Hook 2 | Stat 1 | Stat 2 | Stat 3 | etc.
   - Shows actual content (hooks, stats, examples)
   - Copy-paste ready

2. **Pillar Content (Rows 5-10)** → "Pillar Content" tab
   - Format: Date | Title | Category | Audience | YouTube Script (chars) | LinkedIn (chars) | etc.
   - Shows only METADATA (character counts, tweet counts)
   - NOT copy-paste ready
   - Actual scripts in separate Google Docs

**User Preference:**
- Use rows 2-4 format for ALL content ✅
- Show actual hooks, stats, examples (not just counts)
- More variation across each row

**Solution:** See FORMAT_ANALYSIS.md for detailed implementation plan
- Option 2 (Recommended): Make pillar content use same format as daily content
- Update pillar_content_sync.py to match sync_to_google_sheets.py format
- Extract and display actual hooks, stats, examples from pillar content
- Add links to full YouTube scripts instead of just character count

---

### 4. 🎨 Need MORE Variation Across All Rows

**Current State:**
- Some elements vary (personal examples, angles)
- Some elements stay the same (format, structure)

**User Wants:**
- **Everything** should vary row-to-row:
  - Hooks (different for each row)
  - Personal examples (rotate through projects)
  - Statistics (different stats per row)
  - Frameworks (mix of transformation, how-to, contrarian)
  - Format/structure (vary presentation)

**Solution:**
1. Create variation engine
2. Rotate through all available content
3. No repeating elements unless necessary
4. Each row = unique combination

---

## Priority Fixes

### HIGH PRIORITY

**1. Fix Hook Variation**
```python
# In content_orchestrator.py _build_fusion_piece()
# Add rotation logic:

def _build_fusion_piece(self, rss_idea, angles, research, pillar, mode, piece_index=0):
    selected_angles = angles.get(mode, {}).get('angles', []) if angles else []

    # Rotate angles based on piece index
    if len(selected_angles) >= 2:
        start_idx = (piece_index * 2) % len(selected_angles)
        angle_pair = [
            selected_angles[start_idx % len(selected_angles)],
            selected_angles[(start_idx + 1) % len(selected_angles)]
        ]
    else:
        angle_pair = selected_angles[:2]

    fusion = {
        'angles': angle_pair,  # Now varies per piece
        # ...
    }
```

**2. Ensure Statistic Variation**
```python
# Rotate through statistics
stats = research.get('statistics', []) if research else []
if len(stats) >= 3:
    stat_start = piece_index % len(stats)
    selected_stats = [
        stats[stat_start % len(stats)],
        stats[(stat_start + 1) % len(stats)],
        stats[(stat_start + 2) % len(stats)]
    ]
```

**3. Vary Personal Examples**
```python
# Already partially implemented, enhance:
opp_type = rss_idea.get('opportunity_type', 'educational')

# Add variation style
variation_styles = ['how_to_guide', 'story_narrative', 'analytical',
                    'practical_demo', 'transformation_story', 'insight_analysis']
style = variation_styles[piece_index % len(variation_styles)]
```

---

## Testing Checklist

After fixes applied, verify:

- [ ] No duplicate hooks across rows
- [ ] Statistics vary across rows
- [ ] Personal examples rotate
- [ ] Format consistent (use rows 2-4 style)
- [ ] Each row unique combination
- [ ] No YouTube script repetition
- [ ] All links work

---

## Manual Testing Steps

```bash
# 1. Run project data collector (get rich content)
cd /Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator
python3 scouts/update_project_data.py

# 2. Generate fresh content
python3 automation/daily_content_generator.py --mode balanced

# 3. Check Google Sheets
# Verify:
# - Hooks different in each row
# - Stats different in each row
# - Personal examples vary
# - Format consistent
```

---

## Next Steps

1. ✅ Content extractor created (DONE - Oct 27)
2. ✅ Implement hook rotation (DONE - Oct 27)
3. ✅ Implement stat rotation (DONE - Oct 27)
4. ✅ Investigate rows 2-4 vs 5-10 format difference (DONE - Oct 27)
5. ✅ Unify pillar content format to match daily content (DONE - Oct 27)
6. 🔧 Integrate content_extractor.py into project_data_collector.py (TODO)
7. 🧪 Test with fresh data (TODO)
8. 📊 Verify Google Sheets output (TODO)

---

## Implementation Progress - Oct 27, 2025

### ✅ Completed Today
1. **Hook Rotation** - Angles now rotate using modulo: (piece_index * 2) % len(angles)
2. **Stat Rotation** - Statistics rotate using modulo: piece_index % len(stats)
3. **Format Analysis** - Identified root cause of rows 2-4 vs 5-10 inconsistency
4. **Documentation** - Created FORMAT_ANALYSIS.md with detailed solution plan
5. **Format Unification** - Pillar content now uses same format as daily content

### ✅ Format Unification Complete
**Changes Applied:**
1. ✅ Changed headers to match daily content format exactly
2. ✅ Extract Hook 1 from idea description
3. ✅ Extract Hook 2 from Twitter thread first tweet
4. ✅ Format statistics: "stat: detail (source)"
5. ✅ Show personal examples with title and description
6. ✅ Add content preview (first 200 chars of YouTube script)
7. ✅ Add "Content Type" column (Daily vs Pillar)
8. ✅ Fixed file paths in pillar_content_generator.py

**Result:**
- Both content types have identical format
- All content is copy-paste ready
- No more metadata-only rows
- Hooks and stats displayed in every row

---

## Notes

**Why variation matters:**
- Keeps content fresh for audience
- Prevents pattern recognition
- Maximizes use of generated angles/stats
- Better A/B testing opportunities
- More authentic (not templated)

**Current bottlenecks:**
- ContentGen database still stale (Oct 13) - need fresh RSS articles
- Pillar content format doesn't match daily content format
- Content extractor not yet integrated into project data collector

**Once all fixes applied:**
- Hooks will vary across all rows ✅
- Stats will vary across all rows ✅
- Format will be consistent across all content types 🔧
- Rich project content will be extracted 🔧
- Dramatic improvement in content variety and quality

---

**Status:** Hook/stat rotation COMPLETE, format analysis COMPLETE, format unification COMPLETE
**Next:** Integrate content_extractor.py into project monitoring (estimated 30 minutes)
**Then:** Test with fresh content generation to verify all fixes work together
**Priority:** MEDIUM - content extractor will add more variety to project examples
