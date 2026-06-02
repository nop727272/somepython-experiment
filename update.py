#!/usr/bin/env python3
"""
MONOGRAPH UPDATE SCRIPT v2
Run this to update to the latest version!
"""

import urllib.request
import zipfile
import os
import shutil

REPO_URL = "https://github.com/nop727272/somepython-experiment/archive/refs/heads/main.zip"
REPO_NAME = "somepython-experiment-main"

def update():
    print("=" * 50)
    print("MONOGRAPH EDITOR - AUTO UPDATE")
    print("=" * 50)
    print()
    
    # Download
    print("[1/4] Downloading from GitHub...")
    zip_path = "monograph_update.zip"
    
    try:
        urllib.request.urlretrieve(REPO_URL, zip_path)
        print(f"     Downloaded!")
    except Exception as e:
        print(f"     ERROR: {e}")
        print()
        print("Alternative: Download manually from:")
        print("https://github.com/nop727272/somepython-experiment")
        return
    
    # Extract
    print("[2/4] Extracting files...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        print(f"     Extracted!")
    except Exception as e:
        print(f"     ERROR: {e}")
        return
    
    # Copy files
    print("[3/4] Updating files...")
    updated = 0
    
    for root, dirs, files in os.walk(REPO_NAME):
        for f in files:
            src = os.path.join(root, f)
            rel_path = os.path.relpath(src, REPO_NAME)
            dst = os.path.join(os.getcwd(), rel_path)
            
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"     {rel_path}")
                updated += 1
            except Exception as e:
                pass
    
    print(f"     Updated {updated} files!")
    
    # Cleanup
    print("[4/4] Cleaning up...")
    try:
        os.remove(zip_path)
    except:
        pass
    
    try:
        shutil.rmtree(REPO_NAME, ignore_errors=True)
    except:
        pass
    
    print()
    print("=" * 50)
    print("UPDATE COMPLETE!")
    print("=" * 50)
    print()
    print("Run: py monograph-editor-gui.py")
    print()

if __name__ == "__main__":
    update()