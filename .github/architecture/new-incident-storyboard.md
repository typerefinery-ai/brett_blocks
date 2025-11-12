# New Incident Storyboard - Ransomware Attack Scenario

## Document Purpose

This storyboard describes the story for creating an entirely new incident type beyond the phishing scenario. This demonstrates how to apply the graph patterns from stix-graph-patterns.md to a different threat scenario - in this case, a ransomware attack. This serves as a template for creating storyboards for any incident type.

---

## Story Overview: Ransomware Attack on Healthcare Provider

### Scenario Selection Rationale

**Why Ransomware:**
- Different attack vector (exploitation vs social engineering)
- Different primary impacts (availability + integrity vs confidentiality)
- Different urgency (immediate operational disruption)
- Different stakeholders (patient safety concerns)
- Demonstrates different STIX object combinations

**Alternative scenarios this template supports:**
- Malware infections (banking trojans, RATs, etc.)
- Data breaches (insider threat, misconfiguration)
- DDoS attacks (availability focus)
- Supply chain compromises (trusted relationship exploitation)
- Insider threats (privileged access abuse)

---

## Narrative: When the Hospital's Systems Encrypt

**Setting:**  
MedCare Regional Hospital - a 400-bed healthcare facility with electronic health records (EHR), medical imaging systems, and connected medical devices. Created in Step 1 as company identity with IT system identities.

**Characters:**
- Dr. Sarah Chen (radiologist) - first to notice encrypted files
- Marcus Thompson (IT administrator) - discovers ransom note
- Jennifer Walsh (IR team lead) - your identity, incident commander
- David Kim (forensics analyst) - investigates patient zero
- Chief Information Security Officer (executive sponsor)

**Inciting Incident:**  
3:47 AM - Automated backup job fails. By 7:15 AM, radiologists cannot access medical images. By 8:00 AM, ransom note discovered on file servers.

---

## Act 1: Initial Detection and Triage

### Scene 1: The First Signs (Pattern 6.2 - Evidence Collection)

**Story:**  
Dr. Chen arrives for her shift and cannot open any DICOM medical images. Everything shows "encrypted" extensions. She calls IT helpdesk. While troubleshooting, Marcus the IT admin discovers a ransom note on the file server: "All your files have been encrypted by LockBit 3.0. Pay 50 Bitcoin..."

**Graph Pattern Used:** Pattern 6.2 - Evidence Collection (sighting-alert)

**Objects to Create:**

**1. SCOs - The Evidence Artifacts:**

```yaml
file SCO - Ransom Note:
  type: "file"
  name: "README_FOR_DECRYPT.txt"
  size: 1247
  hashes:
    SHA-256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  parent_directory_ref: file-server-directory
  
file SCO - Encrypted Medical Image:
  type: "file"
  name: "patient_12345_xray.dcm.locked"
  size: 5248576
  hashes:
    SHA-256: "..."
  extensions:
    archive-ext:
      contains_refs: [original-file]
  
directory SCO - Affected File Server:
  type: "directory"
  path: "\\\\medcare-fs01\\radiology\\imaging"
  contains_refs: [ransom-note-file, encrypted-files]

windows-registry-key SCO - Persistence Mechanism:
  type: "windows-registry-key"
  key: "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
  values:
    - name: "SystemUpdate"
      data: "C:\\Windows\\Temp\\svchost.exe"
      data_type: "REG_SZ"

process SCO - Ransomware Process:
  type: "process"
  pid: 4728
  name: "svchost.exe"
  command_line: "C:\\Windows\\Temp\\svchost.exe --encrypt --fast"
  created: "2024-01-15T03:47:23.000Z"
  binary_ref: malicious-binary-file
  parent_ref: explorer-process
  
network-traffic SCO - C2 Communication:
  type: "network-traffic"
  protocols: ["tcp", "https"]
  src_ref: infected-workstation-ipv4
  dst_ref: c2-server-ipv4
  dst_port: 443
  extensions:
    http-request-ext:
      request_method: "POST"
      request_value: "/api/keys/submit"
      
ipv4-addr SCO - C2 Server:
  type: "ipv4-addr"
  value: "185.220.101.42"
  resolves_to_refs: [c2-server-domain]
  
domain-name SCO - C2 Domain:
  type: "domain-name"
  value: "update-security-service.com"
```

