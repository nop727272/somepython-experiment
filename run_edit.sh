#!/bin/bash
# ============================================================
# MONOGRAPH EDITOR - ONE-CLICK POST SYSTEM
# ============================================================
# 
# JUST ADD YOUR FILES AND RUN THIS SCRIPT!
#
# Files needed in the same folder as this script:
#   1. clips/ folder with your video clips (.mp4, .mov, .avi)
#   2. audio.mp3 (the song you want to use)
#
# That's it! Run: ./run_edit.sh
# ============================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║       MONOGRAPH AUTO-EDITOR - POST READY EDITS          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}❌ FFmpeg not found!${NC}"
    echo "Installing ffmpeg..."
    apt-get update && apt-get install -y ffmpeg
fi

# Create clips folder if not exists
mkdir -p clips

# Check for clips
CLIP_COUNT=$(ls -1 clips/*.mp4 clips/*.mov clips/*.avi clips/*.mkv 2>/dev/null | wc -l)
if [ "$CLIP_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No clips found in 'clips' folder!${NC}"
    echo "   Please add your video clips to the 'clips' folder"
    echo "   Supported formats: .mp4, .mov, .avi, .mkv"
    exit 1
fi

echo -e "${GREEN}✓ Found $CLIP_COUNT clips${NC}"

# Check for audio
if [ ! -f "audio.mp3" ]; then
    echo -e "${YELLOW}⚠️  No audio.mp3 found!${NC}"
    echo "   Please add your audio file as 'audio.mp3'"
    exit 1
fi

echo -e "${GREEN}✓ Audio found: audio.mp3${NC}"

# Get clip list
CLIPS=""
for clip in clips/*.mp4 clips/*.mov clips/*.avi clips/*.mkv; do
    if [ -f "$clip" ]; then
        if [ -z "$CLIPS" ]; then
            CLIPS="$clip"
        else
            CLIPS="$CLIPS,$clip"
        fi
    fi
done

echo ""
echo -e "${BLUE}🎬 Starting automated edit...${NC}"
echo ""

# Run the Python editor
python3 monograph-auto-editor.py \
    --clips "$CLIPS" \
    --audio "audio.mp3" \
    --output "FINAL_MONOGRAPH_EDIT.mp4" \
    --title "NARUTO" \
    2>&1

# Check result
if [ -f "FINAL_MONOGRAPH_EDIT.mp4" ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗"
    echo "║                    🎉 EDIT COMPLETE! 🎉                       ║"
    echo "╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "📤 Your video is ready: ${GREEN}FINAL_MONOGRAPH_EDIT.mp4${NC}"
    echo ""
    echo "You can now upload this video directly to:"
    echo "  • YouTube"
    echo "  • TikTok"
    echo "  • Instagram Reels"
    echo "  • Twitter/X"
    echo "  • Any other platform!"
    echo ""
    
    # Show file size
    SIZE=$(du -h "FINAL_MONOGRAPH_EDIT.mp4" | cut -f1)
    echo "📊 File size: $SIZE"
else
    echo ""
    echo -e "${RED}❌ Edit failed!${NC}"
    echo "Please check the error messages above."
    exit 1
fi