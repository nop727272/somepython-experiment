#!/usr/bin/env python3
"""
MONOGRAPH EDITOR v4.1 - Fixed DaVinci Resolve Integration
"""

import os, sys, tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess, threading, shutil, json, urllib.request

BG_DARK, BG_CARD, BG_INPUT = "#050510", "#0a0a1a", "#12122a"
CYAN, MAGENTA, GREEN, RED, ORANGE, WHITE, GRAY = "#00f5ff", "#ff00aa", "#00ff88", "#ff3366", "#ff9500", "#ffffff", "#666688"

DAVINCI_SCRIPT = '''#!/usr/bin/env python3
"""
Monograph AI Generated Edit for DaVinci Resolve
Paste this into Fusion Console
"""
import sys, os

# Windows API setup
if sys.platform == "win32":
    api_path = os.environ.get("RESOLVE_SCRIPT_API", "C:\\\\ProgramData\\\\Blackmagic Design\\\\DaVinci Resolve\\\\Support\\\\Developer\\\\Scripting")
    if os.path.exists(api_path):
        sys.path.insert(0, api_path + "\\\\Modules")

try:
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
    fusion = resolve.Fusion()
    print("Connected to DaVinci Resolve!")
except:
    print("ERROR: Cannot connect to DaVinci Resolve")
    sys.exit(1)

print("Starting Monograph AI Edit...")

projectManager = resolve.GetProjectManager()
project = projectManager.CreateProject("Monograph AI Edit")
mediaPool = project.GetMediaPool()

# Import clips
clips = {clips_list}
if clips:
    imported = mediaPool.ImportMedia(clips)
    if imported:
        print(f"Imported {len(imported)} clips")
        timeline = mediaPool.CreateTimelineFromClips("AI Edit", imported)
        if timeline:
            project.SetCurrentTimeline(timeline)
            resolve.OpenPage("fusion")
            comp = fusion.GetCurrentComp()
            if comp:
                # Letterbox
                crop = comp.AddTool("Crop")
                crop.Top.Value = 0.13
                crop.Bottom.Value = 0.13
                print("- Letterbox applied")
                # Color grade
                cc = comp.AddTool("ColorCorrect")
                cc.Saturation.Value = 0.65
                cc.Contrast.Value = 1.05
                cc.Lift[0].Value = 0.010
                cc.Lift[1].Value = 0.012
                cc.Lift[2].Value = 0.020
                print("- Color grading applied")
                # Film grain
                grain = comp.AddTool("FilmGrain")
                grain.GrainAmount.Value = 0.08
                print("- Film grain applied")
                # Text
                text = comp.AddTool("Text+")
                text.Titles[0].Value = "MONOGRAPH"
                text.Styles[0].Font.Value = "Arial"
                text.Styles[0].Size.Value = 48
                text.GlobalPosition[0].Value = 0.5
                text.GlobalPosition[1].Value = 0.8
                print("- Text overlay added")

print("Effects applied! Go to Deliver page to render.")
'''

