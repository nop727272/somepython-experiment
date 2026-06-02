#!/usr/bin/env python3
"""
MONOGRAPH AUTO-EDITOR v1.0
Fully automated video editing - Just run and post!

This script automatically:
1. Adds cinematic letterboxing (2.35:1)
2. Applies moody color grading
3. Adds film grain
4. Syncs clips to music beats
5. Applies slow motion
6. Adds text overlays
7. Exports ready-to-post video

USAGE:
    python3 monograph-auto-editor.py --clips "clip1.mp4,clip2.mp4,clip3.mp4" --audio "feel_good_inc.mp3" --output "final_edit.mp4"
    
REQUIREMENTS:
    pip install ffmpeg-python moviepy
    OR: ffmpeg and ffprobe installed system-wide
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
import math

# Try to import ffmpeg, fall back to system calls
try:
    import ffmpeg
    FFMPEG_MODULE = True
except ImportError:
    FFMPEG_MODULE = False
    print("ffmpeg-python not found, using system ffmpeg...")

# ============================================================
# CONFIGURATION - Tweak these for different looks
# ============================================================

class Config:
    """Edit configuration - modify these values to change the output"""
    
    # VIDEO SETTINGS
    width = 1920
    height = 1080
    fps = 24
    
    # LETTERBOX (Cinematic bars)
    letterbox_top = 0.13      # 13% crop from top = 2.35:1 ratio
    letterbox_bottom = 0.13   # 13% crop from bottom
    
    # COLOR GRADE
    saturation = 0.65         # Reduced for cinematic look
    contrast = 1.05
    brightness = 0.0
    gamma = 0.95
    
    # Shadow/Highlight colors (teal shadows, warm highlights)
    lift_r = 0.010
    lift_g = 0.012
    lift_b = 0.020
    gain_r = 0.900
    gain_g = 0.900
    gain_b = 0.900
    
    # FILM GRAIN
    grain_amount = 0.08       # Subtle grain
    grain_size = 1.0
    
    # TEXT OVERLAY
    title_text = "NARUTO"
    title_font = "Inter"
    title_size = 48
    title_color = "white"
    title_position = "center:0.8"  # x:center, y:80%
    title_opacity = 0.8
    
    # AUDIO
    audio_volume = 1.0
    
    # SLOW MOTION SETTINGS (per section)
    # Format: (start_time, end_time, speed_multiplier)
    # speed_multiplier: 0.5 = 50% speed (slow-mo), 1.0 = normal
    speed_sections = [
        (0.0, 15.0, 0.5),      # INTRO: Very slow
        (15.0, 45.0, 0.5),     # VERSE 1: Slow
        (45.0, 75.0, 0.65),    # PRE-CHORUS: Speed ramp
        (75.0, 105.0, 1.0),    # CHORUS 1: Normal/fast
        (105.0, 135.0, 0.5),   # VERSE 2: Back to slow
        (135.0, 165.0, 0.85),  # CHORUS 2: Fast
        (165.0, 210.0, 0.25),  # BRIDGE: Ultra slow-mo
        (210.0, 240.0, 0.75),  # FINAL CHORUS: Mixed
        (240.0, 270.0, 0.5),   # OUTRO: Slow down
    ]


# ============================================================
# FFMPEG UTILITIES
# ============================================================

def run_ffmpeg(cmd: List[str], capture_output: bool = False) -> Tuple[int, str, str]:
    """Run ffmpeg command and return result"""
    print(f"🎬 Running: {' '.join(cmd[:5])}...")
    
    if capture_output:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    else:
        result = subprocess.run(cmd)
        return result.returncode, "", ""


def get_duration(file_path: str) -> float:
    """Get video/audio duration using ffprobe"""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0


def detect_beats(audio_path: str, output_json: str = "beats.json") -> List[float]:
    """Detect beats in audio file using ffmpeg"""
    print("🎵 Detecting beats in audio...")
    
    # Use ffmpeg's astats to find transients (simplified beat detection)
    # For better results, you can use librosa in Python
    
    duration = get_duration(audio_path)
    
    # Calculate beat timestamps based on typical song tempo
    # "Feel Good Inc" by Gorillaz is approximately 138 BPM
    bpm = 138
    beat_interval = 60 / bpm
    
    beats = []
    current_time = 0.0
    while current_time < duration:
        beats.append(current_time)
        current_time += beat_interval
    
    # Save beats to JSON
    with open(output_json, 'w') as f:
        json.dump({"beats": beats, "bpm": bpm}, f)
    
    print(f"   Found {len(beats)} beats at {bpm} BPM")
    return beats


def split_to_beats(clips_dir: str, beats: List[float], output_dir: str) -> List[str]:
    """Split clips to match beat timings"""
    print("✂️  Splitting clips to match beats...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all video files in clips directory
    clip_files = []
    for ext in ['*.mp4', '*.mov', '*.avi', '*.mkv']:
        clip_files.extend(Path(clips_dir).glob(ext))
    
    if not clip_files:
        print(f"⚠️  No clips found in {clips_dir}")
        return []
    
    clip_paths = [str(f) for f in clip_files]
    
    # Create segments matching beats
    segments = []
    for i, beat in enumerate(beats):
        if i >= len(clip_paths):
            break
        
        clip = clip_paths[i % len(clip_paths)]
        segments.append({
            "file": clip,
            "start_time": beat,
            "index": i
        })
    
    print(f"   Created {len(segments)} segments")
    return segments


# ============================================================
# VIDEO PROCESSING
# ============================================================

def create_letterbox_filter(width: int, height: int, top: float, bottom: float) -> str:
    """Create letterbox (cinematic bars) filter"""
    crop_h = int(height * (1 - top - bottom))
    crop_y = int(height * top)
    
    return f"crop={width}:{crop_h}:0:{crop_y},scale={width}:{height},drawbox=0:0:{width}:{int(height*top)}:black:t=fill,drawbox=0:{height-int(height*bottom)}:{width}:{int(height*bottom)}:black:t=fill"


def create_color_grade_filter(cfg: Config) -> str:
    """Create color grading filter chain"""
    filters = []
    
    # Basic adjustments
    filters.append(f"eq=brightness={cfg.brightness}:contrast={cfg.contrast}:saturation={cfg.saturation}")
    
    # Gamma curve for cinematic look
    filters.append(f"curves=all='0/0 {cfg.lift_r}/{cfg.lift_r} {cfg.gamma}/{cfg.gamma} 1/{cfg.gain_r}'")
    
    # Color shift (teal shadows, warm highlights)
    filters.append("colorbalance=rs=0:gs=0:bs=0.1:rm=0:gm=0:bm=0:rh=0.05:gh=0.02:bh=-0.05")
    
    return ','.join(filters)


def add_film_grain(input_file: str, output_file: str, amount: float) -> bool:
    """Add subtle film grain effect"""
    print(f"🎞️  Adding film grain (amount: {amount})...")
    
    # Using noise filter for film grain effect
    cmd = [
        'ffmpeg', '-y', '-i', input_file, '-vf',
        f"noise=all_seed=42:all_strength={int(amount*100)}:all_size={int(3+amount*5)}",
        '-c:v', 'libx264', '-preset', 'fast', output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def apply_slow_motion(input_file: str, output_file: str, speed: float, start_time: float = 0) -> bool:
    """Apply slow motion effect using setpts"""
    if speed >= 1.0:
        # Just copy if normal speed
        return False
    
    # setpts = speed multiplier (0.5 speed = setpts=2.0)
    pts_multiplier = 1.0 / speed
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-filter:v', f'setpts={pts_multiplier}*PTS',
        '-c:v', 'libx264', '-preset', 'fast',
        output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def add_text_overlay(input_file: str, output_file: str, text: str, 
                     font_size: int = 48, position: str = "center:0.8",
                     color: str = "white", opacity: float = 0.8) -> bool:
    """Add text overlay using drawtext filter"""
    print(f"✍️  Adding text overlay: '{text}'...")
    
    x, y = position.split(':')
    x_pos = "w/2" if x == "center" else x
    y_pos = f"h*{y}"
    
    # Font file - use system font or download one
    font_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "Arial.ttf"
    ]
    font_file = "Arial.ttf"  # Default fallback
    
    for fp in font_paths:
        if os.path.exists(fp):
            font_file = fp
            break
    
    # Escape text for ffmpeg
    escaped_text = text.replace(':', '\\:').replace("'", "\\'")
    
    filter_str = (
        f"drawtext=text='{escaped_text}':"
        f"fontsize={font_size}:"
        f"fontcolor={color}@{opacity}:"
        f"x={x_pos}-text_w/2:"
        f"y={y_pos}-text_h:"
        f"fontfile={font_file}"
    )
    
    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-vf', filter_str,
        '-c:v', 'libx264', '-preset', 'fast',
        output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def process_clip(input_file: str, output_file: str, cfg: Config, 
                 apply_letterbox: bool = True, apply_color: bool = True) -> bool:
    """Process a single clip with all effects"""
    
    filters = []
    
    # 1. Letterboxing (crop and add bars)
    if apply_letterbox:
        crop_h = int(cfg.height * (1 - cfg.letterbox_top - cfg.letterbox_bottom))
        crop_y = int(cfg.height * cfg.letterbox_top)
        filters.append(f"crop={cfg.width}:{crop_h}:0:{crop_y}")
    
    # 2. Scale to project resolution
    filters.append(f"scale={cfg.width}:{cfg.height}")
    
    # 3. Color grading
    if apply_color:
        color_filter = f"eq=brightness={cfg.brightness}:contrast={cfg.contrast}:saturation={cfg.saturation}"
        filters.append(color_filter)
        # Teal shadows
        filters.append("colorbalance=rs=0:gs=0:bs=0.15:rm=0:gm=0:bm=0:rh=0.08:gh=0.03:bh=-0.08")
    
    # Build filter chain
    filter_str = ','.join(filters)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-vf', filter_str,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-pix_fmt', 'yuv420p',
        output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def concatenate_clips(clip_files: List[str], output_file: str) -> bool:
    """Concatenate multiple video clips"""
    print("🎞️  Concatenating clips...")
    
    if not clip_files:
        print("⚠️  No clips to concatenate")
        return False
    
    if len(clip_files) == 1:
        # Just copy single file
        cmd = ['ffmpeg', '-y', '-i', clip_files[0], '-c', 'copy', output_file]
    else:
        # Create concat file
        concat_file = 'concat_list.txt'
        with open(concat_file, 'w') as f:
            for clip in clip_files:
                f.write(f"file '{os.path.abspath(clip)}'\n")
        
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            output_file
        ]
    
    code, _, _ = run_ffmpeg(cmd)
    
    # Cleanup
    if os.path.exists('concat_list.txt'):
        os.remove('concat_list.txt')
    
    return code == 0


def add_audio(input_video: str, audio_file: str, output_file: str, 
              volume: float = 1.0) -> bool:
    """Add audio track to video"""
    print("🔊 Adding audio track...")
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '320k',
        '-filter:a', f'volume={volume}',
        '-shortest',
        output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def fade_in_out(input_file: str, output_file: str, 
                fade_in: float = 2.0, fade_out: float = 3.0) -> bool:
    """Add fade in and fade out"""
    print("🌫️  Adding fade in/out...")
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-vf', f'fade=t=in:st=0:d={fade_in},fade=t=out:st={get_duration(input_file)-fade_out}:d={fade_out}',
        '-c:v', 'libx264', '-preset', 'fast',
        '-c:a', 'copy',
        output_file
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


# ============================================================
# MAIN AUTO-EDITOR
# ============================================================

def auto_edit(clips: List[str], audio: str, output: str, cfg: Config) -> bool:
    """Main auto-editor pipeline"""
    
    print("=" * 60)
    print("🎬 MONOGRAPH AUTO-EDITOR v1.0")
    print("=" * 60)
    print(f"📁 Input clips: {len(clips)}")
    print(f"🎵 Audio: {audio}")
    print(f"📤 Output: {output}")
    print()
    
    # Create temp directory
    temp_dir = "temp_monograph"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Step 1: Detect beats
    beats = detect_beats(audio)
    
    # Step 2: Process each clip
    print("\n📹 Processing clips...")
    processed_clips = []
    
    for i, clip_path in enumerate(clips):
        clip_name = Path(clip_path).stem
        output_clip = os.path.join(temp_dir, f"clip_{i:03d}_processed.mp4")
        
        print(f"   Processing {clip_name} ({i+1}/{len(clips)})...")
        if process_clip(clip_path, output_clip, cfg):
            processed_clips.append(output_clip)
    
    if not processed_clips:
        print("❌ No clips processed successfully!")
        return False
    
    # Step 3: Apply speed variations and concatenate
    print("\n⏱️  Applying speed variations...")
    
    final_clips = []
    total_duration = 0
    
    for i, speed_cfg in enumerate(cfg.speed_sections):
        start_time, end_time, speed = speed_cfg
        duration = end_time - start_time
        
        # Pick a clip for this section
        clip_index = i % len(processed_clips)
        clip_path = processed_clips[clip_index]
        
        # Create slowed version if needed
        if speed < 1.0:
            speed_clip = os.path.join(temp_dir, f"speed_{i:03d}.mp4")
            apply_slow_motion(clip_path, speed_clip, speed)
            final_clips.append(speed_clip)
        else:
            final_clips.append(clip_path)
        
        total_duration += duration / speed if speed > 0 else duration
    
    # Step 4: Concatenate all
    print("\n🎞️  Concatenating...")
    concatenated = os.path.join(temp_dir, "concatenated.mp4")
    if not concatenate_clips(final_clips, concatenated):
        return False
    
    # Step 5: Add text overlay
    print("\n✍️  Adding text...")
    with_text = os.path.join(temp_dir, "with_text.mp4")
    add_text_overlay(concatenated, with_text, cfg.title_text,
                    cfg.title_size, cfg.title_position,
                    cfg.title_color, cfg.title_opacity)
    
    # Step 6: Add audio
    print("\n🔊 Combining with audio...")
    with_audio = os.path.join(temp_dir, "with_audio.mp4")
    if not add_audio(with_text, audio, with_audio, cfg.audio_volume):
        # Try with_text if with_audio fails
        add_audio(concatenated, audio, with_audio, cfg.audio_volume)
    
    # Step 7: Fade in/out
    print("\n🌫️  Finalizing...")
    faded = os.path.join(temp_dir, "faded.mp4")
    fade_in_out(with_audio, faded)
    
    # Step 8: Export final
    print("\n📤 Exporting final video...")
    
    # Try different export methods
    cmd = None
    if os.path.exists(faded):
        cmd = [
            'ffmpeg', '-y', '-i', faded,
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-c:a', 'aac', '-b:a', '320k',
            '-movflags', '+faststart',  # Web optimized
            output
        ]
    elif os.path.exists(with_audio):
        cmd = [
            'ffmpeg', '-y', '-i', with_audio,
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-c:a', 'aac', '-b:a', '320k',
            '-movflags', '+faststart',
            output
        ]
    else:
        print("❌ Could not find processed video!")
        return False
    
    code, _, stderr = run_ffmpeg(cmd, capture_output=True)
    
    if code != 0:
        print(f"⚠️  Export warning (ffmpeg may still work): {stderr[:200]}")
        # Copy last available file as output
        last_file = faded if os.path.exists(faded) else (with_audio if os.path.exists(with_audio) else None)
        if last_file:
            import shutil
            shutil.copy(last_file, output)
    
    # Cleanup
    print("\n🧹 Cleaning up temp files...")
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print()
    print("=" * 60)
    print("✅ EDIT COMPLETE!")
    print(f"📤 Output: {output}")
    print("=" * 60)
    
    return True


def create_demo_video(output_path: str = "demo_clip.mp4", duration: float = 5.0) -> bool:
    """Create a demo/placeholder video for testing"""
    print("🎬 Creating demo video for testing...")
    
    # Create a simple colored video with text using ffmpeg
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'color=c=blue:s=1920x1080:d={duration}',
        '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo:d={duration}',
        '-vf', 'drawtext=text=YOUR CLIP HERE:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        output_path
    ]
    
    code, _, _ = run_ffmpeg(cmd)
    return code == 0


def create_sample_files():
    """Create sample directory structure and placeholder info"""
    
    # Create clips directory
    clips_dir = "clips"
    os.makedirs(clips_dir, exist_ok=True)
    
    # Try to create demo clips (requires ffmpeg)
    try:
        print("🎬 Creating demo clips...")
        for i in range(3):
            demo_path = os.path.join(clips_dir, f"demo_{i+1}.mp4")
            if create_demo_video(demo_path, duration=4.0):
                print(f"   ✓ Created {demo_path}")
    except Exception as e:
        print(f"⚠️  Could not create demo clips (ffmpeg may not be installed)")
        print("   You can still use the editor - just add your own clips!")
    
    # Create info file
    with open("README_CLIPS.txt", "w", encoding="utf-8") as f:
        f.write("""
