# Rename Current Block_Families\StixORM Directory Names in SCO, SDO and SRO directories to their class names

## SCO:
Consider the current names of directories in the Block_Families\StixORM\SCO directory versus the Python class names we want to convert them to in the markdown table below.

| Current_Name                                                                         | Future_Class_Name  |
| ------------------------------------------------------------------------------------ | ------------------ |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Anecdote                   | Anecdote           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Artifact                   | Artifact           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Autonomous_System          | AutonomousSystem   |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Directory                  | Directory          |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Domain_Name                | DomainName         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Email_Addr                 | EmailAddress       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Email_Message              | EmailMessage       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\File                       | File               |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\IPv4_Addr                  | IPv4Address        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\IPv6_Addr                  | IPv6Address        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\MAC_Address                | MACAddress         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Mutex                      | Mutex              |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Network_Traffic            | NetworkTraffic     |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Asset                  | OCAAsset           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Custom_File            | OCAFile            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Custom_Network_Traffic | OCANetworkTraffic  |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Custom_Process         | OCAProcess         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Custom_Software        | OCASoftware        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Custom_User_Account    | OCAUserAccount     |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Event                  | OCAEvent           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Finding                | OCAFinding         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_Geo                    | OCAGeo             |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\OCA_TTP_Tag                | OCATagging         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Process                    | Process            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Software                   | Software           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\URL                        | URL                |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\User_Account               | UserAccount        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\Windows_Registry_Key       | WindowsRegistryKey |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SCO\\X509_Cert                  | X509Certificate    |

## SDO:
Consider the current names of directories in the Block_Families\StixORM\SDO directory versus the Python class names we want to convert them to in the markdown table below.

| Current_Name                                                                   | Future_Name         |
| ------------------------------------------------------------------------------ | ------------------- |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Analytic             | Analytic            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Asset         | AttackAsset         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Campaign      | AttackCampaign      |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_DataComponent | DataComponent       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_DataSource    | DataSource          |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Group         | Group               |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Malware       | SoftwareMalware     |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Pattern       | AttackPattern       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Attack_Tool          | SoftwareTool        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\AttackFlow           | AttackFlow          |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Behavior             | Behavior            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Campaign             | Campaign            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Course_of_Action     | CourseOfAction      |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Detection            | Detection           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\DetectionStrategy    | DetectionStrategy   |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Detector             | Detector            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Event                | Event               |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Extension_Definition | ExtensionDefinition |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Flow_Action          | FlowAction          |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Flow_Asset           | FlowAsset           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Flow_Condition       | FlowCondition       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Flow_Operator        | FlowOperator        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Grouping             | Grouping            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Identity             | Identity            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Impact               | Impact              |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Incident             | Incident            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Indicator            | Indicator           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Infrastructure       | Infrastructure      |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Instrusion_Set       | IntrusionSet        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Location             | Location            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Malware              | Malware             |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Malware_Analysis     | MalwareAnalysis     |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Malware_Behavior     | MalwareBehavior     |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Malware_Method       | MalwareMethod       |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Malware_Objective    | MalwareObjective    |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Matrix               | Matrix              |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Mitigation           | Mitigation          |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Note                 | Note                |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Observed_Data        | ObservedData        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Opinion              | Opinion             |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Playbook             | Playbook            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Report               | Report              |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Sequence             | Sequence            |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Sub_Technique        | SubTechnique        |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Tactic               | Tactic              |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Task                 | Task                |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Technique            | Technique           |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Threat_Actor         | ThreatActor         |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Tool                 | Tool                |
| C:\\projects\\brett_blocks\\Block_Families\\StixORM\\SDO\\Vulnerability        | Vulnerability       |