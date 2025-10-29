# Context Memory Management - CRITICAL INSTRUCTIONS

## � CONTEXT MEMORY DEFINITION

**Context Memory Location:** `Orchestration/generated/os-triage/context_mem/`

This is the **permanent directory** containing:
- All user directories and context memory files
- All company directories and context memory files  
- All incident directories and context memory files
- All context memory subdirectories and data structures

**Also known as:** `context_mem` or "context memory"

## 🧹 CLEARING CONTEXT MEMORY DEFINITION

**"Clearing the context memory"** means:
- ✅ **DELETE all files within** `generated/os-triage/context_mem/`
- ✅ **DELETE all subdirectories within** `generated/os-triage/context_mem/`
- ❌ **NEVER delete** the `context_mem` directory itself

## �🚨 CRITICAL RULE: NEVER DELETE CONTEXT DIRECTORIES

### ❌ FORBIDDEN OPERATIONS

```python
# NEVER DO THIS - Will break the context memory system
shutil.rmtree("generated/os-triage/context_mem")  # ❌ BREAKS SYSTEM
shutil.rmtree("Results")                          # ❌ BREAKS SYSTEM
```

### ✅ CORRECT CONTEXT CLEARING

```python
def clear_context_memory_contents_only():
    """Clear context memory contents - PRESERVE directory structure"""
    paths_to_clear = [
        "generated/os-triage/context_mem",
        "Results"
    ]
    
    for path_str in paths_to_clear:
        path = Path(path_str)
        if path.exists() and path.is_dir():
            # ONLY delete contents, NEVER the directory itself
            for item in path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            print(f"✅ Cleared contents of: {path}")
```

## 📁 REQUIRED DIRECTORY STRUCTURE

These directories MUST exist for context saving blocks to function:

```text
generated/
  └── os-triage/
      └── context_mem/          # NEVER DELETE - only clear contents
Results/                       # NEVER DELETE - only clear contents
```

## 🔧 RECOVERY PROCEDURE

If directories were accidentally deleted:

```python
import os
os.makedirs("generated/os-triage/context_mem", exist_ok=True)
os.makedirs("Results", exist_ok=True)
```

## 🎯 WHY THIS MATTERS

- Context saving blocks (`invoke_save_user_context_block`, etc.) depend on these directories existing
- Deleting directories breaks the context memory infrastructure
- Only the CONTENTS should be cleared between tests, not the directories themselves

## 📋 TESTING PROTOCOLS

1. **Before any equivalence test:** Clear context memory contents only (not directories)
   - Use the definition above: delete all files/subdirs within `context_mem/`
   - PRESERVE the `context_mem/` directory structure itself
2. **CRITICAL: Clear ALL notebook outputs** after clearing context memory (outputs become stale)
3. Verify `context_mem/` directory exists before running notebooks
4. Execute notebooks fresh (no cached outputs)
5. Never use `shutil.rmtree()` on `context_mem/` or `Results/` directories
6. Always preserve directory infrastructure

## 🔧 CORRECT IMPLEMENTATION

```python
def clear_context_memory(self):
    """Clear context memory contents - NEVER delete context_mem directory itself"""
    context_mem_path = Path("generated/os-triage/context_mem")
    
    if context_mem_path.exists() and context_mem_path.is_dir():
        # CRITICAL: Only delete CONTENTS, never the directory itself
        for item in context_mem_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"✅ Cleared contents of context_mem (directory preserved)")
```

## 🚨 Critical Workflow Rule
**After clearing context memory, ALWAYS clear all notebook outputs:**
- All existing outputs reference deleted files
- Outputs become misleading and cause analysis errors
- Must execute notebooks fresh to get accurate results

## 🚨 ENFORCEMENT

This rule is CRITICAL for:

- Equivalence testing between notebook sequences
- Context memory functionality
- STIX object storage and retrieval
- Template-driven architecture operations