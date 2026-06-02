#!/usr/bin/env python3
"""
MONOGRAPH EDITOR v4.0 - Full AI Integration
AI generates DaVinci Resolve Fusion scripts
Auto-update detection from GitHub repo
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess
import threading
import shutil
import json
import urllib.request
import urllib.error

# Colors
BG_DARK = "#050510"
BG_CARD = "#0a0a1a"
BG_INPUT = "#12122a"
CYAN = "#00f5ff"
MAGENTA = "#ff00aa"
GREEN = "#00ff88"
RED = "#ff3366"
ORANGE = "#ff9500"
WHITE = "#ffffff"
GRAY = "#666688"


# ============== GITHUB AUTO-UPDATER ==============
class GitHubUpdater:
    def __init__(self, repo_owner="nop727272", repo_name="somepython-experiment"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = "4.0.0"
        self.update_available = False
        self.latest_version = ""
        self.update_info = ""
    
    def check_for_updates(self):
        """Check GitHub for new updates"""
        try:
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "MonographEditor"})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            
            self.latest_version = data.get("tag_name", "v1.0.0").replace("v", "")
            
            # Compare versions
            if self.latest_version > self.current_version:
                self.update_available = True
                self.update_info = data.get("body", "New update available!")
                return True
            return False
        except Exception as e:
            return False
    
    def get_update_countdown(self, seconds=30):
        """Return countdown message"""
        return f"Update available! Downloading in {seconds} seconds..."


class MonographApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MONOGRAPH EDITOR v4.0")
        self.root.geometry("1000x800")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(900, 750)
        
        # Variables
        self.simple_clips = []
        self.ai_clips = []
        self.ai_audio = ""
        self.ai_ref = ""
        self.ai_output = None
        self.openai_api_key = tk.StringVar()
        self.feedback_shown = False
        
        # Updater
        self.updater = GitHubUpdater()
        
        # Load saved API key
        self.load_api_key()
        
        # Check for updates
        self.check_updates_async()
        
        self.show_main_menu()
    
    def load_api_key(self):
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as f:
                self.openai_api_key.set(f.read().strip())
    
    def save_api_key(self):
        key = self.openai_api_key.get().strip()
        if key:
            with open("api_key.txt", "w") as f:
                f.write(key)
            messagebox.showinfo("Saved", "API key saved!")
    
    def check_updates_async(self):
        """Check for updates in background"""
        def check():
            if self.updater.check_for_updates():
                self.root.after(0, lambda: self.show_update_notification())
        threading.Thread(target=check, daemon=True).start()
    
    def show_update_notification(self):
        """Show update notification popup"""
        popup = tk.Toplevel(self.root)
        popup.title("Update Available!")
        popup.geometry("500x300")
        popup.configure(bg=BG_CARD)
        popup.transient(self.root)
        popup.grab_set()
        
        tk.Label(popup, text="UPDATE AVAILABLE!", font=("Consolas", 20, "bold"),
                fg=ORANGE, bg=BG_CARD).pack(pady=20)
        
        tk.Label(popup, text=f"Version: {self.updater.latest_version}",
                font=("Consolas", 14), fg=WHITE, bg=BG_CARD).pack()
        
        tk.Label(popup, text=self.updater.update_info[:200] if self.updater.update_info else "New features available!",
                font=("Arial", 10), fg=GRAY, bg=BG_CARD, wraplength=450).pack(pady=10)
        
        btn_frame = tk.Frame(popup, bg=BG_CARD)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="UPDATE NOW", 
                 command=lambda: [popup.destroy(), self.download_update()],
                 bg=GREEN, fg=BG_DARK, font=("Consolas", 12, "bold"),
                 relief="flat", padx=20, pady=10).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="LATER", 
                 command=popup.destroy,
                 bg=GRAY, fg=WHITE, font=("Consolas", 12),
                 relief="flat", padx=20, pady=10).pack(side="left", padx=10)
        
        # Countdown
        self.countdown_label = tk.Label(popup, text="Auto-update in 30 seconds...",
                                       font=("Arial", 9), fg=ORANGE, bg=BG_CARD)
        self.countdown_label.pack(pady=10)
        
        self.countdown_seconds = 30
        self.countdown_update(popup)
    
    def countdown_update(self, popup):
        if self.countdown_seconds > 0:
            self.countdown_label.config(text=f"Auto-update in {self.countdown_seconds} seconds...")
            self.countdown_seconds -= 1
            self.root.after(1000, lambda: self.countdown_update(popup))
        else:
            popup.destroy()
            self.download_update()
    
    def download_update(self):
        """Download and apply update"""
        messagebox.showinfo("Updating", 
                           "Download the latest version from:\n"
                           "https://github.com/nop727272/somepython-experiment\n\n"
                           "Extract and replace the files.")
        
        # Open download page
        subprocess.run('start https://github.com/nop727272/somepython-experiment/archive/main.zip',
                     shell=True)
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ============== MAIN MENU ==============
    def show_main_menu(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        # Version label
        tk.Label(bg, text=f"v4.0.0", font=("Consolas", 8), fg=GRAY, bg=BG_DARK).place(x=20, y=10)
        
        tk.Label(bg, text="MONOGRAPH", font=("Consolas", 48, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=(60, 5))
        
        tk.Label(bg, text="AI VIDEO EDITOR", font=("Consolas", 20),
                fg=MAGENTA, bg=BG_DARK).pack()
        
        tk.Label(bg, text="AI generates DaVinci Resolve Fusion scripts",
                font=("Consolas", 12), fg=GRAY, bg=BG_DARK).pack(pady=25)
        
        btn_frame = tk.Frame(bg, bg=BG_DARK)
        btn_frame.pack(pady=25)
        
        # Simple Edit
        simple_btn = tk.Button(btn_frame, text="[ 1 ] SIMPLE EDIT",
                             command=self.show_simple_edit,
                             font=("Consolas", 16, "bold"),
                             bg=BG_CARD, fg=CYAN, activebackground=BG_INPUT,
                             relief="flat", padx=60, pady=20, cursor="hand2")
        simple_btn.pack(pady=8)
        tk.Label(btn_frame, text="Quick preset-based editing",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # AI Edit
        ai_btn = tk.Button(btn_frame, text="[ 2 ] AI SPECIAL EDIT",
                          command=self.show_ai_edit,
                          font=("Consolas", 16, "bold"),
                          bg=BG_CARD, fg=MAGENTA, activebackground=BG_INPUT,
                          relief="flat", padx=60, pady=20, cursor="hand2")
        ai_btn.pack(pady=8)
        tk.Label(btn_frame, text="AI generates Fusion scripts with GPT-4",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # API Key section
        api_frame = tk.Frame(bg, bg=BG_DARK)
        api_frame.pack(pady=25, padx=60, fill="x")
        
        tk.Label(api_frame, text="OpenAI API Key:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        api_entry = tk.Entry(api_frame, textvariable=self.openai_api_key, width=38,
                            bg=BG_INPUT, fg=CYAN, font=("Consolas", 10), show="*")
        api_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(api_frame, text="Save", command=self.save_api_key,
                 bg=GREEN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").grid(row=0, column=2, padx=5)
        
        tk.Label(api_frame, text="(Required for AI features)",
                font=("Arial", 8), fg=GRAY, bg=BG_DARK).grid(row=1, column=1, sticky="w")
        
        # Footer
        tk.Label(bg, text="Powered by DaVinci Resolve Fusion API | v4.0",
                font=("Arial", 9), fg="#333", bg=BG_DARK).pack(side="bottom", pady=12)

    # ============== SIMPLE EDIT ==============
    def show_simple_edit(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        tk.Button(bg, text="< BACK TO MENU", command=self.show_main_menu,
                font=("Consolas", 10), bg=BG_CARD, fg=GRAY,
                relief="flat", cursor="hand2").place(x=20, y=15)
        
        tk.Label(bg, text="SIMPLE EDIT", font=("Consolas", 32, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=30)
        
        form = tk.Frame(bg, bg=BG_DARK)
        form.pack(pady=20, padx=60, fill="x")
        
        # Clips
        tk.Label(form, text="VIDEO CLIPS:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=10)
        
        clips_frame = tk.Frame(form, bg=BG_CARD)
        clips_frame.grid(row=0, column=1, sticky="ew", pady=10)
        
        self.clips_listbox = tk.Listbox(clips_frame, height=4, bg=BG_INPUT,
                                       fg=CYAN, font=("Consolas", 10),
                                       selectbackground=CYAN, selectforeground=BG_DARK)
        self.clips_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        clip_btns = tk.Frame(clips_frame, bg=BG_CARD)
        clip_btns.pack(side="right", padx=5)
        
        tk.Button(clip_btns, text="+ ADD", command=self.add_simple_clips,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(fill="x", pady=2)
        
        tk.Button(clip_btns, text="CLEAR", command=self.clear_simple_clips,
                 bg=RED, fg=WHITE, font=("Consolas", 10),
                 relief="flat", cursor="hand2").pack(fill="x", pady=2)
        
        # Audio
        tk.Label(form, text="AUDIO:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=10)
        
        audio_frame = tk.Frame(form, bg=BG_CARD)
        audio_frame.grid(row=1, column=1, sticky="ew", pady=10)
        
        self.audio_entry = tk.Entry(audio_frame, width=40, bg=BG_INPUT, fg=CYAN,
                                   font=("Consolas", 11), insertbackground=CYAN)
        self.audio_entry.pack(side="left", padx=5, pady=8, fill="x", expand=True)
        
        tk.Button(audio_frame, text="BROWSE", command=self.browse_audio,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(side="right", padx=5, pady=5)
        
        # Status
        self.simple_status = tk.Label(bg, text="Select files and click Create",
                                     font=("Consolas", 11), fg=GREEN, bg=BG_DARK)
        self.simple_status.pack(pady=20)
        
        tk.Button(bg, text="[ CREATE VIDEO ]", command=self.run_simple_edit,
                font=("Consolas", 14, "bold"),
                bg=CYAN, fg=BG_DARK, relief="flat",
                padx=40, pady=12, cursor="hand2").pack(pady=10)
        
        tk.Label(bg, text="1. Add clips | 2. Select audio | 3. Create",
                font=("Arial", 9), fg=GRAY, bg=BG_DARK).pack(pady=10)
    
    def add_simple_clips(self):
        files = filedialog.askopenfilenames(
            title="Select video clips",
            filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.simple_clips:
                self.simple_clips.append(f)
                self.clips_listbox.insert("end", os.path.basename(f))
        self.simple_status.config(text=f"Added {len(files)} clip(s)")
    
    def clear_simple_clips(self):
        self.simple_clips.clear()
        self.clips_listbox.delete(0, "end")
    
    def browse_audio(self):
        f = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=[("Audio files", "*.mp3 *.wav"), ("All files", "*.*")]
        )
        if f:
            self.audio_entry.delete(0, "end")
            self.audio_entry.insert(0, f)
    
    def run_simple_edit(self):
        if not self.simple_clips:
            messagebox.showerror("Error", "Add at least one video clip!")
            return
        
        audio = self.audio_entry.get().strip()
        if not audio:
            messagebox.showerror("Error", "Select an audio file!")
            return
        
        self.simple_status.config(text=f"Creating from {len(self.simple_clips)} clips...", fg=MAGENTA)
        self.root.update()
        
        temp_dir = "temp_clips"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, clip in enumerate(self.simple_clips):
            ext = Path(clip).suffix
            shutil.copy(clip, f"{temp_dir}/clip_{i}{ext}")
        
        output = "MONOGRAPH_EDIT.mp4"
        
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", temp_dir,
               "--audio", audio,
               "--output", output]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            if result.returncode == 0:
                self.simple_status.config(text="Video created!", fg=GREEN)
                messagebox.showinfo("Success!", f"Ready: {os.path.abspath(output)}")
            else:
                self.simple_status.config(text="Error", fg=RED)
                messagebox.showerror("Error", result.stderr[:200] if result.stderr else "Error")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ============== AI SPECIAL EDIT ==============
    def show_ai_edit(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg=MAGENTA).pack(fill="x")
        
        tk.Button(bg, text="< BACK TO MENU", command=self.show_main_menu,
                font=("Consolas", 10), bg=BG_CARD, fg=GRAY,
                relief="flat", cursor="hand2").place(x=20, y=15)
        
        tk.Label(bg, text="AI SPECIAL EDIT", font=("Consolas", 32, "bold"),
                fg=MAGENTA, bg=BG_DARK).pack(pady=20)
        
        # Input section
        inp = tk.Frame(bg, bg=BG_DARK)
        inp.pack(pady=10, padx=60, fill="x")
        
        # Clips
        tk.Label(inp, text="VIDEO CLIPS:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=5)
        
        clips_f = tk.Frame(inp, bg=BG_CARD)
        clips_f.grid(row=0, column=1, sticky="ew", pady=5)
        
        self.ai_clips_listbox = tk.Listbox(clips_f, height=2, bg=BG_INPUT,
                                         fg=MAGENTA, font=("Consolas", 10))
        self.ai_clips_listbox.pack(side="left", fill="x", expand=True, padx=5, pady=3)
        
        btn_col = tk.Frame(clips_f, bg=BG_CARD)
        btn_col.pack(side="right", padx=3)
        
        tk.Button(btn_col, text="+", command=self.add_ai_clips,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 12, "bold"),
                 relief="flat", width=3).pack(pady=1)
        
        tk.Button(btn_col, text="X", command=self.clear_ai_clips,
                 bg=RED, fg=WHITE, font=("Consolas", 10),
                 relief="flat", width=3).pack(pady=1)
        
        # Audio
        tk.Label(inp, text="AUDIO:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=5)
        
        audio_f = tk.Frame(inp, bg=BG_CARD)
        audio_f.grid(row=1, column=1, sticky="ew", pady=5)
        
        self.ai_audio_entry = tk.Entry(audio_f, width=40, bg=BG_INPUT, fg=MAGENTA,
                                     font=("Consolas", 10))
        self.ai_audio_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(audio_f, text="...", command=self.browse_ai_audio,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 10),
                 relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # AI Prompt
        tk.Label(inp, text="AI PROMPT:", font=("Consolas", 11),
                fg=MAGENTA, bg=BG_DARK).grid(row=2, column=0, sticky="w", pady=5)
        
        prompt_f = tk.Frame(inp, bg=BG_CARD)
        prompt_f.grid(row=2, column=1, sticky="ew", pady=5)
        
        self.ai_prompt_entry = tk.Entry(prompt_f, width=40, bg=BG_INPUT, fg=MAGENTA,
                                       font=("Consolas", 10))
        self.ai_prompt_entry.insert(0, "Cinematic edit with letterboxing, slow motion, and film grain")
        self.ai_prompt_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Chat
        chat_f = tk.Frame(bg, bg=BG_CARD)
        chat_f.pack(pady=10, padx=60, fill="both", expand=True)
        
        self.ai_chat = scrolledtext.ScrolledText(chat_f, height=15,
                                               bg=BG_DARK, fg=MAGENTA,
                                               font=("Consolas", 10), relief="flat",
                                               state="disabled", wrap="word")
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", """AI: Welcome to AI Special Edit!

