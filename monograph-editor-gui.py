#!/usr/bin/env python3
"""
MONOGRAPH EDITOR - Simple GUI Interface
Click buttons, select files, create videos!
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import subprocess

class MonographEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monograph Video Editor")
        self.root.geometry("600x500")
        self.root.configure(bg="#1a1a2e")
        
        # Variables
        self.clips_folder = tk.StringVar(value="clips")
        self.audio_file = tk.StringVar(value="")
        self.output_file = tk.StringVar(value="FINAL_MONOGRAPH_EDIT.mp4")
        self.title_text = tk.StringVar(value="NARUTO")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="MONOGRAPH VIDEO EDITOR", 
                        font=("Arial", 24, "bold"), fg="#e94560", bg="#1a1a2e")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="Create cinematic edits with one click", 
                           font=("Arial", 10), fg="#888", bg="#1a1a2e")
        subtitle.pack()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Clips folder
        row = 0
        tk.Label(main_frame, text="Video Clips Folder:", fg="#fff", bg="#1a1a2e", 
                font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=10)
        
        frame = tk.Frame(main_frame, bg="#16213e")
        frame.grid(row=row, column=1, sticky="ew", pady=10, padx=5)
        
        tk.Entry(frame, textvariable=self.clips_folder, width=30, bg="#0f3460", 
                fg="#fff", insertbackground="#fff").pack(side="left", padx=5, pady=5)
        
        tk.Button(frame, text="Browse", command=self.browse_clips, 
                 bg="#e94560", fg="#fff", relief="flat", padx=10).pack(side="right", padx=5, pady=5)
        
        # Audio file
        row += 1
        tk.Label(main_frame, text="Audio File:", fg="#fff", bg="#1a1a2e", 
                font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=10)
        
        frame = tk.Frame(main_frame, bg="#16213e")
        frame.grid(row=row, column=1, sticky="ew", pady=10, padx=5)
        
        tk.Entry(frame, textvariable=self.audio_file, width=30, bg="#0f3460", 
                fg="#fff", insertbackground="#fff").pack(side="left", padx=5, pady=5)
        
        tk.Button(frame, text="Browse", command=self.browse_audio, 
                 bg="#e94560", fg="#fff", relief="flat", padx=10).pack(side="right", padx=5, pady=5)
        
        # Title text
        row += 1
        tk.Label(main_frame, text="Title Text:", fg="#fff", bg="#1a1a2e", 
                font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=10)
        
        entry = tk.Entry(main_frame, textvariable=self.title_text, width=32, bg="#0f3460", 
                        fg="#fff", insertbackground="#fff")
        entry.grid(row=row, column=1, sticky="w", pady=10)
        
        # Output file
        row += 1
        tk.Label(main_frame, text="Output File:", fg="#fff", bg="#1a1a2e", 
                font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=10)
        
        entry = tk.Entry(main_frame, textvariable=self.output_file, width=32, bg="#0f3460", 
                        fg="#fff", insertbackground="#fff")
        entry.grid(row=row, column=1, sticky="w", pady=10)
        
        # Status
        row += 1
        self.status_label = tk.Label(main_frame, text="Ready to create your edit!", 
                                    fg="#4ecca3", bg="#1a1a2e", font=("Arial", 10))
        self.status_label.grid(row=row, column=0, columnspan=2, pady=20)
        
        # Run button
        row += 1
        run_btn = tk.Button(main_frame, text="CREATE VIDEO", command=self.run_editor,
                           font=("Arial", 14, "bold"), bg="#e94560", fg="#fff",
                           relief="flat", padx=30, pady=15, cursor="hand2")
        run_btn.grid(row=row, column=0, columnspan=2, pady=10)
        
        # Help text
        row += 1
        help_text = tk.Label(self.root, 
                            text="1. Put clips in 'clips' folder  |  2. Select audio file  |  3. Click CREATE",
                            fg="#666", bg="#1a1a2e", font=("Arial", 9))
        help_text.pack(pady=10)
        
    def browse_clips(self):
        folder = filedialog.askdirectory(title="Select clips folder")
        if folder:
            self.clips_folder.set(folder)
            
    def browse_audio(self):
        file = filedialog.askopenfilename(title="Select audio file",
                                         filetypes=[("MP3 files", "*.mp3"), 
                                                   ("All files", "*.*")])
        if file:
            self.audio_file.set(file)
            
    def run_editor(self):
        clips = self.clips_folder.get()
        audio = self.audio_file.get()
        output = self.output_file.get()
        title = self.title_text.get()
        
        # Validate
        if not clips:
            messagebox.showerror("Error", "Please select a clips folder!")
            return
            
        if not audio:
            messagebox.showerror("Error", "Please select an audio file!")
            return
            
        if not os.path.exists(clips):
            messagebox.showerror("Error", f"Clips folder not found: {clips}")
            return
            
        if not os.path.exists(audio):
            messagebox.showerror("Error", f"Audio file not found: {audio}")
            return
            
        # Check for clips
        clips_found = list(Path(clips).glob("*.mp4")) + list(Path(clips).glob("*.mov")) + \
                     list(Path(clips).glob("*.avi")) + list(Path(clips).glob("*.mkv"))
        
        if not clips_found:
            messagebox.showerror("Error", f"No video clips found in {clips}\n\nSupported: .mp4, .mov, .avi, .mkv")
            return
            
        self.status_label.config(text=f"Found {len(clips_found)} clips. Creating video...")
        self.root.update()
        
        # Build command
        cmd = [
            "py", "monograph-auto-editor.py",
            "--clips-folder", clips,
            "--audio", audio,
            "--output", output,
            "--title", title
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.status_label.config(text="Video created successfully!", fg="#4ecca3")
                messagebox.showinfo("Success!", f"Your video is ready:\n{output}")
            else:
                self.status_label.config(text="Error creating video", fg="#e94560")
                messagebox.showerror("Error", result.stderr or "Something went wrong!")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Error", fg="#e94560")


def padx(l, r):
    return (l, r)

if __name__ == "__main__":
    root = tk.Tk()
    app = MonographEditorGUI(root)
    root.mainloop()