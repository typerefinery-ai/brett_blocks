# Rules for Design of Blocks and Templates

## 1. Three Types of Names, each with a specific Format


There are 3 types of names for any object in this repo:

- **Class Name**: The name of the Python class, unique for every object, capitalised, no spaces
- **TypeQL Name**: The name of the TypeQL object, converted from the Class Name, unique for each object, lowercase with dashes between words
- **Stix Type**: The name of the object type, not unique for all object, lowercase with dashes

### 1.1 Examples of names

| Class Name     | TypeQL Name                        | Stix Type          |
|:--------------|:------------|:-------------------|
| "EmailAddress" | "email-address" | "email-addr" |
| "Finding"      | "finding"       | "x-ibm-finding"        |
| "Technique"     | "technique"      | "attack-pattern"       |
| "AttackPattern" | "attack-pattern" | "attack-pattern" |
| "HTTPRequestExt" | "http-request-ext" | "http-request-ext" |
| "WindowsPEBinaryExt" | "windows-pe-binary-ext" | "windows-pebinary-ext" |

## 2. Template Names and Structure

The template is the data structure that defines the object, and all of its extensions and subobjects. 

The salient feature of the [underlying Stix object model is the 21 different properties](https://docs.google.com/presentation/d/1hY0PK2XxlKhHr1MoLA_iufXW3MkgANpf/edit?usp=sharing&ouid=113752273524998502191&rtpof=true&sd=true), and the template leverages  all of them. The 21 Properties fall into two groups of properties:

- **Simple Properties:** string, integer, float, timestamp, boolean, binary, and hexadecimal

- **Composite Properties:** vocab, enum, sub-objects, extensions, foreign-keys, key-value store, and list of object types

The template leverages these 21 properties to describe all aspects of a Stix object at a high-level. 

### 2.1 Things not described by the Template

The template describes everything about an object, except for the following, where we fortunately have the existing content in the Dialect Data and StixORM repos to fill the gaps:

- **SRO Relations**: The objects may play source or target roles in one of the SRO types, and these relation constraints are described in the [dialect data repo.](https://github.com/os-threat/stix2-dialect-definitions/blob/main/summary/constraints.json)
- **Foreign-Key Constraints**: There are constraints on Stix object foreign keys, controlling which objects can play which foreign keys. These constraints are not described in the template, but are defined in the [dialect data repo](https://github.com/os-threat/stix2-dialect-definitions/blob/main/summary/connections.json)
- **TypeQL Role Names**: TypeQL structures are more verbose than JSON or Python classes, as role names are required for relations. The parent relation has  default names (e.g. "owner" and "pointed-to), but to specialise the relation it is necessary to define custom role names. We already have all of these names derived for the StixORM, based on the 4 main TypeQL composite object types [Foreign Keys](https://github.com/os-threat/Stix-ORM/blob/main/stixorm/module/definitions/stix21/mappings/relations_embedded.json), [Dictionaries](https://github.com/os-threat/Stix-ORM/blob/main/stixorm/module/definitions/stix21/mappings/relations_key_value.json), [List of Objects](https://github.com/os-threat/Stix-ORM/blob/main/stixorm/module/definitions/stix21/mappings/relations_list_of_objects.json), and [Extensions and Sub-Objects](https://github.com/os-threat/Stix-ORM/blob/main/stixorm/module/definitions/stix21/mappings/relations_extensions_and_objects.json)
- **Vocab and Enum**: The name of the vocab/enum is in the Template, and using a fixed transform it is possible to retrieve the terms and descriptions for each from the [vocab](https://github.com/os-threat/stix2-dialect-definitions/tree/main/summary/vocab) and [enum](https://github.com/os-threat/stix2-dialect-definitions/tree/main/summary/enum) directories in the Dialect Data repo. 

It seems easy to conceive of a User Interface based on the Templates, where one could create Custom Objects, by dragging and dropping Property Types,  specifying their  details, and slowly building up the Template object. One could specify Extensions, and even Sub Objects, and then save the Template to a file.

As shown above, the description in the template alone is insufficient, and more fields need to be added to the User Interface then are in the Template. These additional fields would capture information not in the Template, such as the SRO relations, Foreign-Key constraints, TypeQL role names and Vocab and Enum.

Additionally, one would want the ability to select an icon for the object, and icons for any form buttons used to expand custom extensions in the form. With all of those facilities then one could instantiate an object into the OSTriage system.

### 2.2 Template Structure

The Template is a dict-like structure with two key-vlue pairs:

- **"class_name"**: The value of this Field is a valid Stix object ClassName, which is unique for each object (but not unique for each icon).
- **"ClassName_template"**: The key must be equal to the Stix class name, with the suffix "_template" added to it, and it holds the  contents of the template. The value of this key is a dict-like structure with the following 6 keys:

 1. **"_type"**: A valid Stix type.
 2. **"base_required"**: Fixed properties of each of the Stix groups, SDO, SRO, SCO and Meta
 3. **"base_optional"**: Optional properties of each of the Stix groups, SDO, SRO, SCO and Meta
 4. **"object"**: Properties that describe the object, including both simple and composite properties. Some properties may be required to make the object.
 5. **"extensions"**: A dict of extensions that can be added to the object, using the Stix Type, each with its own set of properties.
 6. **"sub"**: A dict of sub-objects that can be added to the object, each with its own set of properties. The key is the Class Name of the sub-object, and it can only ever called by an **"EmbeddedObjectProperty"** used in the object or extensions part of a template.

 ![Fixed Template Structure](/img/image.png)

  The Template is the foundation object description, on which the other composite fields can be annotated (e.g. SRO Relations, Foreign Keys, TypeQL Role Names, Vocab and Enum). The Template can be used to generate the TypeQL schema, and the Python/Pydantic class for the object, as well as the JSON Form definition.

  ## 3. Data Form Type

  The Data Form is a dict-like structure with a single key and value.

  The key is (currently) equal to **the name of the Stix Type with a suffix "_form"**, and the value is a dict-like structure with 5 keys:

 1. **"base_required"**: Fixed properties of each of the Stix groups, SDO, SRO, SCO and Meta
 2. **"base_optional"**: Optional properties of each of the Stix groups, SDO, SRO, SCO and Meta
 3. **"object"**: Properties that describe the object, including both simple and composite properties. Some properties may be required to make the object.
 4. **"extensions"**: A dict of extensions that can be added to the object, using the Stix Type, each with its own set of properties.
 5. **"sub"**: A dict of sub-objects that can be added to the object, each with its own set of properties. The key is the Class Name of the sub-object, and it can only ever called by an **"EmbeddedObjectProperty"** used in the object or extensions part of a template.

 Importantly, it differs from the CMS Form model in that the sub-objects have been separated from the objects and extensions that would use them, This is critical for the Python object creation process, as the the sub-objects must be created first, then any extensions and finally the object, as they are nested.

 Separating the sub-objects from the object and extensions is the Primary purpose of the Tangular Transforms, which are used to convert the CMS Form into a Data Form, prior to processing by a StixORM block.

![The Data Form has five components](/img/image2.png)

More sophisticated forms have data through the *"extensions"* and *"sub"* sections, such as the identity form below.

![data forms can be more sophisticated](/img/image3.png)

## 4. API Form Structure

Typically with an object that includes Foreign Keys, one makes the objects in a sequence. Thus it is often desirable to feed in the objects, or lists of objects that are required to make the object. The API Form is used in Postman, Flow examples, or Brett Blocks to send a both form and any objects for foreign keys.

The API Form is a dict-like structure with multiple keys. The first is a Data Form, and then there are one or more Foreign Key Fields, each with a Typed Stix Object or List of Stix Objects that are required to extract the foreign keys for the field.

1. **"Stix Type"+"_form"**: The value of this Field is a valid Stix Data Form as described in Section 3 above.
2. **"Foreign_Key_Field_Name_1"**: A Typed Stix Object, or List of Stix Objects, that are required to extract the foreign keys for the field.
3. **"Foreign_Key_Field_Name_X"**: Inputs for Additional Foreign Keys


As an example, consider an email Message API Form as shown below, with the **"from_ref"** object, and the **"to_refs"** object list. If the field name ends with an **"refs"** then it is a Foreign Key to a list of objects, otherwise if it ends with a **"ref"** it is a Foreign Key to a single object.

![API Form Example](/img/image4.png)

## 5. JS Block Ports and Names

While the current Flow execution is asynchronous, and multiple inputs do not currently work, the blocks are designed to work in a synchronous mode, where blocks can be cascaded hierarchically, and the output of one block is the input to another block.

Thus, the Python block code and JS wrapper code both need to be designed to suit both the asynch and the future synch execution scenarios.

An example of one of the earlier synchronous blocks is shown below, where the block has multiple connected imports, both a form, an object to represent the from email, and a list to represent the to email addresses. All blocks have two outputs, the actual output and a raw payload output.

![Original Synchronous JS Block Example](/img/image5.png)

Just to reiterate, this synchronous mode does not currently work, but is necessary in the future to introduce simplified forms, where for example a user fills out a simplified Phishing Form, and the block then creates the Phishing Email object, and all of the related objects, such as the From Email Address, To Email Addresses, and any other Foreign Keys, and connects them into a sub-graph.

### 5.1 Adding the API Port

The initial release of the OS Threat app will focus on having individual forms for ecery object, and thus having a single API to make any Stix object is a good idea.

The JS Block design was altered to include an API port that could take an API form from Postman or other external users. This is shown in the image below.

![JS Block with API Port](/img/image6.png)

The API port can take an API Form, which is described above in Section 4, and the block will then extract the form and any objects, or object lists needed for foreign keys to make the Stix object. The block will then make the Stix object, and return it as the output of the block.

The Postman example is shown below, where the API Form is sent to the block, and the block returns the Stix object as the output.
![Postman Example with API Port](/img/image9.png)

### 5.2 Typed Port Nomenclature for JS Blocks

For the future, it will be important to establish a clear nomenclature for the typed ports in the JS Blocks. This will help to ensure consistency and clarity in the design and implementation of the blocks. Some key considerations for the typed port nomenclature include:

1. **Form Names**: Every block is associated with a specific form, and the port name is based on the Stix Type, with the type form in brackets.
**Port Name = "Stix-Type" + "(form)"**

   For example, the port name for an Email Message block would be "email-message(form)".

2. **Stix Objects**: When an existing Stix object is used as the input to a block, the port name should be the Stix Field Name, followed by braces to indicate an object.
**Port Name = "Stix-Field-Name" + "{}"**
   For example, the port name for an Email Address block would be "from-email{}".

3. **List of Stix Objects**: When a list of Stix objects is used as the input to a block, the port name should be the Stix Field Name, followed by braces, and surrounded by square brackets to indicate a list.
**Port Name = "[" + "Stix-Field-Name" + "{}" + "]"**

   For example, the port name for a list of Email Address blocks would be "[to-emails{}]".

By following these guidelines, we can create a nomenclature for typed ports, that can later on be enforced with strict port typing control (i.e. can only create a link if the export type of one block and the input type of the other block match).

### 5.3 Setting up JS Block Code for a New Block

The JS block code is set up by Max to take the port inputs, wait till all connected ports have delivered their data (runs synchronously when you have the Flow page open), but this waiting for all connected ports does not happen in API mode.

Make a new block, by dragging the block from the left-hand pallette, onto the canvas. Right-click on the block, and select "Edit Code". This will open the code editor, where you can edit the code for the block.

![Select Edit to open the JS Block Code Editor](/img/image7.png)

You only need fill out the details for four variables in the first 12 lines of the JS script, as it wil then work correctly by default. Do not change other stuff in the file, without first checking with Max, as it may break the block.

![Only change 4 variables in the first 12 lines of the JS script](/img/image8.png)

First, work out your Block unique name, and Block title. Then calculate how many ports are needed for your block, by adding together:

- the **"Stix Type_form"** port, which is always required
- the number of Stix field names ending in **"refs"** or **"ref"** in object, extensions or sub
- the **"api"** port, that encapsulates all of the above

Armed with these details, then the procedure for modifying the JS block code to suit this new data, is to change the following four variables in a single sequence and select the Submit button.

1. **exports.id**: The unique name of the block, how it is known in the Palette. Once this is set and Submit is pressed, a new block will apper in the Palette with this name. Make sure you set the other properties as well.

2. **exports.name**: The title of the block, which is shown in the Palette and on the front of the block when it is in the canvas. It is useful to start with the Group Name, such as SCO, SDO, SRO, or Meta, and then follow that with "Make" and the name of the object, such as "Make Email Address", "Make Email Message", "Make URL", etc. This means the ordering of the blocks in the palette will first be by group, rather than alphabetical by block name (inconvenient).

3. **exports.inputs**: A list of the dicts that define each input port in order. For each port, the **"id"** field is the name that will become the key in the json that holds the port data, and the name used in the Python block to extract that specific data block from the input json. The **"name"** field is the title that is visible when the block is on the canvas. This must be set using the scheme described in Section 5.2 above. The port type must be set to "form" for the form port, end in "{}" for a single Stix object, or be within "[]" for a list of Stix objects.

4. **exports.outputs**: Only change the Title of the output port on the block, by changing the name property (i.e. what is shown on the outside of the block). No other property should be changed. The name property must be changed to a value that reflects the outgoing type, using the scheme described in Section 5.2 above. The output port for StixORM blocks will always be a Stix object, so the type is always of the form **"stix-type{}"**.

Once the modifications are made, select the **"Submit"** button to save the changes. The block will then appear in the Palette, and can be dragged onto the canvas ready for the Python code to be entered.

An example of the first 12 lines of the JS code Block for the **SCO Make Email Message** block are shown below, including the 4 relevant variables.

```html
<script total>

	exports.id = 'Make_Email_Message';
	exports.name = 'SCO Make Email Message';
	exports.icon = 'fa fa-code';
	exports.group = '@StixORM';
	exports.author = 'StixORM.io';
	exports.version = '1';

	exports.config = { title: exports.name, version: exports.version, algorithm: '', algorithmrequirements: 'argparse stixorm', endpoint: 'http://127.0.0.1:8000/algorithm', jyputerid: "" };
	exports.inputs = [{ id: 'api', name: 'api' }, {id: 'email_msg_form', name: 'email-message(form)'}, {id: 'from_ref', name: 'from-email{}'}, {id: 'to_refs', name: '[to-emails{}]'}, {id: 'cc_refs', name: '[cc-emails{}]'}, {id: 'bcc_refs', name: '[bcc-emails{}]'}];
	exports.outputs = [{ id: 'output', name: 'email-message{}' }, { id: 'payload', name: 'Payload' }];

	...

	...

</script>
```

## 6. StixORM Python Block

### 6.1 Block Trigger Parameters

Every Python Block script, is given two paramters when it is triggered.

1. **"Inputfilename"**: The input data, which is a JSON that holds the data from the JS Block, including the form and any foreign key objects. The keys in this JSON will be the **"id"** fields for each port in the JS Block's **"exports.inputs"** list shown above.

2. **"Outputfilename"**: The output JSON to hold the results of the block processing.

### 6.2 StixORM Block Processing Objective

The objective of the Python Block processing is the same for every StixORM block. Import a JSON file, including a form, plus potentially additional objects and/or lists of objects, and then produce a Stix object, and save it in JSON to the output filename.

### 6.3 StixORM Python Script Structure

There are only two functions in each StixORM Python Block script, unless a timestamp property is used, in which case there is a third function to convert the timestamp to a datetime object. 

Every SDO, SRO and some SCO objects will have a timestamp property, so this is a common function. It is only necessary while we are using TypeDB v2.x, or ORM v1, as the ORM v2 will not need the timestamp conversion.

All StiORM scripts work in the exact same way, only the classes and keys change. 

### 6.4 The `main(inputfile, outputfile)` function

This is the main function that is called when the block is triggered. It takes two parameters, the input filename and the output filename. It:

- reads the input JSON file,
- extracts the form and any foreign key objects, 
- runs the **"make_stix_type"** function and receives the Stix JSON object
- takes the Stix JSON object, puts it in a list and writes the list to the output file.

As a simple example with only one foreign key, the code for the **"Make Email Address"** block is shown below, while the more complex **"Make Email Message"** block with many foreign keysis shown in the [Make Email Message Block Code](https://github.com/typerefinery-ai/brett_blocks/blob/main/Block_Families/StixORM/SCO/Email_Message/make_email_msg.py#L150)

```python
def main(inputfile, outputfile):
    belongs_to = None
    if os.path.exists(inputfile):
        with open(inputfile, "r") as script_input:
            input_data = json.load(script_input)

    if "email_addr_form" in input_data:
        email_addr_form = input_data["email_addr_form"]
        if "user-account" in input_data:
            belongs_to = input_data["user-account"]
    elif "api" in input_data:
        api_input = input_data["api"]
        email_addr_form = api_input["email_addr_form"]
        if "user-account" in api_input:
            belongs_to = api_input["user-account"]

    # setup logger for execution
    stix_dict = make_email_addr(email_addr_form, belongs_to)
    results = {}
    results["email-addr"] = []
    results["email-addr"].append(json.loads(stix_dict))
    with open(outputfile, "w") as outfile:
        json.dump(json.loads(stix_dict), outfile)
```

There are always two paths to the input process. Either the form and foreign keys are directly connected, or they are aggregated together into an API form and sent through that port. These results then go to the **"make_stix_type"** function, which is the second function in the script.

### 6.5 The `make_stix_type(form, foreign_key_1, ...)` function

This the function that makes the Stix object from the input, and returns it as a JSON string. The order of the processing depends on how many classes are involved 

#### 6.5.1 The Simplest Case

The simplest example is one based solely on the Main StixORM class such as the **"Make Email Address"** block, which we know has no extensions or sub-objects, and thereby uses only the **EmailAddress** class only.

In this case, the setup is trivial, as the contents are built in order and the base required are not needed for SCO objects as the class makes them automatically

```python
def make_email_addr(email_addr_form, usr_account=None):
    # 1. Extract the components of the object
    required = email_addr_form["base_required"]
    optional = email_addr_form["base_optional"]
    main = email_addr_form["object"]
    extensions = email_addr_form["extensions"]
    sub = email_addr_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    for k,v in main.items():
        contents[k] = v
    for k,v in optional.items():
        contents[k] = v
    for k,v in extensions.items():
        contents["extensions"] = {k, v}
    for k,v in sub.items():
        pass

    for (k,v) in contents.items():
        if v == "":
            continue
        elif v == []:
            continue
        elif v == None:
            continue
        else:
            empties_removed[k] = v

    if usr_account:
        empties_removed["belongs_to_ref"] = usr_account["id"]
        # object needs to be created
        stix_dict = EmailAddress(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_dict = EmailAddress(**empties_removed)

    return stix_dict.serialize()
```

#### 6.5.2 A More Complex Case

The more complex case requires  multiple sub-objects with the main object, and so multiple classes are required, which must be made in a sequence of "sub" objects first, then "extensions" objects if required before the main object is made.

As an example, the Make Identity block includes an extension, with 3 lists of objects, where the objects are both sub-objects and include foreign keys. The code for this block is shown below, and it is more complex than the previous example. Consider it with its [template](https://github.com/typerefinery-ai/brett_blocks/blob/main/Block_Families/StixORM/SDO/Identity/Identity_template.json) to understand the key references.

````python
def make_identity(identity_form, email_addr=None, user_account=None):
    print(f"Step 1 >>")
    # 1. Extract the components of the object
    required = identity_form["base_required"]
    optional = identity_form["base_optional"]
    main = identity_form["object"]
    extensions = identity_form["extensions"]
    sub = identity_form["sub"]
    contents = {}
    empties_removed = {}
    # 2. Setup Object Params first
    print(f"Step 2 >>")
    for k, v in main.items():
        contents[k] = v
    for k, v in optional.items():
        contents[k] = v
    for k,v in sub.items():
        if k == "contact_numbers":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                for val in v:
                    stix_list.append(ContactNumber(**val))
                identity_contact["contact_numbers"] = stix_list
        if k == "email_addresses":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                print(f"#>> v {v}")
                print(f"#>> email_addrs {email_addr}")
                for i, val in enumerate(v):
                    print(f"#>> v {v}")
                    if email_addr:
                        val["email_address_ref"] = email_addr["id"]
                    stix_list.append(EmailContact(**val))
                identity_contact["email_addresses"] = stix_list
        if k == "social_media_accounts":
            if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
                identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
                stix_list = []
                for i, val in enumerate(v):
                    if user_account:
                        val["user_account_ref"] = user_account["id"]
                    stix_list.append(SocialMediaContact(**val))
                identity_contact["social_media_accounts"] = stix_list

    if extensions != {}:
        if "extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498" in extensions:
            identity_contact = extensions["extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498"]
            identity_ext = IdentityContact(**identity_contact)
            contents["extensions"] = {"extension-definition--66e2492a-bbd3-4be6-88f5-cc91a017a498":identity_ext}

    for (k,v) in contents.items():
        if v == "":
            continue
        elif v == []:
            continue
        elif v == None:
            continue
        else:
            empties_removed[k] = v

    if "modified" in required and required["modified"] == "":
        # object needs to be created
        stix_obj = Identity(**empties_removed)

    else:
        # object needs to be updated, but we can't
        #  update properly yet, so recreate instead
        stix_obj = Identity(**empties_removed)

    stix_dict = json.loads(stix_obj.serialize())
    print(f"Step 3 >>")
    time_list = ["created", "modified"]
    for tim in time_list:
        if tim in stix_dict:
            temp_string = convert_dt(stix_dict[tim])
            stix_dict[tim] = temp_string

    return stix_dict
````



### 6.6 The `convert_dt(timestamp)` function

This is important while we are using ORM v1 and TypeDB v2.x, as the timestamp is a string, and needs to be converted to a datetime object, only storing millisecond resolution. It is pointless trying to generate this and we should just copy and paste it manually into each file, as it is the same for every block with a timestamp.

## 7. The CMS Form Specification

There are two CMS StixORM forms for each object, one for Create, and one for Update. The Body of each CMS StixORM Form is split into 3 sections:

- Header
- Main, and
- Footer

### 7.1 Form Taxonomy

Form names and their paths are carefully controlled, so that the correct form can be shown in the UI, simply by providing 3 pieces of data from the wrapper to each Stix object in the visualization. Data objects in the visualization do not know their form url, and instead just contain these 3 parameters:

- **"object_family"**: The Stix dialect family, such as stix, attack, oca, etc.
- **"object_group"**: The Stix group, either SDO, SRO, SCO or Meta
- **"object_form"**: The Class Name of the Stix object

The original data objects is contained in the wrappers **"original"** field, while the wrapper contains the 3 parameters above, plus details for tooltips and icons, as shown below.

```json
{
    "id": "email-addr--eb38d07e-6ba8-56c1-b107-d4db4aacf212",
    "type": "email-addr",
    "original": {
        "type": "email-addr",
        "spec_version": "2.1",
        "id": "email-addr--eb38d07e-6ba8-56c1-b107-d4db4aacf212",
        "value": "evil@northkorea.nk",
        "display_name": "Bad Man"
    },
    "icon": "email-addr",
    "name": "Email Address",
    "heading": "Email Address -> Bad Man",
    "description": "<br>Value -> evil@northkorea.nk",
    "object_form": "email-addr",
    "object_group": "sco-forms",
    "object_family": "stix-forms"
}
```

### 7.2 Form Header

The Form header is inherited and includes a container with two columns. Inside one column is a container with a text field, as the Form Title. Inside the other columns is a container with the Create and Cancel buttons.

In the case of objects which should not be updated, such as SCO's, then the Create button is deleted, and only a Cancel button exists. When a "Cancel" button is pressed, then the default form is shown.

An example of a form header is shown below

![The Form Header has two containers](/img/image10.png)

### 7.3 Form Main

The main part of the form is filled with a Form component, inside of which is a Container and 4 Composite Fields. The Container holds a 2-column container and a series of Buttons to open optional templates in the form.

The four Composite Fields arenamed as follows:

1. **Base Required**: This is a Composite Field that holds the required properties of the Stix object, such as the id, type, spec_version, created_by_ref, created, modified, and description. These are required for all Stix objects.
2. **Base Optional**: This is a Composite Field that holds the optional properties of the Stix object, such as the labels, external_references, and confidence. These are optional for all Stix objects.
3. **Object**: This is a Composite Field that holds the properties of the Stix  object, such as the value, display_name, and any other properties that are specific to the Stix object. These are required for all Stix objects.
4. **Extensions**: This is a Composite Field that holds the extensions of the Stix object, which are additional properties that can be added to the object.

Note that the form does not include a **"sub"** section as these are embedded in fields that contain an **"EmbeddedObjectProperty"**.These 4 sections can be seen in the example below.

![The Form component in the Main part of the Form Body](/img/image11.png)