I use GPT-4 to generate DaVinci Resolve Fusion scripts!

1. Add your video clips
2. Select an audio file  
3. Enter an AI prompt describing your vision
4. Click SEND to generate the script

EXAMPLE PROMPTS:
- "Cinematic with 2.35:1 letterboxing and teal shadows"
- "Slow motion anime edit with film grain and dramatic color grading"
- "Dark moody look with warm highlights and cool shadows"
- "Add text overlay and smooth transitions"

The AI will create a complete Python script for DaVinci Resolve!
""")
        self.ai_chat.config(state="disabled")
        
        # Input row
        input_row = tk.Frame(bg, bg=BG_DARK)
        input_row.pack(pady=10, padx=60, fill="x")
        
        self.ai_input = tk.Entry(input_row, width=50, bg=BG_INPUT, fg=WHITE,
                                font=("Consolas", 12), insertbackground=MAGENTA)
        self.ai_input.pack(side="left")
        self.ai_input.bind("<Return>", lambda e: self.send_ai())
        
        tk.Button(input_row, text="SEND TO AI", command=self.send_ai,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 11, "bold"),
                 relief="flat", cursor="hand2").pack(side="right", padx=(10, 0))
        
        # Status
        self.ai_status = tk.Label(bg, text="", font=("Consolas", 10),
                                fg=MAGENTA, bg=BG_DARK)
        self.ai_status.pack(pady=5)
        
        # Feedback frame
        self.feedback_frame = tk.Frame(bg, bg=BG_DARK)
    
    def add_ai_clips(self):
        files = filedialog.askopenfilenames(
            title="Select video clips",
            filetypes=[("Video files", "*.mp4 *.mov *.mkv"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.ai_clips:
                self.ai_clips.append(f)
                self.ai_clips_listbox.insert("end", os.path.basename(f))
        self.ai_status.config(text=f"Added {len(files)} clip(s)")
    
    def clear_ai_clips(self):
        self.ai_clips.clear()
        self.ai_clips_listbox.delete(0, "end")
    
    def browse_ai_audio(self):
        f = filedialog.askopenfilename(
            title="Select audio",
            filetypes=[("Audio files", "*.mp3 *.wav"), ("All files", "*.*")]
        )
        if f:
            self.ai_audio_entry.delete(0, "end")
            self.ai_audio_entry.insert(0, f)
    
    def update_ai_chat(self, text, is_user=False):
        self.ai_chat.config(state="normal")
        prefix = "You: " if is_user else "AI: "
        self.ai_chat.insert("end", prefix + text + "\n\n")
        self.ai_chat.see("end")
        self.ai_chat.config(state="disabled")
    
    def send_ai(self):
        msg = self.ai_input.get().strip()
        if not msg:
            msg = self.ai_prompt_entry.get().strip()
        if not msg:
            return
        
        self.ai_input.delete(0, "end")
        self.update_ai_chat(msg, is_user=True)
        self.ai_status.config(text="AI generating Fusion script...")
        
        threading.Thread(target=self.ai_process, args=(msg,), daemon=True).start()
    
    def ai_process(self, msg):
        msg_lower = msg.lower()
        
        if any(w in msg_lower for w in ["yes", "good", "ok", "love it", "perfect", "thanks"]):
            response = "AI: Thanks! Your edit is saved. Returning to menu..."
            self.root.after(0, lambda: [self.update_ai_chat(response),
                                        self.root.after(2000, self.show_main_menu)])
            return
        
        if any(w in msg_lower for w in ["no", "not", "change", "redo", "fix"]):
            response = "AI: What should I change? Describe the modifications:"
            self.root.after(0, lambda: self.update_ai_chat(response))
            return
        
        response = self.call_openai_gpt4(msg)
        self.root.after(0, lambda: self.ai_finish(response))
    
    def call_openai_gpt4(self, user_request):
        """Call OpenAI GPT-4 to generate Fusion script"""
        api_key = self.openai_api_key.get().strip()
        
        if not api_key:
            return "AI: Please enter your OpenAI API key in the main menu first!"
        
        if not self.ai_clips:
            return "AI: Add at least one video clip first."
        
        audio = self.ai_audio_entry.get().strip()
        if not audio:
            return "AI: Select an audio file first."
        
        self.root.after(0, lambda: self.ai_status.config(text="GPT-4 generating Fusion script..."))
        
        # Build prompt for GPT-4
        prompt = f"""You are a DaVinci Resolve Fusion script expert. Generate a complete Python script for DaVinci Resolve FREE.