**2. Observed Data - Grouping Evidence:**

```yaml
observed-data SDO - Ransomware Artifacts:
  first_observed: "2024-01-15T03:47:23.000Z"
  last_observed: "2024-01-15T08:00:00.000Z"
  number_observed: 1
  object_refs:
    - ransom-note-file
    - encrypted-files (multiple)
    - malicious-process
    - registry-key
    - network-traffic
    - c2-ipv4
    - c2-domain
  created_by_ref: jennifer-walsh-identity
```

**3. Indicator - Ransomware Pattern:**

```yaml
indicator SDO - LockBit 3.0 Pattern:
  name: "LockBit 3.0 Ransomware Indicators"
  indicator_types: ["malicious-activity", "file-hash-watchlist"]
  pattern: "[file:hashes.'SHA-256' = 'e3b0c44...' OR process:name = 'svchost.exe' AND process:command_line CONTAINS '--encrypt']"
  pattern_type: "stix"
  valid_from: "2024-01-15T08:00:00.000Z"
  kill_chain_phases:
    - kill_chain_name: "lockheed-martin-cyber-kill-chain"
      phase_name: "actions-on-objectives"
  created_by_ref: jennifer-walsh-identity
```

**4. Sighting with Alert Extension:**

```yaml
sighting SRO - EDR Alert:
  sighting_of_ref: lockbit-indicator
  observed_data_refs: [ransomware-artifacts-observed-data]
  where_sighted_refs:
    - medcare-hospital-identity
    - radiology-workstation-identity
  first_seen: "2024-01-15T03:47:23.000Z"
  last_seen: "2024-01-15T08:00:00.000Z"
  count: 47  # number of encrypted workstations
  extensions:
    extension-definition--sighting-alert:
      name: "Ransomware Encryption Activity Detected"
      product: "CrowdStrike Falcon EDR"
      severity: "critical"
      source: "EDR Behavioral Analysis"
      description: "Mass file encryption detected on 47 workstations"
      log: "crowdstrike-event-12847.json"
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~15-25 objects (SCOs, observed-data, indicator, sighting)

**Story Checkpoint:**  
You now have documented the initial ransomware evidence as discovered by the EDR system and IT staff.

---

### Scene 2: Human Witness - IT Admin Reports (Pattern 6.2 - sighting-anecdote)

**Story:**  
Marcus the IT admin provides his account: "I was checking the backup logs when I saw the ransom note pop up on my screen. I immediately disconnected the file server from the network, but the encryption had already spread to the radiology department shares."

**Objects to Create:**

```yaml
anecdote SCO:
  value: "Discovered ransom note on file server at approximately 8:00 AM. Immediately disconnected server from network. Observed encrypted file extensions .locked on approximately 50% of radiology imaging files."
  provided_by_ref: marcus-thompson-identity
  report_date: "2024-01-15T08:15:00.000Z"
  
sighting SRO - IT Admin Report:
  sighting_of_ref: ransomware-event (created next)
  observed_data_refs: [observed-data-with-anecdote]
  where_sighted_refs: [file-server-identity]
  extensions:
    extension-definition--sighting-anecdote:
      person_name: "Marcus Thompson"
      person_context: "IT Administrator, 8 years tenure"
      report_submission: "in-person to IR team"
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~3-5 objects

---

## Act 2: Investigation and Containment

### Scene 3: Creating the Initial Event (Pattern 6.3)

**Story:**  
With evidence documented, you declare this a formal security event requiring immediate response.

**Objects to Create:**

