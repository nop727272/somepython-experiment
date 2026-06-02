#!/usr/bin/env python3
"""
MONOGRAPH EDITOR v3.0 - Fixed & Working
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import subprocess
import threading
import shutil

# ============== COLORS ==============
BG_DARK = "#050510"
BG_CARD = "#0a0a1a"
BG_INPUT = "#12122a"
CYAN = "#00f5ff"
MAGENTA = "#ff00aa"
GREEN = "#00ff88"
RED = "#ff3366"
WHITE = "#ffffff"
GRAY = "#666688"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MONOGRAPH EDITOR")
        self.root.geometry("1000x750")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(900, 700)
        
        # Variables
        self.simple_clips = []
        self.simple_audio = ""
        self.simple_output = "MONOGRAPH_EDIT.mp4"
        self.simple_title = "MONOGRAPH"
        
        self.ai_clips = []
        self.ai_audio = ""
        self.ai_ref = ""
        self.ai_output = None
        
        self.show_main_menu()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ============== MAIN MENU ==============
    def show_main_menu(self):
        self.clear()
        
        # Background
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        # Top accent
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        # Title
        tk.Label(bg, text="MONOGRAPH", font=("Consolas", 48, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=(100, 5))
        
        tk.Label(bg, text="VIDEO EDITOR", font=("Consolas", 20),
                fg=MAGENTA, bg=BG_DARK).pack()
        
        tk.Label(bg, text="Craft Visual Masterpieces",
                font=("Consolas", 12), fg=GRAY, bg=BG_DARK).pack(pady=40)
        
        # Buttons
        btn_frame = tk.Frame(bg, bg=BG_DARK)
        btn_frame.pack(pady=40)
        
        # Simple Edit Button
        simple_btn = tk.Button(btn_frame, text="[ 1 ] SIMPLE EDIT",
                              command=self.show_simple_edit,
                              font=("Consolas", 16, "bold"),
                              bg=BG_CARD, fg=CYAN, activebackground=BG_INPUT,
                              activeforeground=CYAN, relief="flat",
                              padx=60, pady=25, cursor="hand2",
                              bd=2, highlightthickness=2, highlightcolor=CYAN)
        simple_btn.pack(pady=15)
        
        tk.Label(btn_frame, text="Quick preset-based editing with cinematic effects",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # AI Edit Button
        ai_btn = tk.Button(btn_frame, text="[ 2 ] AI SPECIAL EDIT",
                          command=self.show_ai_edit,
                          font=("Consolas", 16, "bold"),
                          bg=BG_CARD, fg=MAGENTA, activebackground=BG_INPUT,
                          activeforeground=MAGENTA, relief="flat",
                          padx=60, pady=25, cursor="hand2",
                          bd=2, highlightthickness=2, highlightcolor=MAGENTA)
        ai_btn.pack(pady=15)
        
        tk.Label(btn_frame, text="Describe your vision or copy a reference style",
                font=("Arial", 10), fg=GRAY, bg=BG_DARK).pack()
        
        # Footer
        tk.Label(bg, text="Powered by DaVinci Resolve Fusion | v3.0",
                font=("Arial", 9), fg="#333", bg=BG_DARK).pack(side="bottom", pady=20)

    # ============== SIMPLE EDIT ==============
    def show_simple_edit(self):
        self.clear()
        
        # Background
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        # Top accent
        tk.Frame(bg, height=4, bg=CYAN).pack(fill="x")
        
        # Back button
        back_btn = tk.Button(bg, text="< BACK TO MENU",
                            command=self.show_main_menu,
                            font=("Consolas", 10),
                            bg=BG_CARD, fg=GRAY, relief="flat",
                            cursor="hand2")
        back_btn.place(x=20, y=15)
        
        # Title
        tk.Label(bg, text="SIMPLE EDIT", font=("Consolas", 32, "bold"),
                fg=CYAN, bg=BG_DARK).pack(pady=40)
        
        # Form
        form = tk.Frame(bg, bg=BG_DARK)
        form.pack(pady=20, padx=60, fill="x")
        
        # --- CLIPS SECTION ---
        tk.Label(form, text="VIDEO CLIPS:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=15)
        
        clips_frame = tk.Frame(form, bg=BG_CARD)
        clips_frame.grid(row=0, column=1, sticky="ew", pady=15)
        
        # Listbox for clips
        self.clips_listbox = tk.Listbox(clips_frame, height=4, bg=BG_INPUT,
                                       fg=CYAN, font=("Consolas", 10),
                                       selectbackground=CYAN, selectforeground=BG_DARK)
        self.clips_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Clip buttons
        clip_btns = tk.Frame(clips_frame, bg=BG_CARD)
        clip_btns.pack(side="right", padx=5)
        
        tk.Button(clip_btns, text="+ ADD", command=self.add_simple_clips,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(fill="x", pady=2)
        
        tk.Button(clip_btns, text="CLEAR", command=self.clear_simple_clips,
                 bg=RED, fg=WHITE, font=("Consolas", 10),
                 relief="flat", cursor="hand2").pack(fill="x", pady=2)
        
        # --- AUDIO SECTION ---
        tk.Label(form, text="AUDIO FILE:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=15)
        
        audio_frame = tk.Frame(form, bg=BG_CARD)
        audio_frame.grid(row=1, column=1, sticky="ew", pady=15)
        
        self.audio_entry = tk.Entry(audio_frame, width=40, bg=BG_INPUT, fg=CYAN,
                                   font=("Consolas", 11), insertbackground=CYAN)
        self.audio_entry.pack(side="left", padx=5, pady=8, fill="x", expand=True)
        
        tk.Button(audio_frame, text="BROWSE", command=self.browse_audio,
                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10, "bold"),
                 relief="flat", cursor="hand2").pack(side="right", padx=5, pady=5)
        
        # --- TITLE SECTION ---
        tk.Label(form, text="TITLE:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=2, column=0, sticky="w", pady=15)
        
        title_frame = tk.Frame(form, bg=BG_CARD)
        title_frame.grid(row=2, column=1, sticky="w", pady=15)
        
        self.title_entry = tk.Entry(title_frame, width=42, bg=BG_INPUT, fg=CYAN,
                                  font=("Consolas", 11), insertbackground=CYAN)
        self.title_entry.insert(0, "MONOGRAPH")
        self.title_entry.pack(side="left", padx=5, pady=8)
        
        # --- OUTPUT SECTION ---
        tk.Label(form, text="OUTPUT:", font=("Consolas", 12),
                fg=WHITE, bg=BG_DARK).grid(row=3, column=0, sticky="w", pady=15)
        
        output_frame = tk.Frame(form, bg=BG_CARD)
        output_frame.grid(row=3, column=1, sticky="w", pady=15)
        
        self.output_entry = tk.Entry(output_frame, width=42, bg=BG_INPUT, fg=CYAN,
                                   font=("Consolas", 11), insertbackground=CYAN)
        self.output_entry.insert(0, "MONOGRAPH_EDIT.mp4")
        self.output_entry.pack(side="left", padx=5, pady=8)
        
        # --- STATUS ---
        self.simple_status = tk.Label(bg, text="Select files and click Create",
                                    font=("Consolas", 11), fg=GREEN, bg=BG_DARK)
        self.simple_status.pack(pady=25)
        
        # --- CREATE BUTTON ---
        create_btn = tk.Button(bg, text="[ CREATE VIDEO ]",
                              command=self.run_simple_edit,
                              font=("Consolas", 14, "bold"),
                              bg=CYAN, fg=BG_DARK, relief="flat",
                              padx=40, pady=15, cursor="hand2")
        create_btn.pack(pady=10)
        
        # Help
        tk.Label(bg, text="1. Add video clips | 2. Select audio | 3. Click Create",
                font=("Arial", 9), fg=GRAY, bg=BG_DARK).pack(pady=20)
    
    def add_simple_clips(self):
        files = filedialog.askopenfilenames(
            title="Select video clips",
            filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.simple_clips:
                self.simple_clips.append(f)
                self.clips_listbox.insert("end", os.path.basename(f))
        self.simple_status.config(text=f"Added {len(files)} clip(s). Total: {len(self.simple_clips)}")
    
    def clear_simple_clips(self):
        self.simple_clips.clear()
        self.clips_listbox.delete(0, "end")
        self.simple_status.config(text="Clips cleared")
    
    def browse_audio(self):
        f = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=[("Audio files", "*.mp3 *.wav"), ("All files", "*.*")]
        )
        if f:
            self.audio_entry.delete(0, "end")
            self.audio_entry.insert(0, f)
            self.simple_status.config(text=f"Audio selected: {os.path.basename(f)}")
    
    def run_simple_edit(self):
        # Get values
        self.simple_audio = self.audio_entry.get().strip()
        self.simple_output = self.output_entry.get().strip()
        self.simple_title = self.title_entry.get().strip()
        
        # Validate
        if not self.simple_clips:
            messagebox.showerror("Error", "Please add at least one video clip!")
            return
        
        if not self.simple_audio:
            messagebox.showerror("Error", "Please select an audio file!")
            return
        
        if not os.path.exists(self.simple_audio):
            messagebox.showerror("Error", "Audio file not found!")
            return
        
        self.simple_status.config(text=f"Creating video from {len(self.simple_clips)} clips...", fg=MAGENTA)
        self.root.update()
        
        # Create temp folder
        temp_dir = "temp_simple_clips"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Copy clips
        for i, clip in enumerate(self.simple_clips):
            ext = Path(clip).suffix
            dest = f"{temp_dir}/clip_{i}{ext}"
            shutil.copy(clip, dest)
        
        # Run editor
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", temp_dir,
               "--audio", self.simple_audio,
               "--output", self.simple_output,
               "--title", self.simple_title]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            if result.returncode == 0:
                self.simple_status.config(text="Video created successfully!", fg=GREEN)
                messagebox.showinfo("Success!", f"Your video is ready:\n{os.path.abspath(self.simple_output)}")
            else:
                self.simple_status.config(text="Error occurred", fg=RED)
                messagebox.showerror("Error", result.stderr[:300] if result.stderr else "Unknown error")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ============== AI SPECIAL EDIT ==============
    def show_ai_edit(self):
        self.clear()
        
        # Background
        bg = tk.Frame(self.root, bg=BG_DARK)
        bg.pack(fill="both", expand=True)
        
        # Top accent
        tk.Frame(bg, height=4, bg=MAGENTA).pack(fill="x")
        
        # Back button
        back_btn = tk.Button(bg, text="< BACK TO MENU",
                            command=self.show_main_menu,
                            font=("Consolas", 10),
                            bg=BG_CARD, fg=GRAY, relief="flat",
                            cursor="hand2")
        back_btn.place(x=20, y=15)
        
        # Title
        tk.Label(bg, text="AI SPECIAL EDIT", font=("Consolas", 32, "bold"),
                fg=MAGENTA, bg=BG_DARK).pack(pady=30)
        
        # Input section
        inp = tk.Frame(bg, bg=BG_DARK)
        inp.pack(pady=10, padx=60, fill="x")
        
        # --- CLIPS ---
        tk.Label(inp, text="VIDEO CLIPS:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=0, column=0, sticky="w", pady=8)
        
        clips_f = tk.Frame(inp, bg=BG_CARD)
        clips_f.grid(row=0, column=1, sticky="ew", pady=8)
        
        self.ai_clips_listbox = tk.Listbox(clips_f, height=3, bg=BG_INPUT,
                                         fg=MAGENTA, font=("Consolas", 10))
        self.ai_clips_listbox.pack(side="left", fill="x", expand=True, padx=5, pady=3)
        
        btn_col = tk.Frame(clips_f, bg=BG_CARD)
        btn_col.pack(side="right", padx=3)
        
        tk.Button(btn_col, text="+", command=self.add_ai_clips,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 14, "bold"),
                 relief="flat", width=3).pack(pady=2)
        
        tk.Button(btn_col, text="X", command=self.clear_ai_clips,
                 bg=RED, fg=WHITE, font=("Consolas", 10),
                 relief="flat", width=3).pack(pady=2)
        
        # --- AUDIO ---
        tk.Label(inp, text="AUDIO:", font=("Consolas", 11),
                fg=WHITE, bg=BG_DARK).grid(row=1, column=0, sticky="w", pady=8)
        
        audio_f = tk.Frame(inp, bg=BG_CARD)
        audio_f.grid(row=1, column=1, sticky="ew", pady=8)
        
        self.ai_audio_entry = tk.Entry(audio_f, width=40, bg=BG_INPUT, fg=MAGENTA,
                                     font=("Consolas", 10))
        self.ai_audio_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(audio_f, text="...", command=self.browse_ai_audio,
                 bg=MAGENTA, fg=BG_DARK, font=("Consolas", 10),
                 relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # --- REFERENCE ---
        tk.Label(inp, text="STYLE REF:", font=("Consolas", 10),
                fg=GRAY, bg=BG_DARK).grid(row=2, column=0, sticky="w", pady=8)
        
        ref_f = tk.Frame(inp, bg=BG_CARD)
        ref_f.grid(row=2, column=1, sticky="ew", pady=8)
        
        self.ai_ref_entry = tk.Entry(ref_f, width=40, bg=BG_INPUT, fg=GRAY,
                                   font=("Consolas", 10))
        self.ai_ref_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        tk.Button(ref_f, text="...", command=self.browse_ai_ref,
                 bg="#444", fg=WHITE, font=("Consolas", 10),
                 relief="flat", width=4).pack(side="right", padx=5, pady=5)
        
        # --- CHAT ---
        chat_f = tk.Frame(bg, bg=BG_CARD)
        chat_f.pack(pady=10, padx=60, fill="both", expand=True)
        
        self.ai_chat = scrolledtext.ScrolledText(chat_f, height=12,
                                               bg=BG_DARK, fg=MAGENTA,
                                               font=("Consolas", 10), relief="flat",
                                               state="disabled", wrap="word")
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial message
        self.ai_chat.config(state="normal")
        self.ai_chat.insert("end", """AI: Welcome to AI Special Edit!

