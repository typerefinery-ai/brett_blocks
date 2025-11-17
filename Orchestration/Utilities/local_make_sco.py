import stixorm
from stixorm.module.definitions.stix21 import (
    Identity, EmailAddress, UserAccount, Relationship, Bundle, URL, EmailMessage
)
from stixorm.module.definitions.os_threat import (
    IdentityContact, EmailContact, SocialMediaContact, ContactNumber, Anecdote
)
from stixorm.module.authorise import import_type_factory
from stixorm.module.typedb_lib.instructions import ResultStatus, Result
from stixorm.module.parsing import parse_objects
import json
import os

context_base = "../Orchestration/Context_Mem/"
path_base = "../Block_Families/StixORM/"
results_base = "../Orchestration/Results/"


from Block_Families.StixORM.SCO.URL.make_url import main as make_url
from Block_Families.StixORM.SCO.EmailAddress.make_email_addr import main as make_email_addr
from Block_Families.StixORM.SCO.EmailMessage.make_email_message import main as make_email_msg
from Block_Families.StixORM.SCO.UserAccount.make_user_account import main as make_user_account
from Block_Families.StixORM.SCO.Anecdote.make_anecdote import main as make_anecdote
from .util import emulate_ports, unwind_ports, conv


def invoke_make_email_addr_block(email_path, results_path, acct_results=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    email_data_rel_path = path_base + email_path
    email_results_rel_path = results_base + results_path + "__email.json"
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    #
    if os.path.exists(email_data_rel_path):
        with open(email_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            if acct_results:
                results_data["user-account"] = acct_results
        with open(email_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    #
    # Make the Email Address object
    #
    make_email_addr(email_data_rel_path,email_results_rel_path)
    #
    # Remove Port Emulation - Fix the data file so it only has form data
    #
    unwind_ports(email_data_rel_path)

    # Retrieve the saved file
    if os.path.exists(email_results_rel_path):
        with open(email_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            email_addr = EmailAddress(**stix_object)
            print(email_addr.serialize(pretty=True))
            return conv(email_addr)


def invoke_make_user_account_block(user_path, results_path):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    # Set the Relative Input and Output Paths for the block
    acct_data_rel_path = path_base + user_path
    acct_results_rel_path = results_base + results_path + "__usr_acct.json"
    # Run the Make User Account block
    make_user_account(acct_data_rel_path, acct_results_rel_path)
    #
    # Remove Port Emulation - Fix the data file so it only has form data
    #
    # Retrieve the saved file
    if os.path.exists(acct_results_rel_path):
        with open(acct_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            usr_acct = UserAccount(**stix_object)
            print(usr_acct.serialize(pretty=True))
            return conv(usr_acct)



def invoke_make_url_block(url_path, results_path, hyperlink=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    url_data_rel_path = path_base + url_path
    url_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    # Add the URL object
    #  Form data file
    #
    if os.path.exists(url_data_rel_path):
        with open(url_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            results_data["hyperlink"] = hyperlink
        with open(url_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    #
    # 2. Make the URL object
    #
    make_url(url_data_rel_path,url_results_rel_path)
    #
    # Remove Port Emulation - Fix the data file so it only has form data
    #
    #unwind_ports(url_data_rel_path)
    # 2. Make the Email Address object
    make_url(url_data_rel_path,url_results_rel_path)
    # 3. Retrieve the saved file
    if hyperlink:
        if os.path.exists(url_results_rel_path):
            with open(url_results_rel_path, "r") as script_input:
                stix_object = json.load(script_input)
                # 4. convert it into a Stix Object and append to the bundle
                url_object = URL(**stix_object)
                print(url_object.serialize(pretty=True))
                return conv(url_object)


def invoke_make_e_msg_block(msg_path, results_path, from_ref=None, to_refs=None, cc_refs=None, bcc_refs=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    msg_data_rel_path = path_base + msg_path
    msg_results_rel_path = results_base + results_path
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    #
    if os.path.exists(msg_data_rel_path):
        with open(msg_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            if from_ref:
                results_data["from_ref"] = from_ref
            if to_refs or to_refs != []:
                results_data["to_refs"] = to_refs
            if cc_refs or cc_refs != []:
                results_data["cc_refs"] = cc_refs
            if bcc_refs or bcc_refs != []:
                results_data["bcc_refs"] = bcc_refs
        with open(msg_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    #
    # Make the Email Msg object
    #
    make_email_msg(msg_data_rel_path,msg_results_rel_path)
    #
    # Remove Port Emulation - Fix the data file so it only has form data
    #
    #unwind_ports(msg_data_rel_path)
    # 3. Retrieve the saved file
    if os.path.exists(msg_results_rel_path):
        with open(msg_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # 4. convert it into a Stix Object and append to the bundle
            msg_object = EmailMessage(**stix_object)
            print(msg_object.serialize(pretty=True))
            return conv(msg_object)



def invoke_make_anecdote_block(anecdote_path, results_path, anecdote_reporter=None):
    #
    # 1. Set the Relative Input and Output Paths for the block
    #
    anecdote_data_rel_path = path_base + anecdote_path
    anecdote_results_rel_path = results_base + results_path + "__anecdote.json"
    #
    # NOTE: This code is only To fake input ports
    # Add the User Account object and the  EmailAddress
    #  Form data file
    #
    if os.path.exists(anecdote_data_rel_path):
        with open(anecdote_data_rel_path, "r") as sro_form:
            results_data = json.load(sro_form)
            if anecdote_reporter:
                results_data["anecdote_reporter"] = anecdote_reporter
        with open(anecdote_data_rel_path, 'w') as f:
            f.write(json.dumps(results_data))
    #
    # Make the Email Address object
    #
    make_anecdote(anecdote_data_rel_path,anecdote_results_rel_path)
    #
    # Remove Port Emulation - Fix the data file so it only has form data
    #
    unwind_ports(anecdote_data_rel_path)

    # Retrieve the saved file
    if os.path.exists(anecdote_results_rel_path):
        with open(anecdote_results_rel_path, "r") as script_input:
            stix_object = json.load(script_input)
            # convert it into a Stix Object and append to the bundle
            anecdote = Anecdote(**stix_object)
            print(anecdote.serialize(pretty=True))
            return conv(anecdote)