```yaml
event SDO - Ransomware Encryption Event:
  name: "LockBit 3.0 Ransomware Encryption"
  event_types: ["malware", "ransomware", "data-encrypted"]
  status: "occurred"
  start_time: "2024-01-15T03:47:23.000Z"  # when encryption began
  end_time: "2024-01-15T08:05:00.000Z"     # when network disconnected
  sighting_refs:
    - edr-alert-sighting
    - it-admin-anecdote-sighting
  changed_objects:
    - StateChangeObject:
        object_ref: radiology-file-share-identity
        property: "availability"
        old_value: "operational"
        new_value: "encrypted"
        changed_time: "2024-01-15T03:47:23.000Z"
    - StateChangeObject:
        object_ref: ehr-system-identity
        property: "availability"
        old_value: "operational"
        new_value: "degraded"
        changed_time: "2024-01-15T06:30:00.000Z"
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~1-3 objects

---

### Scene 4: Immediate Response Tasks (Pattern 6.4)

**Story:**  
IR team lead (you) creates urgent response tasks for the team.

**Objects to Create:**

```yaml
task SDO - Network Isolation:
  name: "Isolate infected systems from network"
  task_types: ["contain"]
  priority: 100  # highest priority
  status: "completed"
  owner: marcus-thompson-identity
  start_time: "2024-01-15T08:05:00.000Z"
  end_time: "2024-01-15T08:20:00.000Z"
  outcome: "47 workstations isolated, file server disconnected, network segmentation activated"
  impacted_entity_refs: [hospital-network-identity]
  created_by_ref: jennifer-walsh-identity

task SDO - Forensic Preservation:
  name: "Preserve forensic evidence from patient zero"
  task_types: ["investigate", "forensics"]
  priority: 95
  status: "in-progress"
  owner: david-kim-identity
  start_time: "2024-01-15T08:30:00.000Z"
  impacted_entity_refs: [dr-chen-workstation-identity]
  created_by_ref: jennifer-walsh-identity

task SDO - Backup Verification:
  name: "Verify backup integrity and recovery capability"
  task_types: ["recover", "assess"]
  priority: 90
  status: "in-progress"
  owner: marcus-thompson-identity
  created_by_ref: jennifer-walsh-identity

task SDO - Clinical Impact Assessment:
  name: "Assess impact on patient care operations"
  task_types: ["assess", "safety"]
  priority: 98
  status: "completed"
  owner: ciso-identity
  outcome: "Non-emergency procedures delayed. Emergency department unaffected. Alternative imaging procedures activated."
  created_by_ref: jennifer-walsh-identity

task SDO - Legal Notification Review:
  name: "Assess HIPAA breach notification requirements"
  task_types: ["legal", "compliance"]
  priority: 85
  status: "in-progress"
  owner: legal-counsel-identity
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~5-7 tasks

---

## Act 3: Timeline Reconstruction

### Scene 5: The Attack Kill Chain (Pattern 6.3 + 6.5)

**Story:**  
Forensics analyst David reconstructs how the attack unfolded by analyzing logs and memory dumps.

**Events to Create (in chronological order):**

```yaml
event SDO - Initial Compromise:
  name: "Exploitation of Unpatched VPN Appliance"
  event_types: ["exploitation", "initial-access"]
  status: "occurred"
  start_time: "2024-01-12T22:15:00.000Z"  # 3 days before encryption
  sighting_refs: [vpn-log-sighting]
  changed_objects:
    - StateChangeObject:
        object_ref: vpn-appliance-identity
        property: "security-state"
        old_value: "secure"
        new_value: "compromised"
  created_by_ref: jennifer-walsh-identity

event SDO - Lateral Movement:
  name: "Credential Dumping and Lateral Movement"
  event_types: ["credential-access", "lateral-movement"]
  status: "occurred"
  start_time: "2024-01-12T23:30:00.000Z"
  end_time: "2024-01-13T02:00:00.000Z"
  sighting_refs: [mimikatz-detection-sighting]
  changed_objects:
    - StateChangeObject:
        object_ref: domain-admin-credentials
        property: "security-state"
        old_value: "protected"
        new_value: "compromised"
  created_by_ref: jennifer-walsh-identity

event SDO - Persistence Establishment:
  name: "Registry Modification for Persistence"
  event_types: ["persistence", "registry-modification"]
  status: "occurred"
  start_time: "2024-01-13T03:15:00.000Z"
  sighting_refs: [registry-change-sighting]
  created_by_ref: jennifer-walsh-identity

event SDO - Defense Evasion:
  name: "Antivirus and EDR Disabled"
  event_types: ["defense-evasion"]
  status: "occurred"
  start_time: "2024-01-14T18:30:00.000Z"
  sighting_refs: [av-disabled-sighting]
  created_by_ref: jennifer-walsh-identity

event SDO - Data Staging:
  name: "Sensitive Data Collection and Staging"
  event_types: ["collection", "data-staged"]
  status: "occurred"
  start_time: "2024-01-15T01:00:00.000Z"
  end_time: "2024-01-15T03:30:00.000Z"
  sighting_refs: [large-file-movement-sighting]
  changed_objects:
    - StateChangeObject:
        object_ref: patient-records-database
        property: "data-state"
        old_value: "at-rest"
        new_value: "copied-to-staging"
  created_by_ref: jennifer-walsh-identity

event SDO - Data Exfiltration:
  name: "Patient Data Exfiltration to C2"
  event_types: ["exfiltration"]
  status: "occurred"
  start_time: "2024-01-15T03:30:00.000Z"
  end_time: "2024-01-15T03:45:00.000Z"
  sighting_refs: [network-exfil-sighting]
  created_by_ref: jennifer-walsh-identity

event SDO - Ransomware Deployment:
  name: "LockBit 3.0 Ransomware Encryption"
  # (Already created in Scene 3)

relationship SRO - Event Causality Chain:
  relationship_type: "led-to"
  source_ref: initial-compromise-event
  target_ref: lateral-movement-event
  
  # Repeat for each event pair in timeline
```

