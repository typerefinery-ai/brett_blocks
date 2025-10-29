################################################################################
## header start                                                               ##
################################################################################
# allow importing og service local packages
import os.path

where_am_i = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.environ["APP_SERVICE_PACKAGES_PATH"])
# sys.path.append(where_am_i)
# end of local package imports
################################################################################
## header end                                                                 ##
################################################################################


################################################################################
## body start                                                                 ##
################################################################################

##############################################################################
# Title: Clear Context Memory
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 29/10/2025
#
# Description: This block clears all context memory contents while preserving
#              the directory structure. CRITICAL: Never deletes the context_mem
#              directory itself, only its contents.
#
# One Optional Input:
# 1. clear_options (optional) - specify what to clear
# One Output:
# 1. context_result - confirmation of what was cleared
#
# This code is licensed under the terms of the BSD.
##############################################################################

from stixorm.module.authorise import import_type_factory
import json
import os
import shutil
from pathlib import Path

import importlib.util
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import_type = import_type_factory.get_all_imports()

# Common File Stuff
TR_Common_Files = "./generated/os-triage/common_files"
common = [
    {"module": "convert_n_and_e", "file": "convert_n_and_e.py", "url" : "https://raw.githubusercontent.com/typerefinery-ai/brett_blocks/main/Block_Families/General/_library/convert_n_and_e.py"}
]