Select your clips and audio, then describe the style you want.

Example prompts:
- "Make it cinematic with slow motion"
- "Copy the style of my reference video"  
- "Create an epic anime-style edit"
- "Add dramatic lighting effects"

I'll create your custom edit!
""")
        self.ai_chat.config(state="disabled")
        
        # --- INPUT ROW ---
        input_row = tk.Frame(bg, bg=BG_DARK)
        input_row.pack(pady=10, padx=60, fill="x")
        
        self.ai_input = tk.Entry(input_row, width=55, bg=BG_INPUT, fg=WHITE,
                                font=("Consolas", 12), insertbackground=MAGENTA)
        self.ai_input.pack(side="left")
        self.ai_input.bind("<Return>", lambda e: self.send_ai_message())
        
        send_btn = tk.Button(input_row, text="SEND", command=self.send_ai_message,
                            bg=MAGENTA, fg=BG_DARK, font=("Consolas", 11, "bold"),
                            relief="flat", cursor="hand2")
        send_btn.pack(side="right", padx=(10, 0))
        
        # --- STATUS ---
        self.ai_status = tk.Label(bg, text="", font=("Consolas", 10),
                                fg=MAGENTA, bg=BG_DARK)
        self.ai_status.pack(pady=5)
        
        # --- FEEDBACK BUTTONS (hidden) ---
        self.feedback_frame = tk.Frame(bg, bg=BG_DARK)
        self.feedback_shown = False
        self.ai_output = None
    
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
        self.ai_status.config(text="Clips cleared")
    
    def browse_ai_audio(self):
        f = filedialog.askopenfilename(
            title="Select audio",
            filetypes=[("Audio files", "*.mp3 *.wav"), ("All files", "*.*")]
        )
        if f:
            self.ai_audio_entry.delete(0, "end")
            self.ai_audio_entry.insert(0, f)
            self.ai_status.config(text=f"Audio: {os.path.basename(f)}")
    
    def browse_ai_ref(self):
        f = filedialog.askopenfilename(
            title="Select reference video for style",
            filetypes=[("Video files", "*.mp4 *.mov"), ("All files", "*.*")]
        )
        if f:
            self.ai_ref_entry.delete(0, "end")
            self.ai_ref_entry.insert(0, f)
            self.ai_status.config(text=f"Reference: {os.path.basename(f)}")
    
    def update_ai_chat(self, text, is_user=False):
        self.ai_chat.config(state="normal")
        prefix = "You: " if is_user else "AI: "
        self.ai_chat.insert("end", prefix + text + "\n\n")
        self.ai_chat.see("end")
        self.ai_chat.config(state="disabled")
    
    def send_ai_message(self):
        msg = self.ai_input.get().strip()
        if not msg:
            return
        self.ai_input.delete(0, "end")
        
        self.update_ai_chat(msg, is_user=True)
        self.ai_status.config(text="AI processing...")
        
        threading.Thread(target=self.ai_process, args=(msg,), daemon=True).start()
    
    def ai_process(self, msg):
        msg_lower = msg.lower()
        
        # Check responses
        if any(w in msg_lower for w in ["yes", "good", "ok", "love it", "perfect", "thanks"]):
            response = "AI: Thanks! Your edit is saved. Returning to menu..."
            self.root.after(0, lambda: [self.update_ai_chat(response),
                                        self.root.after(2000, self.show_main_menu)])
            return
        
        if any(w in msg_lower for w in ["no", "not", "change", "redo", "fix", "wrong"]):
            response = "AI: Got it! Please describe what changes you want:"
            self.root.after(0, lambda: self.update_ai_chat(response))
            return
        
        # Generate video
        response = self.ai_generate_video()
        self.root.after(0, lambda: self.ai_finish(response))
    
    def ai_generate_video(self):
        audio = self.ai_audio_entry.get().strip()
        
        if not self.ai_clips:
            return "AI: Please add at least one video clip first."
        
        if not audio:
            return "AI: Please select an audio file."
        
        if not os.path.exists(audio):
            return "AI: Audio file not found. Please check the path."
        
        self.root.after(0, lambda: self.ai_status.config(text="Creating your custom edit..."))
        
        # Create temp folder
        temp = "temp_ai_clips"
        os.makedirs(temp, exist_ok=True)
        
        # Copy clips
        for i, clip in enumerate(self.ai_clips):
            ext = Path(clip).suffix
            shutil.copy(clip, f"{temp}/clip_{i}{ext}")
        
        output = "AI_CUSTOM_EDIT.mp4"
        
        cmd = [sys.executable, "monograph-auto-editor.py",
               "--clips-folder", temp,
               "--audio", audio,
               "--output", output]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            shutil.rmtree(temp, ignore_errors=True)
            
            if result.returncode == 0 and os.path.exists(output):
                self.ai_output = output
                return f"""AI: Your custom edit is ready!

