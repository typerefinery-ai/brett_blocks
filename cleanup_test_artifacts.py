#!/usr/bin/env python3
"""
Cleanup Test Artifacts

This script removes all files and directories created during the round-trip test.
It reads the test_artifacts.json file to know what to delete.
"""

import json
import shutil
from pathlib import Path


def cleanup_artifacts():
    """Clean up all tracked test artifacts"""
    artifacts_file = Path('test_artifacts.json')
    
    if not artifacts_file.exists():
        print("❌ No test_artifacts.json found. Nothing to clean up.")
        return
    
    print("=" * 70)
    print("CLEANUP TEST ARTIFACTS")
    print("=" * 70)
    
    with open(artifacts_file, 'r') as f:
        artifacts = json.load(f)
    
    total_files = len(artifacts.get('files', []))
    total_dirs = len(artifacts.get('directories', []))
    
    print(f"\n📊 Found {total_files} files and {total_dirs} directories to clean up")
    
    # Delete files
    deleted_files = 0
    for filepath in artifacts.get('files', []):
        path = Path(filepath)
        if path.exists():
            try:
                path.unlink()
                deleted_files += 1
                print(f"   ✅ Deleted file: {path.name}")
            except Exception as e:
                print(f"   ❌ Failed to delete {path}: {e}")
    
    # Delete directories
    deleted_dirs = 0
    for dirpath in artifacts.get('directories', []):
        path = Path(dirpath)
        if path.exists() and path.is_dir():
            try:
                shutil.rmtree(path)
                deleted_dirs += 1
                print(f"   ✅ Deleted directory: {path.name}")
            except Exception as e:
                print(f"   ❌ Failed to delete {path}: {e}")
    
    # Delete the artifacts file itself
    try:
        artifacts_file.unlink()
        print(f"\n   ✅ Deleted artifacts list: {artifacts_file.name}")
    except Exception as e:
        print(f"\n   ❌ Failed to delete artifacts list: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ CLEANUP COMPLETE")
    print("=" * 70)
    print(f"   - Files deleted: {deleted_files}/{total_files}")
    print(f"   - Directories deleted: {deleted_dirs}/{total_dirs}")


if __name__ == '__main__':
    cleanup_artifacts()
