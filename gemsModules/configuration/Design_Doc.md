# Design Documentation for the Configuration gemsModule

The main work of this module is the production, management, and parsing of the instance configuration file.

The file is called `instance_config.json` by default, but other names can be specified using the environment
variable `GEMS_INSTANCE_CONFIG`.

This Module has no child Modules and no parent Module. It does not inherit from Common or from any other
GEMS modules. 

The instance configuration is often called 'instance config' or simply 'IC'.

---

## Important background: 

GEMS can provide communication between computers. This Module manages the database of information regarding
available communications. See `$GEMSHOME/docs/GEMS_to_GEMS_Communication.md` for further information.

---

## Purpose and Goals

The Configuration module provides a way to generate and query a database of available GEMS instances,
including the local GEMS. This database, called an _Instance Configuration (IC)_, contains information 
regarding the capabilities of the available GEMS instances and how they can be contacted.

The IC also contains other locally-relevant information, for example the locations of input files and the 
places to which output files should be written. 

---

## Security, Access and Connectivity

Allowing communication between GEMS instances increases the attack surface of computers running GEMS. 
The following mitigations are required. 

_Scope of the Configuration Module_

The sole duty of the Configuration Module is to manage the IC and report about its contents.

It will only interact directly with users via one or more scripts in `GEMSHOME/bin`. Only via these scripts
can the contents of the IC be changed.

When interacting with any other part of GEMS, this module will report data only. It will not make changes to
the IC or its data on behalf of any other part of GEMS.

_Interaction with other Modules_

The Network Connections Module may query this module for information regarding the IC.

_Interaction with other Entities_

Only the Batch Compute, Delegator, and Project Entities will directly access the Configuration Entity. Their
access will be for retrieval of information only.

_Interaction with code in the deprecated folder_

The `gemsModules/deprecated/instance_config` folder should no longer be used by any code. The few existing
uses of the instance config should be refactored once the new Pydantic-based version is available. When 
finished, the deprecated version should not be used at all. It might be kept for a while as a reference in
case code (possibly external to GEMS) is found to use it or communicate in its terms.

---

## Supported Entities

This section refers to the Entities that are mentioned in the IC.

The information assigned to them falls into roughly two categories:

1. Connection information related to any remote hosts that are available to perform the service.
2. Information telling the local host, which might or might not be able to perform a given service, where
   to place input and where to look for output.
   - This information is needed even if the local host cannot support an Entity.
   - Currently, the inputs and outputs are directory paths.
     - Eventually, they could be any form of storage, e.g., an object store.
     - Because many of our files are very large, and because I/O might require several or more files, we 
       avoid passing data stored in files via the JSON Objects.
     - Once storage options expand, the structure of this information should resemble (perhaps inherit from)
       the Resource object defined in `gemsmodules/common/main_api_resources.py`.

---

## Computing Resources

These are included in:
- The `BatchComputingResources` object in `main_api.py`
  - Reports generic computing resources per partition (queue).
  - Scheduler-specific language should be avoided here.
- Various objects in: `resource_management_api.py`
  - These objects contain information specific to a scheduler/resource-manager that cannot be known simply 
    by knowing how to use the particular scheduler/manager.
    - Example: Slurm might use --gres for tracking certain resources even if there are built-in arguments
      that can also be used, such as --gpus. Because the choice is made when the scheduler is configured,
      the Batch Compute Entity cannot know this without being told.
  - All logic for realistically knowable options should reside in Batch Compute.
  - Logic related to using resource specific information should also reside in Batch Compute.

---

## Provided Services

These are the services available via user-facing scripts in the bin directory. The Delegator and Project
Entities will be able to query any part of the IC, and some queries might happen via these services. Some
of these services will invoke Delegator (which might trigger Project).

Although it doesn't inherit from Common, it provides services with standard names where appropriate.

The Services are:
- Validate
- Evaluate
- Report Host Capabilities
- Check Remote Host Connectivity
- Confirm Remote Host Capabilities
- Generate New Configuration
- Export Local Host
- Import Remote Host
- Status

