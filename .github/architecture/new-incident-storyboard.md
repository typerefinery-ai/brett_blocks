# New Incident Storyboard

## Purpose
This storyboard provides detailed instructions for creating new incident types beyond the phishing example. It demonstrates how the same STIX graph patterns apply to different incident scenarios.

**Target Audience**: Developers creating notebooks for new incident types (malware, ransomware, data breach, insider threat, DDoS, etc.).

## The Reusability Principle

The patterns from the phishing incident (Step_2/3) are reusable templates:
- **Pattern 3.1**: Every incident needs a container
- **Pattern 3.3**: Every incident has evidence (sightings)
- **Pattern 3.4**: Every incident has events
- **Pattern 3.5**: Every incident has tasks
- **Pattern 3.6**: Every incident has impacts
- **Pattern 3.7**: Every incident has workflows

**What changes**: The specific SCOs, indicator patterns, task details, and story narrative. The graph structure remains consistent.

## Incident Type Template

For any new incident type, follow this structure:

### Phase 1: Identity Requirements (reuse Step_0/1)
- Victim identities (users, systems, organizations)
- Attacker identities (if known)
- Witness identities (who reported it)

### Phase 2: Evidence Collection
- What observables exist? (files, network traffic, log entries)
- What SCOs represent them? (file, network-traffic, process, etc.)
- How was it detected? (Which sighting extension?)

### Phase 3: Analysis
- What indicators exist? (STIX patterns)
- What's the attack flow? (Events timeline)
- What's affected? (Impact assessment)

### Phase 4: Response
- What investigation steps? (Tasks with dependencies)
- What workflows? (Sequences)
- What containment actions? (Tasks)

### Phase 5: Incident Container
- Create incident with IncidentCoreExt
- Link all evidence, events, impacts, tasks, sequences

## Example Incidents

This storyboard provides templates for four common incident types. Each demonstrates pattern reusability while showing type-specific adaptations.

## Incident Overview



**Incident Type**: Ransomware attack with data encryption## Story Overview: Ransomware Attack on Healthcare Provider

**Attack Vector**: Malicious email attachment (different from phishing link)

**Impact**: File encryption, availability loss, ransom demand### Scenario Selection Rationale

**Evidence**: Alert, system logs, encrypted files, ransom note

**Why Ransomware:**

**Comparison to Phishing Incident**:- Different attack vector (exploitation vs social engineering)

- **Different**: Attack type, observables, impacts, indicators- Different primary impacts (availability + integrity vs confidentiality)

- **Same**: Graph patterns, dependency hierarchy, evidence structure- Different urgency (immediate operational disruption)

- Different stakeholders (patient safety concerns)

---- Demonstrates different STIX object combinations



## Incident Creation Following Dependency Hierarchy**Alternative scenarios this template supports:**

- Malware infections (banking trojans, RATs, etc.)

### Phase 0: Prerequisites (from Step_0 & Step_1)- Data breaches (insider threat, misconfiguration)

- DDoS attacks (availability focus)

**Existing Objects** (created in earlier notebooks):- Supply chain compromises (trusted relationship exploitation)

- Personal identity (security analyst)- Insider threats (privileged access abuse)

- Company identity

- Employee identities---

- IT system identities (file server, workstation, Active Directory)

## Narrative: When the Hospital's Systems Encrypt

**Pattern**: 5.2 (Identity Sub-Pattern) - already completed

**Setting:**  

---MedCare Regional Hospital - a 400-bed healthcare facility with electronic health records (EHR), medical imaging systems, and connected medical devices. Created in Step 1 as company identity with IT system identities.



### Phase 1: Foundation Objects (Level 0-2)**Characters:**

- Dr. Sarah Chen (radiologist) - first to notice encrypted files

#### Objects Created- Marcus Thompson (IT administrator) - discovers ransom note

- Jennifer Walsh (IR team lead) - your identity, incident commander

**1. Victim User Account (Level 0)**- David Kim (forensics analyst) - investigates patient zero

- Object: `user-account` SCO- Chief Information Security Officer (executive sponsor)

- Fields:

  - user_id: "jdoe"**Inciting Incident:**  

  - account_login: "jdoe@company.com"3:47 AM - Automated backup job fails. By 7:15 AM, radiologists cannot access medical images. By 8:00 AM, ransom note discovered on file servers.

  - display_name: "John Doe"

- Purpose: Victim account that opened malicious attachment---



**2. Victim Email Address (Level 1)**## Act 1: Initial Detection and Triage

- Object: `email-addr` SCO

- Fields:### Scene 1: The First Signs (Pattern 6.2 - Evidence Collection)

  - value: "jdoe@company.com"

  - belongs_to_ref → user-account (jdoe)**Story:**  

- Purpose: Email where ransomware attachment receivedDr. Chen arrives for her shift and cannot open any DICOM medical images. Everything shows "encrypted" extensions. She calls IT helpdesk. While troubleshooting, Marcus the IT admin discovers a ransom note on the file server: "All your files have been encrypted by LockBit 3.0. Pay 50 Bitcoin..."



**3. Attacker Email Address (Level 1)****Graph Pattern Used:** Pattern 6.2 - Evidence Collection (sighting-alert)

- Object: `email-addr` SCO

- Fields:**Objects to Create:**

  - value: "payroll@company-fake.com"

  - display_name: "Payroll Department" (spoofed)**1. SCOs - The Evidence Artifacts:**

- Purpose: Attacker's email address

```yaml

**4. Malicious Attachment File (Level 1)**file SCO - Ransom Note:

- Object: `file` SCO  type: "file"

- Fields:  name: "README_FOR_DECRYPT.txt"

  - name: "Invoice_2024_Q1.pdf.exe"  size: 1247

  - size: 4234567 (bytes)  hashes:

  - hashes:    SHA-256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    - MD5: "d41d8cd98f00b204e9800998ecf8427e"  parent_directory_ref: file-server-directory

    - SHA-256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  

- Purpose: Ransomware payload filefile SCO - Encrypted Medical Image:

  type: "file"

**5. Encrypted Files (Level 1)**  name: "patient_12345_xray.dcm.locked"

- Objects: Multiple `file` SCOs  size: 5248576

- Fields:  hashes:

  - name: "document.docx.locked", "spreadsheet.xlsx.locked"    SHA-256: "..."

  - hashes: Post-encryption hashes  extensions:

- Purpose: Victim files encrypted by ransomware    archive-ext:

      contains_refs: [original-file]

**6. Ransom Note File (Level 1)**  

- Object: `file` SCOdirectory SCO - Affected File Server:

- Fields:  type: "directory"

  - name: "README_DECRYPT.txt"  path: "\\\\medcare-fs01\\radiology\\imaging"

  - content_ref → artifact (ransom note content)  contains_refs: [ransom-note-file, encrypted-files]

- Purpose: Attacker's ransom demand

windows-registry-key SCO - Persistence Mechanism:

**Pattern**: Foundation objects (Level 0-1), no dependencies beyond each other  type: "windows-registry-key"

  key: "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"

---  values:

    - name: "SystemUpdate"

### Phase 2: Ransomware Email Evidence (Level 3-4, Pattern 5.3)      data: "C:\\Windows\\Temp\\svchost.exe"

      data_type: "REG_SZ"

#### Story: "Malicious Email with Ransomware Attachment"

process SCO - Ransomware Process:

**7. Email Message Observable (Level 3)**  type: "process"

- Object: `email-message` SCO  pid: 4728

- Fields:  name: "svchost.exe"

  - subject: "Urgent: Q1 Invoice Requires Immediate Attention"  command_line: "C:\\Windows\\Temp\\svchost.exe --encrypt --fast"

  - from_ref → email-addr (attacker)  created: "2024-01-15T03:47:23.000Z"

  - to_refs → [email-addr (victim)]  binary_ref: malicious-binary-file

  - date: Attack timestamp  parent_ref: explorer-process

  - body: "Please review attached invoice..."  

  - body_multipart:network-traffic SCO - C2 Communication:

    - EmailMIMEComponent:  type: "network-traffic"

      - content_type: "application/octet-stream"  protocols: ["tcp", "https"]

      - body_raw_ref → file (malicious attachment)  src_ref: infected-workstation-ipv4

- Purpose: Delivery mechanism for ransomware  dst_ref: c2-server-ipv4

  dst_port: 443

**8. Observed-Data for Email (Level 3)**  extensions:

- Object: `observed-data` SDO    http-request-ext:

- Fields:      request_method: "POST"

  - first_observed: Email receipt timestamp      request_value: "/api/keys/submit"

  - number_observed: 1      

  - object_refs → [email-message, email-addr (attacker), email-addr (victim), file (attachment)]ipv4-addr SCO - C2 Server:

- Purpose: Container for email observables  type: "ipv4-addr"

  value: "185.220.101.42"

**9. Email Alert Sighting (Level 4)**  resolves_to_refs: [c2-server-domain]

- Object: `sighting` SRO  

- Fields:domain-name SCO - C2 Domain:

  - sighting_of_ref → indicator (ransomware email campaign)  type: "domain-name"

  - observed_data_refs → [observed-data (email)]  value: "update-security-service.com"

  - where_sighted_refs → [identity (email gateway), identity (victim workstation)]```

  - created_by_ref → identity (security analyst)

