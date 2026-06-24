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

## Available Services

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
  - Read and write a simplified human-friendly format for the data (see below).
    - For managing a proper IC file, this option is not avaialable.

### Friendly format:
The specific format is irrelevant. A well-known format, e.g. Markdown, is fine. It needs to be easy to 
parse in Python (and ideally in BASH) as well as easy to read and write by humans. It should be able to 
represent all of the IC or the specific parts provided in the services.

--- 

## Interactions with Delegator

Generally, interacting with Delegator involves sending a JSON string to Delegator's `receive` feature.
The script `$GEMSHOME/bin/delegate` provides an example of normal use by users and the website.

Delegation within the code generally proceeds something like:

```
from gemsModules.delegator.receive import receive
responseObjectString=receive(jsonObjectString)
sys.stdout.write(responseObjectString)
```

The jsonObjectString should conform to the API as defined in `gemsModules/delegator/main_api.py`.

Samples can be found in `gemsModules/delegator/tests/inputs/` for Delegator-provided services and in
`gemsModules/deprecated/delegator/test_in` for samples of JSON objects to be delegated to other Entities.
Note that not all of the test inputs will work. There is much cleaning to do.

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

