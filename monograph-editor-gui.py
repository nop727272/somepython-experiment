#!/usr/bin/env python3
"""
MONOGRAPH EDITOR v3.0 - Premium Cyberpunk Interface
Designed with strong visual aesthetic
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess
import threading
import shutil

# ============== ART & STYLE CONSTANTS ==============

COLORS = {
    "bg_dark": "#050510",
    "bg_card": "#0a0a1a",
    "bg_input": "#12122a",
    "cyan": "#00f5ff",
    "magenta": "#ff00aa",
    "purple": "#8b5cf6",
    "green": "#00ff88",
    "red": "#ff3366",
    "white": "#ffffff",
    "gray": "#666688",
    "dark_gray": "#2a2a4a"
}

FONTS = {
    "title": ("Consolas", 42, "bold"),
    "subtitle": ("Consolas", 18),
    "heading": ("Consolas", 16, "bold"),
    "body": ("Consolas", 11),
    "small": ("Arial", 9),
    "button": ("Consolas", 13, "bold")
}


class GradientCanvas(tk.Canvas):
    """Custom canvas with gradient background"""
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.draw_gradient)
        
    def draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        for i in range(height):
            ratio = i / height
            r = int(5 + ratio * 0)
            g = int(5 + ratio * 5)
            b = int(16 + ratio * 10)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(0, i, width, i, fill=color, tags="gradient")


class NeonButton(tk.Canvas):
    """Button with neon glow effect"""
    def __init__(self, parent, text, command, color="#00f5ff", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.command = command
        self.color = color
        self.hover = False
        self.text = text
        
        self.configure(height=45, bg="#050510", highlightthickness=0)
        self.bind("<Configure>", lambda e: self.draw())
        
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self.on_enter())
        self.bind("<Leave>", lambda e: self.on_leave())
        
    def draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        
        # Glow
        if self.hover:
            self.create_rounded_rect(2, 2, w-2, h-2, radius=10, fill=self.color)
        
        # Background
        bg = "#0a0a1a" if self.hover else "#050510"
        self.create_rounded_rect(4, 4, w-4, h-4, radius=8, fill=bg)
        
        # Text
        txt_color = "#050510" if self.hover else self.color
        self.create_text(w//2, h//2, text=self.text, font=("Consolas", 13, "bold"), fill=txt_color)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = []
        for x, y in [(x1+radius, y1), (x2-radius, y1), (x2, y1+radius),
                    (x2, y2-radius), (x2-radius, y2), (x1+radius, y2),
                    (x1, y2-radius), (x1, y1+radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self):
        self.hover = True
        self.draw()
    
    def on_leave(self):
        self.hover = False
        self.draw()


class MonographApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MONOGRAPH EDITOR")
        self.root.geometry("1000x750")
        self.root.configure(bg="#050510")
        self.root.minsize(900, 700)
        
        self.show_main_menu()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ============== MAIN MENU ==============
    def show_main_menu(self):
        self.clear()
        
        bg = GradientCanvas(self.root, bg="#050510", highlightthickness=0)
        bg.pack(fill="both", expand=True)
        
        # Accent bars
        tk.Frame(bg, height=4, bg="#00f5ff").pack(fill="x")
        tk.Frame(bg, width=4, bg="#00f5ff").pack(side="left", fill="y")
        tk.Frame(bg, width=4, bg="#ff00aa").pack(side="right", fill="y")
        
        # Title
        tk.Label(bg, text="MONOGRAPH", font=("Consolas", 48, "bold"),
                fg="#00f5ff", bg="#050510").pack(pady=(120, 5))
        
        tk.Label(bg, text="VIDEO EDITOR", font=("Consolas", 24),
                fg="#ff00aa", bg="#050510").pack()
        
        tk.Label(bg, text="// Craft Visual Masterpieces //",
                font=("Consolas", 12), fg="#666688", bg="#050510").pack(pady=40)
        
        # Menu cards
        cards = tk.Frame(bg, bg="#050510")
        cards.pack(pady=40)
        
        # Simple Edit Card
        simple = self.make_card(cards, "[ 1 ] SIMPLE EDIT",
                              "Quick preset-based editing\nwith cinematic effects",
                              "#00f5ff", lambda: self.show_simple_edit())
        simple.pack(side="left", padx=30)
        
        # AI Edit Card
        ai = self.make_card(cards, "[ 2 ] AI SPECIAL EDIT",
                            "Describe your vision\nor copy a reference style",
                            "#ff00aa", lambda: self.show_ai_edit())
        ai.pack(side="left", padx=30)
        
        # Footer
        tk.Label(bg, text="Powered by DaVinci Resolve Fusion | v3.0",
                font=("Arial", 9), fg="#2a2a4a", bg="#050510").pack(side="bottom", pady=20)
    
    def make_card(self, parent, title, desc, color, command):
        card = tk.Frame(parent, bg="#0a0a1a", cursor="hand2")
        
        tk.Frame(card, height=4, bg=color).pack(fill="x")
        
        content = tk.Frame(card, bg="#0a0a1a")
        content.pack(pady=35, padx=25, fill="both", expand=True)
        
        tk.Label(content, text=title, font=("Consolas", 16, "bold"),
                fg=color, bg="#0a0a1a").pack(pady=(15, 15))
        
        tk.Label(content, text=desc, font=("Consolas", 11),
                fg="#666688", bg="#0a0a1a", justify="center").pack()
        
        def enter(e):
            card.configure(bg="#12122a")
            content.configure(bg="#12122a")
            for w in content.winfo_children():
                w.configure(bg="#12122a")
        
        def leave(e):
            card.configure(bg="#0a0a1a")
            content.configure(bg="#0a0a1a")
            for w in content.winfo_children():
                w.configure(bg="#0a0a1a")
        
        card.bind("<Button-1>", lambda e: command())
        card.bind("<Enter>", enter)
        card.bind("<Leave>", leave)
        
        return card

    # ============== SIMPLE EDIT ==============
    def show_simple_edit(self):
        self.clear()
        
        bg = GradientCanvas(self.root, bg="#050510", highlightthickness=0)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg="#00f5ff").pack(fill="x")
        
        tk.Label(bg, text="< BACK", font=("Consolas", 11), fg="#666688",
                bg="#050510", cursor="hand2").place(x=20, y=15)
        tk.Label(bg, text="< BACK", font=("Consolas", 11), fg="#00f5ff",
                bg="#050510", cursor="hand2").place(x=20, y=15)
        
        def back(e): self.show_main_menu()
        bg.children[bg.winfo_children()[-1].__class__.__name__].bind("<Button-1>", back)
        
        # Find and bind back button
        for w in bg.winfo_children():
            if isinstance(w, tk.Label) and w.cget("text") == "< BACK":
                w.bind("<Button-1>", back)
                break
        
        tk.Label(bg, text="SIMPLE EDIT", font=("Consolas", 36, "bold"),
                fg="#00f5ff", bg="#050510").pack(pady=40)
        
        form = tk.Frame(bg, bg="#050510")
        form.pack(pady=20)
        
        self.simple_clips = []
        self.simple_audio = tk.StringVar()
        self.simple_output = tk.StringVar(value="MONOGRAPH_EDIT.mp4")
        self.simple_title = tk.StringVar(value="MONOGRAPH")
        
        # Clips
        tk.Label(form, text="VIDEO CLIP:", font=("Consolas", 12),
                fg="#ffffff", bg="#050510").grid(row=0, column=0, sticky="w", padx=20, pady=18)
        
        clips_frame = tk.Frame(form, bg="#0a0a1a")
        clips_frame.grid(row=0, column=1, pady=18, sticky="ew", padx=(0, 20))
        
        self.clips_list = tk.Listbox(clips_frame, height=3, bg="#12122a",
                                    fg="#00f5ff", font=("Consolas", 10),
                                    selectbackground="#00f5ff", selectforeground="#050510")
        self.clips_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(clips_frame, bg="#0a0a1a")
        btn_frame.pack(side="right", padx=5)
        
        tk.Button(btn_frame, text="+ ADD", command=self.add_simple_clips,
                 bg="#00f5ff", fg="#050510", font=("Consolas", 10, "bold"),
                 relief="flat").pack(pady=2, fill="x")
        
        tk.Button(btn_frame, text="CLEAR", command=self.clear_simple_clips,
                 bg="#ff3366", fg="#ffffff", font=("Consolas", 10),
                 relief="flat").pack(pady=2, fill="x")
        
        # Audio
        tk.Label(form, text="AUDIO FILE:", font=("Consolas", 12),
                fg="#ffffff", bg="#050510").grid(row=1, column=0, sticky="w", padx=20, pady=18)
        
        audio_frame = tk.Frame(form, bg="#0a0a1a")
        audio_frame.grid(row=1, column=1, pady=18, sticky="ew", padx=(0, 20))
        
        tk.Entry(audio_frame, textvariable=self.simple_audio, width=42,
                bg="#12122a", fg="#00f5ff", font=("Consolas", 11),
                insertbackground="#00f5ff").pack(side="left", padx=5, pady=8, fill="x", expand=True)
        
        tk.Button(audio_frame, text="BROWSE", command=lambda: self.browse_file(self.simple_audio, "audio"),
                 bg="#00f5ff", fg="#050510", font=("Consolas", 10, "bold"),
                 relief="flat").pack(side="right", padx=5, pady=5)
        
        # Title
        tk.Label(form, text="TITLE:", font=("Consolas", 12),
                fg="#ffffff", bg="#050510").grid(row=2, column=0, sticky="w", padx=20, pady=18)
        
        tk.Entry(form, textvariable=self.simple_title, width=44,
                bg="#12122a", fg="#00f5ff", font=("Consolas", 11),
                insertbackground="#00f5ff").grid(row=2, column=1, sticky="w", pady=18)
        
        # Output
        tk.Label(form, text="OUTPUT:", font=("Consolas", 12),
                fg="#ffffff", bg="#050510").grid(row=3, column=0, sticky="w", padx=20, pady=18)
        
        tk.Entry(form, textvariable=self.simple_output, width=44,
                bg="#12122a", fg="#00f5ff", font=("Consolas", 11),
                insertbackground="#00f5ff").grid(row=3, column=1, sticky="w", pady=18)
        
        # Status
        self.simple_status = tk.Label(bg, text="Select files and create",
                                    font=("Consolas", 11), fg="#00ff88", bg="#050510")
        self.simple_status.pack(pady=30)
        
        # Create button
        btn = NeonButton(bg, "[ CREATE VIDEO ]", self.run_simple_edit, "#00f5ff")
        btn.pack(pady=20)
        
        tk.Label(bg, text="Select video clips and audio, then create!",
                font=("Arial", 9), fg="#666688", bg="#050510").pack(pady=20)
    
    def add_simple_clips(self):
        files = filedialog.askopenfilenames(title="Select video clips",
                                           filetypes=[("Video", "*.mp4 *.mov *.avi *.mkv"), ("All", "*.*")])
        for f in files:
            if f not in self.simple_clips:
                self.simple_clips.append(f)
                self.clips_list.insert("end", os.path.basename(f))
    
    def clear_simple_clips(self):
        self.simple_clips.clear()
        self.clips_list.delete(0, "end")
    
    def browse_file(self, var, ftype):
        if ftype == "audio":
            f = filedialog.askopenfilename(title="Select audio", filetypes=[("Audio", "*.mp3 *.wav"), ("All", "*.*")])
        else:
            f = filedialog.askopenfilename(title="Select file", filetypes=[("All", "*.*")])
        if f:
            var.set(f)
    
    def run_simple_edit(self):
        if not self.simple_clips:
            messagebox.showerror("Error", "Select at least one video clip!")
            return
        if not self.simple_audio.get():
            messagebox.showerror("Error", "Select an audio file!")
            return
        
        self.simple_status.config(text="Creating video...", fg="#ff00aa")
        self.root.update()
        
        temp_dir = "temp_clips"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, clip in enumerate(self.simple_clips):
            ext = Path(clip).suffix
            shutil.copy(clip, f"{temp_dir}/clip_{i}{ext}")
        
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", temp_dir,
               "--audio", self.simple_audio.get(),
               "--output", self.simple_output.get(),
               "--title", self.simple_title.get()]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            if result.returncode == 0:
                self.simple_status.config(text="Video created!", fg="#00ff88")
                messagebox.showinfo("Success!", f"Ready: {self.simple_output.get()}")
            else:
                self.simple_status.config(text="Error occurred", fg="#ff3366")
                messagebox.showerror("Error", result.stderr[:200] if result.stderr else "Error")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ============== AI SPECIAL EDIT ==============
    def show_ai_edit(self):
        self.clear()
        
        bg = GradientCanvas(self.root, bg="#050510", highlightthickness=0)
        bg.pack(fill="both", expand=True)
        
        tk.Frame(bg, height=4, bg="#ff00aa").pack(fill="x")
        
        tk.Label(bg, text="< BACK", font=("Consolas", 11), fg="#ff00aa",
                bg="#050510", cursor="hand2").place(x=20, y=15)
        
        for w in bg.winfo_children():
            if isinstance(w, tk.Label) and w.cget("text") == "< BACK":
                w.bind("<Button-1>", lambda e: self.show_main_menu())
                break
        
        tk.Label(bg, text="AI SPECIAL EDIT", font=("Consolas", 36, "bold"),
                fg="#ff00aa", bg="#050510").pack(pady=30)
        
        # Input section
        inp = tk.Frame(bg, bg="#050510")
        inp.pack(pady=10, padx=60, fill="x")
        
        self.ai_clips = []
        self.ai_audio = tk.StringVar()
        self.ai_ref = tk.StringVar()
        
        # Clips
        tk.Label(inp, text="CLIPS:", font=("Consolas", 11), fg="#ffffff",
                bg="#050510").grid(row=0, column=0, sticky="w", pady=8)
        
        clips_f = tk.Frame(inp, bg="#0a0a1a")
        clips_f.grid(row=0, column=1, sticky="ew", pady=8)
        
        self.ai_clips_list = tk.Listbox(clips_f, height=2, bg="#12122a",
                                       fg="#ff00aa", font=("Consolas", 10))
        self.ai_clips_list.pack(side="left", fill="x", expand=True, padx=5, pady=3)
        
        tk.Button(clips_f, text="+", command=self.add_ai_clips,
                 bg="#ff00aa", fg="#050510", font=("Consolas", 14, "bold"),
                 relief="flat", width=3).pack(side="right", padx=3, pady=3)
        
        tk.Button(clips_f, text="X", command=self.clear_ai_clips,
                 bg="#ff3366", fg="#ffffff", font=("Consolas", 10),
                 relief="flat", width=3).pack(side="right", padx=(0, 3), pady=3)
        
        # Audio
        tk.Label(inp, text="AUDIO:", font=("Consolas", 11), fg="#ffffff",
                bg="#050510").grid(row=1, column=0, sticky="w", pady=8)
        
        audio_f = tk.Frame(inp, bg="#0a0a1a")
        audio_f.grid(row=1, column=1, sticky="ew", pady=8)
        
        tk.Entry(audio_f, textvariable=self.ai_audio, width=38,
                bg="#12122a", fg="#ff00aa", font=("Consolas", 10)).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(audio_f, text="...", command=lambda: self.browse_file(self.ai_audio, "audio"),
                 bg="#ff00aa", fg="#050510", font=("Consolas", 10), relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # Reference
        tk.Label(inp, text="STYLE REF:", font=("Consolas", 10), fg="#666688",
                bg="#050510").grid(row=2, column=0, sticky="w", pady=8)
        
        ref_f = tk.Frame(inp, bg="#0a0a1a")
        ref_f.grid(row=2, column=1, sticky="ew", pady=8)
        
        tk.Entry(ref_f, textvariable=self.ai_ref, width=38,
                bg="#12122a", fg="#666688", font=("Consolas", 10)).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(ref_f, text="...", command=lambda: self.browse_file(self.ai_ref, "video"),
                 bg="#2a2a4a", fg="#ffffff", font=("Consolas", 10), relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # Chat
        chat_f = tk.Frame(bg, bg="#0a0a1a")
        chat_f.pack(pady=10, padx=60, fill="both", expand=True)
        
        self.ai_chat = scrolledtext.ScrolledText(chat_f, height=12,
                                                bg="#050510", fg="#ff00aa",
                                                font=("Consolas", 10), relief="flat",
                                                state="disabled", wrap="word")
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", """AI: Welcome to AI Special Edit!