- Extension: **sighting-alert** (`SightingAlert` class)**2. Observed Data - Grouping Evidence:**

  - name: "Email Gateway Alert - Suspicious Attachment"

  - source: "Proofpoint Email Security"```yaml

  - product: "Proofpoint TAP"observed-data SDO - Ransomware Artifacts:

  - system_id: "ALERT-RANSOMWARE-2024-001"  first_observed: "2024-01-15T03:47:23.000Z"

  - log: "Attachment matched malware signature"  last_observed: "2024-01-15T08:00:00.000Z"

- Purpose: Initial detection of ransomware email  number_observed: 1

- Confidence: Medium (email gateway detection)  object_refs:

    - ransom-note-file

**Pattern 5.3 Application**:    - encrypted-files (multiple)

```    - malicious-process

SCOs (email-message, email-addrs, file)    - registry-key

    ↓ object_refs    - network-traffic

observed-data (email)    - c2-ipv4

    ↓ observed_data_refs    - c2-domain

sighting (sighting-alert)  created_by_ref: jennifer-walsh-identity

    ├── sighting_of_ref → indicator (ransomware)```

    └── where_sighted_refs → [identity (email gateway)]

```**3. Indicator - Ransomware Pattern:**



---```yaml

indicator SDO - LockBit 3.0 Pattern:

### Phase 3: Endpoint Detection Evidence (Level 3-4, Pattern 5.3)  name: "LockBit 3.0 Ransomware Indicators"

  indicator_types: ["malicious-activity", "file-hash-watchlist"]

#### Story: "Endpoint Security Detects Malicious Process Execution"  pattern: "[file:hashes.'SHA-256' = 'e3b0c44...' OR process:name = 'svchost.exe' AND process:command_line CONTAINS '--encrypt']"

  pattern_type: "stix"

**10. Malicious Process (Level 1)**  valid_from: "2024-01-15T08:00:00.000Z"

- Object: `process` SCO  kill_chain_phases:

- Fields:    - kill_chain_name: "lockheed-martin-cyber-kill-chain"

  - pid: 1234      phase_name: "actions-on-objectives"

  - name: "Invoice_2024_Q1.pdf.exe"  created_by_ref: jennifer-walsh-identity

  - command_line: "Invoice_2024_Q1.pdf.exe --encrypt --key abc123"```

  - created_time: Execution timestamp

  - opened_connection_refs → [network-traffic (C2 communication)]**4. Sighting with Alert Extension:**



**11. Network Traffic to C2 (Level 1)**```yaml

- Object: `network-traffic` SCOsighting SRO - EDR Alert:

- Fields:  sighting_of_ref: lockbit-indicator

  - src_ref → ipv4-addr (victim workstation)  observed_data_refs: [ransomware-artifacts-observed-data]

  - dst_ref → ipv4-addr (C2 server: 198.51.100.42)  where_sighted_refs:

  - dst_port: 443    - medcare-hospital-identity

  - protocols: ["tcp", "https"]    - radiology-workstation-identity

- Purpose: Command and control communication  first_seen: "2024-01-15T03:47:23.000Z"

  last_seen: "2024-01-15T08:00:00.000Z"

**12. C2 Server IP (Level 0)**  count: 47  # number of encrypted workstations

- Object: `ipv4-addr` SCO  extensions:

- Fields:    extension-definition--sighting-alert:

  - value: "198.51.100.42"      name: "Ransomware Encryption Activity Detected"

      product: "CrowdStrike Falcon EDR"

**13. Observed-Data for Endpoint Detection (Level 3)**      severity: "critical"

- Object: `observed-data` SDO      source: "EDR Behavioral Analysis"

- Fields:      description: "Mass file encryption detected on 47 workstations"

  - object_refs → [process, network-traffic, ipv4-addr, file (malicious attachment)]      log: "crowdstrike-event-12847.json"

- Purpose: Container for endpoint observables  created_by_ref: jennifer-walsh-identity

```

**14. Endpoint Alert Sighting (Level 4)**

- Object: `sighting` SRO**Objects Created:** ~15-25 objects (SCOs, observed-data, indicator, sighting)

- Fields:

  - sighting_of_ref → malware (ransomware family)**Story Checkpoint:**  

  - observed_data_refs → [observed-data (endpoint)]You now have documented the initial ransomware evidence as discovered by the EDR system and IT staff.

  - where_sighted_refs → [identity (victim workstation), identity (EDR platform)]

  - created_by_ref → identity (security analyst)---

- Extension: **sighting-alert** (`SightingAlert` class)

  - name: "EDR Alert - Ransomware Execution Detected"### Scene 2: Human Witness - IT Admin Reports (Pattern 6.2 - sighting-anecdote)

  - source: "CrowdStrike Falcon"

  - product: "Falcon Endpoint Protection"**Story:**  

  - system_id: "ALERT-EDR-RANSOMWARE-2024-001"Marcus the IT admin provides his account: "I was checking the backup logs when I saw the ransom note pop up on my screen. I immediately disconnected the file server from the network, but the encryption had already spread to the radiology department shares."

  - log: "Malicious process execution with file encryption behavior"

- Purpose: Endpoint detection of ransomware execution**Objects to Create:**

- Confidence: High (behavioral detection)

```yaml

**Pattern 5.3 Application**:anecdote SCO:

```  value: "Discovered ransom note on file server at approximately 8:00 AM. Immediately disconnected server from network. Observed encrypted file extensions .locked on approximately 50% of radiology imaging files."

SCOs (process, network-traffic, ipv4-addr, file)  provided_by_ref: marcus-thompson-identity

    ↓ object_refs  report_date: "2024-01-15T08:15:00.000Z"

observed-data (endpoint)  

    ↓ observed_data_refssighting SRO - IT Admin Report:

sighting (sighting-alert)  sighting_of_ref: ransomware-event (created next)

    ├── sighting_of_ref → malware (ransomware)  observed_data_refs: [observed-data-with-anecdote]

    └── where_sighted_refs → [identity (workstation), identity (EDR)]  where_sighted_refs: [file-server-identity]

```  extensions:

    extension-definition--sighting-anecdote:

---      person_name: "Marcus Thompson"

      person_context: "IT Administrator, 8 years tenure"

### Phase 4: File Encryption Evidence (Level 3-4, Pattern 5.3)      report_submission: "in-person to IR team"

  created_by_ref: jennifer-walsh-identity

#### Story: "Files Encrypted with Ransom Note Left Behind"```



**15. Observed-Data for Encryption (Level 3)****Objects Created:** ~3-5 objects

- Object: `observed-data` SDO

- Fields:---

  - object_refs → [file (encrypted-1), file (encrypted-2), ..., file (ransom note)]

- Purpose: Container for encrypted file observables## Act 2: Investigation and Containment



**16. Context Sighting - File System Scan (Level 4)**### Scene 3: Creating the Initial Event (Pattern 6.3)

- Object: `sighting` SRO

- Fields:**Story:**  

  - sighting_of_ref → malware (ransomware)With evidence documented, you declare this a formal security event requiring immediate response.

  - observed_data_refs → [observed-data (encryption)]

  - where_sighted_refs → [identity (file server)]**Objects to Create:**

  - created_by_ref → identity (security analyst)

