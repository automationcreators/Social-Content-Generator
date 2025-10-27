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

### 2. 🔧 Hook Variations Repeat Across Rows (NEEDS FIX)

**Problem:** Same hooks appear in multiple rows
- Row 2: Hook A, Hook B
- Row 3: Hook A, Hook B  ← SAME
- Row 4: Hook A, Hook B  ← SAME

**Root Cause:** `content_orchestrator.py` line 279
```python
'angles': selected_angles[:2]  # Always takes first 2
```

**Solution Needed:**
1. Rotate through angles for each content piece
2. Use hash-based selection for variety
3. Ensure each row gets different hooks

**Implementation:**
```python
# Instead of always [:2]
angle_start = hash(str(rss_idea)) % len(selected_angles)
'angles': selected_angles[angle_start:angle_start+2]
```

---

### 3. 🔍 Format Inconsistency: Rows 2-4 vs Rows 5-10

**Problem:** Different formats between row groups
- Rows 2-4: Good format (user likes this)
- Rows 5-10: Different format, YouTube script repetition, broken links

**Possible Causes:**
1. Different content sources (daily content vs pillar content)?
2. Multiple runs with different configurations?
3. Tab consolidation issues?

**Investigation Needed:**
- Check if rows 2-4 are from `Content` tab (daily content)
- Check if rows 5-10 are from `Pillar Content` tab (long-form)
- Verify sync_to_google_sheets.py formatting

**User Preference:**
- Format from rows 2-4 ✅
- But with MORE variation across each row
- Remove repetition

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

1. ✅ Content extractor created (DONE)
2. 🔧 Implement hook rotation (TODO)
3. 🔧 Implement stat rotation (TODO)
4. 🔧 Enhance example variation (TODO)
5. 🔍 Investigate rows 2-4 vs 5-10 format difference (TODO)
6. 🧪 Test with fresh data (TODO)
7. 📊 Verify Google Sheets output (TODO)

---

## Notes

**Why variation matters:**
- Keeps content fresh for audience
- Prevents pattern recognition
- Maximizes use of generated angles/stats
- Better A/B testing opportunities
- More authentic (not templated)

**Current bottleneck:**
- ContentGen database still stale (Oct 13)
- Need fresh RSS articles for true variety
- Once fresh data + fixes applied = dramatic improvement

---

**Status:** Partial fixes applied, hook/stat rotation still needed
**ETA:** 30 minutes for remaining fixes
**Priority:** HIGH - affects content quality directly
