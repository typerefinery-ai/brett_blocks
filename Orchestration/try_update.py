
from stixorm.module.typedb import TypeDBSink, TypeDBSource
from stixorm.module.authorise import import_type_factory
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, Incident, URL, EmailMessage, ObservedData
)
from stixorm.module.definitions.os_threat import (
    EventCoreExt, Event, SocialMediaContact, ContactNumber, IncidentCoreExt, TaskCoreExt,
    Task, SightingEvidence, Sequence, SequenceExt, AnecdoteExt, Anecdote,
    SightingAnecdote, SightingAlert, SightingContext, SightingExclusion,
    SightingEnrichment, SightingHunt, SightingFramework, SightingExternal
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
from deepdiff import DeepDiff, parse_path
from pprint import pprint

import_type = import_type_factory.get_all_imports()
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import json
import os

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
def load_context():
    cwd = os.getcwd()
    print(f"cwd {cwd}")
    # 1. Load the Context
    TR_Context_Memory_Path = "./Orchestration/Context_Mem/Type_Refinery_Context.json"
    with open(TR_Context_Memory_Path, "r") as context_file:
        Type_Refinery_Context = json.load(context_file)
    #
    # 2. Setup the  TR User Context
    #
    local = Type_Refinery_Context["local"]
    me = local["me"]
    team = local["team"]
    company = local["company"]
    systems = local["systems"]
    assets = local["assets"]
    #
    # 3. Setup the Incident Context
    #
    incident = Type_Refinery_Context["incident"]
    sequence_start_objs = incident["sequence_start_objs"]
    sequence_objs = incident["sequence_objs"]
    task_objs = incident["task_objs"]
    event_objs = incident["event_objs"]
    impact_objs = incident["impact_objs"]
    other_object_objs = incident["other_object_objs"]
    incident_obj = incident["incident_obj"]

    #
    # 4. Load the TypeDB Context
    #
    typedb = Type_Refinery_Context["typedb"]
    t_sequence_start_objs = typedb["sequence_start_objs"]
    t_sequence_objs = typedb["sequence_objs"]
    t_task_objs = typedb["task_objs"]
    t_event_objs = typedb["event_objs"]
    t_impact_objs = typedb["impact_objs"]
    t_other_object_objs = typedb["other_object_objs"]
    t_incident_obj = typedb["incident_obj"]
    #
    # 5. Add the lists together and put them into typedb
    #
    typedb_add_list = t_sequence_start_objs + t_sequence_objs + t_task_objs + t_event_objs + t_other_object_objs + t_impact_objs
    typedb_add_list = typedb_add_list + me + team + company + systems + assets
    typedb_add_list.append(t_incident_obj)
    typedb_sink = TypeDBSink(connection, True, import_type)
    results_raw = typedb_sink.add(typedb_add_list)
    result_list = [res.model_dump_json() for res in results_raw]
    for res in result_list:
        print(f"\n result is -> {res}")




# if this file is run directly, then start here
if __name__ == '__main__':
    load_context()