- Extension: **sighting-context** (`SightingContext` class)```yaml

  - name: "File Server Scan - Encryption Verification"event SDO - Ransomware Encryption Event:

  - description: "Automated scan of file server to identify encrypted files"  name: "LockBit 3.0 Ransomware Encryption"

  - value: "2,847 files encrypted with .locked extension"  event_types: ["malware", "ransomware", "data-encrypted"]

- Purpose: Document scope of encryption  status: "occurred"

- Confidence: 100% (direct file system query)  start_time: "2024-01-15T03:47:23.000Z"  # when encryption began

  end_time: "2024-01-15T08:05:00.000Z"     # when network disconnected

**Pattern 5.3 Application**:  sighting_refs:

```    - edr-alert-sighting

SCOs (encrypted files, ransom note)    - it-admin-anecdote-sighting

    ↓ object_refs  changed_objects:

observed-data (encryption)    - StateChangeObject:

    ↓ observed_data_refs        object_ref: radiology-file-share-identity

sighting (sighting-context)        property: "availability"

    ├── sighting_of_ref → malware (ransomware)        old_value: "operational"

    └── where_sighted_refs → [identity (file server)]        new_value: "encrypted"

```        changed_time: "2024-01-15T03:47:23.000Z"

    - StateChangeObject:

---        object_ref: ehr-system-identity

        property: "availability"

### Phase 5: Threat Intelligence Evidence (Level 3-4, Pattern 5.3)        old_value: "operational"

        new_value: "degraded"

#### Story: "Ransomware Identified as Known Strain"        changed_time: "2024-01-15T06:30:00.000Z"

  created_by_ref: jennifer-walsh-identity

**17. Malware Object (Level 3)**```

- Object: `malware` SDO

- Fields:**Objects Created:** ~1-3 objects

  - name: "Conti Ransomware"

  - malware_types: ["ransomware"]---

  - is_family: True

  - kill_chain_phases: [{"kill_chain_name": "lockheed-martin-cyber-kill-chain", "phase_name": "actions-on-objectives"}]### Scene 4: Immediate Response Tasks (Pattern 6.4)



**18. Observed-Data for Malware Analysis (Level 3)****Story:**  

- Object: `observed-data` SDOIR team lead (you) creates urgent response tasks for the team.

- Fields:

  - object_refs → [file (malicious attachment), file (ransom note)]**Objects to Create:**



**19. Enrichment Sighting - VirusTotal (Level 4)**```yaml

- Object: `sighting` SROtask SDO - Network Isolation:

- Extension: **sighting-enrichment** (`SightingEnrichment` class)  name: "Isolate infected systems from network"

  - name: "VirusTotal - Malware Hash Lookup"  task_types: ["contain"]

  - url: "https://virustotal.com"  priority: 100  # highest priority

  - paid: False  status: "completed"

  - value: "File hash matches Conti ransomware family (52/70 detections)"  owner: marcus-thompson-identity

- Confidence: High (52/70 AV engines)  start_time: "2024-01-15T08:05:00.000Z"

  end_time: "2024-01-15T08:20:00.000Z"

**20. External Sighting - MISP (Level 4)**  outcome: "47 workstations isolated, file server disconnected, network segmentation activated"

- Object: `sighting` SRO  impacted_entity_refs: [hospital-network-identity]

- Extension: **sighting-external** (`SightingExternal` class)  created_by_ref: jennifer-walsh-identity

  - source: "MISP - Financial Sector Sharing"

  - payload: "Conti ransomware campaign targeting financial institutions"task SDO - Forensic Preservation:

  - pattern: "file.hashes.SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'"  name: "Preserve forensic evidence from patient zero"

  - pattern_type: "stix"  task_types: ["investigate", "forensics"]

  priority: 95

**21. Framework Sighting - ATT&CK (Level 4)**  status: "in-progress"

- Object: `sighting` SRO  owner: david-kim-identity

- Extension: **sighting-framework** (`SightingFramework` class)  start_time: "2024-01-15T08:30:00.000Z"

  - framework: "MITRE ATT&CK"  impacted_entity_refs: [dr-chen-workstation-identity]

  - version: "v14.1"  created_by_ref: jennifer-walsh-identity

  - comparison: "T1486 - Data Encrypted for Impact"

  - comparison_approach: "Automated mapping from EDR telemetry"task SDO - Backup Verification:

  name: "Verify backup integrity and recovery capability"

**Pattern 5.3 Application** (3 sightings, same pattern):  task_types: ["recover", "assess"]

```  priority: 90

malware (Conti ransomware)  status: "in-progress"

    ↑ sighting_of_ref  owner: marcus-thompson-identity

sighting-enrichment (VirusTotal)  created_by_ref: jennifer-walsh-identity

sighting-external (MISP)

sighting-framework (ATT&CK T1486)task SDO - Clinical Impact Assessment:

    ↓ observed_data_refs  name: "Assess impact on patient care operations"

observed-data (malware analysis)  task_types: ["assess", "safety"]

```  priority: 98

  status: "completed"

---  owner: ciso-identity

  outcome: "Non-emergency procedures delayed. Emergency department unaffected. Alternative imaging procedures activated."

### Phase 6: Event Creation (Level 4, Pattern 5.4)  created_by_ref: jennifer-walsh-identity



#### Story: "Deriving Events from Evidence"task SDO - Legal Notification Review:

  name: "Assess HIPAA breach notification requirements"

**22. Email Delivery Event (Level 4)**  task_types: ["legal", "compliance"]

- Object: `event` SDO  priority: 85

- Fields:  status: "in-progress"

  - name: "Ransomware Email Delivered to User"  owner: legal-counsel-identity

  - description: "Malicious email with ransomware attachment delivered to user inbox"  created_by_ref: jennifer-walsh-identity

  - sighting_refs → [sighting (email alert)]```

  - created_by_ref → identity (security analyst)

- Extension: Event New SDO**Objects Created:** ~5-7 tasks



**23. File Execution Event (Level 4)**---

- Object: `event` SDO

- Fields:## Act 3: Timeline Reconstruction

  - name: "User Opened Malicious Attachment"

  - description: "User executed ransomware payload from email attachment"### Scene 5: The Attack Kill Chain (Pattern 6.3 + 6.5)

  - sighting_refs → [sighting (endpoint alert)]

- Sub-object: StateChangeObject**Story:**  

  - initial_ref → file (attachment, unexecuted)Forensics analyst David reconstructs how the attack unfolded by analyzing logs and memory dumps.

  - result_ref → process (ransomware running)

**Events to Create (in chronological order):**

**24. Encryption Event (Level 4)**

- Object: `event` SDO```yaml

- Fields:event SDO - Initial Compromise:

  - name: "Ransomware Encrypted Files"  name: "Exploitation of Unpatched VPN Appliance"

  - description: "Conti ransomware encrypted 2,847 files on file server"  event_types: ["exploitation", "initial-access"]

  - sighting_refs → [sighting (context - file scan), sighting (endpoint alert)]  status: "occurred"

- Sub-object: StateChangeObject  start_time: "2024-01-12T22:15:00.000Z"  # 3 days before encryption

  - initial_ref → file (original document)  sighting_refs: [vpn-log-sighting]

  - result_ref → file (encrypted document)  changed_objects:

    - StateChangeObject:

**25. Event Relationships (SROs)**        object_ref: vpn-appliance-identity

- event (email delivery) → led-to → event (file execution)        property: "security-state"

- event (file execution) → led-to → event (encryption)        old_value: "secure"

- malware (Conti) → performed → event (encryption)        new_value: "compromised"

  created_by_ref: jennifer-walsh-identity

**Pattern 5.4 Application**:

```event SDO - Lateral Movement:

sighting-alert (email) → event (email delivery)  name: "Credential Dumping and Lateral Movement"

    ↓ led-to  event_types: ["credential-access", "lateral-movement"]

sighting-alert (endpoint) → event (file execution)  status: "occurred"

    ↓ led-to  start_time: "2024-01-12T23:30:00.000Z"

sighting-context (file scan) → event (encryption)  end_time: "2024-01-13T02:00:00.000Z"

