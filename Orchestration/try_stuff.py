from stixorm.module.definitions.stix21 import (
    Process, File
)
from Orchestration.Common.convert_n_and_e import convert_node
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