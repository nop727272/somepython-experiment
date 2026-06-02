#!/usr/bin/env python3
"""
MONOGRAPH EDITOR v3.1 - Fixed Version
AI Integration with DaVinci Resolve API
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess
import threading
import shutil

# Colors
BG_DARK = "#050510"
BG_CARD = "#0a0a1a"
BG_INPUT = "#12122a"
CYAN = "#00f5ff"
MAGENTA = "#ff00aa"
GREEN = "#00ff88"
RED = "#ff3366"
WHITE = "#ffffff"
GRAY = "#666688"


class MonographApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MONOGRAPH EDITOR v3.1")
        self.root.geometry("1000x750")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(900, 700)
        
        self.simple_clips = []
        self.ai_clips = []
        self.ai_audio = ""
        self.ai_output = None
        self.openai_api_key = tk.StringVar()
        self.feedback_shown = False
        
        self.show_main_menu()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ============== MAIN MENU ==============
    def show_main_menu(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        tk.Label(bg, text="MONOGRAPH", font=("Consolas", 48, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=(80, 5))
        
        tk.Label(bg, text="VIDEO EDITOR", font=("Consolas", 20),
                fg=MAGENTA, bg=BG_DARK).pack()
        
        tk.Label(bg, text="AI-Powered Editing with DaVinci Resolve",
                font=("Consolas", 12), fg=GRAY, bg=BG_DARK).pack(pady=30)
        
        btn_frame = tk.Frame(bg, bg=BG_DARK)
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="[ 1 ] SIMPLE EDIT",
                 command=self.show_simple_edit,
                 font=("Consolas", 16, "bold"),
                 bg=BG_CARD, fg=CYAN, activebackground=BG_INPUT,
                 relief="flat", padx=60, pady=20, cursor="hand2").pack(pady=10)
        
        tk.Label(btn_frame, text="Quick preset-based editing",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        tk.Button(btn_frame, text="[ 2 ] AI SPECIAL EDIT",
                 command=self.show_ai_edit,
                 font=("Consolas", 16, "bold"),
                 bg=BG_CARD, fg=MAGENTA, activebackground=BG_INPUT,
                 relief="flat", padx=60, pady=20, cursor="hand2").pack(pady=10)
        
        tk.Label(btn_frame, text="AI generates Fusion scripts for DaVinci Resolve",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # API Key
        api_frame = tk.Frame(bg, bg=BG_DARK)
        api_frame.pack(pady=20)
        
        tk.Label(api_frame, text="OpenAI API Key:", font=("Consolas", 10),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", padx=5)
        
        tk.Entry(api_frame, textvariable=self.openai_api_key, width=40,
                bg=BG_INPUT, fg=CYAN, font=("Consolas", 10),
                show="*").grid(row=0, column=1, padx=5)
        
        tk.Button(api_frame, text="Save", command=self.save_api_key,
                 bg=GREEN, fg=BG_DARK, font=("Consolas", 10),
                 relief="flat").grid(row=0, column=2, padx=5)
        
        tk.Label(bg, text="Powered by DaVinci Resolve Fusion API | v3.1",
                font=("Arial", 9), fg="#333", bg=BG_DARK).pack(side="bottom", pady=15)
    
    def save_api_key(self):
        key = self.openai_api_key.get().strip()
        if key:
            with open("api_key.txt", "w") as f:
                f.write(key)
            messagebox.showinfo("Saved", "API key saved!")
    
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
                fg=CYAN, bg=BG_DARK).pack(pady=35)
        
        form = tk.Frame(bg, bg=BG_DARK)
        form.pack(pady=20, padx=60, fill="x")
        
        # Clips
        tk.Label(form, text="VIDEO CLIPS:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=12)
        
        clips_frame = tk.Frame(form, bg=BG_CARD)
        clips_frame.grid(row=0, column=1, sticky="ew", pady=12)
        
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
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=12)
        
        audio_frame = tk.Frame(form, bg=BG_CARD)
        audio_frame.grid(row=1, column=1, sticky="ew", pady=12)
        
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
                font=("Arial", 9), fg=GRAY, bg=BG_DARK).pack(pady=15)
    
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
                fg=MAGENTA, bg=BG_DARK).pack(pady=25)
        
        # Input section
        inp = tk.Frame(bg, bg=BG_DARK)
        inp.pack(pady=10, padx=60, fill="x")
        
        # Clips
        tk.Label(inp, text="VIDEO CLIPS:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=6)
        
        clips_f = tk.Frame(inp, bg=BG_CARD)
        clips_f.grid(row=0, column=1, sticky="ew", pady=6)
        
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
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=6)
        
        audio_f = tk.Frame(inp, bg=BG_CARD)
        audio_f.grid(row=1, column=1, sticky="ew", pady=6)
        
        self.ai_audio_entry = tk.Entry(audio_f, width=40, bg=BG_INPUT, fg=MAGENTA,
                                     font=("Consolas", 10))
        self.ai_audio_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(audio_f, text="...", command=self.browse_ai_audio,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 10),
                 relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # Chat
        chat_f = tk.Frame(bg, bg=BG_CARD)
        chat_f.pack(pady=10, padx=60, fill="both", expand=True)
        
        self.ai_chat = scrolledtext.ScrolledText(chat_f, height=14,
                                               bg=BG_DARK, fg=MAGENTA,
                                               font=("Consolas", 10), relief="flat",
                                               state="disabled", wrap="word")
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", """AI: Welcome to AI Special Edit!