```  sighting_refs: [mimikatz-detection-sighting]

  changed_objects:

**Event Chain**: Email delivery → File execution → File encryption (causal chain via led-to relationships)    - StateChangeObject:

        object_ref: domain-admin-credentials

---        property: "security-state"

        old_value: "protected"

### Phase 7: Impact Assessment (Level 4, Pattern 5.6)        new_value: "compromised"

  created_by_ref: jennifer-walsh-identity

#### Story: "Quantifying Ransomware Impact"

event SDO - Persistence Establishment:

**26. Availability Impact (Level 4)**  name: "Registry Modification for Persistence"

- Object: `impact` SDO  event_types: ["persistence", "registry-modification"]

- Fields:  status: "occurred"

  - name: "File Server Unavailability - Data Encrypted"  start_time: "2024-01-13T03:15:00.000Z"

  - description: "2,847 business-critical files encrypted and inaccessible"  sighting_refs: [registry-change-sighting]

  - impacted_refs → [identity (file server), file (encrypted-1), file (encrypted-2), ...]  created_by_ref: jennifer-walsh-identity

  - created_by_ref → identity (security analyst)

- Extension: **availability** (Availability impact type)event SDO - Defense Evasion:

  - Impact severity: Critical  name: "Antivirus and EDR Disabled"

  - Availability loss: 100% (files completely inaccessible)  event_types: ["defense-evasion"]

- Purpose: Document availability impact from encryption  status: "occurred"

  start_time: "2024-01-14T18:30:00.000Z"

**27. Confidentiality Impact (Level 4)**  sighting_refs: [av-disabled-sighting]

- Object: `impact` SDO  created_by_ref: jennifer-walsh-identity

- Fields:

  - name: "Potential Data Exfiltration"event SDO - Data Staging:

  - description: "C2 communication suggests possible data exfiltration before encryption"  name: "Sensitive Data Collection and Staging"

  - impacted_refs → [identity (file server), network-traffic (C2)]  event_types: ["collection", "data-staged"]

- Extension: **confidentiality** (Confidentiality impact type)  status: "occurred"

  - Impact severity: High  start_time: "2024-01-15T01:00:00.000Z"

  - Data at risk: Customer records, financial documents  end_time: "2024-01-15T03:30:00.000Z"

- Purpose: Document potential confidentiality breach  sighting_refs: [large-file-movement-sighting]

  changed_objects:

**28. Monetary Impact (Level 4)**    - StateChangeObject:

- Object: `impact` SDO        object_ref: patient-records-database

- Fields:        property: "data-state"

  - name: "Ransom Demand and Business Disruption"        old_value: "at-rest"

  - description: "Attacker demands $500,000 ransom; business operations halted"        new_value: "copied-to-staging"

  - impacted_refs → [identity (company)]  created_by_ref: jennifer-walsh-identity

- Extension: **monetary** (Monetary impact type)

  - Ransom amount: $500,000 (Bitcoin)event SDO - Data Exfiltration:

  - Business loss: $50,000/day (operations halted)  name: "Patient Data Exfiltration to C2"

  - Recovery cost estimate: $100,000  event_types: ["exfiltration"]

- Purpose: Document financial impact  status: "occurred"

  start_time: "2024-01-15T03:30:00.000Z"

**29. Integrity Impact (Level 4)**  end_time: "2024-01-15T03:45:00.000Z"

- Object: `impact` SDO  sighting_refs: [network-exfil-sighting]

- Fields:  created_by_ref: jennifer-walsh-identity

  - name: "File Integrity Compromised"

  - description: "Original file contents modified by encryption"event SDO - Ransomware Deployment:

  - impacted_refs → [file (encrypted files)]  name: "LockBit 3.0 Ransomware Encryption"

- Extension: **integrity** (Integrity impact type)  # (Already created in Scene 3)

  - Integrity loss: 100% (files modified)

- Purpose: Document integrity impactrelationship SRO - Event Causality Chain:

  relationship_type: "led-to"

**Pattern 5.6 Application**:  source_ref: initial-compromise-event

```  target_ref: lateral-movement-event

impact (availability)  

    ├── impacted_refs → [identity (file server), files]  # Repeat for each event pair in timeline

    └── availability extension (critical severity)```



impact (confidentiality)**Sequence Object - Attack Timeline:**

    ├── impacted_refs → [identity (file server), network-traffic]

    └── confidentiality extension (high severity)```yaml

sequence SDO - Ransomware Kill Chain:

impact (monetary)  name: "LockBit 3.0 Attack Timeline"

    ├── impacted_refs → [identity (company)]  sequenced_object: "event"

    └── monetary extension (ransom + business loss)  sequence_type: "attack-chain"

  step_type: "serial"

impact (integrity)  step_refs:

    ├── impacted_refs → [files]    - initial-compromise-event

    └── integrity extension (100% loss)    - lateral-movement-event

```    - persistence-event

    - defense-evasion-event

**Multiple Impact Types**: Ransomware affects availability, confidentiality, monetary, and integrity (4 of 7 impact types)    - data-staging-event

    - data-exfiltration-event

---    - ransomware-encryption-event

  created_by_ref: jennifer-walsh-identity

### Phase 8: Investigation and Remediation Tasks (Level 4, Pattern 5.5)```



#### Story: "Response Actions and Workflow"**Objects Created:** ~7 events + 6 relationship SROs + 1 sequence = ~14 objects



**30. Isolate Infected System Task (Level 4)**---

- Object: `task` SDO

- Fields:## Act 4: Impact Assessment

  - name: "Network Isolation of Infected Workstation"

  - description: "Disconnect victim workstation from network to prevent lateral movement"### Scene 6: Understanding the Damage (Pattern 6.6)

  - owner → identity (IT administrator)

  - task_types: ["containment"]**Story:**  

  - priority: 1 (critical)The IR team assesses the full scope of impact across multiple dimensions.

  - outcome: "Completed - workstation isolated"

  - created_by_ref → identity (security analyst)**Impact Objects to Create:**

- Extension: Task New SDO

```yaml

**31. Malware Analysis Task (Level 4)**impact SDO - Availability Impact (Critical Systems):

- Object: `task` SDO  impact_category: "availability"

- Fields:  extensions:

  - name: "Analyze Ransomware Sample"    extension-definition--availability:

  - description: "Reverse engineer malicious attachment to identify ransomware family and capabilities"      availability_loss_type: "loss"

  - owner → identity (malware analyst)      duration: "temporary"

  - task_types: ["analysis"]  impacted_refs:

  - outcome: "Completed - identified as Conti ransomware"    - radiology-imaging-system-identity

    - ehr-system-identity

**32. File Recovery Task (Level 4)**    - file-server-identity

- Object: `task` SDO  start_time: "2024-01-15T03:47:23.000Z"

- Fields:  end_time: null  # ongoing

  - name: "Restore Files from Backup"  recoverability: "extended"  # will take 3-5 days to restore

  - description: "Restore encrypted files from last clean backup"  criticality: "high"

  - owner → identity (backup administrator)  created_by_ref: jennifer-walsh-identity

  - task_types: ["recovery"]

  - priority: 1 (critical)impact SDO - Integrity Impact (Data):

- Sub-object: StateChangeObject  impact_category: "integrity"

  - initial_ref → file (encrypted)  extensions:

  - result_ref → file (restored from backup)    extension-definition--integrity:

      alteration_type: "encryption"

**33. Password Reset Task (Level 4)**      integrity_loss_type: "confirmed-loss"

- Object: `task` SDO  impacted_refs:

- Fields:    - patient-records-database

  - name: "Force Password Reset for Compromised User"    - medical-imaging-files

  - description: "Reset credentials for user who executed ransomware"  start_time: "2024-01-15T03:47:23.000Z"

  - owner → identity (IT administrator)  recoverability: "supplemented"  # restore from backups

  - task_types: ["remediation"]  created_by_ref: jennifer-walsh-identity



**34. Hunt for Lateral Movement Task (Level 4)**impact SDO - Confidentiality Impact (Data Breach):

- Object: `task` SDO  impact_category: "confidentiality"

- Fields:  extensions:

  - name: "Hunt for Additional Infected Systems"    extension-definition--confidentiality:

  - description: "Search network for signs of ransomware lateral movement"      information_type: "patient-health-information"

  - owner → identity (security analyst)      loss_type: "suspected-loss"  # exfiltration detected but not confirmed

  - task_types: ["investigation"]  impacted_refs:

    - patient-identity-1

**35. Task Relationships (SROs)**    - patient-identity-2

- identity (IT admin) → performed → task (isolation)    # ... (all affected patients)

- identity (malware analyst) → performed → task (analysis)  start_time: "2024-01-15T03:30:00.000Z"

- task (isolation) → blocks → event (encryption) (prevents further spread)  recoverability: "not-recoverable"  # data cannot be un-stolen

- task (recovery) → followed-by → task (password reset)  created_by_ref: jennifer-walsh-identity

- task (analysis) → creates → indicator (ransomware signature)

impact SDO - Safety Impact (Patient Care):

**Pattern 5.5 Application**:  impact_category: "safety"

```  extensions:

