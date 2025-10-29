"""
Context Memory Equivalence Testing Script
========================================

This script systematically tests the equivalence of the new notebook sequence 
(Step_0 + Step_1 + Step_2 + Step_3) against the old notebook sequence
(Step_0_Build_Initial_Identities + Step_1_Create_Incident_with_an_Alert + Step_2_Get_the_Anecdote)

Test Plan:
1. Test 1: New Step_0 vs Old Step_0_Build_Initial_Identities
2. Test 2: New Step_0+Step_1 vs Old Step_0_Build_Initial_Identities+Step_1_Create_Incident_with_an_Alert
3. Test 3: New Step_0+Step_1+Step_2 vs Old Step_0_Build_Initial_Identities+Step_1_Create_Incident_with_an_Alert+Step_2_Get_the_Anecdote
4. Review: Analysis of Test 1, Test 2 and Test 3

For each test:
- Clear context memory
- Run notebook sequence
- Record context memory structure
- Compare file counts, types, and contents
"""

import os
import json
import shutil
from pathlib import Path

class ContextMemoryTester:
    def __init__(self):
        self.context_base = "generated/os-triage/context_mem"
        self.old_notebooks = [
            "Step_0_Build_Initial_Identities.ipynb",
            "Step_1_Create_Incident_with_an_Alert.ipynb", 
            "Step_2_Get the Anecdote.ipynb"
        ]
        self.new_notebooks = [
            "Step_0_User_Setup.ipynb",
            "Step_1_Company_Setup.ipynb",
            "Step_2_Create_Incident_with_an_Alert.ipynb",
            "Step_3_Get the Anecdote.ipynb"
        ]
        
    def clear_context_memory(self):
        """Clear all context memory while preserving directory structure"""
        context_path = Path(self.context_base)
        if context_path.exists():
            for item in context_path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        print(f"✅ Context memory cleared: {context_path}")
                    
    def capture_context_structure(self, label=""):
        """Capture the current context memory structure"""
        context_path = Path(self.context_base)
        structure = {
            "label": label,
            "directories": [],
            "files": {},
            "total_files": 0,
            "total_directories": 0
        }
        
        if context_path.exists():
            for root, dirs, files in os.walk(context_path):
                rel_root = os.path.relpath(root, context_path)
                if rel_root != ".":
                    structure["directories"].append(rel_root)
                    structure["total_directories"] += 1
                
                for file in files:
                    rel_path = os.path.join(rel_root, file) if rel_root != "." else file
                    structure["files"][rel_path] = {
                        "size": os.path.getsize(os.path.join(root, file)),
                        "exists": True
                    }
                    structure["total_files"] += 1
                    
        return structure
    
    def compare_structures(self, struct1, struct2):
        """Compare two context memory structures"""
        comparison = {
            "files_match": True,
            "directories_match": True,
            "differences": [],
            "summary": {}
        }
        
        # Compare file counts
        comparison["summary"]["struct1_files"] = struct1["total_files"]
        comparison["summary"]["struct2_files"] = struct2["total_files"]
        comparison["summary"]["struct1_dirs"] = struct1["total_directories"] 
        comparison["summary"]["struct2_dirs"] = struct2["total_directories"]
        
        # Compare files
        files1 = set(struct1["files"].keys())
        files2 = set(struct2["files"].keys())
        
        only_in_1 = files1 - files2
        only_in_2 = files2 - files1
        common_files = files1 & files2
        
        if only_in_1:
            comparison["files_match"] = False
            comparison["differences"].append(f"Files only in {struct1['label']}: {list(only_in_1)}")
            
        if only_in_2:
            comparison["files_match"] = False  
            comparison["differences"].append(f"Files only in {struct2['label']}: {list(only_in_2)}")
            
        # Compare directories
        dirs1 = set(struct1["directories"])
        dirs2 = set(struct2["directories"])
        
        if dirs1 != dirs2:
            comparison["directories_match"] = False
            comparison["differences"].append(f"Directory structure differs")
            comparison["differences"].append(f"Dirs in {struct1['label']}: {sorted(dirs1)}")
            comparison["differences"].append(f"Dirs in {struct2['label']}: {sorted(dirs2)}")
            
        return comparison
    
    def print_structure(self, structure):
        """Print a context memory structure in a readable format"""
        print(f"\n📁 Context Structure: {structure['label']}")
        print(f"   Total Files: {structure['total_files']}")
        print(f"   Total Directories: {structure['total_directories']}")
        
        if structure['directories']:
            print("   Directories:")
            for dir_name in sorted(structure['directories']):
                print(f"     - {dir_name}/")
                
        if structure['files']:
            print("   Files:")
            for file_path in sorted(structure['files'].keys()):
                size = structure['files'][file_path]['size']
                print(f"     - {file_path} ({size} bytes)")
                
    def print_comparison(self, comparison):
        """Print comparison results in a readable format"""
        print(f"\n🔍 Comparison Results:")
        print(f"   Files Match: {'✅' if comparison['files_match'] else '❌'}")
        print(f"   Directories Match: {'✅' if comparison['directories_match'] else '❌'}")
        
        if comparison['differences']:
            print("   Differences:")
            for diff in comparison['differences']:
                print(f"     - {diff}")
                
        print(f"   Summary:")
        summary = comparison['summary']
        print(f"     - Structure 1: {summary['struct1_files']} files, {summary['struct1_dirs']} dirs")
        print(f"     - Structure 2: {summary['struct2_files']} files, {summary['struct2_dirs']} dirs")

# Example usage for manual testing
if __name__ == "__main__":
    tester = ContextMemoryTester()
    
    print("🧪 Context Memory Equivalence Tester")
    print("====================================")
    print()
    print("This script provides tools to compare context memory structures")
    print("between old and new notebook sequences.")
    print()
    print("Manual Usage:")
    print("1. Run: tester.clear_context_memory()")
    print("2. Execute old notebook sequence")
    print("3. Capture: old_structure = tester.capture_context_structure('Old Sequence')")
    print("4. Run: tester.clear_context_memory()")  
    print("5. Execute new notebook sequence")
    print("6. Capture: new_structure = tester.capture_context_structure('New Sequence')")
    print("7. Compare: tester.compare_structures(old_structure, new_structure)")
    print()