# OS_Triage Memory Stuff
TR_Context_Memory_Dir = "./generated/os-triage/context_mem"
TR_User_Dir = "/usr"
context_map = "context_map.json"
user_data = {
    "global": "/global_variables_dict.json",
    "me": "/cache_me.json",
    "team": "/cache_team.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
comp_data = {
    "users": "/users.json",
    "company" : "/company.json",
    "assets" : "/assets.json",
    "systems" : "/systems.json",
    "relations" : "/relations.json",
    "edges" : "/edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
incident_data = {
    "incident" : "/incident.json",
    "start" : "/sequence_start_refs.json",
    "sequence" : "/sequence_refs.json",
    "impact" : "/impact_refs.json",
    "event" : "/event_refs.json",
    "task" : "/task_refs.json",
    "other" : "/other_object_refs.json",
    "unattached" : "/unattached_objs.json",
    "unattached_relations" : "/unattached_relation.json",
    "relations" : "/incident_relations.json",
    "edges" : "/incident_edges.json",
    "relation_edges" : "/relation_edges.json",
    "relation_replacement_edges" : "/relation_replacement_edges.json"
}
field_names = {
    "start" : "sequence_start_refs",
    "sequence" : "sequence_refs",
    "impact" : "impact_refs",
    "event" : "event_refs",
    "task" : "task_refs",
    "other" : "other_object_refs"
}
key_list = ["start", "sequence", "impact", "event", "task", "other"]


def clear_context_memory(clear_options=None):
    """
    Clear context memory contents while preserving directory structure.
    
    CRITICAL: This function NEVER deletes the context_mem directory itself,
    only its contents (files and subdirectories).
    
    Args:
        clear_options (dict, optional): Options for what to clear
            - "scope": "all" (default), "user", "company", "incident"
            - "preserve_structure": True (default) - keeps directories
    
    Returns:
        str: Report of what was cleared
    """
    
    # Default options
    if clear_options is None:
        clear_options = {"scope": "all", "preserve_structure": True}
    
    scope = clear_options.get("scope", "all")
    preserve_structure = clear_options.get("preserve_structure", True)
    
    cleared_items = []
    
    # Ensure context memory directory exists
    context_mem_path = Path(TR_Context_Memory_Dir)
    if not context_mem_path.exists():
        os.makedirs(context_mem_path, exist_ok=True)
        logger.info(f"Created context memory directory: {context_mem_path}")
        return f"Context memory directory created: {context_mem_path}"
    
    logger.info(f"Clearing context memory - Scope: {scope}, Preserve structure: {preserve_structure}")
    
    try:
        if scope == "all":
            # Clear all contents of context_mem directory
            for item in context_mem_path.iterdir():
                if item.is_file():
                    item.unlink()
                    cleared_items.append(f"file: {item.name}")
                    logger.info(f"Deleted file: {item}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    cleared_items.append(f"directory: {item.name}/")
                    logger.info(f"Deleted directory: {item}")
        
        elif scope == "user":
            # Clear only user-related data
            user_dir = context_mem_path / "usr"
            if user_dir.exists():
                shutil.rmtree(user_dir)
                cleared_items.append("directory: usr/")
                logger.info(f"Deleted user directory: {user_dir}")
        
        elif scope == "company":
            # Clear company directories (pattern: company_*)
            for item in context_mem_path.iterdir():
                if item.is_dir() and item.name.startswith("company_"):
                    shutil.rmtree(item)
                    cleared_items.append(f"directory: {item.name}/")
                    logger.info(f"Deleted company directory: {item}")
        
        elif scope == "incident":
            # Clear incident directories (pattern: incident_*) 
            for item in context_mem_path.iterdir():
                if item.is_dir() and item.name.startswith("incident_"):
                    shutil.rmtree(item)
                    cleared_items.append(f"directory: {item.name}/")
                    logger.info(f"Deleted incident directory: {item}")
            
            # Also clear context_map.json if it exists
            context_map_file = context_mem_path / context_map
            if context_map_file.exists():
                context_map_file.unlink()
                cleared_items.append(f"file: {context_map}")
                logger.info(f"Deleted context map: {context_map_file}")
        
        else:
            return f"Error: Unknown scope '{scope}'. Valid options: 'all', 'user', 'company', 'incident'"
        
        # Verify context_mem directory still exists
        if not context_mem_path.exists():
            # This should never happen, but if it does, recreate it
            os.makedirs(context_mem_path, exist_ok=True)
            logger.warning("Context memory directory was accidentally deleted - recreated")
        
        if cleared_items:
            result_msg = f"Context memory cleared (scope: {scope}). Removed: {len(cleared_items)} items - {', '.join(cleared_items[:5])}"
            if len(cleared_items) > 5:
                result_msg += f" ... and {len(cleared_items) - 5} more"
        else:
            result_msg = f"Context memory was already empty (scope: {scope})"
            
        # Additional safety check: ensure Results directory exists too
        results_path = Path("./Results")
        if not results_path.exists():
            os.makedirs(results_path, exist_ok=True)
            os.makedirs(results_path / "step0", exist_ok=True)
            os.makedirs(results_path / "step0" / "context", exist_ok=True)
            os.makedirs(results_path / "step1", exist_ok=True) 
            os.makedirs(results_path / "step1" / "context", exist_ok=True)
            result_msg += " | Results directories created"
        
        logger.info(f"Context memory clearing complete: {result_msg}")
        return result_msg
        
    except Exception as e:
        error_msg = f"Error clearing context memory: {str(e)}"
        logger.error(error_msg)
        return error_msg


def main(inputfile, outputfile):
    """
    Main function following brett_blocks standard signature.
    
    Input format:
    {
        "clear_options": {
            "scope": "all|user|company|incident",
            "preserve_structure": true
        }
    }
    
    Output format:
    {
        "context_result": "description of what was cleared"
    }
    """
    clear_options = None
    
    # Read input if file exists
    if os.path.exists(inputfile):
        try:
            with open(inputfile, "r") as script_input:
                input_data = json.load(script_input)
                clear_options = input_data.get("clear_options")
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Could not parse input file {inputfile}: {e}")
    
    # Execute context memory clearing
    result_string = clear_context_memory(clear_options)
    
    # Prepare output
    context_result = {
        "context_result": result_string,
        "timestamp": str(Path().cwd()),  # Include current working directory for debugging
        "operation": "clear_context_memory"
    }
    
    # Write output
    with open(outputfile, "w") as outfile:
        json.dump(context_result, outfile, indent=2)
    
    logger.info(f"Context memory clearing result written to: {outputfile}")


################################################################################
## body end                                                                   ##
################################################################################


################################################################################
## footer start                                                               ##
################################################################################
import argparse
import os


def getArgs():

  parser = argparse.ArgumentParser(description="Script params",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("inputfile", nargs='?', default=f"{os.path.basename(__file__)}.input", help="input file (default: %(default)s)")
  parser.add_argument("outputfile", nargs='?', default=f"{os.path.basename(__file__)}.output", help="output file (default: %(default)s)")
  return parser.parse_args()

if __name__ == '__main__':
  args = getArgs()
  # setup logger for init
  # log = Logger
  # log.remove()
  # log.add(f'{os.path.basename(__file__)}.log', level="INFO")
  # log.info(args)
  main(args.inputfile, args.outputfile)


################################################################################
## footer end                                                                 ##
################################################################################