# B-Roll Visual Generation Workflow Guide

## Overview

You now have **593 AI-generated visual prompts** across 33 scripts, each with multiple production approaches. This guide shows you how to use them effectively.

---

## Quick Stats

- **Total Scripts**: 33 (24 new scripts from Nov 10 selection)
- **Total Visual Moments**: 593 visuals
- **Average per Script**: 18 visuals
- **Cost Range**: $5-10 per script (hybrid approach)
- **Production Time**: 2-4 hours per script (hybrid)

---

## What You Have

### Files Generated

Each script now has a corresponding visual prompt JSON file in `/visual_prompts/`:

```
2025-11-10_claude_sonnet_45_30_hours_autonomous_contrarian_visual_prompts.json
2025-11-10_multi_agent_systems_62_percent_authority_visual_prompts.json
... (33 total)
```

### Each Visual Prompt Includes

1. **Runway Gen-4 Prompt** - Cinematic, high-quality ($1.25 per visual)
2. **Kling AI 2.0 Prompt** - Photorealistic, dynamic ($0.30 per visual)
3. **Pika Labs 2.5 Prompt** - Fast, social media optimized ($0.20 per visual)
4. **Real Footage Suggestion** - When to film yourself vs. use AI
5. **HeyGen Avatar Suggestion** - Avatar style, script text, background
6. **Recommended Approach** - Best method for that specific visual

---

## 4 Production Approaches

### Approach 1: Pure AI (Fastest)

**Best For**: Testing ideas, quick turnaround, abstract concepts

**Tools Needed**:
- Kling AI 2.0 account ($12/month)
- OR Pika Labs 2.5 account ($12/month)

**Workflow**:
1. Open script's visual prompt JSON file
2. For each visual, copy the `kling.prompt` or `pika.prompt`
3. Paste into Kling/Pika web interface
4. Generate (takes 30-90 seconds per visual)
5. Download and organize by timestamp

**Cost**: $5.70 per script (Kling) or $3.80 (Pika)
**Time**: 1-2 hours per script (mostly waiting for renders)

**Example**:
```json
"kling": {
  "prompt": "Photorealistic 3D data visualization: 30 hours autonomous operation stat.
             Physical objects representing data, dynamic camera rotation, professional
             studio lighting",
  "duration": "10s",
  "settings": "Professional Mode, 1080p, dynamic camera"
}
```

---

### Approach 2: Hybrid AI + Real Footage (Recommended)

**Best For**: Authentic, credible content with personality

**Tools Needed**:
- Kling AI account ($12/month)
- Smartphone or camera
- Basic lighting (ring light or window light)
- Descript for editing

**Workflow**:

**Part A - Film Real Footage (1 hour)**:
1. Check each visual's `real_footage.type` field
2. Film any marked as "Real Footage - Required" or "Screen Recording"
3. Examples:
   - Talking head shots (you speaking to camera)
   - Screen recordings (dashboards, systems)
   - Workspace b-roll (desk, office, hands typing)

**Part B - Generate AI B-Roll (1 hour)**:
1. For visuals marked "AI Recommended", use Kling prompts
2. Generate abstract concepts, data viz, comparisons
3. Download and organize

**Part C - Assembly in Descript (1-2 hours)**:
1. Import all footage (real + AI)
2. Match visuals to script timestamps
3. Add captions, transitions
4. Export

**Cost**: ~$5.32 per script (60% AI, 40% real)
**Time**: 3-4 hours per script

**What to Film Yourself**:
- Intro/outro (credibility)
- Key statistics explanations (engagement)
- Workspace shots (authenticity)
- Screen demos (proof)

**What to Generate with AI**:
- Abstract concepts ("AI automation workflow")
- Data visualizations ("4× faster comparison")
- System diagrams ("architecture visualization")
- Transitions and effects

---

### Approach 3: HeyGen Avatar + AI B-Roll (Scalable)

**Best For**: High volume, consistent brand, no camera shyness

**Tools Needed**:
- HeyGen account ($29/month)
- Kling AI account ($12/month)

**Workflow**:
1. Create HeyGen avatar (one-time setup, 5-10 min video)
2. For each visual with `heygen.script_text`:
   - Copy the script text
   - Generate avatar video with that text
   - Use the recommended `avatar_style` and `background`
3. Generate AI b-roll with Kling for other visuals
4. Assemble in Descript

**Cost**: $5-7 per script
**Time**: 2-3 hours per script (mostly scripting + assembly)

**Pros**:
- No need to film yourself
- Consistent quality
- Faster than real filming

**Cons**:
- Less authentic than real presenter
- Avatar limitations (expressions, gestures)
- Monthly HeyGen cost

---

### Approach 4: Real Presenter + Premium AI (Best Quality)