Select your clips and audio, then describe your vision.

Examples:
- "Make it cinematic with slow motion"
- "Copy the style of that reference video"
- "Create an epic anime-style edit"
- "Add dramatic lighting and color grading"

I'll create your custom edit!
""")
        self.ai_chat.config(state="disabled")
        
        # Input
        inp_row = tk.Frame(bg, bg="#050510")
        inp_row.pack(pady=10, padx=60, fill="x")
        
        self.ai_input = tk.Entry(inp_row, width=55, bg="#12122a", fg="#ffffff",
                                font=("Consolas", 12), insertbackground="#ff00aa")
        self.ai_input.pack(side="left")
        self.ai_input.bind("<Return>", self.send_ai)
        
        tk.Label(inp_row, text="SEND >>", font=("Consolas", 12, "bold"),
                fg="#ff00aa", bg="#050510", cursor="hand2").pack(side="right", padx=10)
        
        for w in inp_row.winfo_children():
            if isinstance(w, tk.Label) and "SEND" in w.cget("text"):
                w.bind("<Button-1>", lambda e: self.send_ai())
                break
        
        # Status
        self.ai_status = tk.Label(bg, text="", font=("Consolas", 10),
                                 fg="#ff00aa", bg="#050510")
        self.ai_status.pack(pady=5)
        
        # Feedback (hidden)
        self.ai_feedback = tk.Frame(bg, bg="#050510")
        self.feedback_shown = False
        self.ai_output = None
    
    def add_ai_clips(self):
        files = filedialog.askopenfilenames(title="Select clips",
                                           filetypes=[("Video", "*.mp4 *.mov *.mkv"), ("All", "*.*")])
        for f in files:
            if f not in self.ai_clips:
                self.ai_clips.append(f)
                self.ai_clips_list.insert("end", os.path.basename(f))
    
    def clear_ai_clips(self):
        self.ai_clips.clear()
        self.ai_clips_list.delete(0, "end")
    
    def send_ai(self, event=None):
        msg = self.ai_input.get().strip()
        if not msg:
            return
        self.ai_input.delete(0, "end")
        
        self.ai_update(f"You: {msg}", True)
        self.ai_status.config(text="AI processing...")
        
        threading.Thread(target=self.ai_process, args=(msg,), daemon=True).start()
    
    def ai_update(self, text, is_user=False):
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", text + "\n\n")
        self.ai_chat.see("end")
        self.ai_chat.config(state="disabled")
    
    def ai_process(self, msg):
        msg_lower = msg.lower()
        
        if any(w in msg_lower for w in ["yes", "good", "ok", "love it", "perfect", "thanks"]):
            self.root.after(0, lambda: [self.ai_update("AI: Thanks! Returning to menu..."),
                                        self.root.after(2000, self.show_main_menu)])
            return
        
        if any(w in msg_lower for w in ["no", "not", "change", "redo", "fix"]):
            self.root.after(0, lambda: self.ai_update("AI: Got it! What should I change?"))
            return
        
        response = self.ai_generate()
        self.root.after(0, lambda: self.ai_finish(response))
    
    def ai_generate(self):
        if not self.ai_clips:
            return "AI: Add at least one video clip first."
        if not self.ai_audio.get():
            return "AI: Select an audio file."
        
        self.root.after(0, lambda: self.ai_status.config(text="Creating custom edit..."))
        
        temp = "temp_ai"
        os.makedirs(temp, exist_ok=True)
        
        for i, clip in enumerate(self.ai_clips):
            ext = Path(clip).suffix
            shutil.copy(clip, f"{temp}/clip_{i}{ext}")
        
        output = "AI_CUSTOM.mp4"
        
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", temp, "--audio", self.ai_audio.get(), "--output", output]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(temp, ignore_errors=True)
            
            if result.returncode == 0 and os.path.exists(output):
                self.ai_output = output
                return f"""AI: Your custom edit is ready!