task (isolation)    extension-definition--safety:

    ├── owner → identity (IT admin)      safety_impact_type: "delayed-care"

    └── blocks → event (encryption)      affected_population_size: 23  # delayed procedures

  impacted_refs:

task (analysis)    - medcare-hospital-identity

    ├── owner → identity (malware analyst)    - patient-identities (multiple)

    └── creates → indicator (ransomware signature)  start_time: "2024-01-15T08:00:00.000Z"

  recoverability: "regular"  # procedures can be rescheduled

task (recovery)  created_by_ref: jennifer-walsh-identity

    ├── StateChangeObject: encrypted → restored

    └── followed-by → task (password reset)impact SDO - Monetary Impact:

  impact_category: "monetary"

SRO relationships:  extensions:

- identity → performed → task    extension-definition--monetary:

- task → blocks/creates → event/indicator      currency: "USD"

- task → followed-by → task      variety:

```        - "ransom-demand"

        - "incident-response-costs"

---        - "downtime-costs"

        - "regulatory-fines"

### Phase 9: Workflow Sequences (Level 5, Pattern 5.7)      min_amount: 500000

      max_amount: 5000000

#### Story: "Orchestrating Incident Response Playbook"  impacted_refs: [medcare-hospital-identity]

  recoverability: "not-recoverable"

**36. Initial Response Sequence (Level 5)**  created_by_ref: jennifer-walsh-identity

- Object: `sequence` SDO

- Fields:impact SDO - Reputational Impact:

  - sequenced_object → task (isolation)  impact_category: "external"

  - sequence_type: "task"  extensions:

  - step_type: "start_step"    extension-definition--external:

  - on_completion → sequence (analysis)      reputation_loss_type: "brand-damage"

  - created_by_ref → identity (security analyst)      stakeholder_type:

- Extension: Sequence New SDO        - "patients"

- Purpose: Workflow entry point - immediate containment        - "insurance-companies"

        - "regulatory-bodies"

**37. Analysis Sequence (Level 5)**  impacted_refs: [medcare-hospital-identity]

- Object: `sequence` SDO  recoverability: "extended"  # long-term trust rebuilding

- Fields:  created_by_ref: jennifer-walsh-identity

  - sequenced_object → task (malware analysis)```

  - sequence_type: "task"

  - step_type: "intermediate_step"**Objects Created:** ~6-8 impact objects

  - on_completion → sequence (recovery decision)

---

**38. Recovery Decision Sequence (Level 5)**

- Object: `sequence` SDO## Act 5: Incident Assembly and Response Workflow

- Fields:

  - sequenced_object → task (recovery)### Scene 7: The Complete Incident (Pattern 6.7)

  - sequence_type: "task"

  - step_type: "intermediate_step"**Story:**  

  - on_success → sequence (password reset) (if recovery successful)You assemble all the evidence, events, tasks, and impacts into a formal incident case.

  - on_failure → sequence (escalation) (if recovery fails, consider ransom payment)

**Incident Object:**

**39. Password Reset Sequence (Level 5)**

- Object: `sequence` SDO```yaml

- Fields:incident SDO:

  - sequenced_object → task (password reset)  name: "LockBit 3.0 Ransomware Attack - MedCare Regional Hospital"

  - step_type: "intermediate_step"  description: "Ransomware attack via VPN exploitation, resulting in encryption of radiology systems, EHR degradation, suspected PHI exfiltration, and operational impact to patient care."

  - on_completion → sequence (hunt)  

  extensions:

**40. Hunt Sequence (Level 5)**    extension-definition--ef765651-680c-498d-9894-99799f2fa126:  # Incident Core

- Object: `sequence` SDO      determination: "confirmed-true-positive"

- Fields:      incident_types: ["ransomware", "data-breach", "extortion"]

  - sequenced_object → task (hunt for lateral movement)      investigation_status: "active-investigation"

  - step_type: "end_step"      

      # Core references

**Workflow Pattern**:      event_refs:

```        - initial-compromise-event

sequence(start: isolation)        - lateral-movement-event

    ↓ on_completion        - persistence-event

sequence(intermediate: analysis)        - defense-evasion-event

    ↓ on_completion        - data-staging-event

sequence(intermediate: recovery)        - data-exfiltration-event

    ├── on_success → sequence(password reset) → sequence(hunt: end)        - ransomware-encryption-event

    └── on_failure → sequence(escalation: ransom decision)      

```      task_refs:

        - network-isolation-task

**Pattern 5.7 Application**:        - forensic-preservation-task

- Linear workflow: isolation → analysis → recovery        - backup-verification-task

- Conditional branching: recovery success/failure paths        - clinical-impact-task

- Entry point: sequence (isolation) in incident.sequence_start_refs        - legal-notification-task

      

---      impact_refs:

        - availability-impact

### Phase 10: Incident Container (Level 6, Pattern 5.1)        - integrity-impact

        - confidentiality-impact

#### Story: "Complete Ransomware Incident Graph"        - safety-impact

        - monetary-impact

**41. Incident Object (Level 6)**        - reputational-impact

- Object: `incident` SDO      

- Fields:      other_object_refs:

  - name: "Ransomware Attack - Conti Family"        - all SCOs (files, processes, network-traffic, etc.)

  - description: "Ransomware delivered via email attachment, encrypting 2,847 files on file server"        - all observed-data objects

  - created_by_ref → identity (security analyst)        - all sightings (alert, anecdote, hunt, enrichment)

- Extension: **IncidentCore** (`extension-definition--ef765651-680c-498d-9894-99799f2fa126`)        - all indicators

  - **event_refs** → [event (email delivery), event (file execution), event (encryption)]        - all sequences

  - **task_refs** → [task (isolation), task (analysis), task (recovery), task (password reset), task (hunt)]        - all relationship SROs

  - **impact_refs** → [impact (availability), impact (confidentiality), impact (monetary), impact (integrity)]        - all identities (attackers, victims, responders)

  - **sequence_refs** → [sequence (isolation), sequence (analysis), sequence (recovery), sequence (password reset), sequence (hunt)]  

  - **sequence_start_refs** → [sequence (isolation)]  # Standard incident properties

  - **other_object_refs** → [  first_seen: "2024-01-15T03:47:23.000Z"

      // Observables  last_seen: "2024-01-15T08:00:00.000Z"

      email-message, email-addr (attacker), email-addr (victim),   

      file (attachment), file (encrypted files), file (ransom note),  confidence: 95

      process, network-traffic, ipv4-addr (C2),  

        impact_criticality: "high"

      // Evidence  

      observed-data (email), observed-data (endpoint), observed-data (encryption), observed-data (malware),  labels:

      sighting (email alert), sighting (endpoint alert), sighting (context),     - "ransomware"

      sighting (enrichment), sighting (external), sighting (framework),    - "lockbit-3.0"

          - "healthcare"

      // Threat characterization    - "patient-safety-impact"

      malware (Conti), indicator (ransomware signature),    - "HIPAA-breach"

          - "double-extortion"

      // Identities  

      identity (victim user), identity (email gateway), identity (workstation),   external_references:

      identity (file server), identity (EDR platform), identity (VirusTotal),     - source_name: "CISA Alert"

      identity (MISP), identity (IT admin), identity (malware analyst), ...      url: "https://www.cisa.gov/lockbit-ransomware"

    ]      description: "LockBit 3.0 Ransomware Affiliates Exploit CVE 2023-4966"

- Purpose: Container organizing entire ransomware incident investigation  

  created_by_ref: jennifer-walsh-identity

**Pattern 5.1 Application**:  created: "2024-01-15T08:30:00.000Z"

``````

incident (Level 6)

└── IncidentCore extension**Objects Created:** 1 incident (container for ~80-120 objects)

    ├── event_refs → [3 events: email delivery, execution, encryption]

    ├── task_refs → [5 tasks: isolation, analysis, recovery, password reset, hunt]---

    ├── impact_refs → [4 impacts: availability, confidentiality, monetary, integrity]

    ├── sequence_refs → [5 sequences: full workflow chain]### Scene 8: Coordinated Response Workflow (Pattern 6.5)

    ├── sequence_start_refs → [sequence (isolation): entry point]

    └── other_object_refs → [40+ objects: SCOs, sightings, identities, etc.]**Story:**  

```Multiple response teams coordinate through a structured workflow.