**Sequence Object - Attack Timeline:**

```yaml
sequence SDO - Ransomware Kill Chain:
  name: "LockBit 3.0 Attack Timeline"
  sequenced_object: "event"
  sequence_type: "attack-chain"
  step_type: "serial"
  step_refs:
    - initial-compromise-event
    - lateral-movement-event
    - persistence-event
    - defense-evasion-event
    - data-staging-event
    - data-exfiltration-event
    - ransomware-encryption-event
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~7 events + 6 relationship SROs + 1 sequence = ~14 objects

---

## Act 4: Impact Assessment

### Scene 6: Understanding the Damage (Pattern 6.6)

**Story:**  
The IR team assesses the full scope of impact across multiple dimensions.

**Impact Objects to Create:**

```yaml
impact SDO - Availability Impact (Critical Systems):
  impact_category: "availability"
  extensions:
    extension-definition--availability:
      availability_loss_type: "loss"
      duration: "temporary"
  impacted_refs:
    - radiology-imaging-system-identity
    - ehr-system-identity
    - file-server-identity
  start_time: "2024-01-15T03:47:23.000Z"
  end_time: null  # ongoing
  recoverability: "extended"  # will take 3-5 days to restore
  criticality: "high"
  created_by_ref: jennifer-walsh-identity

impact SDO - Integrity Impact (Data):
  impact_category: "integrity"
  extensions:
    extension-definition--integrity:
      alteration_type: "encryption"
      integrity_loss_type: "confirmed-loss"
  impacted_refs:
    - patient-records-database
    - medical-imaging-files
  start_time: "2024-01-15T03:47:23.000Z"
  recoverability: "supplemented"  # restore from backups
  created_by_ref: jennifer-walsh-identity

impact SDO - Confidentiality Impact (Data Breach):
  impact_category: "confidentiality"
  extensions:
    extension-definition--confidentiality:
      information_type: "patient-health-information"
      loss_type: "suspected-loss"  # exfiltration detected but not confirmed
  impacted_refs:
    - patient-identity-1
    - patient-identity-2
    # ... (all affected patients)
  start_time: "2024-01-15T03:30:00.000Z"
  recoverability: "not-recoverable"  # data cannot be un-stolen
  created_by_ref: jennifer-walsh-identity

impact SDO - Safety Impact (Patient Care):
  impact_category: "safety"
  extensions:
    extension-definition--safety:
      safety_impact_type: "delayed-care"
      affected_population_size: 23  # delayed procedures
  impacted_refs:
    - medcare-hospital-identity
    - patient-identities (multiple)
  start_time: "2024-01-15T08:00:00.000Z"
  recoverability: "regular"  # procedures can be rescheduled
  created_by_ref: jennifer-walsh-identity

