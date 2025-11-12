# Quick Start: Generate Your First Video B-Roll (30 Minutes)

## Goal
Create AI-generated B-roll for one script in the next 30 minutes using the visual prompts we generated.

---

## Step 1: Pick Your Script (1 minute)

**Recommended**: Start with `2025-11-10_claude_sonnet_45_30_hours_autonomous_contrarian.md`

Why? It's about Claude's breakthrough feature - highly relevant to you.

---

## Step 2: Open Your Visual Prompts (1 minute)

**Location**:
```
/visual_prompts/2025-11-10_claude_sonnet_45_30_hours_autonomous_contrarian_visual_prompts.json
```

**What's inside**:
- 19 visual moments
- Each with 5 different prompt options
- Timecoded to your script

---

## Step 3: Sign Up for Kling AI (3 minutes)

**Why Kling**: Best balance of quality ($0.30/visual) vs cost vs speed

**Action**:
1. Go to https://klingai.com
2. Sign up (email or Google)
3. Choose plan: $12/month (200 credits = ~65 videos)
4. OR try free tier first (10 credits = ~3 videos)

---

## Step 4: Generate Your First 3 Visuals (20 minutes)

### Visual #1: Hook - Claude Headlines

**From your JSON file**, find this visual:
```json
{
  "section": "HOOK",
  "timestamp": "0:00-0:30",
  "description": "Typical claude_ai headlines",
  "prompts": {
    "kling": {
      "prompt": "Photorealistic scene: Typical claude_ai headlines. Natural lighting, camera movement, high detail, cinematic framing"
    }
  }
}
```

**Action**:
1. Copy the `kling.prompt` text
2. In Kling AI, click "Video Generation"
3. Paste the prompt
4. Settings: Professional Mode, 10s duration
5. Click "Generate"
6. Wait 60-90 seconds
7. Download the MP4

**Save as**: `00_30_hook_headlines.mp4`

---

### Visual #2: Key Stat Reveal

**Find this in your JSON**:
```json
{
  "section": "HOOK",
  "description": "Key stat appearing - \"30 hours autonomous operation (vs 7 hours before)\"",
  "prompts": {
    "kling": {
      "prompt": "Professional data visualization: Key stat appearing stat. Clean minimalist design, subtle animations, corporate aesthetic, 4K quality, smooth transitions"
    }
  }
}
```

**Action**: Same as Visual #1
- Copy prompt
- Generate in Kling
- Download

**Save as**: `00_30_key_stat.mp4`

---

### Visual #3: System Dashboard

**Find this in your JSON**:
```json
{
  "description": "System dashboard",
  "prompts": {
    "kling": {
      "prompt": "Realistic tech environment: System dashboard. Modern office setting, actual screens displaying data, natural lighting, professional workspace"
    }
  }
}
```

**Action**: Same process
**Save as**: `01_00_system_dashboard.mp4`

---

## Step 5: Review Your Results (5 minutes)

You now have 3 AI-generated B-roll clips!

**Check**:
- Quality matches your expectations?
- Visuals fit the script context?
- Any adjustments needed?

**If you're happy**: Continue generating the remaining 16 visuals
**If not**: Try the Pika or Runway prompts instead

---

## Next Steps

### Option A: Generate All 19 Visuals (2 hours)

Repeat Step 4 for all visuals in your JSON file.

**Result**: Complete B-roll package for your first video
**Cost**: $5.70 (if using all Kling prompts)

---

### Option B: Mix AI + Real Footage (3 hours)

**Film yourself** (30 min):
- Intro talking head: "I'm Liz, and I build autonomous AI systems"
- Outro: "Drop a comment: What's the first task you're automating?"
- 1-2 workspace shots

**Generate AI** for the rest (1.5 hours):
- Abstract concepts (autonomous operation, system architecture)
- Data visualizations
- Comparisons

**Assemble in Descript** (1 hour):
- Import all clips
- Match to script timestamps
- Add captions
- Export

**Result**: More authentic, engaging video
**Cost**: $3-4 (fewer AI visuals needed)

---

### Option C: Test Different Tools (1 hour)

Generate the SAME visual with all 3 tools to compare:

**Pick one visual**, generate with:
1. **Kling** (photorealistic, $0.30)
2. **Pika** (social media style, $0.20)
3. **Runway** (cinematic premium, $1.25) - if you want to test quality

**Compare**: Which style fits your brand best?

---

## Pro Tips

### Organizing Your Files

Create a folder structure:
```
/B-roll/
  /claude_sonnet_45_contrarian/
    /00_30_hook/
      00_30_hook_headlines.mp4
      00_30_key_stat.mp4
    /01_00_intro/
      01_00_system_dashboard.mp4
    /03_30_what_works/
      ...
```

### Batch Generating

Don't wait for each visual to finish:
1. Queue up 5-10 generations at once
2. Kling processes them in parallel
3. Come back in 10 minutes, download all

### Iterating on Prompts

If a visual doesn't match your vision:
1. Look at the other tool prompts (Runway, Pika)
2. Modify the prompt slightly:
   - Add "dark theme" or "light theme"
   - Change camera angle ("overhead view", "close-up")
   - Adjust mood ("professional", "dynamic", "minimalist")
3. Regenerate

---

## Common Questions

**Q: Which tool should I start with?**
A: Kling AI - best value at $0.30/visual, photorealistic quality

**Q: Can I use free tools?**
A: Kling has 10 free credits (3 videos). Pika has limited free tier. Enough to test!

**Q: What if I don't like the AI style?**
A: Try mixing with real footage. Film yourself + use AI for abstract concepts only.

**Q: How long does it take to generate?**
A: 60-90 seconds per visual with Kling. Batch 10 visuals = 15 minutes total.

**Q: Can I customize the prompts?**
A: Yes! The JSON prompts are starting points. Modify to match your vision.

---

## Success Checklist

After 30 minutes, you should have:

- ✅ Kling AI account set up
- ✅ 3 AI-generated B-roll clips downloaded
- ✅ Understanding of the workflow
- ✅ Decision on which approach to use (Pure AI, Hybrid, etc.)

**Next**: Generate the remaining visuals and assemble your first video!

---

## Your First Video Timeline

**Today (30 min)**: Generate 3 test visuals ✅

**This Week**:
- Day 1: Generate all 19 visuals (2 hours)
- Day 2: Film real footage if using hybrid (1 hour)
- Day 3: Assemble in Descript (2 hours)
- Day 4: Review, adjust, export
- Day 5: Publish to YouTube

**Result**: Your first complete video using the new B-roll system

---

**Ready? Open your visual prompt JSON file and start generating!**

File: `/visual_prompts/2025-11-10_claude_sonnet_45_30_hours_autonomous_contrarian_visual_prompts.json`