**Complete Incident Graph**: 40+ objects organized hierarchically via embedded references**Additional Tasks:**



---```yaml

task SDO - Malware Analysis:

## Incident Comparison: Ransomware vs. Phishing  name: "Reverse engineer ransomware binary"

  task_types: ["investigate", "malware-analysis"]

### Similarities (Pattern Reusability)  priority: 80

  status: "in-progress"

**Same Graph Patterns Used**:  owner: malware-analyst-identity

- ✅ Pattern 5.1: Incident Extension (Level 6 container)

- ✅ Pattern 5.2: Identity Sub-Pattern (Level 0-2 foundation)task SDO - Threat Intelligence Query:

- ✅ Pattern 5.3: Sighting/Evidence (multiple evidence types)  name: "Research LockBit 3.0 TTPs and decryption options"

- ✅ Pattern 5.4: Event Derivation (sightings → events)  task_types: ["investigate", "threat-intelligence"]

- ✅ Pattern 5.5: Task Integration (investigation/remediation)  priority: 85

- ✅ Pattern 5.6: Impact Assessment (multiple impact types)  status: "completed"

- ✅ Pattern 5.7: Sequence Workflow (task orchestration)  outcome: "No known decryptor. Group active since 2019. Double-extortion MO confirmed."



**Same Dependency Hierarchy**:task SDO - Backup Restoration:

- Level 0: Foundation SCOs (user-account, url, ipv4-addr)  name: "Restore radiology systems from backups"

- Level 1-3: Observables and containers (email-addr, file, observed-data)  task_types: ["recover"]

- Level 4: Evidence and effects (sighting, event, task, impact)  priority: 95

- Level 5: Workflows (sequence)  status: "in-progress"

- Level 6: Incident container  dependencies: [backup-verification-task]



**Same Template-Driven Approach**:task SDO - Patient Notification:

- Three-file pattern (data, class, python)  name: "Notify affected patients per HIPAA requirements"

- Category-based storage  task_types: ["communication", "compliance"]

- Auto-generated parameters  priority: 75

  status: "pending"

### Differences (Content, Not Structure)  dependencies: [legal-notification-task]



| Aspect | Phishing Incident | Ransomware Incident |task SDO - Law Enforcement Notification:

|--------|-------------------|---------------------|  name: "Report to FBI IC3"

| **Attack Vector** | Malicious URL in email | Malicious attachment in email |  task_types: ["legal", "reporting"]

| **Initial Observable** | url SCO | file SCO |  priority: 70

| **Key SCOs** | url, email-addr | file, process, network-traffic, ipv4-addr |  status: "completed"

| **Primary Sightings** | alert (email gateway), anecdote | alert (email + endpoint), context (file scan) |

| **Events** | credential compromise | email delivery, file execution, encryption |task SDO - Ransom Decision:

| **Impacts** | confidentiality, availability (2 types) | availability, confidentiality, monetary, integrity (4 types) |  name: "Executive decision on ransom payment"

| **Tasks** | password reset, log analysis | isolation, analysis, recovery, password reset, hunt |  task_types: ["decision"]

| **Workflow** | Simple linear (reset → analyze) | Complex branching (recovery success/failure paths) |  priority: 90

| **Threat Object** | indicator (phishing campaign) | malware (Conti ransomware) |  status: "completed"

  outcome: "Decision: Do not pay ransom. Proceed with backup restoration."

### Pattern Flexibility Demonstrated  owner: ciso-identity

```

**Same Pattern, Different Content**:

- Pattern 5.3 (Sighting): Works for email alerts, endpoint alerts, file scans, enrichment**Response Sequence:**

- Pattern 5.4 (Event): Works for credential compromise or file encryption

- Pattern 5.5 (Task): Works for password resets or malware analysis```yaml

- Pattern 5.6 (Impact): Works for confidentiality breaches or file encryptionsequence SDO - Ransomware Response Playbook:

- Pattern 5.7 (Sequence): Works for simple linear or complex branching workflows  name: "Healthcare Ransomware Response Workflow"

  sequenced_object: "task"

**Universal Applicability**: These 7 patterns can model ANY incident type:  sequence_type: "playbook"

- Phishing (demonstrated in Step_2/Step_3)  step_type: "parallel-then-serial"

- Ransomware (demonstrated here)  step_refs:

- Data breach    # Phase 1 - Immediate (parallel)

- Insider threat    - [network-isolation-task, clinical-impact-task, forensic-preservation-task, law-enforcement-task]

- Denial of service    # Phase 2 - Investigation (parallel)

- Malware infection    - [backup-verification-task, malware-analysis-task, threat-intel-task, legal-notification-task]

- Supply chain compromise    # Phase 3 - Decision Point (serial)

- Advanced persistent threat (APT)    - [ransom-decision-task]

    # Phase 4 - Recovery (serial after decision)

---    - [backup-restoration-task]

    # Phase 5 - Notification (parallel, after legal review)

## Context Memory Architecture    - [patient-notification-task]

```

### Incident-Specific Storage

**Objects Created:** ~6 additional tasks + 1 sequence = ~7 objects

**Directory**: `/incident--{ransomware-uuid}/`

---

**Files Created**:

```## Act 6: Extended Evidence Collection

incident--{uuid}/

├── incident.json                   # Incident object with IncidentCore extension### Scene 9: Threat Intelligence Enrichment (Pattern 6.2 - sighting-enrichment)

├── event_refs.json                 # 3 events (email delivery, execution, encryption)

├── task_refs.json                  # 5 tasks (isolation, analysis, recovery, reset, hunt)**Story:**  

├── impact_refs.json                # 4 impacts (availability, confidentiality, monetary, integrity)Threat intel team discovers this attack matches recent LockBit campaigns targeting healthcare.

├── sequence_refs.json              # 5 sequences (workflow chain)

├── observables.json                # SCOs (email-message, files, process, network-traffic, etc.)```yaml

├── indicators.json                 # Ransomware indicatorssighting SRO - Threat Intel Enrichment:

├── evidence.json                   # Sighting objects with extensions  sighting_of_ref: lockbit-indicator

└── other_object_refs.json          # All other objects (identities, malware, etc.)  extensions:

```    extension-definition--sighting-enrichment:

      name: "LockBit 3.0 Healthcare Campaign Attribution"

**Category-Based Routing** (automatic):      enrichment_type: "external-lookup"

- `event` objects → `event_refs.json`      source: "FBI Flash Alert, MISP Event 98234, HealthISAC"

- `task` objects → `task_refs.json`      confidence_score: 90

- `impact` objects → `impact_refs.json`  external_references:

- `sequence` objects → `sequence_refs.json`    - source_name: "FBI Flash Alert CU-000183-MW"

- `sighting` objects → `evidence.json`      url: "https://www.ic3.gov/Media/News/2024/..."

- SCOs → `observables.json`      description: "LockBit 3.0 targeting healthcare sector via CVE-2023-4966"

- Others → `other_object_refs.json````



### Cross-Context References---



**User Context** (`/usr/`):### Scene 10: MITRE ATT&CK Mapping (Pattern 6.2 - sighting-framework)

- Personal identity (security analyst) referenced via `created_by_ref`

**Story:**  

**Company Context** (`/identity--{company-uuid}/`):Map the attack to MITRE ATT&CK for healthcare framework.

- Victim user identity