impact SDO - Monetary Impact:
  impact_category: "monetary"
  extensions:
    extension-definition--monetary:
      currency: "USD"
      variety:
        - "ransom-demand"
        - "incident-response-costs"
        - "downtime-costs"
        - "regulatory-fines"
      min_amount: 500000
      max_amount: 5000000
  impacted_refs: [medcare-hospital-identity]
  recoverability: "not-recoverable"
  created_by_ref: jennifer-walsh-identity

impact SDO - Reputational Impact:
  impact_category: "external"
  extensions:
    extension-definition--external:
      reputation_loss_type: "brand-damage"
      stakeholder_type:
        - "patients"
        - "insurance-companies"
        - "regulatory-bodies"
  impacted_refs: [medcare-hospital-identity]
  recoverability: "extended"  # long-term trust rebuilding
  created_by_ref: jennifer-walsh-identity
```

**Objects Created:** ~6-8 impact objects

---

## Act 5: Incident Assembly and Response Workflow

### Scene 7: The Complete Incident (Pattern 6.7)

**Story:**  
You assemble all the evidence, events, tasks, and impacts into a formal incident case.

**Incident Object:**

```yaml
incident SDO:
  name: "LockBit 3.0 Ransomware Attack - MedCare Regional Hospital"
  description: "Ransomware attack via VPN exploitation, resulting in encryption of radiology systems, EHR degradation, suspected PHI exfiltration, and operational impact to patient care."
  
  extensions:
    extension-definition--ef765651-680c-498d-9894-99799f2fa126:  # Incident Core
      determination: "confirmed-true-positive"
      incident_types: ["ransomware", "data-breach", "extortion"]
      investigation_status: "active-investigation"
      
      # Core references
      event_refs:
        - initial-compromise-event
        - lateral-movement-event
        - persistence-event
        - defense-evasion-event
        - data-staging-event
        - data-exfiltration-event
        - ransomware-encryption-event
      
      task_refs:
        - network-isolation-task
        - forensic-preservation-task
        - backup-verification-task
        - clinical-impact-task
        - legal-notification-task
      
      impact_refs:
        - availability-impact
        - integrity-impact
        - confidentiality-impact
        - safety-impact
        - monetary-impact
        - reputational-impact
      
      other_object_refs:
        - all SCOs (files, processes, network-traffic, etc.)
        - all observed-data objects
        - all sightings (alert, anecdote, hunt, enrichment)
        - all indicators
        - all sequences
        - all relationship SROs
        - all identities (attackers, victims, responders)
  
  # Standard incident properties
  first_seen: "2024-01-15T03:47:23.000Z"
  last_seen: "2024-01-15T08:00:00.000Z"
  
  confidence: 95
  
  impact_criticality: "high"
  
  labels:
    - "ransomware"
    - "lockbit-3.0"
    - "healthcare"
    - "patient-safety-impact"
    - "HIPAA-breach"
    - "double-extortion"
  
  external_references:
    - source_name: "CISA Alert"
      url: "https://www.cisa.gov/lockbit-ransomware"
      description: "LockBit 3.0 Ransomware Affiliates Exploit CVE 2023-4966"
  
  created_by_ref: jennifer-walsh-identity
  created: "2024-01-15T08:30:00.000Z"
```

**Objects Created:** 1 incident (container for ~80-120 objects)

---

### Scene 8: Coordinated Response Workflow (Pattern 6.5)

**Story:**  
Multiple response teams coordinate through a structured workflow.

**Additional Tasks:**

```yaml
task SDO - Malware Analysis:
  name: "Reverse engineer ransomware binary"
  task_types: ["investigate", "malware-analysis"]
  priority: 80
  status: "in-progress"
  owner: malware-analyst-identity

task SDO - Threat Intelligence Query:
  name: "Research LockBit 3.0 TTPs and decryption options"
  task_types: ["investigate", "threat-intelligence"]
  priority: 85
  status: "completed"
  outcome: "No known decryptor. Group active since 2019. Double-extortion MO confirmed."

task SDO - Backup Restoration:
  name: "Restore radiology systems from backups"
  task_types: ["recover"]
  priority: 95
  status: "in-progress"
  dependencies: [backup-verification-task]

task SDO - Patient Notification:
  name: "Notify affected patients per HIPAA requirements"
  task_types: ["communication", "compliance"]
  priority: 75
  status: "pending"
  dependencies: [legal-notification-task]