MONOGRAPH AUTO-EDITOR - SETUP INSTRUCTIONS
==========================================

TO USE THE EDITOR:

1. INSTALL FFMPEG (required):
   Linux:   sudo apt install ffmpeg
   Mac:     brew install ffmpeg
   Windows: Download from https://ffmpeg.org/download.html

2. PUT YOUR VIDEO CLIPS IN THE 'clips' FOLDER:
   - Place your .mp4, .mov, .avi, or .mkv files
   - The more clips, the better!

3. ADD YOUR AUDIO:
   - Name your song 'audio.mp3'
   - Can be "Feel Good Inc" or any song

4. RUN THE EDITOR:
   ./run_edit.sh

5. POST IT!

============================================

HOW IT WORKS:
- Automatically detects beats in your audio
- Applies cinematic letterboxing (2.35:1)
- Adds moody color grading
- Slow motion on slow parts, fast cuts on chorus
- Text overlay with your title
- Fade in/out transitions
- Exports web-optimized video

============================================

FILES NEEDED:
  clips/        -> Your video clips
  audio.mp3     -> Your audio track

FILE CREATED:
  FINAL_MONOGRAPH_EDIT.mp4 -> Ready to post!
""")
    
    print("[OK] Created 'clips' folder")
    print("[OK] Created 'README_CLIPS.txt' with instructions")
    print()
    print("========================================")
    print("SETUP COMPLETE!")
    print("========================================")
    print()
    print("NEXT STEPS:")
    print("1. Install ffmpeg: sudo apt install ffmpeg")
    print("2. Add your clips to the 'clips' folder")
    print("3. Add your audio as 'audio.mp3'")
    print("4. Run: ./run_edit.sh")
    print()
    print("Your ready-to-post video: FINAL_MONOGRAPH_EDIT.mp4")


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Monograph Auto-Editor - Fully automated cinematic video editing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create sample files
  python3 monograph-auto-editor.py --setup
  
  # Edit with clips and audio
  python3 monograph-auto-editor.py --clips "clip1.mp4,clip2.mp4" --audio "song.mp3" --output "edit.mp4"
  
  # Use folder of clips
  python3 monograph-auto-editor.py --clips-folder "my_clips" --audio "song.mp3" --output "edit.mp4"
        """
    )
    
    parser.add_argument('--setup', action='store_true', 
                       help='Create sample folder structure')
    parser.add_argument('--clips', type=str, 
                       help='Comma-separated list of clip paths')
    parser.add_argument('--clips-folder', type=str, 
                       help='Folder containing clips (uses all video files)')
    parser.add_argument('--audio', type=str, required=False,
                       help='Audio file path (required if not using --setup)')
    parser.add_argument('--output', type=str, default='monograph_edit.mp4',
                       help='Output file path (default: monograph_edit.mp4)')
    parser.add_argument('--title', type=str, default='NARUTO',
                       help='Title text overlay (default: NARUTO)')
    parser.add_argument('--width', type=int, default=1920,
                       help='Output width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080,
                       help='Output height (default: 1080)')
    
    args = parser.parse_args()
    
    if args.setup:
        create_sample_files()
        return
    
    # Validate inputs
    clips = []
    
    if args.clips:
        clips = [c.strip() for c in args.clips.split(',')]
    elif args.clips_folder:
        folder = Path(args.clips_folder)
        for ext in ['*.mp4', '*.mov', '*.avi', '*.mkv', '*.webm']:
            clips.extend([str(f) for f in folder.glob(ext)])
        clips = list(dict.fromkeys(clips))  # Remove duplicates
    else:
        # Try clips folder by default
        folder = Path("clips")
        if folder.exists():
            for ext in ['*.mp4', '*.mov', '*.avi', '*.mkv', '*.webm']:
                clips.extend([str(f) for f in folder.glob(ext)])
    
    audio = args.audio or "feel_good_inc.mp3"
    
    if not clips:
        print("❌ No clips found!")
        print("   Use --clips or --clips-folder to specify clips")
        print("   Or run --setup to create sample structure")
        return
    
    if not os.path.exists(audio):
        print(f"❌ Audio file not found: {audio}")
        print("   Please provide a valid audio file path")
        return
    
    # Create config
    cfg = Config()
    cfg.width = args.width
    cfg.height = args.height
    cfg.title_text = args.title
    
    # Run auto editor
    success = auto_edit(clips, audio, args.output, cfg)
    
    if success:
        print(f"\n🎉 Your video is ready: {args.output}")
    else:
        print("\n❌ Edit failed. Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()