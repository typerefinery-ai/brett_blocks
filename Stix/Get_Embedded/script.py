##############################################################################
# Title: Get Report
# Author: OS-Threat
# Organisation Repo: https://github.com/typerefinery-ai/brett_blocks
# Contact Email: denis@cloudaccelerator.co
# Date: 07/08/2023
#
# Description: This script is designed to take in a Connection, and a Report ID,
#       nd return a list of Stix objects containing the report and all dependencies
# One Input:
# 1. Stix_Object
# One Output
# 1. Stix_ID_List
#
# This code is licensed under the terms of the BSD.
##############################################################################

from typedb.client import *
from loguru import logger as Logger
from stixorm.module.typedb import TypeDBSource
from stixorm.module.authorise import import_type_factory
from posixpath import basename
import json
import copy
import os
import sys
import argparse

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
logger = logging.getLogger(__name__)

import_type = import_type_factory.get_all_imports()

connection = {
    "uri": "localhost",
    "port": "1729",
    "database": "stix_test",
    "user": None,
    "password": None
}
report_url = "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json"

report_id = "report--f2b63e80-b523-4747-a069-35c002c690db"

report_dict = {
      "type": "report",
      "spec_version": "2.1",
      "id": "report--f2b63e80-b523-4747-a069-35c002c690db",
      "created_by_ref": "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
      "created": "2015-05-15T09:12:16.432Z",
      "modified": "2015-05-15T09:12:16.432Z",
      "name": "Poison Ivy: Assessing Damage and Extracting Intelligence",
      "report_types": [
        "threat-report",
        "malware"
      ],
      "published": "2013-08-21T00:00:00.000000Z",
      "description": "This report spotlights Poison Ivy (PIVY), a RAT that remains popular and effective a full eight years after its release, despite its age and familiarity in IT security circles. Poison Ivy is a remote access tool that is freely available for download from its official web site at www.poisonivy-rat.com. First released in 2005, the tool has gone unchanged since 2008 with version 2.3.2. Poison Ivy includes features common to most Windows-based RATs, including key logging, screen capturing, video capturing, file transfers, system administration, password theft, and traffic relaying. Poison Ivy's wide availability and easy-to-use features make it a popular choice for all kinds of criminals. But it is probably most notable for its role in many high profile, targeted APT attacks. These APTs pursue specific targets, using RATs to maintain a persistent presence within the target's network. They move laterally and escalate system privileges to extract sensitive information-whenever the attacker wants to do so. Because some RATs used in targeted attacks are widely available, determining whether an attack is part of a broader APT campaign can be difficult. Equally challenging is identifying malicious traffic to determine the attacker's post-compromise activities and assess overall damage - these RATs often encrypt their network communications after the initial exploit. In 2011, three years after the most recent release of PIVY, attackers used the RAT to compromise security firm RSA and steal data about its SecureID authentication system. That data was subsequently used in other attacks. The RSA attack was linked to Chinese threat actors and described at the time as extremely sophisticated. Exploiting a zero-day vulnerability, the attack delivered PIVY as the payload. It was not an isolated incident. The campaign appears to have started in 2010, with many other companies compromised. PIVY also played a key role in the 2011 campaign known as Nitro that targeted chemical makers, government agencies, defense contractors, and human rights groups. Still active a year later, the Nitro attackers used a zero-day vulnerability in Java to deploy PIVY in 2012. Just recently, PIVY  was the payload of a zero-day exploit in Internet Explorer used in what is known as a 'strategic web compromise' attack against visitors to a U.S. government website and a variety of others. RATs require live, direct, real-time human interaction by the APT attacker. This characteristic is distinctly different from crimeware (malware focused on cybercrime), where the criminal can issue commands to their botnet of compromised endpoints whenever they please and set them to work on a common goal such as a spam relay. In contrast, RATs are much more personal and may indicate that you are dealing with a dedicated threat actor that is interested in your organization specifically.",
      "object_refs": [
        "malware--591f0cb7-d66f-4e14-a8e6-5927b597f920",
        "malware--61a62a6a-9a18-4758-8e52-622431c4b8ae",
        "malware--30ea087f-7d2b-496b-9ed1-5f000c8b7695",
        "malware--4de25c38-5826-4ee7-b84d-878064de87ad",
        "malware--dc669921-4a1a-470d-bfae-694e740ce181",
        "malware--f86febd3-609b-4d2e-9fec-aa805cb498bf",
        "malware--80c260d9-a075-4148-9301-ebe4af27f449",
        "malware--3ed0364f-62c8-4ebc-b136-deaf6966880b",
        "malware--17099f03-5ec8-456d-a2de-968aebaafc78",
        "malware--feaf146d-ea67-4eb1-946a-6f352ff79a81",
        "malware--13791e02-6621-45fb-8c10-f6b72e1bf553",
        "malware--703a15a7-eb85-475d-a27a-77d8fcf8f7b9",
        "malware--fade08cb-fa57-485e-97f8-fab5a1bd4460",
        "malware--3050937d-6330-44c7-83ba-8821e1f7e7bd",
        "malware--9d995717-edc3-4bd8-8554-aecf773bdecc",
        "malware--40e15fa5-df8d-4771-a682-21dab0a024fd",
        "malware--69101c2f-da92-47af-b402-7c60a39a982f",
        "malware--1601b8c2-5e6f-4a18-a413-10527e5d90b7",
        "malware--626badcc-4257-4222-946c-6d6e889836ea",
        "malware--3b275ed1-9c2e-4443-b1dd-5cfb51eaef2e",
        "malware--f138b6e0-9a7d-4cd9-a904-08a7df2eabb1",
        "malware--302ac5b5-486c-4c99-8cad-4426aeaf47b6",
        "malware--e1c02dca-d3fe-48f1-bb4b-3cacd2bc3619",
        "malware--a4f315bd-e159-4bfb-8439-0d5a8330fc70",
        "identity--81cade27-7df8-4730-836b-62d880e6d9d3",
        "campaign--752c225d-d6f6-4456-9130-d9580fd4007b",
        "campaign--d02a1560-ff69-49f4-ac34-919b8aa4b91e",
        "campaign--721976f9-56d7-4749-8c69-b3ac7c315f05",
        "attack-pattern--19da6e1c-69a8-4c2f-886d-d620d09d3b5a",
        "attack-pattern--ea2c747d-4aa3-4573-8853-37b7159bc180",
        "attack-pattern--fb6aa549-c94a-4e45-b4fd-7e32602dad85",
        "course-of-action--70b3d5f6-374b-4488-8688-729b6eedac5b",
        "indicator--e8094b09-7df4-4b13-b207-1e27af3c4bde",
        "indicator--329ae6e9-25bd-49e8-89d1-aae4ca52e4a7",
        "indicator--54e1e351-fec0-41a4-b62c-d7f86101e241",
        "indicator--2e59f00b-0986-437e-9ebd-e0d61900d688",
        "indicator--8da68996-f175-4ae0-bd74-aad4913873b8",
        "indicator--4e11b23f-732b-418e-b786-4dbf65459d50",
        "indicator--b7fa7e73-e645-4813-9723-161bbd8dda62",
        "indicator--b2f09ce0-2db4-480f-bd2f-073ddb3a0c87",
        "indicator--9842a3b9-fc5b-44c4-bb48-578cf6f728d9",
        "indicator--4e4c4ad7-4909-456a-b6fa-e24a6f682a40",
        "indicator--137acf67-cedc-4a07-8719-72759174de3a",
        "indicator--9695dc2f-d92a-4f2b-8b16-b0e21d7c631d",
        "indicator--7fd865ed-93e9-481f-953b-82ab386190ae",
        "indicator--e5bc6507-d052-447f-93c7-db7ef32211da",
        "indicator--fead5c52-9533-405c-b822-a034092a1ba8",
        "indicator--405ff732-2c35-4f46-9f78-2a632ce36e03",
        "indicator--4d58096e-b5c9-47d8-af9a-1af5f4762d6b",
        "indicator--9c725598-a160-4e91-8b93-ed0956709892",
        "indicator--2efe7c62-1b96-4568-81ee-c85b840bde39",
        "indicator--b8322c9b-8031-4fb3-9cbc-8a1ea0fe3cfa",
        "indicator--b08f9631-dd94-4d99-a96c-32b42af2ea81",
        "indicator--950c01b8-c647-4cc8-b0c1-3612fa780108",
        "indicator--ae29faa6-5f70-4eb8-981b-30818433a52e",
        "indicator--b6cc482d-89db-4e6b-a592-723070f6d22d",
        "indicator--0b71628d-31dd-4eb8-baee-39f19c0a14b0",
        "vulnerability--c7cab3fb-0822-43a5-b1ba-c9bab34361a2",
        "vulnerability--6a2eab9c-9789-4437-812b-d74323fa3bca",
        "vulnerability--2b7f00d8-b133-4a92-9118-46ce5f8b2531",
        "vulnerability--4d7dc9cb-983f-40b4-b597-d7a38b2d9a4b",
        "vulnerability--8323404c-1fdd-4272-822b-829f85556c53",
        "vulnerability--717cb1c9-eab3-4330-8340-e4858055aa80",
        "relationship--26c5311c-9d9b-4b9b-b3b5-bac10e16a7a3",
        "relationship--e794befc-3270-4050-b560-b6b080ab0418",
        "relationship--77a4c40e-3c33-43dc-8c78-04992ebcabf2",
        "relationship--a91f3d5c-ceac-44cf-b92b-efb819241606",
        "relationship--134c393e-cbe0-433c-9a7a-95263ed8578f",
        "relationship--900b11dc-bfa7-4dea-adb6-0e8d726b4ded",
        "relationship--8076ec7c-f6f6-4dca-a239-8bb6b5ad0c10",
        "relationship--0dd66a71-c45b-4786-bd7b-92cf952afdc1",
        "relationship--dc37f2bb-1a45-48b1-864e-c34dcde75d1d",
        "relationship--670ae011-1649-44e2-a63e-ead0b4a4cffd",
        "relationship--1a2a3630-5764-4d6e-a3c3-cb4ca27ff5f5",
        "relationship--b5046891-d2c0-4497-a167-594f778517f8",
        "relationship--253dbb93-c6f9-4839-8ce9-026c7b0a81e1",
        "relationship--d70ebcc3-5640-423d-b9b0-7158c532c040",
        "relationship--3bb540a4-c3be-478e-85e2-2a6c294c3dbd",
        "relationship--4e726ced-0207-4196-8a14-4400c09b039e",
        "relationship--b9736cd3-9482-4094-9178-1cde2b273aff",
        "relationship--70205e3e-195d-4bd5-a208-ada6cdf143e3",
        "relationship--6bb5a995-b874-4e17-88eb-38e00c8e5740",
        "relationship--d4247377-5302-4ede-a0f2-579f7db67bb6",
        "relationship--b8617e55-00c0-4066-8222-927846edcafe",
        "relationship--f34d9e2e-715f-4baf-8226-40abfcb91012",
        "relationship--937f310a-396a-403f-bb6f-400ad8920018",
        "relationship--14a06709-3c0b-4e72-ad49-dd0f6d775e65",
        "relationship--5f6c6509-ca0c-43db-8c0e-8e138f6d913c",
        "relationship--ca99fa83-0d1b-4ddd-88c8-0dee38856a88",
        "relationship--38a52125-130f-4ce7-9b38-f234553ba83d",
        "relationship--e13b17d0-1fef-4f98-a4a8-895c3e4cf1e2",
        "relationship--262a8234-d7e2-477a-baeb-ed65b639e33a",
        "relationship--f4ceabc6-9302-4dc5-9cc1-4d40ef43503c",
        "relationship--56b1023c-9e28-4449-8b4f-bc2adde45e1a",
        "relationship--8997440e-00f5-48e1-8b56-69d3b6f9f1fd",
        "relationship--80ac0601-0660-4057-b3b0-dca0fe35a6b4",
        "relationship--2583921a-2f02-42c5-bd25-0f37eb2e6ef9",
        "relationship--7231e729-42e3-4f29-ae6f-6d80192c4bd1",
        "relationship--201ee2d5-74f4-4beb-b13a-34d948854655",
        "relationship--afee4dc4-7d0e-450d-9164-4429649ab386",
        "relationship--ed403d0d-b55d-4e78-94d3-4e035a045c39",
        "relationship--4303ebf2-9590-4ec0-a702-e7bfff64bc5f",
        "relationship--54f845bb-0967-4c0f-ac8a-8ad4785cbbe6",
        "relationship--0bd19ca0-2bbb-4df0-92ec-59a4e9169c64",
        "relationship--89ddeb74-ea26-44f9-bb6d-3f17c9d4efaa",
        "relationship--eb400750-c866-47c3-89a2-fa6d1a90e9e7",
        "relationship--7450856e-051f-4d49-953c-ad24f170af0e",
        "relationship--1d6b0425-603d-4217-948a-fabb2a398450",
        "relationship--1895dd86-dc46-4505-ba62-5724a1df2362",
        "relationship--a4e0751d-8d59-4447-96ea-3799fecf66d7",
        "relationship--258796f6-e46a-421a-b3f5-7db6114fb2bc",
        "relationship--9431d9f9-6d8b-4373-b42c-172a663391b3",
        "relationship--07d2f213-1794-483e-b95b-03761826c052",
        "relationship--aa430e5b-0519-4e94-bc2c-8836d196acd7",
        "relationship--c0786bd4-9c15-48ee-a19e-a9d6aba25d67",
        "relationship--498b9f3b-488b-40d5-aaaf-e67b93c1d92b",
        "relationship--d875538e-cc47-4353-a572-2dae27ef0a44",
        "relationship--313d56c4-eef9-417e-952d-073690c20ee4",
        "relationship--6b091c0f-a700-4f3e-9d98-0b8abf9a306b",
        "relationship--5aff864a-1789-4df2-87fa-03ec43cf4fdd",
        "relationship--325ebcb6-723c-4f50-8a32-aca18809e6eb",
        "relationship--0cb9c725-3d55-4165-b2a9-9414d7933987",
        "relationship--640a0454-57eb-408f-aa13-b5732b4d0b6f",
        "relationship--41550302-6e95-4cf6-8d7c-d417a99d98dc",
        "relationship--911dcbb0-96f4-4995-9961-5ea4b2fa7ce2",
        "relationship--7b6ba584-fa87-4a6f-8c21-8123fa88db74",
        "relationship--69101c2f-da92-47af-b402-7c60a39a982f",
        "relationship--25055108-a2ae-4855-bd5f-6ab396aacbc5",
        "relationship--44c80cab-73ce-4b17-a4cb-9a36e2585403",
        "relationship--32655cb3-7455-4761-b1f2-0b82153a0540",
        "relationship--fe963c8c-65a4-49ea-910b-e1cf3c80f1b4",
        "relationship--4b0abf75-6f05-4bd5-8ac5-19778b245274",
        "relationship--154049a5-731d-4e50-af13-f0f2c9b71f91",
        "relationship--db55db06-499d-4867-9ab9-3ed4331eedb2",
        "relationship--cc802697-7677-4bd7-a8b9-e728788ac783",
        "relationship--a371be18-8ca5-4453-80f5-ae52d982c21b",
        "relationship--9a3bd620-01b5-4764-beb0-f085417ed8f3",
        "relationship--48906405-9980-4583-8559-2085c111bf89",
        "relationship--13222c71-d8fa-4688-adae-c3f8ca43a41b",
        "relationship--73c4529e-560e-4831-8497-a0db72f7dfd8",
        "relationship--8d3e1ed6-7d9c-4aa5-b121-f4eb193312cf",
        "relationship--2c11dcc0-7968-4c07-bdde-791a8f5e2e37",
        "relationship--fd97d0ef-370e-4b6f-b2d3-8fb881aadc3f",
        "relationship--c05d2410-848c-47e5-a94f-c64510e2b08d",
        "relationship--92a21b52-2961-42aa-8b01-54ea294d9d73",
        "relationship--76a9283a-b844-47a5-a5d0-b31859115f88",
        "relationship--bbd3ba5c-2a75-4902-bd42-1215a2bc320e",
        "relationship--4f784f2f-7d8e-4f12-9ddd-b685055f8076",
        "relationship--263e38f4-8ecb-414f-b3c4-0f045d1be5ed",
        "relationship--a56e8582-fc6e-4be8-bf35-7e939269d65e",
        "relationship--d7d9952c-4443-4711-a48c-7009a0f0f8ea",
        "relationship--78f110e6-2cd6-442e-971f-a2ff40c3b843",
        "relationship--b2fb88f2-5ad7-4c07-b4b2-61986decb477"
      ]
    }
input = {
    "stix_object": report_dict
}
def get_embedded_links(stix_object):
    stix_type = stix_object["type"].split('--')[0]
    stix_list = []
    if stix_type == "report":
        if stix_object.get("created_by_ref", False):
            stix_list.append(stix_object.get("created_by_ref", False))
        if stix_object.get("object_refs", False):
            report_list = stix_object.get("object_refs", False)
            stix_list = stix_list + report_list

        return stix_list


def main(input, outputfile, logger: Logger):
    stix_dict = input["stix_object"]
    # setup logger for execution
    stix_list = get_embedded_links(stix_dict)
    result = {}
    result["stix_id_list"] = stix_list
    with open(outputfile, "w") as outfile:
        json.dump(result, outfile)


# if this file is run directly, then start here
if __name__ == '__main__':
    main(input, "output2.json", logger)