- IT system identities (file server, workstation, email gateway, EDR)```yaml

- IT administrator identity (task owner)sighting SRO - ATT&CK Mapping (multiple):

- Malware analyst identity (task owner)  # T1190 - Exploit Public-Facing Application

  # T1078 - Valid Accounts

**Incident Context** (`/incident--{ransomware-uuid}/`):  # T1003 - OS Credential Dumping

- All incident-specific objects  # T1547 - Boot or Logon Autostart Execution

- References to user/company context objects  # T1562 - Impair Defenses

  # T1074 - Data Staged

**Global Routing** (`context_map.json`):  # T1041 - Exfiltration Over C2 Channel

- Maps ransomware incident UUID to context directory  # T1486 - Data Encrypted for Impact

  # T1657 - Financial Theft (ransom demand)

---  

  sighting_of_ref: event or indicator

## Evidence Chain for Ransomware  extensions:

    extension-definition--sighting-framework:

### Multi-Source Evidence (Pattern 5.3)      framework: "ATT&CK"

      version: "v14.1"

**Evidence Types Used**:      framework_id: "T1486"

1. ✅ sighting-alert (email gateway)      tactic: ["impact"]

2. ✅ sighting-alert (endpoint EDR)      technique: ["data-encrypted-for-impact"]

3. ✅ sighting-context (file system scan)```

4. ✅ sighting-enrichment (VirusTotal)

5. ✅ sighting-external (MISP)---

6. ✅ sighting-framework (ATT&CK T1486)

## Complete Object Inventory

**Evidence Not Used** (but could be):

7. ❌ sighting-anecdote (victim interview)### Final Count for Ransomware Incident:

8. ❌ sighting-exclusion (threat feed checks)

9. ❌ sighting-hunt (proactive hunting)**SCOs:** ~30-50 (files, processes, network-traffic, registry-keys, IP addresses, domains)  

**Observed-Data:** ~15-25 (grouping SCO observations)  

**Evidence Flow**:**Sightings:** ~10-15 (alert, anecdote, hunt, enrichment, framework)  

```**Indicators:** ~5-10 (file hashes, network IOCs, behavioral patterns)  

Email Alert (low confidence)**Events:** ~7-10 (attack kill chain)  

    +**Tasks:** ~12-15 (response workflow)  

Endpoint Alert (high confidence)**Impacts:** ~6-8 (all impact categories)  

    +**Sequences:** ~2-3 (attack timeline, response workflow)  

File System Scan (100% confidence)**Identities:** ~15-25 (hospital staff, IT systems, patients)  

    +**Relationships:** ~20-30 (led-to, mitigates, investigates, etc.)  

VirusTotal Enrichment (high confidence: 52/70 engines)**Attack Patterns:** ~8-12 (MITRE ATT&CK techniques)  

    +**Malware:** ~1-2 (LockBit 3.0 malware object)  

MISP External Intel (medium confidence: campaign known)**Tool:** ~2-4 (Mimikatz, custom scripts)  

    +**Incident:** 1 (container)  

ATT&CK Framework Mapping (medium confidence: T1486)

    ↓**Total Objects:** ~140-200 objects

Event: Ransomware Encryption Confirmed (high confidence)

    ↓---

Impact Assessment: Critical availability loss, potential confidentiality breach, significant monetary impact

```## Story Themes and Lessons



### Confidence Progression### Why This Scenario Matters



**Initial Alert** (email gateway):**1. Different Threat Model:**

- Confidence: Medium (suspicious attachment detected)- Phishing = social engineering, user error

- Action: Monitor, investigate- Ransomware = exploitation, technical vulnerability

- Demonstrates STIX flexibility across threat types

**Endpoint Alert** (EDR):

- Confidence: High (behavioral detection, process execution)**2. Healthcare-Specific Considerations:**

- Action: Immediate containment (network isolation)- Patient safety impact (unique to healthcare, critical infrastructure)

- HIPAA compliance (legal/regulatory dimension)

**File System Scan** (context):- Clinical operations (availability is life-safety issue)

- Confidence: 100% (direct verification of 2,847 encrypted files)- Double extortion (confidentiality + availability impacts)

- Action: Confirm ransomware impact

**3. Executive Decision Points:**

**Threat Intelligence** (enrichment + external):- Ransom payment decision (captured as task with outcome)

- Confidence: High (malware family identified: Conti)- Patient notification timing (legal vs operational considerations)

- Action: Apply known remediation strategies- Law enforcement coordination (reporting requirements)



**Final Assessment**:**4. Timeline Complexity:**

- Confidence: Very High (multi-source confirmation)- Multi-day dwell time (initial compromise → encryption)

- Impact: Critical (4 impact types: availability, confidentiality, monetary, integrity)- Multiple attack phases (reconnaissance, lateral movement, staging, impact)

- Response: Full incident response playbook activated- Sequential event chain with clear causality



---**5. Response Coordination:**

- Multiple teams (IR, IT, clinical, legal, comms, executive)

## Workflow Orchestration (Pattern 5.7)- Dependencies between tasks (can't restore until isolated)

- Parallel and serial workflow phases

### Incident Response Playbook Mapping

---

**Sequence Chain**:

```## Adapting This Template to Other Scenarios

START: sequence(isolation)

    ├── sequenced_object: task (network isolation)### Malware Infection (Banking Trojan)

    └── on_completion ↓

**Key Changes:**

sequence(analysis)- **Primary Impact:** Confidentiality (credentials stolen)

    ├── sequenced_object: task (malware analysis)- **Evidence:** Memory dumps, keylogger files, network C2 traffic

    └── on_completion ↓- **Events:** Initial infection → persistence → credential harvesting → exfiltration

- **Victims:** Financial institution customers

sequence(recovery)- **Legal:** PCI-DSS, state breach laws

    ├── sequenced_object: task (file recovery from backup)

    ├── on_success → sequence(password reset) → sequence(hunt) → END### Data Breach (Insider Threat)

    └── on_failure → sequence(escalation: ransom decision)

```**Key Changes:**

- **Threat Source:** Insider identity (employee/contractor)

**Conditional Branching**:- **Evidence:** sighting-anecdote (tip from coworker), sighting-context (motive/opportunity), access logs

- **If recovery succeeds**: Password reset → Hunt for lateral movement → END- **Events:** Unauthorized access → data download → departure from company

- **If recovery fails**: Escalate to management for ransom payment decision- **Impacts:** Confidentiality, reputational, competitive advantage loss

- **Response:** HR involvement, legal prosecution

**Playbook Representation**:

- NIST CSF phases: Identify → Protect → Detect → Respond → Recover### DDoS Attack

- Sequence objects map to Respond and Recover phases

- Tasks within sequences represent specific playbook actions**Key Changes:**

- **Primary Impact:** Availability only

**Pattern Advantage**: Sequence pattern enables complex playbook logic with conditional branching.- **Evidence:** Network-traffic SCOs (massive volume), server logs

- **Events:** Attack waves (different techniques: SYN flood, UDP amplification, application layer)

---- **Indicators:** Botnets, amplification servers

- **Response:** Traffic scrubbing, rate limiting, upstream filtering

## SRO Relationships in Ransomware Incident

### Supply Chain Compromise

### Relationship Network

**Key Changes:**

**Event Relationships**:- **Complexity:** Multiple victims (all customers of compromised vendor)

- event (email delivery) → led-to → event (file execution)- **Trust:** Relationship SRO between vendor identity and customer identities

- event (file execution) → led-to → event (encryption)- **Evidence:** Software updates (file SCOs with malicious code), code signing certificates

- event (encryption) → impacts → infrastructure (file server)- **Attribution:** Threat actor → campaign → multiple incidents

- event (encryption) → located-at → location (company office)- **Response:** Third-party risk assessment, vendor notification



**Task Relationships**:---

- task (isolation) → blocks → event (encryption) (prevents further spread)

- task (analysis) → creates → indicator (ransomware signature)## How to Use This Storyboard

- task (analysis) → detects → event (encryption)

- task (recovery) → followed-by → task (password reset)### For Creating New Scenarios:

- identity (IT admin) → performed → task (isolation)

- identity (malware analyst) → performed → task (analysis)1. **Choose Threat Type:** Ransomware, malware, DDoS, insider, supply chain, etc.

- identity (security analyst) → assigned → task (recovery)2. **Define Setting:** Organization type, industry, size, critical assets

3. **Identify Characters:** Victims, responders, executives, threat actors

**Malware Relationships**:4. **Map Kill Chain:** How attack unfolds (events)

- malware (Conti) → performed → event (encryption)5. **Document Evidence:** What you observe (SCOs, observed-data, sightings)

6. **Assess Impacts:** Business consequences (availability, confidentiality, integrity, safety, financial, reputation)

**Incident Relationships**:7. **Plan Response:** Tasks and workflow (containment, eradication, recovery, lessons learned)

- incident (ransomware) → impacts → identity (company)8. **Assemble Incident:** Bring all objects together in incident.other_object_refs