Output: {os.path.abspath(output)}

Is this what you had in mind?

[ YES, GOOD! ] if perfect
[ NO, CHANGE ] to modify"""
            else:
                return f"AI: Error creating video: {result.stderr[:150] if result.stderr else 'Unknown error'}"
        except subprocess.TimeoutExpired:
            return "AI: Video creation timed out. Try with fewer clips."
        except Exception as e:
            return f"AI: Error: {str(e)}"
    
    def ai_finish(self, response):
        self.update_ai_chat(response)
        self.ai_status.config(text="")
        
        if self.ai_output and "ready" in response.lower():
            self.show_ai_feedback()
    
    def show_ai_feedback(self):
        if self.feedback_shown:
            return
        self.feedback_shown = True
        
        self.feedback_frame.pack(pady=15)
        
        # Yes button
        yes_btn = tk.Button(self.feedback_frame, text="[ YES, GOOD! ]",
                           command=self.ai_yes,
                           bg=GREEN, fg=BG_DARK, font=("Consolas", 12, "bold"),
                           relief="flat", cursor="hand2", padx=20, pady=10)
        yes_btn.pack(side="left", padx=10)
        
        # No button
        no_btn = tk.Button(self.feedback_frame, text="[ NO, CHANGE ]",
                          command=self.ai_no,
                          bg=RED, fg=WHITE, font=("Consolas", 12, "bold"),
                          relief="flat", cursor="hand2", padx=20, pady=10)
        no_btn.pack(side="left", padx=10)
        
        # Open folder button
        if self.ai_output:
            folder_btn = tk.Button(self.feedback_frame, text="[ OPEN FOLDER ]",
                                 command=lambda: subprocess.run(f'explorer /select,"{self.ai_output}"'),
                                 bg=CYAN, fg=BG_DARK, font=("Consolas", 10),
                                 relief="flat", cursor="hand2", padx=15, pady=10)
            folder_btn.pack(side="left", padx=10)
    
    def ai_yes(self):
        self.update_ai_chat("You: Yes, it's perfect!")
        self.feedback_frame.pack_forget()
        self.root.after(2000, self.show_main_menu)
    
    def ai_no(self):
        self.update_ai_chat("You: No, please change it...")
        self.update_ai_chat("AI: What should I change?")
        self.feedback_frame.pack_forget()
        self.feedback_shown = False


# ============== RUN ==============
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()