task SDO - Law Enforcement Notification:
  name: "Report to FBI IC3"
  task_types: ["legal", "reporting"]
  priority: 70
  status: "completed"

task SDO - Ransom Decision:
  name: "Executive decision on ransom payment"
  task_types: ["decision"]
  priority: 90
  status: "completed"
  outcome: "Decision: Do not pay ransom. Proceed with backup restoration."
  owner: ciso-identity
```

**Response Sequence:**

```yaml
sequence SDO - Ransomware Response Playbook:
  name: "Healthcare Ransomware Response Workflow"
  sequenced_object: "task"
  sequence_type: "playbook"
  step_type: "parallel-then-serial"
  step_refs:
    # Phase 1 - Immediate (parallel)
    - [network-isolation-task, clinical-impact-task, forensic-preservation-task, law-enforcement-task]
    # Phase 2 - Investigation (parallel)
    - [backup-verification-task, malware-analysis-task, threat-intel-task, legal-notification-task]
    # Phase 3 - Decision Point (serial)
    - [ransom-decision-task]
    # Phase 4 - Recovery (serial after decision)
    - [backup-restoration-task]
    # Phase 5 - Notification (parallel, after legal review)
    - [patient-notification-task]
```

**Objects Created:** ~6 additional tasks + 1 sequence = ~7 objects

---

## Act 6: Extended Evidence Collection

### Scene 9: Threat Intelligence Enrichment (Pattern 6.2 - sighting-enrichment)

**Story:**  
Threat intel team discovers this attack matches recent LockBit campaigns targeting healthcare.

```yaml
sighting SRO - Threat Intel Enrichment:
  sighting_of_ref: lockbit-indicator
  extensions:
    extension-definition--sighting-enrichment:
      name: "LockBit 3.0 Healthcare Campaign Attribution"
      enrichment_type: "external-lookup"
      source: "FBI Flash Alert, MISP Event 98234, HealthISAC"
      confidence_score: 90
  external_references:
    - source_name: "FBI Flash Alert CU-000183-MW"
      url: "https://www.ic3.gov/Media/News/2024/..."
      description: "LockBit 3.0 targeting healthcare sector via CVE-2023-4966"
```

---

### Scene 10: MITRE ATT&CK Mapping (Pattern 6.2 - sighting-framework)

**Story:**  
Map the attack to MITRE ATT&CK for healthcare framework.

```yaml
sighting SRO - ATT&CK Mapping (multiple):
  # T1190 - Exploit Public-Facing Application
  # T1078 - Valid Accounts
  # T1003 - OS Credential Dumping
  # T1547 - Boot or Logon Autostart Execution
  # T1562 - Impair Defenses
  # T1074 - Data Staged
  # T1041 - Exfiltration Over C2 Channel
  # T1486 - Data Encrypted for Impact
  # T1657 - Financial Theft (ransom demand)
  
  sighting_of_ref: event or indicator
  extensions:
    extension-definition--sighting-framework:
      framework: "ATT&CK"
      version: "v14.1"
      framework_id: "T1486"
      tactic: ["impact"]
      technique: ["data-encrypted-for-impact"]