**Best For**: Flagship content, building authority, high-value topics

**Tools Needed**:
- Professional camera or high-end smartphone
- 3-point lighting setup
- Lavalier microphone
- Runway Gen-4 account ($50/month)
- Descript + color grading

**Workflow**:
1. Film yourself presenting (full talking head segments)
2. Generate premium AI b-roll with Runway Gen-4
3. Professional editing in Descript
4. Color grading and effects

**Cost**: $20-30 per script (Runway costs + time)
**Time**: 6-8 hours per script

**Use For**:
- Pillar content (main channel videos)
- High-stakes topics (case studies, thought leadership)
- Building personal brand

---

## Recommended Workflow for Your 24 Scripts

### Phase 1: Test with 1 Script (Week 1)

**Pick**: `2025-11-10_claude_sonnet_45_30_hours_autonomous_contrarian.md`

**Approach**: Hybrid (AI + Real)

**Action Plan**:
1. Open the visual prompt JSON file
2. Film 5 real shots:
   - Intro talking head (30 seconds)
   - Workspace b-roll (15 seconds)
   - Screen recording of Claude dashboard (20 seconds)
   - Hands typing closeup (10 seconds)
   - Outro talking head (20 seconds)

3. Generate 14 AI visuals with Kling:
   - Abstract concepts (autonomous operation, system architecture)
   - Data visualizations (30 hours stat, 4.3× improvement)
   - Comparison graphics (before/after)

4. Assemble in Descript:
   - Import all footage
   - Match to script timestamps
   - Add captions
   - Export

**Expected Result**: 10-minute video, $5.32 cost, 3-4 hours total

---

### Phase 2: Scale to 3 Scripts (Week 2)

**Pick**: 3 variations of same topic (contrarian, authority, transformation)

**Example**:
- `multi_agent_systems_62_percent_contrarian.md`
- `multi_agent_systems_62_percent_authority.md`
- `multi_agent_systems_62_percent_transformation.md`

**Efficiency Trick**:
- Film once, reuse footage across all 3 variations
- Generate unique AI b-roll for each variation's angle
- Total time: 6 hours (2 hours per video) instead of 12

---

### Phase 3: Batch Production (Week 3-4)

**Pick**: Remaining 20 scripts

**Strategy**: Mix approaches based on topic importance

**High-Priority (5 scripts)**: Hybrid AI + Real
- Claude Sonnet 4.5 (your main topic)
- JPMorgan case study (enterprise validation)
- Multi-agent systems (trending topic)

**Medium-Priority (10 scripts)**: Pure Kling AI
- Quick turnaround
- Test engagement
- Lower production cost

**Experimental (5 scripts)**: HeyGen Avatar
- Test avatar acceptance
- Faster scaling
- Consistent branding

---

## Tool Setup Guide

### Kling AI 2.0 Setup

1. **Sign up**: https://klingai.com
2. **Plan**: $12/month (200 credits)
3. **Usage**: ~30 credits per script (6-7 scripts per month)

**How to Use**:
```
1. Click "Video Generation"
2. Paste prompt from JSON file
3. Select "Professional Mode"
4. Duration: 10s
5. Click Generate
6. Wait 60-90 seconds
7. Download MP4
```

### Pika Labs 2.5 Setup

1. **Sign up**: https://pika.art
2. **Plan**: $12/month (unlimited)
3. **Best for**: Fast iterations, social clips

### Runway Gen-4 Setup (Optional)

1. **Sign up**: https://runwayml.com
2. **Plan**: $50/month (625 credits)
3. **Best for**: High-quality flagship content

### HeyGen Setup (Optional)

1. **Sign up**: https://heygen.com
2. **Plan**: $29/month (15 min video/month)
3. **Setup**:
   - Record 5-10 min video of yourself
   - AI creates avatar
   - Use for all scripts

---

## Descript Integration Workflow

### Import Visual Prompts to Descript

1. **Create New Project** per script
2. **Import Audio**: Record voiceover from script
3. **Import Visuals**:
   - Real footage (filmed)
   - AI-generated clips (downloaded from Kling/Pika/Runway)
   - HeyGen avatar clips (if using)

4. **Match to Timestamps**:
   - Each visual prompt has `timestamp` field
   - Align footage to those timecodes

5. **Add Captions**:
   - Descript auto-generates
   - Style for social media

6. **Export**:
   - 1080p MP4
   - YouTube-ready

---

## Cost Breakdown by Approach

### For 24 Scripts (Your Current Batch)

