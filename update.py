#!/usr/bin/env python3
"""
MONOGRAPH AUTO-UPDATER v2
Downloads and updates to latest version from GitHub
"""

import os
import shutil
import urllib.request
import zipfile

REPO_URL = "https://github.com/nop727272/somepython-experiment/archive/refs/heads/main.zip"
REPO_FOLDER = "somepython-experiment-main"

def update():
    print("=" * 50)
    print("MONOGRAPH EDITOR - AUTO UPDATE")
    print("=" * 50)
    print()
    
    # Step 1: Download
    print("[1/4] Downloading latest version...")
    zip_file = "monograph_temp.zip"
    
    try:
        urllib.request.urlretrieve(REPO_URL, zip_file)
        print("      Download complete!")
    except Exception as e:
        print(f"      ERROR: {e}")
        return
    
    # Step 2: Extract
    print("[2/4] Extracting files...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(".")
        print("      Extraction complete!")
    except Exception as e:
        print(f"      ERROR: {e}")
        return
    
    # Step 3: Update files
    print("[3/4] Updating files...")
    updated = 0
    
    if os.path.exists(REPO_FOLDER):
        for item in os.listdir(REPO_FOLDER):
            src = os.path.join(REPO_FOLDER, item)
            dst = os.path.join(os.getcwd(), item)
            
            if os.path.isfile(src):
                if item.endswith((".py", ".txt", ".lua", ".html", ".bat", ".sh")):
                    try:
                        shutil.copy2(src, dst)
                        print(f"      Updated: {item}")
                        updated += 1
                    except:
                        pass
            elif os.path.isdir(src):
                try:
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"      Updated folder: {item}")
                    updated += 1
                except:
                    pass
    
    print(f"      Total: {updated} items updated")
    
    # Step 4: Cleanup
    print("[4/4] Cleaning up...")
    try:
        os.remove(zip_file)
    except:
        pass
    
    try:
        shutil.rmtree(REPO_FOLDER, ignore_errors=True)
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