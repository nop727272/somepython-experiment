# 🎬 MONOGRAPH AUTO-EDITOR - POST READY IN 3 STEPS

## WHAT THIS DOES

Automatically creates professional "monograph style" edits like the ones you referenced:
- ✅ Cinematic letterboxing (2.35:1 film bars)
- ✅ Moody color grading (teal shadows, warm highlights)
- ✅ Slow motion effects
- ✅ Beat-synced edits
- ✅ Text overlays
- ✅ Film grain effect
- ✅ Fade in/out
- ✅ Ready to POST

---

## ⚡ QUICK START (Just do these 3 things)

### Step 1: Add your video clips
```
Put your .mp4, .mov, or .avi files in the `clips/` folder
```
- More clips = more variety
- Use high quality footage (1080p or 4K)
- Can be any content (Naruto clips, action scenes, etc.)

### Step 2: Add your song
```
Rename your song to: audio.mp3
```
- Can be "Feel Good Inc" by Gorillaz
- Or any song you want

### Step 3: Run one command
```bash
./run_edit.sh
```

**That's it!** Your finished video will be `FINAL_MONOGRAPH_EDIT.mp4`

---

## 📁 FILE STRUCTURE

```
your-folder/
├── run_edit.sh                 ← RUN THIS
├── monograph-auto-editor.py    ← The editor script
├── clips/
│   ├── your_clip_1.mp4
│   ├── your_clip_2.mp4
│   ├── your_clip_3.mp4
│   └── ... (as many as you want)
├── audio.mp3                   ← Your song
└── FINAL_MONOGRAPH_EDIT.mp4    ← OUTPUT (created after running)
```

---

## 🎨 CUSTOMIZATION (Optional)

Edit `monograph-auto-editor.py` to change:

```python
# Change the title text
title_text = "NARUTO"  →  title_text = "YOUR TEXT"

# Change color grading intensity
saturation = 0.65  →  lower for more muted, higher for more vivid

# Change letterbox size (bigger = more cinematic bars)
letterbox_top = 0.13  →  0.15 for bigger bars
```

---

## 🔧 REQUIREMENTS

### Linux/Mac:
```bash
# Install ffmpeg (if not installed)
sudo apt install ffmpeg
# or
brew install ffmpeg
```

### Windows:
```powershell
# Install ffmpeg from: https://ffmpeg.org/download.html
# Or use WSL (Windows Subsystem for Linux)
```

---

## 📱 POSTING

Your `FINAL_MONOGRAPH_EDIT.mp4` is optimized for:
- ✅ YouTube (1080p, H.264)
- ✅ TikTok
- ✅ Instagram Reels
- ✅ Twitter/X
- ✅ Facebook
- ✅ Any platform!

---

## 🆘 TROUBLESHOOTING

**"No clips found"**
→ Make sure clips are in the `clips/` folder with .mp4, .mov, or .avi extension

**"Audio file not found"**
→ Rename your song to exactly `audio.mp3`

**"ffmpeg not found"**
→ Install ffmpeg: `sudo apt install ffmpeg`

**Low quality output?**
→ The editor uses high quality encoding by default. If you need more quality, open the Python script and lower the CRF value: `-crf '18'` → `-crf '15'`

---

## 💡 TIPS FOR BEST RESULTS

1. **Use 5-10 clips** for good variety
2. **Match clip energy to song sections:**
   - Slow parts (intro/outro) → Slow, dramatic clips
   - Fast parts (chorus) → Action-packed clips
3. **Use consistent quality** - don't mix 480p with 4K footage
4. **Horizontal clips work best** - vertical may have black bars on sides

---

## 📄 FILES INCLUDED

| File | Purpose |
|------|---------|
| `run_edit.sh` | ONE-CLICK POST - Run this! |
| `monograph-auto-editor.py` | Main editor script |
| `monograph-davinci-tutorial.html` | Visual tutorial (view in browser) |
| `monograph-preset.lua` | DaVinci Resolve preset |
| `clips/` | Put your clips here |
| `audio.mp3` | Put your song here |

---

**Enjoy your post-ready edit! 🎉**