Allowed Entities and Modules can connect to any of the methods in InstanceConfig.

### Validate

Report whether the IC is present and readable by the module.

### Evaluate

Provide a summary:
- Capabilities of the local host.
- Capabilities supported elsewhere.
- List of external hosts defined.

Implies the Validate Service.

### Report Host Capabilities

Return information about a one or more hosts. 

If a requested host is not found in the IC, return a standard error.

### Check Remote Host Connectivity

Check connectivity for one or more remote hosts.

Connectivity will be confirmed using Delegator's Marco Service via gRPC/JSON.

Please see below for information on interacting with Delegator.

### Confirm Remote Host Capabilities

Query one or more remote hosts to confirm (or not) that information in the local IC.

Host Capabilities will be confirmed using Delegator's Check Configuration Service via gRPC/JSON.

Please see below for information on interacting with Delegator.

### Generate New Configuration

Available only via a script in `$GEMSHOME/bin`.

Writes a new IC from user input.

Input options should include:
- Interactive Q/A-style TUI entry.
- Import of dictionary-style data in a file.
- Minified or unminified (default)
- Supply the name for the output IC if it is not `$GEMSHOME/instance_config.json`. 

Output is JSON. It is up to the caller script to put the JSON somewhere.

### Export Local Host

Generate JSON describing the local host. 

Optional Input:
- Name and address for remote contact (remote equivalent of 'localhost' and '127.0.0.1').
- Port assigned to the gRPC serving the GEMS instance.
- Minified or unminified (default)

Output is JSON. It is up to the caller script to put the JSON somewhere.

### Import Remote Host

Available only via a script in `$GEMSHOME/bin`.

Add information from JSON supplied by a remote host to the current IC.

Input:
- Name of a file containing the export from the remote host.

Optional Input:
- Supply the name for the output IC if it is not `$GEMSHOME/instance_config.json`. 

### Status

Report the results of the following
- Evaluate
- Report Host Capabilities
- Confirm Remote Host Capabilities (for all remote hosts)

---

## Mappings from old to new versions

See also comments in the current versions of the code.

### Simple word-change mappings

| Old                          | New                        |
|------------------------------|----------------------------|
| SupportedExecutionContexts   | SupportedServices          |
| host                         | address                    |

### Complex word-change mappings
Comments in the code should also help.

#### Old: `slurmport` ->  New: `port`

The use of gRPC/SLURM, 'slurmreceive' and any associated, un-deprecated, code should be changed to use
gRPC/JSON instead. The code in gRPC/SLURM will still be used until deprecated/sequence is updated. The 
code relevant to the latter is in `deprecated/batchcompute/slurm`.

#### Old: `sbatch_arguments` -> new  `scheduler` + `resource_specific_information`

The old key, `sbatch_arguments` was too specific. This change allows the support of multiple schedulers
and no longer limits the information to job submission arguments.

---

## Script

Although other scripts in `$GEMSHOME/bin` might access it, only a single script is needed for direct access.

The script should be called `instance_config.py`. It should work with all/most variants of Python3. It 
should replace `setup-instance.py`. In the latter, a 'preconfig' is the equivalent of a remote host config.

### Capabilities:

- Provide all Services listed above.
- Command-line arguments for:
  - Alternate file name for read/write of IC.
  - Write minified JSON (unminified is default).
- Q/A-Style TUI for data entry for new IC

See below for command-line options and details regarding Q/A for the TUI.

#### For generating a new IC

The script should accept direct user inputs when configuring a new IC. The user inputs can be in the form of
input files or answers to TUI questions. The TUI should accept input files in normal IC JSON format.

#### For importing remote data to an existing IC

The script should accept only input files in the JSON format.

#### Direct modification via the TUI

For now, this is not supported. The user can, of course, remake it from scratch or edit the file manually.

## Coding Constraints

The script should not attempt to follow the normal Entity format and it should not import from Common.

The Service API in Delegator can include the InstanceConfig API.

IC manipulations by the script should be capabilities separate from the methods in InstanceConfig and should
be written into another file, `gemsModules/configuration/control_script.py`. 

