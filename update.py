#!/usr/bin/env python3
"""
MONOGRAPH UPDATE SCRIPT
Run this to update to the latest version!
"""

import urllib.request
import zipfile
import os
import sys

REPO_URL = "https://github.com/nop727272/somepython-experiment/archive/main.zip"
REPO_NAME = "somepython-experiment-main"

def update():
    print("=" * 50)
    print("MONOGRAPH EDITOR - AUTO UPDATE")
    print("=" * 50)
    print()
    
    # Check for updates
    print("[1/5] Checking for updates...")
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/nop727272/somepython-experiment/releases/latest",
            headers={"User-Agent": "Monograph"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode()
        
        import json
        release = json.loads(data)
        version = release.get("tag_name", "v1.0.0").replace("v", "")
        
        print(f"     Latest version: {version}")
        print("     Current version: 4.1.0")
        print()
    except Exception as e:
        print(f"     Could not check version: {e}")
        print()
    
    # Download
    print("[2/5] Downloading from GitHub...")
    zip_path = "monograph_update.zip"
    
    try:
        urllib.request.urlretrieve(REPO_URL, zip_path)
        print(f"     Downloaded: {zip_path}")
    except Exception as e:
        print(f"     ERROR downloading: {e}")
        return
    
    # Extract
    print("[3/5] Extracting files...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        print(f"     Extracted to: {REPO_NAME}")
    except Exception as e:
        print(f"     ERROR extracting: {e}")
        return
    
    # Copy files
    print("[4/5] Updating files...")
    updated = 0
    
    for f in os.listdir(REPO_NAME):
        src = os.path.join(REPO_NAME, f)
        dst = os.path.join(os.getcwd(), f)
        
        if os.path.isfile(src):
            if f.endswith(".py") or f.endswith(".txt") or f.endswith(".lua") or f.endswith(".html") or f.endswith(".sh"):
                try:
                    shutil.copy2(src, dst)
                    print(f"     Updated: {f}")
                    updated += 1
                except:
                    pass
        elif os.path.isdir(src):
            for sub_f in os.listdir(src):
                sub_src = os.path.join(src, sub_f)
                sub_dst = os.path.join(dst, sub_f)
                if os.path.isfile(sub_src):
                    try:
                        os.makedirs(dst, exist_ok=True)
                        shutil.copy2(sub_src, sub_dst)
                        updated += 1
                    except:
                        pass
    
    print(f"     Updated {updated} files!")
    
    # Cleanup
    print("[5/5] Cleaning up...")
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
    import shutil
    update()