- incident (ransomware) → impacts → identity (file server)

- incident (ransomware) → located-at → location (company office)### For Notebook Development:



**Total Relationships**: 15+ SRO relationship objects connecting incident graph- Each "Scene" could be a separate notebook

- Scene 1: Detection Evidence (Step_4_Ransomware_Detection.ipynb)

**Pattern 5.5 (Task) Heavily Uses SROs**: Tasks primarily connected via SRO relationships, not embedded references.- Scene 3: Event Creation (Step_5_Ransomware_Timeline.ipynb)

- Scene 4: Response Tasks (Step_6_Ransomware_Response.ipynb)

---- Scene 6: Impact Assessment (Step_7_Ransomware_Impact.ipynb)

- Scene 7: Incident Assembly (Step_8_Ransomware_Incident.ipynb)

## Impact Assessment Deep Dive (Pattern 5.6)

### For System Integration:

### Multi-Type Impact

- Use sequence objects to drive SOAR automation

**1. Availability Impact (Critical)**:- Map to incident response playbooks

- **impacted_refs**: file server identity, 2,847 file SCOs- Integrate with ticketing systems (tasks)

- **Extension**: availability- Feed SIEMs with indicators

- **Severity**: Critical- Generate executive reports from impact objects

- **Description**: 100% availability loss for encrypted files

- **Business Effect**: Operations halted, employees cannot access critical documents

**2. Confidentiality Impact (High)**:
- **impacted_refs**: file server identity, network-traffic (C2 communication)
- **Extension**: confidentiality
- **Severity**: High
- **Description**: Potential data exfiltration before encryption (double extortion)
- **Business Effect**: Customer data and financial records at risk

**3. Monetary Impact (Severe)**:
- **impacted_refs**: company identity
- **Extension**: monetary
- **Severity**: Severe
- **Components**:
  - Ransom demand: $500,000 (Bitcoin)
  - Business disruption: $50,000/day
  - Recovery costs: $100,000 (estimated)
  - Total potential loss: $650,000+
- **Business Effect**: Significant financial burden

**4. Integrity Impact (High)**:
- **impacted_refs**: encrypted file SCOs
- **Extension**: integrity
- **Severity**: High
- **Description**: Original file contents modified by encryption algorithm
- **Business Effect**: Original file integrity compromised (mitigated by backups)

**Impact Evolution**:
- Initial: Availability impact only (files encrypted)
- Expanded: Confidentiality impact added (C2 communication suggests exfiltration)
- Final: Monetary impact quantified (ransom + business loss + recovery)

**Pattern 5.6 Flexibility**: Same impact pattern applied 4 times with different extensions.

---

## Conclusion: Pattern Reusability Across Incident Types

### Key Takeaways

**1. Universal Patterns**:
- Same 7 patterns (5.1-5.7) work for ransomware AND phishing
- Patterns are **content-agnostic**, **structure-focused**
- Dependency hierarchy (Level 0-6) applies to ALL incident types

**2. Adaptive Content**:
- Different SCOs (url vs. file vs. process)
- Different events (credential compromise vs. file encryption)
- Different impacts (2 types vs. 4 types)
- Different workflows (simple vs. complex branching)

**3. Template-Driven Flexibility**:
- Same templates (`*_template.json`)
- Different parameter values
- Automatic routing by STIX type

**4. Evidence Diversity**:
- Ransomware uses 6 of 8 evidence types
- Phishing (extended) uses all 8 evidence types
- Pattern 5.3 supports ANY evidence source

**5. Complete Modeling**:
- Both incidents fully modeled using same patterns
- Complete incident graphs (40+ objects each)
- Full traversal via embedded references

### Pattern Coverage Across Both Incidents

| Pattern | Phishing | Ransomware | Notes |
|---------|----------|------------|-------|
| 5.1 Incident Extension | ✅ | ✅ | Both use IncidentCore |
| 5.2 Identity | ✅ | ✅ | Both use user/company identities |
| 5.3 Sighting/Evidence | ✅ | ✅ | Different evidence types |
| 5.4 Event Derivation | ✅ | ✅ | Different events |
| 5.5 Task Integration | ✅ | ✅ | Different tasks |
| 5.6 Impact Assessment | ✅ | ✅ | Different impact types/counts |
| 5.7 Sequence Workflow | ✅ | ✅ | Different complexity |

**100% Pattern Coverage**: Both incidents demonstrate all 7 patterns.

### Applicability to Other Incident Types

**These same patterns can model**:
- ✅ Phishing (demonstrated in Step_2/Step_3)
- ✅ Ransomware (demonstrated here)
- ⚡ Data breach (Pattern 5.6: confidentiality impact)
- ⚡ Insider threat (Pattern 5.3: anecdote + context evidence)
- ⚡ Denial of service (Pattern 5.6: availability impact)
- ⚡ Malware infection (Pattern 5.3: enrichment + external evidence)
- ⚡ Supply chain compromise (Pattern 5.4: event chains)
- ⚡ Advanced persistent threat (Pattern 5.7: complex workflows)

**Pattern Universality**: 7 patterns + 8 evidence types = comprehensive incident modeling framework

---

## Implementation Guide

### Step-by-Step Incident Creation

**Phase 0: Prerequisites** (Step_0 & Step_1)
- Create personal identity
- Create company identities
- Create system/asset identities

**Phase 1: Foundation Objects** (Level 0-2)
- Create foundation SCOs (user-account, url, ipv4-addr)
- Create Level 1 SCOs (email-addr, file)

**Phase 2: Evidence Collection** (Pattern 5.3, Level 3-4)
- Create observed-data containers
- Create sightings with evidence extensions
- Use appropriate evidence type for source

**Phase 3: Threat Characterization** (Level 3)
- Create indicator or malware objects
- Map to frameworks (ATT&CK)

**Phase 4: Event Derivation** (Pattern 5.4, Level 4)
- Derive events from sightings
- Create event chains (led-to relationships)
- Add StateChangeObject for state tracking

**Phase 5: Impact Assessment** (Pattern 5.6, Level 4)
- Assess impacts (availability, confidentiality, etc.)
- Use appropriate impact extensions
- Link to impacted entities

**Phase 6: Task Creation** (Pattern 5.5, Level 4)
- Create investigation/remediation tasks
- Assign owners
- Create SRO relationships (performed, assigned, etc.)

**Phase 7: Workflow Orchestration** (Pattern 5.7, Level 5)
- Create sequence objects
- Define workflow order
- Add conditional branching

**Phase 8: Incident Container** (Pattern 5.1, Level 6)
- Create incident object
- Populate IncidentCore extension
- Register all objects in appropriate ref fields

**Build Order**: ALWAYS follow dependency hierarchy (Level 0 → Level 6)

### Template Usage

**For Each Object Type**:
1. Load data template (`{object}_data.json`)
2. Load class template (`{Object}_template.json`)
3. Call Python block (`invoke_make_{object}_block()`)
4. Auto-generated parameters from property types
5. Automatic routing to correct context file

**Context Memory Integration**:
- User context: `/usr/` (personal identity)
- Company context: `/identity--{company-uuid}/` (organizational identities)
- Incident context: `/incident--{incident-uuid}/` (all incident objects)
- Global routing: `context_map.json`

---

## Final Comparison Summary

### What's Different Between Incidents

**Attack Characteristics**:
- Phishing: Credential theft via fake login page
- Ransomware: File encryption via malicious executable

**Observables**:
- Phishing: url, email-addr
- Ransomware: file, process, network-traffic, ipv4-addr

**Impact Types**:
- Phishing: 2 types (confidentiality, availability)
- Ransomware: 4 types (availability, confidentiality, monetary, integrity)

**Workflow Complexity**:
- Phishing: Simple linear (reset → analyze)
- Ransomware: Complex branching (recovery success/failure)

### What's Same Between Incidents

**Graph Patterns**: All 7 patterns (5.1-5.7)

**Dependency Hierarchy**: Level 0 → Level 6

**Evidence Structure**: Pattern 5.3 (observed-data → sighting)

**Template Approach**: Three-file pattern (data, class, python)

**Context Memory**: Same storage architecture

**Incident Container**: Pattern 5.1 (IncidentCore extension)

**Pattern Reusability Proven**: ✅ Same patterns, different content, complete modeling