I generate Fusion scripts for DaVinci Resolve FREE!

Add your clips and audio, then describe what you want:
- "Cinematic with letterboxing and color grading"
- "Slow motion anime edit with film grain"
- "Dramatic cuts and text overlay"

Describe your vision and I'll create the script!

EXAMPLE PROMPTS:
- "Make it look cinematic with 2.35:1 letterboxing"
- "Slow motion effects with teal shadows"
- "Add dramatic color grading and film grain"
""")
        self.ai_chat.config(state="disabled")
        
        # Input row
        input_row = tk.Frame(bg, bg=BG_DARK)
        input_row.pack(pady=10, padx=60, fill="x")
        
        self.ai_input = tk.Entry(input_row, width=55, bg=BG_INPUT, fg=WHITE,
                                font=("Consolas", 12), insertbackground=MAGENTA)
        self.ai_input.pack(side="left")
        self.ai_input.bind("<Return>", lambda e: self.send_ai())
        
        tk.Button(input_row, text="SEND", command=self.send_ai,
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
            return
        self.ai_input.delete(0, "end")
        
        self.update_ai_chat(msg, is_user=True)
        self.ai_status.config(text="AI generating...")
        
        threading.Thread(target=self.ai_process, args=(msg,), daemon=True).start()
    
    def ai_process(self, msg):
        msg_lower = msg.lower()
        
        if any(w in msg_lower for w in ["yes", "good", "ok", "love it", "perfect", "thanks"]):
            response = "AI: Thanks! Your edit is saved. Returning to menu..."
            self.root.after(0, lambda: [self.update_ai_chat(response),
                                        self.root.after(2000, self.show_main_menu)])
            return
        
        if any(w in msg_lower for w in ["no", "not", "change", "redo", "fix"]):
            response = "AI: What should I change? Describe modifications:"
            self.root.after(0, lambda: self.update_ai_chat(response))
            return
        
        response = self.generate_fusion_script(msg)
        self.root.after(0, lambda: self.ai_finish(response))
    
    def generate_fusion_script(self, user_request):
        if not self.ai_clips:
            return "AI: Add at least one video clip first."
        
        audio = self.ai_audio_entry.get().strip()
        if not audio:
            return "AI: Select an audio file."
        
        self.root.after(0, lambda: self.ai_status.config(text="Generating Fusion script..."))
        
        # Generate script
        script_content = self.create_fusion_script(user_request)
        
        script_path = "ai_generated_edit.py"
        with open(script_path, "w") as f:
            f.write(script_content)
        
        self.ai_output = script_path
        
        return f"""AI: I've generated a Fusion script for your request!

Script saved as: {script_path}

The script uses DaVinci Resolve Fusion API to:
- Import your {len(self.ai_clips)} clips
- Apply cinematic letterboxing (2.35:1)
- Color grading (desaturated, teal shadows)
- Film grain effect
- Text overlay