The purpose here is to discourage other Entities and Modules from attempting to manipulate the IC. Once the 
file is created using the script, use of the data should be read-only. 

Once created, where an OS supports it, the file should be marked read-only. The IC, and a command-line user,
can change the write access, but casual modification should be discouraged.

--- 

## Entity Access to the IC

The function `_load_instance_config` should be loadable only once during a session. Once it is loaded, it should
become read-only. Entities should only access the IC data via this procedure.

--- 

## Interactions with Delegator via gRPC/JSON

Generally, interacting with Delegator involves sending a JSON string to Delegator's `receive` feature.
The script `$GEMSHOME/bin/delegate` provides an example of normal use by users and the website.

In this situation, it should be mediated by `json_grpc_submit` in `gemsModules/networkconnections/grpc.py`.

To use that function as defined, the 'host' is the 'address'.  The jsonObjectString should conform to the 
API as defined in `gemsModules/delegator/main_api.py`.

Sample JSON can be found in `gemsModules/delegator/tests/inputs/` for Delegator-provided services.

### Brief contextual information about Delegator

Submission should occur viat gRPC as described in the statements above. This section provides a brief 
description of the role of Delegator.

Interaction with any gemsModule that acts as an Entity generally occurs via Delegator. Delegator determines
which Entity should provide a given service, leaving the Entity to become concerned only with its duties.
Because of this role, it is also appropriate for Delegator to find the correct execution host.

See `gemsModules/deprecated/delegator/test_in` for samples of JSON objects to be delegated to other Entities.
Note that not all of the test inputs will work. There is much cleaning to do.

Delegation within the code, not invoving gRPC, generally proceeds something like:

```
from gemsModules.delegator.receive import receive
responseObjectString=receive(jsonObjectString)
sys.stdout.write(responseObjectString)
```

### Marco

Based on the game 'Marco Polo', this is the GEMS equivalent of 'ping'. We use 'Marco Polo' because the
service occurs in a cloud and need not be tied to a specific host as is 'ping'. In practice, the current
code acts like 'ping', but the idea is to, one day, call to a host of machines 'Marco' and get replies
from all that are available to provide services.

Simplest input and output: File `gemsModules/delegator/tests/inputs/default.json`
The Marco service is the default service for Delegator, so a tiny JSON will work.

However, as a kindness to users and coders, explicit request is probably better. So, instead use this:
File `gemsModules/delegator/tests/inputs/marco_explicit.json`

The response will look something like:
File `$GEMSHOME/tests/correct_outputs/024.marco_delegator_explicit_output.json`
The difference will be that placeholders like 'theUUID' will have real values.

The main section of interest in the response is:
```
    "responses": {
      "Marco": {
        "type": "Marco",
        "myUuid": "theUUID",
        "outputs": {
          "message": "Polo"
        },
        "notices": {}
      }
    },
```

If it helps, see also File `$GEMSHOME/tests/024.test-disabled.Marco.sh`
The test works, but only in some circumstances.

There are Easter Egg inputs for Marco. They were written to help explain parts of the new architecture. They
can be ignored for this.

### Confirm Remote Host Capabilities

This contract needs to be written. It will use the JSON API as in Marco.

Doing this will require:

1. Generating an API similar to Marco but with these changes:
   - Service Name:  ConfirmRemoteHostCapabilities 
   - Required Input: Name of the host or address/port if name is not unique (should be for now).
   - Output: An export of the localhost capabilities of the queried host.
   - Validation: the localhost capabilities of the queried host should match those in the local IC, except
     for obvious differences such as the queried host not being declared localhost in the local IC.

For now, placeholder methods will be ok.

--- 

## TUI and Q/A Process

The TUI should be called `instance_config` and be located in `GEMSHOME/bin`.

It should have these options:

    # generation of a new IC
    generate --from-file <filename>
    generate --use-tui
    # export part or all of an IC
    export   localhost [--to-file <filename>]
    export   host="name" [--to-file <filename>]
    # import a remote host - re-generates the IC with a new timestamp
    import   --from-file <filename> 

All the above can be provided with a help statement if 'help' occurs at the end or in the place of 
a filename or other required input.