```

---

## Complete Object Inventory

### Final Count for Ransomware Incident:

**SCOs:** ~30-50 (files, processes, network-traffic, registry-keys, IP addresses, domains)  
**Observed-Data:** ~15-25 (grouping SCO observations)  
**Sightings:** ~10-15 (alert, anecdote, hunt, enrichment, framework)  
**Indicators:** ~5-10 (file hashes, network IOCs, behavioral patterns)  
**Events:** ~7-10 (attack kill chain)  
**Tasks:** ~12-15 (response workflow)  
**Impacts:** ~6-8 (all impact categories)  
**Sequences:** ~2-3 (attack timeline, response workflow)  
**Identities:** ~15-25 (hospital staff, IT systems, patients)  
**Relationships:** ~20-30 (led-to, mitigates, investigates, etc.)  
**Attack Patterns:** ~8-12 (MITRE ATT&CK techniques)  
**Malware:** ~1-2 (LockBit 3.0 malware object)  
**Tool:** ~2-4 (Mimikatz, custom scripts)  
**Incident:** 1 (container)  

**Total Objects:** ~140-200 objects

---

## Story Themes and Lessons

### Why This Scenario Matters

**1. Different Threat Model:**
- Phishing = social engineering, user error
- Ransomware = exploitation, technical vulnerability
- Demonstrates STIX flexibility across threat types

**2. Healthcare-Specific Considerations:**
- Patient safety impact (unique to healthcare, critical infrastructure)
- HIPAA compliance (legal/regulatory dimension)
- Clinical operations (availability is life-safety issue)
- Double extortion (confidentiality + availability impacts)

**3. Executive Decision Points:**
- Ransom payment decision (captured as task with outcome)
- Patient notification timing (legal vs operational considerations)
- Law enforcement coordination (reporting requirements)

**4. Timeline Complexity:**
- Multi-day dwell time (initial compromise → encryption)
- Multiple attack phases (reconnaissance, lateral movement, staging, impact)
- Sequential event chain with clear causality

**5. Response Coordination:**
- Multiple teams (IR, IT, clinical, legal, comms, executive)
- Dependencies between tasks (can't restore until isolated)
- Parallel and serial workflow phases

---

## Adapting This Template to Other Scenarios

### Malware Infection (Banking Trojan)

**Key Changes:**
- **Primary Impact:** Confidentiality (credentials stolen)
- **Evidence:** Memory dumps, keylogger files, network C2 traffic
- **Events:** Initial infection → persistence → credential harvesting → exfiltration
- **Victims:** Financial institution customers
- **Legal:** PCI-DSS, state breach laws

### Data Breach (Insider Threat)

**Key Changes:**
- **Threat Source:** Insider identity (employee/contractor)
- **Evidence:** sighting-anecdote (tip from coworker), sighting-context (motive/opportunity), access logs
- **Events:** Unauthorized access → data download → departure from company
- **Impacts:** Confidentiality, reputational, competitive advantage loss
- **Response:** HR involvement, legal prosecution

### DDoS Attack

**Key Changes:**
- **Primary Impact:** Availability only
- **Evidence:** Network-traffic SCOs (massive volume), server logs
- **Events:** Attack waves (different techniques: SYN flood, UDP amplification, application layer)
- **Indicators:** Botnets, amplification servers
- **Response:** Traffic scrubbing, rate limiting, upstream filtering

### Supply Chain Compromise

**Key Changes:**
- **Complexity:** Multiple victims (all customers of compromised vendor)
- **Trust:** Relationship SRO between vendor identity and customer identities
- **Evidence:** Software updates (file SCOs with malicious code), code signing certificates
- **Attribution:** Threat actor → campaign → multiple incidents
- **Response:** Third-party risk assessment, vendor notification

---

## How to Use This Storyboard

### For Creating New Scenarios:

1. **Choose Threat Type:** Ransomware, malware, DDoS, insider, supply chain, etc.
2. **Define Setting:** Organization type, industry, size, critical assets
3. **Identify Characters:** Victims, responders, executives, threat actors
4. **Map Kill Chain:** How attack unfolds (events)
5. **Document Evidence:** What you observe (SCOs, observed-data, sightings)
6. **Assess Impacts:** Business consequences (availability, confidentiality, integrity, safety, financial, reputation)
7. **Plan Response:** Tasks and workflow (containment, eradication, recovery, lessons learned)
8. **Assemble Incident:** Bring all objects together in incident.other_object_refs

### For Notebook Development:

- Each "Scene" could be a separate notebook
- Scene 1: Detection Evidence (Step_4_Ransomware_Detection.ipynb)
- Scene 3: Event Creation (Step_5_Ransomware_Timeline.ipynb)
- Scene 4: Response Tasks (Step_6_Ransomware_Response.ipynb)
- Scene 6: Impact Assessment (Step_7_Ransomware_Impact.ipynb)
- Scene 7: Incident Assembly (Step_8_Ransomware_Incident.ipynb)

### For System Integration:

- Use sequence objects to drive SOAR automation
- Map to incident response playbooks
- Integrate with ticketing systems (tasks)
- Feed SIEMs with indicators
- Generate executive reports from impact objects