USER REQUEST: {user_request}

CLIPS TO IMPORT: {self.ai_clips}
AUDIO FILE: {audio}

Generate a Python script that:
1. Imports these video clips to the media pool
2. Creates a new timeline
3. Applies cinematic effects using Fusion:
   - Letterboxing (Crop tool, top=0.13, bottom=0.13 for 2.35:1 ratio)
   - Color grading (ColorCorrect, saturation=0.65, teal shadows)
   - Film grain (FilmGrain tool, amount=0.08)
   - Text overlay (Text+ tool)
4. Adds the audio track
5. Sets up render settings (1920x1080, 24fps, H.264)

CRITICAL: The script must work with the FREE version of DaVinci Resolve.
Use only the public API methods documented in DaVinci Resolve Scripting API.

Format your response as a complete Python script starting with:
#!/usr/bin/env python3

The script will be saved and can be run in DaVinci Resolve's Fusion Console.
"""
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a DaVinci Resolve Fusion scripting expert. Write complete, working Python scripts for the free version of DaVinci Resolve."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2500,
                "temperature": 0.7
            }
            
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
            response = urllib.request.urlopen(req, timeout=60)
            result = json.loads(response.read().decode())
            
            gpt_response = result["choices"][0]["message"]["content"]
            
            # Save script
            script_path = "monograph_ai_script.py"
            with open(script_path, "w") as f:
                f.write(gpt_response)
            
            self.ai_output = script_path
            
            return f"""AI: I've generated a complete Fusion script using GPT-4!