Output: {os.path.abspath(output)}

Is this good?
- "Yes, Good!" if perfect
- Tell me what to change"""
            else:
                return f"AI: Error: {result.stderr[:100] if result.stderr else 'Unknown'}"
        except subprocess.TimeoutExpired:
            return "AI: Timed out. Try fewer clips."
        except Exception as e:
            return f"AI: Error: {str(e)}"
    
    def ai_finish(self, response):
        self.ai_update(response)
        self.ai_status.config(text="")
        
        if self.ai_output and "ready" in response.lower():
            self.show_ai_feedback()
    
    def show_ai_feedback(self):
        if self.feedback_shown:
            return
        self.feedback_shown = True
        
        self.ai_feedback.pack(pady=15)
        
        yes = tk.Label(self.ai_feedback, text="[ YES, GOOD! ]",
                      font=("Consolas", 12, "bold"), bg="#050510", fg="#00ff88", cursor="hand2")
        yes.pack(side="left", padx=15)
        yes.bind("<Button-1>", lambda e: self.ai_yes())
        
        no = tk.Label(self.ai_feedback, text="[ NO, CHANGE ]",
                     font=("Consolas", 12, "bold"), bg="#050510", fg="#ff3366", cursor="hand2")
        no.pack(side="left", padx=15)
        no.bind("<Button-1>", lambda e: self.ai_no())
        
        if self.ai_output:
            folder = tk.Label(self.ai_feedback, text="[ OPEN FOLDER ]",
                            font=("Consolas", 10), bg="#050510", fg="#00f5ff", cursor="hand2")
            folder.pack(side="left", padx=15)
            folder.bind("<Button-1>", lambda e: subprocess.run(f'explorer /select,"{self.ai_output}"'))
    
    def ai_yes(self):
        self.ai_update("You: Yes, perfect!")
        self.ai_feedback.pack_forget()
        self.root.after(2000, self.show_main_menu)
    
    def ai_no(self):
        self.ai_update("You: No, please change it...")
        self.ai_update("AI: What should I change?")
        self.ai_feedback.pack_forget()
        self.feedback_shown = False


if __name__ == "__main__":
    root = tk.Tk()
    app = MonographApp(root)
    root.mainloop()