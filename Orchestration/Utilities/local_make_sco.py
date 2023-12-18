import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/Objects/"
results_base = "../Orchestration/Results/"


from Block_Families.Objects.SCO.URL.make_url import main as make_url
from Block_Families.Objects.SCO.Email_Addr.make_email_addr import main as make_email_addr
from Block_Families.Objects.SCO.Email_Message.make_email_msg import main as make_email_msg
from Block_Families.Objects.SRO.Relationship.make_sro import main as make_sro
from utilities import emulate_ports, unwind_ports, conv