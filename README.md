# brett_blocks

This is an experimental repo for containg data flow blocks for use in Type Refinery.

Each block is documented in a sub-directory, named after the block, and contains:
- Script - a python or javascript file containing the exact script to be executed in the block
- Config - a JSON file that contains the exact data needed to fill out the other config fields
- UI_Code - a HTML file that contians the javascript and HTML from the Edit part of the block
- README - a markdown file that contains the description of how the block works, and how to get the best out of it (unlike those TotalJS tossers)

The Python blocks can be loaded and tested locally. Each Script wil take imports and export a file, and so testing and glue code can be written

It is not clear yet how the HTLM code, or javascript code could be tested locally, so we are open to suggestions.

Note Poetry Install, Python v3.9

## StixORM Blocks
There are two types of block families o focus on:
- StixORM: Blocks that apply to create a valid Stix object from data
- OS-Triage: Blocks that apply to system or app tasks, such as saving to context

### StixORM Blocks
| Directory | Name                   |   Type    | Inputs            |        Outputs        | Description                                                      |
|:-------:|:-----------------------|:---------:|:------------------|:---------------------:|:-----------------------------------------------------------------|
| Common | 	Common Template         |  Template   | 	  |      	       | 	Common data to be applied to every class-based Template          |
| Get_Embedded | 	Get Object's sub-graph            | 	GetObjects | 	Stix ID	  |      [Stix objects]	       | Given an ID, get an object, and all its sub-objects            |
| SCO | 	SCO Objects | 	Make Object | 	Template, Data Form, Objects |      	Stix Object (JSON)       | 	Given a DataForm, and potentailly more objects, make a JSON stix object |
| SDO | 	SDO Objects           | Make Object  | 	Template, Data Form, Objects          |      	URL String      | 	Given a DataForm, and potentailly more objects, make a JSON stix object                                    |
| SRO | 	SRO Objects        | 	Make Object | 	Template, Data Form, Objects	         | Email address String	 | Given a DataForm, and potentailly more objects, make a JSON stix object                          |
| Meta | 	Meta Objects          | 	Make Object | 	Template, Data Form, Objects          |     	IPv4 String      | 	Given a DataForm, and potentailly more objects, make a JSON stix object                                   |


### OS_Triage Blocks
| Directory | Name          |   Type    | Inputs                      |  Outputs   | Description                                                |
|:-------:|:--------------|:---------:|:----------------------------|:----------:|:-----------------------------------------------------------|
|  Create_Context   | 	Create Context Store   | Create Store  | 	Stix Object             | 	Message | 	Given an object, setup the context store                   |
|  Form Actions   | 	Actions in Form    | 	Get Valid Objects | 	Object, spec	 | Stix_List	 | From a Form, search for all valid objects for a foreign key          |
|  Get Context   | 	Get objects from Store     | 	Get Objects | 	Query form Data   | 	Stix Object | 	Given a query form, find the data from Store                    |
|  Mouse   | 	Mouse Actions     | 	Actions in Viz | 	Selected Objects	  | Stix_List	 | Get data for Mouse Actions in Viz            |
|  Open Incident   | 	Incident-level Actions | 	Incident | 	nil or ID       | 	Stix_List | 	Open all incidents, or one incident             |
|  Save Context   | 	Save Objects to Context    | 	Save Objects | 	Stix Object           | 	Message | 	Given a Stix Object, save it to a specific context                     |
|  Viz Dataviews   | 	Get Viz Data      | 	Retrieve | 	nil          | 	Stix_List | 	Return the force graph or tree data for a view                       |		
|  Update Context   | 	Update context and TypeDB   | 	Local<->Remote | 	Current List, Prior List         | 	TypeQL CRUD statements | 	Given a curent list of objects, and       an old list, generate the TypeQL statements needed to update             |


## Installation
To install the blocks, clone the repo and run:

```bash
poetry install
```

## Testing

A comprehensive testing system validates all StixORM blocks through round-trip conversion tests.

### Quick Test Run

**Windows (PowerShell):**
```powershell
.\tests\run_tests.ps1
```

**Linux/Mac:**
```bash
./tests/run_tests.sh
```

**Using Poetry directly:**
```bash
poetry run pytest tests/
```

### Documentation

- **[TESTING.md](TESTING.md)** - Quick reference guide
- **[tests/README.md](tests/README.md)** - Complete testing documentation  
- **[architecture/stixorm-testing-system-design.md](architecture/stixorm-testing-system-design.md)** - System design details

## Usage
Note that personal data in the **Orchestration/generated/context_mem** and **Orchestration/Results** directories should not be pushed to github, and the gitignore is updated to reflect this.

Delete everything within the **Orchestration/generated/context_mem** directory before starting to use this system.

Then run the Step 0, Step 1, Step 2, and Step 3 Jupyter Notebooks in order, and check out the generated data in the **Orchestration/Results** and **Orchestration/generated/context_mem** directories.