| Approach | Per Script | Total (24 scripts) | Time |
|----------|-----------|-------------------|------|
| Pure Kling AI | $5.70 | $136.80 | 24-48 hours |
| Pure Pika AI | $3.80 | $91.20 | 24-48 hours |
| Hybrid (Recommended) | $5.32 | $127.68 | 72-96 hours |
| HeyGen + AI | $7.00 | $168.00 | 48-72 hours |
| Real + Runway Premium | $25.00 | $600.00 | 144-192 hours |

**Recommended Budget**: $130-170 (Hybrid approach)
**Recommended Time**: 3-4 hours per script = 72-96 hours total

---

## Next Steps

### Immediate Actions (Today)

1. **Pick 1 script** to test (recommend Claude Sonnet 4.5 contrarian)
2. **Sign up for Kling AI** ($12/month)
3. **Open the visual prompt JSON** for that script
4. **Film 5 real shots** (30 minutes):
   - Intro talking head
   - Workspace b-roll
   - Screen recording
   - Detail shots
   - Outro

5. **Generate 3 AI visuals** with Kling (test quality)

### This Week

- Complete 1 full video using hybrid approach
- Evaluate quality and workflow
- Adjust prompts if needed

### Next 2 Weeks

- Batch produce 5-10 videos
- Experiment with different approaches
- Find your optimal workflow

### Month 1 Goal

- All 24 scripts produced
- Published to YouTube
- Data on what works

---

## Tips for Success

### Filming Real Footage

**Lighting**:
- Natural window light (free)
- OR ring light ($30-50)
- 3-point lighting if serious ($100-200)

**Audio**:
- Lavalier mic ($30) minimum
- Room with soft furnishings (reduces echo)

**Framing**:
- Rule of thirds
- Eye level camera
- Clean background

### AI Generation Tips

**Kling AI Best Practices**:
- Be specific about lighting ("professional studio lighting")
- Mention camera movement ("dynamic camera rotation")
- Specify aesthetic ("photorealistic", "cinematic")
- Add quality markers ("high detail", "4K quality")

**Common Mistakes**:
- Vague prompts ("show data") → Be specific ("3D bar chart rising")
- Too many elements in one prompt → Keep focused
- Unrealistic expectations → AI does abstract concepts better than complex narratives

### Descript Workflow

**Organization**:
- Name clips by timestamp (e.g., "00_30_hook_headlines.mp4")
- Create folders per script
- Use Descript's transcription for captions

**Efficiency**:
- Create template projects (save intro/outro style)
- Reuse transitions and effects
- Batch export multiple videos

---

## Troubleshooting

### "AI visual doesn't match my vision"

**Solution**: Regenerate with modified prompt
- Add more descriptive words
- Change the tool (Kling vs Pika vs Runway)
- Check the alternate prompts in JSON

### "Real footage looks amateurish"

**Solution**: Lighting + framing
- Use window light or ring light
- Frame yourself at eye level
- Clean, uncluttered background
- Test camera before filming all shots

### "Taking too long to produce"

**Solution**: Simplify approach
- Start with Pure Kling AI (fastest)
- Film fewer real shots
- Use templates in Descript
- Batch similar tasks

### "Costs adding up"

**Solution**: Optimize tool usage
- Use Pika ($12/month unlimited) instead of Runway ($50/month)
- Film more real footage (free)
- Reuse AI clips across similar scripts
- Mix 1-2 premium (Runway) with 20+ budget (Kling/Pika)

---

## Success Metrics to Track

**Per Video**:
- Production time (target: <4 hours)
- Cost (target: <$10)
- Viewer retention (YouTube Analytics)
- Engagement rate (likes, comments)

**Overall**:
- Videos published per week (target: 3-5)
- Cost per 1000 views
- Subscriber growth rate
- Which approach performs best

---

## Future Enhancements

### Automation Opportunities

1. **Auto-download AI clips** (script Kling/Pika API)
2. **Auto-import to Descript** (watch folder)
3. **Template-based assembly** (Descript templates)
4. **Batch rendering** (overnight exports)

### Quality Upgrades

1. **Professional camera** (vs smartphone)
2. **Runway Gen-4** for flagship content
3. **Motion graphics** (After Effects integration)
4. **Music + SFX** (Epidemic Sound)

---

## Summary: Your Path Forward

**Week 1**: Test 1 script, hybrid approach, $5-10, 3-4 hours

**Week 2-3**: Produce 10 scripts, mix approaches, $50-100, 30-40 hours

**Week 4**: Complete remaining 14 scripts, refine workflow

**Result**: 24 professional YouTube videos, $130-170 total, ready to publish

---

## Questions?

Refer to individual visual prompt JSON files for detailed prompts.

Check `_SUMMARY_REPORT.json` for cost breakdowns and recommendations.

All files in: `/visual_prompts/`

---

**Ready to start? Pick your first script and generate your first AI visual!**