Otherwise:
    '--from-file' and '--to-file' must have a file name as an argument
    if an output file is not specified, output goes to stdout
    input files must be specified (no stdin)

### Q/A Process

The Q/A Process should follow the structure of the InstanceConfig object.

The expected text and questions follow. 

All values should be interpreted as strings (extra security due to Pydantic V1).

User replies in angle brackets are required; in square brackets, optional.

In questions, information in curly braces is supplied by the TUI script. 
Entries in square brackets provide information about default values, if any.

Use the descriptions for each field (see code) for hints to give the user.

Empty square defaults should become "" or None as appropriate.

If any line is longer than 110 characters, split the line.

Please be able to print a summary of this questionnaire if the command line is:
    `instance_config generate --use-tui help`

```
Beginning a new Instance Configuration file on {date-time}.

At any prompt, enter '?' for help.

------------------------------------------
Basic Setup
------------------------------------------

Instance configuration file name ["instance_config.json"] : [new-name]

First we must gather some local data storage information

Enter the list of Entities that can be delegated from the Local Host (space separated)
  Note that this is NOT the list of Entities that can run on this host. 
  It is the list of all entities considered, including those sent to remote hosts.
  [{SupportedEntities.values()}] : [space separated values]
  {if ? then supply the value and description for each enum and prompt again} 

For each delegatable Entity, please provide a local filesystem path
  {if ? at any point, then supply the field description and prompt again}
  {SupportedEntity entered} [] : [path]
  {...repeat as needed...}

For each delegatable Entity, please provide a local secure inputs path 
  {if ? at any point, then supply the field description and prompt again}
  {SupportedEntity entered} [] : [path]
  {...repeat as needed...}


------------------------------------------
Local Host Setup

Host information for the local host must be given.
    You will be prompted for information on other hosts later in this script.
    Other hosts can be imported after this script is complete.
-----------------------------------------

{the script should supply "true" to the is_localhost field}


Please enter the name by which this host is known ["Glycon"] : [name]
{if ? show the description}

Please enter the host address. 
If this host is to be contacted by other hosts, enter a remote address,
otherwise 'localhost' is sufficient ["localhost"] : [address]
{if ? show the description}

Please enter the port address if this host is to be contacted by other hosts [] : [port]
{if ? show the description}

Please enter the list of execution environments supported by this host ["Standalone"] : [env]
  Notes:
        If 'Batch' is specified, a scheduler should be entered below.
        If 'Website' is specified, a website environment should be entered below.
  {if ? show ExecutionEnvironments.values() and their descriptions} 

If this host serves a website, please enter the website environment that it will serve 
  [DevEnv] : [environment]
  {if ? show WebsiteEnvironments.values() and their descriptions} 

Enter the list of Entities that can be Served from the Local Host (space separated)
  Note that this IS the list of Entities that can run on this host. 
  Depending on setup, these entities might be delegated to this host.
  [SupportedEntities.values()] : [space separated values]
  {if ? then supply the value and description for each enum and prompt again} 

If this host uses a resource scheduler, please give the type [None] 
  Note that the only possible options right now are "Slurm" and "None" : [scheduler]
  {if ? show the description}

{Show the following if the scheduer is not None}
For the resource, please fill in the following information.
If you are unsure of the answers, give a dummy answer and contact the staff for the resource.
{show the fields, defaults and descriptions in the BatchComputingResources class,
asking for answers similar to before}

{Show the following if the scheduer is not None}
For the resource, please fill in the following information.
If you are unsure of the answers, give a dummy answer and contact the staff for the resource.
{show the fields, defaults and descriptions in the relevant resource specific information class,
asking for answers similar to before}

------------------------------------------
Remote Host Setup

The best method for doing this is to get the remote host 
to export its instance_config and then import it here.
But, you can enter the information by hand if you want.
-----------------------------------------

Do you want to enter remote host information? [No] : [answer]
{
if 'yes'
Go through the host setup like above but for the remote host.
Change text to disallow using 'localhost'.
repeat the entire process until the reply is 'no'.
}

```