class Updater:
    def __init__(self):
        self.repo = "nop727272/somepython-experiment"
        self.version = "4.1.0"
        self.has_update = False
    
    def check(self):
        try:
            url = f"https://api.github.com/repos/{self.repo}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Monograph"})
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            tag = data.get("tag_name", "v1.0.0").replace("v", "")
            if tag > self.version:
                self.has_update = True
                return True
        except: pass
        return False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MONOGRAPH EDITOR v4.1")
        self.root.geometry("1000x800")
        self.root.configure(bg=BG_DARK)
        self.updater = Updater()
        self.simple_clips = []
        self.ai_clips = []
        self.api_key = tk.StringVar()
        self.feedback_shown = False
        self.load_key()
        self.check_updates()
        self.show_menu()
    
    def load_key(self):
        if os.path.exists("api_key.txt"):
            with open("api_key.txt") as f:
                self.api_key.set(f.read().strip())
    
    def save_key(self):
        with open("api_key.txt", "w") as f:
            f.write(self.api_key.get().strip())
        messagebox.showinfo("Saved", "API key saved!")
    
    def check_updates(self):
        def check():
            if self.updater.check():
                self.root.after(0, self.show_update_popup)
        threading.Thread(target=check, daemon=True).start()
    
    def show_update_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Update!")
        popup.geometry("400x250")
        popup.configure(bg=BG_CARD)
        popup.grab_set()
        
        tk.Label(popup, text="UPDATE AVAILABLE!", font=("Consolas", 20, "bold"),
                fg=ORANGE, bg=BG_CARD).pack(pady=20)
        tk.Label(popup, text="v" + self.updater.version,
                font=("Consolas", 14), fg=WHITE, bg=BG_CARD).pack()
        
        frame = tk.Frame(popup, bg=BG_CARD)
        frame.pack(pady=20)
        
        tk.Button(frame, text="UPDATE NOW", command=lambda: [popup.destroy(), self.do_update()],
                 bg=GREEN, fg=BG_DARK, font=("Consolas", 12, "bold"),
                 relief="flat", padx=20, pady=10).pack(side="left", padx=10)
        
        tk.Button(frame, text="LATER", command=popup.destroy,
                 bg=GRAY, fg=WHITE, font=("Consolas", 12),
                 relief="flat", padx=20, pady=10).pack(side="left", padx=10)
    
    def do_update(self):
        messagebox.showinfo("Update", "Download from:\nhttps://github.com/nop727272/somepython-experiment")
        subprocess.run('start https://github.com/nop727272/somepython-experiment/archive/main.zip', shell=True)
    
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()
    
    def show_menu(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        tk.Label(bg, text="MONOGRAPH", font=("Consolas", 48, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=(80, 5))
        tk.Label(bg, text="AI VIDEO EDITOR", font=("Consolas", 20),
                fg=MAGENTA, bg=BG_DARK).pack()
        tk.Label(bg, text="DaVinci Resolve Fusion Script Generator",
                font=("Consolas", 11), fg=GRAY, bg=BG_DARK).pack(pady=30)
        
        f = tk.Frame(bg, bg=BG_DARK)
        f.pack(pady=20)
        
        tk.Button(f, text="[ 1 ] SIMPLE EDIT", command=self.show_simple,
                 font=("Consolas", 16, "bold"), bg=BG_CARD, fg=CYAN,
                 activebackground=BG_INPUT, relief="flat", padx=60, pady=20, cursor="hand2").pack(pady=8)
        tk.Label(f, text="FFmpeg-based preset editing",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        tk.Button(f, text="[ 2 ] AI SPECIAL EDIT", command=self.show_ai,
                 font=("Consolas", 16, "bold"), bg=BG_CARD, fg=MAGENTA,
                 activebackground=BG_INPUT, relief="flat", padx=60, pady=20, cursor="hand2").pack(pady=8)
        tk.Label(f, text="GPT-4 generates DaVinci Resolve scripts",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # API Key
        kf = tk.Frame(bg, bg=BG_DARK)
        kf.pack(pady=25, padx=60, fill="x")
        tk.Label(kf, text="OpenAI API Key:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", padx=5)
        tk.Entry(kf, textvariable=self.api_key, width=38, bg=BG_INPUT, fg=CYAN,
                font=("Consolas", 10), show="*").grid(row=0, column=1, padx=5)
        tk.Button(kf, text="Save", command=self.save_key, bg=GREEN, fg=BG_DARK,
                 font=("Consolas", 10), relief="flat").grid(row=0, column=2, padx=5)
        
        tk.Label(bg, text="v4.1.0 | DaVinci Resolve Fusion API",
                font=("Arial", 9), fg="#333", bg=BG_DARK).pack(side="bottom", pady=12)
    
    # ============== SIMPLE EDIT ==============
    def show_simple(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        tk.Button(bg, text="< BACK", command=self.show_menu,
                 font=("Consolas", 10), bg=BG_CARD, fg=GRAY,
                 relief="flat", cursor="hand2").place(x=20, y=15)
        
        tk.Label(bg, text="SIMPLE EDIT", font=("Consolas", 32, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=30)
        
        form = tk.Frame(bg, bg=BG_DARK)
        form.pack(pady=20, padx=60, fill="x")
        
        # Clips
        tk.Label(form, text="CLIPS:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=10)
        cf = tk.Frame(form, bg=BG_CARD)
        cf.grid(row=0, column=1, sticky="ew", pady=10)
        self.s_clips = tk.Listbox(cf, height=4, bg=BG_INPUT, fg=CYAN,
                                font=("Consolas", 10))
        self.s_clips.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        bf = tk.Frame(cf, bg=BG_CARD)
        bf.pack(side="right", padx=5)
        tk.Button(bf, text="+ ADD", command=self.add_simple_clips,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(fill="x")
        tk.Button(bf, text="CLEAR", command=lambda: [self.simple_clips.clear(), self.s_clips.delete(0, "end")],
                 bg=RED, fg=WHITE, font=("Consolas", 10), relief="flat").pack(fill="x")
        
        # Audio
        tk.Label(form, text="AUDIO:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=10)
        af = tk.Frame(form, bg=BG_CARD)
        af.grid(row=1, column=1, sticky="ew", pady=10)
        self.s_audio = tk.Entry(af, width=40, bg=BG_INPUT, fg=CYAN, font=("Consolas", 11))
        self.s_audio.pack(side="left", padx=5, pady=8, fill="x", expand=True)
        tk.Button(af, text="BROWSE", command=self.browse_audio,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(side="right", padx=5, pady=5)
        
        self.s_status = tk.Label(bg, text="Select files", font=("Consolas", 11),
                               fg=GREEN, bg=BG_DARK)
        self.s_status.pack(pady=20)
        
        tk.Button(bg, text="[ CREATE VIDEO ]", command=self.run_simple,
                font=("Consolas", 14, "bold"), bg=CYAN, fg=BG_DARK,
                relief="flat", padx=40, pady=12, cursor="hand2").pack(pady=10)
    
    def add_simple_clips(self):
        files = filedialog.askopenfilenames(title="Select clips",
            filetypes=[("Video", "*.mp4 *.mov *.avi *.mkv"), ("All", "*.*")])
        for f in files:
            if f not in self.simple_clips:
                self.simple_clips.append(f)
                self.s_clips.insert("end", os.path.basename(f))
    
    def browse_audio(self):
        f = filedialog.askopenfilename(title="Audio",
            filetypes=[("Audio", "*.mp3 *.wav"), ("All", "*.*")])
        if f:
            self.s_audio.delete(0, "end")
            self.s_audio.insert(0, f)
    
    def run_simple(self):
        if not self.simple_clips:
            messagebox.showerror("Error", "Add clips first!")
            return
        if not self.s_audio.get().strip():
            messagebox.showerror("Error", "Select audio!")
            return
        
        self.s_status.config(text="Creating...", fg=MAGENTA)
        self.root.update()
        
        tmp = "temp_clips"
        os.makedirs(tmp, exist_ok=True)
        for i, c in enumerate(self.simple_clips):
            shutil.copy(c, f"{tmp}/c{i}{Path(c).suffix}")
        
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", tmp, "--audio", self.s_audio.get().strip(),
               "--output", "MONOGRAPH_EDIT.mp4"]
        
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(tmp, ignore_errors=True)
            if r.returncode == 0:
                self.s_status.config(text="Done!", fg=GREEN)
                messagebox.showinfo("Success", "Video ready!")
            else:
                self.s_status.config(text="Error", fg=RED)
                messagebox.showerror("Error", r.stderr[:200] if r.stderr else "Error")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ============== AI EDIT ==============
    def show_ai(self):
        self.clear()
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        tk.Frame(bg, height=4, bg=MAGENTA).pack(fill="x")
        
        tk.Button(bg, text="< BACK", command=self.show_menu,
                 font=("Consolas", 10), bg=BG_CARD, fg=GRAY,
                 relief="flat", cursor="hand2").place(x=20, y=15)
        
        tk.Label(bg, text="AI SPECIAL EDIT", font=("Consolas", 32, "bold"),
                fg=MAGENTA, bg=BG_DARK).pack(pady=20)
        
        inp = tk.Frame(bg, bg=BG_DARK)
        inp.pack(pady=10, padx=60, fill="x")
        
        # Clips
        tk.Label(inp, text="CLIPS:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=5)
        cf = tk.Frame(inp, bg=BG_CARD)
        cf.grid(row=0, column=1, sticky="ew", pady=5)
        self.ai_clips_box = tk.Listbox(cf, height=2, bg=BG_INPUT, fg=MAGENTA, font=("Consolas", 10))
        self.ai_clips_box.pack(side="left", fill="x", expand=True, padx=5, pady=3)
        bf = tk.Frame(cf, bg=BG_CARD)
        bf.pack(side="right", padx=3)
        tk.Button(bf, text="+", command=self.add_ai_clips,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 12, "bold"),
                 relief="flat", width=3).pack(pady=1)
        tk.Button(bf, text="X", command=lambda: [self.ai_clips.clear(), self.ai_clips_box.delete(0, "end")],
                 bg=RED, fg=WHITE, font=("Consolas", 10), relief="flat", width=3).pack(pady=1)
        
        # Audio
        tk.Label(inp, text="AUDIO:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=5)
        af = tk.Frame(inp, bg=BG_CARD)
        af.grid(row=1, column=1, sticky="ew", pady=5)
        self.ai_audio = tk.Entry(af, width=40, bg=BG_INPUT, fg=MAGENTA, font=("Consolas", 10))
        self.ai_audio.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(af, text="...", command=lambda: self.browse_ai_audio(),
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 10), relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # Prompt
        tk.Label(inp, text="PROMPT:", font=("Consolas", 11),
                fg=MAGENTA, bg=BG_DARK).grid(row=2, column=0, sticky="w", pady=5)
        pf = tk.Frame(inp, bg=BG_CARD)
        pf.grid(row=2, column=1, sticky="ew", pady=5)
        self.ai_prompt = tk.Entry(pf, width=40, bg=BG_INPUT, fg=MAGENTA, font=("Consolas", 10))
        self.ai_prompt.insert(0, "Cinematic with letterboxing and color grading")
        self.ai_prompt.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Chat
        chat = tk.Frame(bg, bg=BG_CARD)
        chat.pack(pady=10, padx=60, fill="both", expand=True)
        self.ai_chat = scrolledtext.ScrolledText(chat, height=15,
                bg=BG_DARK, fg=MAGENTA, font=("Consolas", 10),
                relief="flat", state="disabled", wrap="word")
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", """AI: Welcome to AI Special Edit!

I generate DaVinci Resolve Fusion scripts!

1. Add video clips (+)
2. Select audio (...)
3. Type your prompt
4. Click SEND TO AI

EXAMPLES:
- "Cinematic with 2.35:1 letterboxing"
- "Slow motion with film grain"
- "Teal shadows and warm highlights"
- "Anime style edit"

Script will be saved as: monograph_ai_script.py
""")
        self.ai_chat.config(state="disabled")
        
        # Input
        ir = tk.Frame(bg, bg=BG_DARK)
        ir.pack(pady=10, padx=60, fill="x")
        self.ai_input = tk.Entry(ir, width=50, bg=BG_INPUT, fg=WHITE,
                               font=("Consolas", 12), insertbackground=MAGENTA)
        self.ai_input.pack(side="left")
        self.ai_input.bind("<Return>", lambda e: self.send_ai())
        tk.Button(ir, text="SEND TO AI", command=self.send_ai,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 11, "bold"),
                 relief="flat", cursor="hand2").pack(side="right", padx=(10, 0))
        
        self.ai_status = tk.Label(bg, text="", font=("Consolas", 10),
                               fg=MAGENTA, bg=BG_DARK)
        self.ai_status.pack(pady=5)
        self.ai_feedback = tk.Frame(bg, bg=BG_DARK)
    
    def add_ai_clips(self):
        files = filedialog.askopenfilenames(title="Select clips",
            filetypes=[("Video", "*.mp4 *.mov *.mkv"), ("All", "*.*")])
        for f in files:
            if f not in self.ai_clips:
                self.ai_clips.append(f)
                self.ai_clips_box.insert("end", os.path.basename(f))
    
    def browse_ai_audio(self):
        f = filedialog.askopenfilename(title="Audio",
            filetypes=[("Audio", "*.mp3 *.wav"), ("All", "*.*")])
        if f:
            self.ai_audio.delete(0, "end")
            self.ai_audio.insert(0, f)
    
    def update_chat(self, text, user=False):
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", ("You: " if user else "AI: ") + text + "\n\n")
        self.ai_chat.see("end")
        self.ai_chat.config(state="disabled")
    
    def send_ai(self):
        msg = self.ai_input.get().strip() or self.ai_prompt.get().strip()
        if not msg:
            return
        self.ai_input.delete(0, "end")
        self.update_chat(msg, user=True)
        self.ai_status.config(text="Generating...")
        threading.Thread(target=self.process_ai, args=(msg,), daemon=True).start()
    
    def process_ai(self, msg):
        msg_lower = msg.lower()
        
        if any(w in msg_lower for w in ["yes", "good", "ok", "perfect", "thanks"]):
            resp = "AI: Thanks! Returning to menu..."
            self.root.after(0, lambda: [self.update_chat(resp), self.root.after(2000, self.show_menu)])
            return
        
        if any(w in msg_lower for w in ["no", "not", "change", "fix"]):
            resp = "AI: What should I change?"
            self.root.after(0, lambda: self.update_chat(resp))
            return
        
        resp = self.generate_script(msg)
        self.root.after(0, lambda: self.finish_ai(resp))
    
    def generate_script(self, request):
        if not self.ai_clips:
            return "AI: Add clips first!"
        if not self.ai_audio.get().strip():
            return "AI: Select audio first!"
        
        clips_str = str(self.ai_clips).replace("\\", "\\\\")
        script = DAVINCI_SCRIPT.format(clips_list=clips_str)
        
        path = "monograph_ai_script.py"
        with open(path, "w") as f:
            f.write(script)
        
        return f"""AI: Script generated!

Saved as: {path}

TO USE IN DAVINCI RESOLVE:
1. Open DaVinci Resolve
2. Go to Fusion page
3. View > Console
4. Type: exec(open('{path}').read())
5. Press Enter

Effects included:
- Letterbox (2.35:1)
- Color grading
- Film grain
- Text overlay

Is this good? [YES] or [NO, CHANGE]"""
    
    def finish_ai(self, resp):
        self.update_chat(resp)
        self.ai_status.config(text="")
        if "Script generated" in resp or "generated" in resp.lower():
            self.show_feedback_buttons()
    
    def show_feedback_buttons(self):
        if self.feedback_shown:
            return
        self.feedback_shown = True
        self.ai_feedback.pack(pady=15)
        
        tk.Button(self.ai_feedback, text="[ YES, GOOD! ]",
                 command=self.ai_yes, bg=GREEN, fg=BG_DARK,
                 font=("Consolas", 12, "bold"), relief="flat",
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=8)
        
        tk.Button(self.ai_feedback, text="[ NO, CHANGE ]",
                 command=self.ai_no, bg=RED, fg=WHITE,
                 font=("Consolas", 12, "bold"), relief="flat",
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=8)
    
    def ai_yes(self):
        self.update_chat("You: Perfect!")
        self.ai_feedback.pack_forget()
        self.root.after(2000, self.show_menu)
    
    def ai_no(self):
        self.update_chat("You: Please change it...")
        self.update_chat("AI: What should I modify?")
        self.ai_feedback.pack_forget()
        self.feedback_shown = False

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()