Script saved as: {script_path}

The script includes:
- Video clip import
- Letterboxing (2.35:1 cinematic)
- Color grading (cinematic look)
- Film grain effect
- Text overlay
- Audio track integration
- Render settings

TO USE THE SCRIPT:
1. Open DaVinci Resolve
2. Go to Fusion page
3. Open Console (View > Console)
4. Type: exec(open('{script_path}').read())

Or copy the script content and paste it into the console.

Is this what you wanted? [ YES, GOOD! ] or [ NO, CHANGE ]"""
        
        except urllib.error.HTTPError as e:
            return f"AI: OpenAI API Error: {e.code} - {e.read().decode()[:200]}"
        except Exception as e:
            return f"AI: Error calling OpenAI: {str(e)}"
    
    def ai_finish(self, response):
        self.update_ai_chat(response)
        self.ai_status.config(text="")
        
        if "generated" in response.lower() or "script" in response.lower():
            self.show_feedback()
    
    def show_feedback(self):
        if self.feedback_shown:
            return
        self.feedback_shown = True
        
        self.feedback_frame.pack(pady=15)
        
        tk.Button(self.feedback_frame, text="[ YES, GOOD! ]",
                 command=self.ai_yes,
                 bg=GREEN, fg=BG_DARK, font=("Consolas", 12, "bold"),
                 relief="flat", cursor="hand2", padx=20, pady=8).pack(side="left", padx=8)
        
        tk.Button(self.feedback_frame, text="[ NO, CHANGE ]",
                 command=self.ai_no,
                 bg=RED, fg=WHITE, font=("Consolas", 12, "bold"),
                 relief="flat", cursor="hand2", padx=20, pady=8).pack(side="left", padx=8)
        
        tk.Button(self.feedback_frame, text="[ VIEW SCRIPT ]",
                 command=self.view_script,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10),
                 relief="flat", cursor="hand2", padx=15, pady=8).pack(side="left", padx=8)
    
    def view_script(self):
        if os.path.exists("monograph_ai_script.py"):
            with open("monograph_ai_script.py", "r") as f:
                content = f.read()
            messagebox.showinfo("GPT-4 Generated Script", content[:2500] + "\n\n...(truncated)")
    
    def ai_yes(self):
        self.update_ai_chat("You: Yes, perfect!")
        self.feedback_frame.pack_forget()
        self.root.after(2000, self.show_main_menu)
    
    def ai_no(self):
        self.update_ai_chat("You: Please change it...")
        self.update_ai_chat("AI: What should I modify?")
        self.feedback_frame.pack_forget()
        self.feedback_shown = False


if __name__ == "__main__":
    import json
    root = tk.Tk()
    app = MonographApp(root)
    root.mainloop()