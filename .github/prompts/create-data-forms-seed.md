# Create data forms from stix data objects using class templates as a reference

Read a_seed\3_class_template_description.md and then a_seed\4_data_form_description.md to understand how class templates define the structure of STIX objects and how data forms are created based on those templates.

Open a_seed\2_initial_set_of_blocks.md and retrieve sdo_make_files, and sco_make_files
Go through every directory in both of these lists, for each:
1. Find the class template file in the directory (it will be named <Class_Name>_template.json)
2. Compare it to every other json file in the same directory (these are the data examples), and examine how each one is based on the class template

Only look at examples in these directories that have a make_object.py file, as these are the ones that have working implementations. Sometimes the type label will be filled in incorrectly, please change it when you encounter that.

When you have gone through all of them, create a summary of how to convert from a STIX JSON object to a data form using the class template as a reference and store it in the architecture documentation.

Update your instructions in github/instructions to include this new understanding of how to create data forms from STIX JSON objects using class templates.

Then, with this new knowledge, refactor Orchestration\Convert_Examples_to_DataForms.ipynb, so that it actually creates data forms with the correct structure. Build a test that can be run using the Identity data object and data form example provided in a_seed\4_data_form_description.md to verify that the data form created matches the expected output.

Finally, create a prompt that can be used to instruct an AI assistant to create data forms from STIX JSON objects using the class templates as a reference. The prompt should include context about when to use it, the input required, and the expected output. Provide an example usage of the prompt. Store this prompt in .github/prompts/create-data-forms.md