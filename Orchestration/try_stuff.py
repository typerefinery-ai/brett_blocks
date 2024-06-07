from Block_Families.Context.Tab_Selections.sighting_index import main as sighting_index
from Block_Families.Context.Tab_Selections.task_index import main as task_index
from Block_Families.Context.Tab_Selections.impact_index import main as impact_index
from Block_Families.Context.Tab_Selections.event_index import main as event_index
from Block_Families.Context.Tab_Selections.company_index import main as company_index
from Block_Families.Context.Tab_Selections.me_index import main as me_index
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, Software, Process, File
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber
)
from Block_Families.General._library.convert_n_and_e import convert_node
from Block_Families.Context.Tab_Selections.get_unattached import get_unattached
import json
import os
from Utilities.util import conv


context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/Objects/"
results_base = "../Orchestration/Results/examples/"

data_path = ""
sighting_results_path = "sightingIndex.json"
task_results_path = "taskIndex.json"
impact_results_path = "impactIndex.json"
event_results_path = "eventIndex.json"
company_results_path = "companyIndex.json"
me_results_path = "meIndex.json"
#
# sighting_index(data_path, results_base + sighting_results_path)
# task_index(data_path, results_base + task_results_path)
# impact_index(data_path, results_base + impact_results_path)
# event_index(data_path, results_base + event_results_path)
# company_index(data_path, results_base + company_results_path)
# me_index(data_path, results_base + me_results_path)

hashes ={"SHA-256": "fe90a7e910cb3a4739bed9180e807e93fa70c90f25a8915476f5e4bfbac681db"}
file = File(name="evil.exe", hashes=hashes)


process = Process(pid=1221, created_time="2023-01-20T14:11:25.55Z",
                  command_line="./gedit-bin --destroy-alll", image_ref=file.id)
nodes2, edges2 = convert_node(conv(process))