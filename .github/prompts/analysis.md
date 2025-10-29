# Analysis and Troubleshooting Prompts

## Debug Function Performance

**Context:** When a function appears to be performing incorrectly
**Input:** Function name, expected behavior, observed issues
**Expected Output:** Diagnostic analysis and test results

### Prompt Text

```
I need to debug the [FUNCTION_NAME] function that appears to be performing incorrectly.

Please help me:
1. Examine the function code and understand its expected behavior
2. Check for common issues (file paths, working directory, missing dependencies)
3. Create a comprehensive test script that:
   - Tests the function in isolation
   - Checks for required files and dependencies
   - Provides detailed output both to terminal and JSON files
   - Handles errors gracefully with clear error messages
4. Run the test and analyze the results
5. Provide a detailed analysis of what's working, what's not, and recommendations

Current issues observed: [DESCRIBE_ISSUES]
Expected behavior: [DESCRIBE_EXPECTED_BEHAVIOR]

Focus on creating a standalone test that can be run independently to verify function operation.
```

## Analyze Data Flow

**Context:** When investigating how data moves through the system
**Input:** Starting point, data type, or workflow
**Expected Output:** Data flow diagram and analysis

### Prompt Text

```
Analyze the data flow for [DATA_TYPE/WORKFLOW] in the brett_blocks system.

Please:
1. Trace the data from input to output
2. Identify all transformation points
3. Map file locations where data is stored/retrieved
4. Show relationships between different data elements
5. Identify potential bottlenecks or failure points
6. Document the context management approach
7. Create a visual representation of the flow

Starting from: [INPUT_SOURCE]
Ending at: [OUTPUT_DESTINATION]

Include:
- File paths and directory structures involved
- Function calls and data transformations
- STIX object relationships and mappings
- Context switching and memory management
- Error handling and recovery mechanisms
```

## Performance Analysis

**Context:** When investigating system performance issues
**Input:** Component or workflow experiencing issues
**Expected Output:** Performance analysis and optimization recommendations

### Prompt Text

```
Perform a performance analysis of [COMPONENT/WORKFLOW] in the brett_blocks system.

Analysis should include:
1. Execution time measurements
2. Memory usage patterns
3. File I/O operations and efficiency
4. Database/storage access patterns
5. Object creation and relationship processing overhead
6. Potential optimization opportunities

Test scenarios:
- Small dataset (< 10 objects)
- Medium dataset (10-100 objects)  
- Large dataset (100+ objects)

Provide:
- Benchmark results with timing data
- Bottleneck identification
- Optimization recommendations
- Code improvements where applicable
- Scaling considerations for larger datasets
```

## Context Investigation

**Context:** When investigating context memory and incident data
**Input:** Incident ID or context directory
**Expected Output:** Context analysis and object inventory

### Prompt Text

```
Investigate the context data for incident [INCIDENT_ID] or analyze the current context.

Please:
1. Load and examine the context_map.json to understand current state
2. Inventory all objects in the incident context
3. Analyze object relationships and connections
4. Check for data consistency issues
5. Identify unattached or orphaned objects
6. Verify STIX object integrity
7. Generate summary statistics

Analysis should cover:
- Object counts by type (SDO, SCO, SRO)
- Relationship mapping completeness
- Data quality issues
- Missing or incomplete objects
- Context switching implications
- Memory usage and storage efficiency

Output format:
- Executive summary
- Detailed object inventory
- Relationship analysis
- Issues and recommendations
- Data quality report
```