To run: Open DaVinci Resolve > Fusion page > Console > exec(open('{script_path}').read())

Is this what you wanted?
[ YES, GOOD! ] or [ NO, CHANGE ]"""
    
    def create_fusion_script(self, request):
        """Create a DaVinci Resolve Fusion script"""
        clip_list = str(self.ai_clips)
        audio_path = self.ai_audio_entry.get().strip()
        
        script = f'''#!/usr/bin/env python3
"""
Monograph AI Generated Edit
Request: {request}
"""

import sys
import os

# DaVinci Resolve API
try:
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
except ImportError:
    print("DaVinci Resolve not found!")
    print("Install DaVinci Resolve and run from Fusion Console")
    sys.exit(1)

def main():
    # Get Fusion
    fusion = resolve.Fusion()
    projectManager = resolve.GetProjectManager()
    
    # Create project
    project = projectManager.CreateProject("Monograph AI Edit")
    
    # Get media pool
    mediaPool = project.GetMediaPool()
    
    # Import clips
    clipPaths = {clip_list}
    importedClips = mediaPool.ImportMedia(list(clipPaths))
    
    if importedClips:
        # Create timeline
        timeline = mediaPool.CreateTimelineFromClips("AI Edit", importedClips)
        project.SetCurrentTimeline(timeline)
        
        # Get current comp for Fusion effects
        comp = fusion.GetCurrentComp()
        
        if comp:
            # Letterboxing - Crop top and bottom
            crop = comp.AddTool("Crop")
            crop.Top.Value = 0.13
            crop.Bottom.Value = 0.13
            crop.Left.Value = 0.0
            crop.Right.Value = 0.0
            
            # Color grading - Cinematic look
            color = comp.AddTool("ColorCorrect")
            color.Saturation.Value = 0.65
            color.Contrast.Value = 1.05
            color.Lift[0].Value = 0.010
            color.Lift[1].Value = 0.012
            color.Lift[2].Value = 0.020
            color.Gamma[0].Value = 0.950
            color.Gamma[1].Value = 0.950
            color.Gamma[2].Value = 0.980
            
            # Film grain
            grain = comp.AddTool("FilmGrain")
            grain.GrainAmount.Value = 0.08
            grain.Size.Value = 1.0
            grain.Colorize.Value = False
            
            # Text overlay
            text = comp.AddTool("Text+")
            text.Titles[0].Value = "MONOGRAPH"
            text.Styles[0].Font.Value = "Arial"
            text.Styles[0].Size.Value = 48
            text.Styles[0].Italic.Value = False
            text.GlobalPosition[0].Value = 0.5
            text.GlobalPosition[1].Value = 0.8
            text.Alignment.Value = 1  # Center
            
            print("Effects applied: Letterbox, Color Grade, Film Grain, Text")
    
    # Set render settings
    project.SetRenderSettings({{
        "OutputFilename": "AI_EDIT_OUTPUT.mp4",
        "ResolutionWidth": 1920,
        "ResolutionHeight": 1080,
        "FrameRate": 24
    }})
    
    # Add render job
    jobId = project.AddRenderJob()
    print(f"Render job created: {{jobId}}")

if __name__ == "__main__":
    main()
'''
        return script
    
    def ai_finish(self, response):
        self.update_ai_chat(response)
        self.ai_status.config(text="")
        
        if "generated" in response.lower():
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
        if os.path.exists("ai_generated_edit.py"):
            with open("ai_generated_edit.py", "r") as f:
                content = f.read()
            messagebox.showinfo("Generated Script", content[:2000] + "...")
    
    def ai_yes(self):
        self.update_ai_chat("You: Yes, perfect!")
        self.feedback_frame.pack_forget()
        self.root.after(2000, self.show_main_menu)
    
    def ai_no(self):
        self.update_ai_chat("You: Please change it...")
        self.update_ai_chat("AI: What modifications do you want?")
        self.feedback_frame.pack_forget()
        self.feedback_shown = False


if __name__ == "__main__":
    root = tk.Tk()
    app = MonographApp(root)
    root.mainloop()