# Conventions and Normal Practices for gemsModules

If a use case is not addressed here, use a convention from elsewhere in the codebase or something 
widely used.

Not all of the conventions from the codebase are listed here. Adding them to this document is encouraged.

---

## Services

Generally, there should be at least three services: Validate, Evaluate and Status. There can be as many other
services as needed.

Generally, the minimal three are defined as follows:

- Validate:
  - Returns information about the form and format of the request. 
  - It makes no judgments about the appropriateness of the form of any inputs. Its concern is that all the needed
    inputs are contained in the request.
    - Example: If a file is part of the inputs, Validate will:
      - Ensure that a file is included in the inputs.
      - Possibly ensure that the file exists (if that applies to the Entity).
      - Not check that the contents of the file for any characteristics.
    - Example: If a carbohydrate sequence is part of the inputs, Validate will:
      - Check that the sequence passes the formatting requirements for a sequence.
      - Not check that the sequence refers to a carbohydrate that is supported by the Entity.
    - That is, it merely checks that the request is complete and correct.
  - Should not depend on any other Services and should not imply any other Services (see Implied Services).
- Evaluate:
  - Examines the inputs to determine what actions can be performed with those inputs.
  - Considering our 'file.txt' from above, Evaluate will determine what can be done with the file.
    - Example: If the Entity requires a carbohydrate sequence, Evaluate will:
      - Check that all the components of the string are supported by the builder. 
      - Determine the conformational possibilities of the sequence.
      - Report the results to the user.
  - Depends on Validte.
- Status:
  - Given sufficent project information to locate the expected output, Status will:
    - Inspect the expected location of the output.
    - If the location is accessible, it will provide Service-specific information. 
      - Examples might include:
        - Estimated time to completion of a partially-finished project.
        - Reports of error messages.
  - Note that Status does not return, investigate or analyze output. It merely reports status.

### Implied Services

Services can be implied in two ways:

1. They can be dependencies of other Services. 
   - If Service B needs Service A to have run first, then Service A is an Implied Service for Service B.
2. They can be inferred from certain user inputs. This is a convenience feature.
   - Example from the Sequence Entity:
     - Assume that the json input contains only the following:
```
{
    "entity": {
        "type": "Sequence",
        "inputs":
            {
                "sequence": {
                    "payload": "DManpa1-OH"
                }
    }
}
```
    - In this case, despite a Service not being explicitly requested, these inputs are taken to imply that the 
      user wants a predicted 3D structure of alpha-D-mannopyranose.
     

---

## Imports

Minimize the number of imports in a given workflow to greatly reduce the possibility of head-scratcher bugs.

Doing that also makes the code faster.

### Leave `__init__.py` empty.

Keep all imports purposeful, local, and targeted to the need. Because each gemsModule is its own 'package',
and because the packages interact, use of `__init__.py` obfuscates the code more than simplifies it.

### Use Full Paths

Don't use relative paths (that start with dots). As with the use of `__init__.py`, relative imports tend to 
obfuscate more than simplify. This is especially so because the gemsModules refer to each other, and sometimes 
to deprecated code, and package components share names. Namespacing is important, especially when debugging.

Be verbose and unambiguous.

### Place imports as close to the imported code as possible. 

Top-level (file-level) imports should be reserved for:

- File-level imports, e.g., logging utilities.
- Requirements for defining classes or definitions, e.g., `class MyChildClass(ParentClass):`. 
  In the latter, it is appropriate to import ParentClass at the file-level.

It is also ok to use file-level imports for:

- Imports that are used in multiple places by many defs/classes.
- Especially lower-level imports like 'os'.

... but avoid doing that even then. 

Regarding lower-level imports, see also Syntactic Sugar, below.

Examples of proper uses:

```
## This import must be file-level because it is needed for inheritance at the file level
from gemsModules.common.main_api import Common_API  

class myAPI(Common_API):
    ...  
    def check_directories():
        ## This import is only needed here, so import it here rather than at the top
        from gemsModules.systemoperations.filesystem_ops import check_make_directory directory_is_writable
        ...
```

---

## Security Concerns

Because scientific software is very finicky about inputs, we have some built-in protection from injection
attacks, but, of course, we do not assume this will always protect us.

### General coding principles

The main coding principle to adopt is:

- Always perform actions on behalf of the inputs.
- Never use the inputs themselves as instructions to be executed directly by the code.

You will find presumably useless information like this:

```
REGISTRY = {
    "MDaaS": ModuleData('gemsModules.mmservice.mdaas.receive', 'receive'),
    "MmService": ModuleData('gemsModules.mmservice.receive', 'receive'),
    ...
}
```

This has three purposes:

1. When a user requests an entity, for example "MDaaS", the code does not use that as the directive for
   finding the appropriate module. Instead, the location of the module is always defined by the code.
2. This enables flexibility. If a specific situation requires a different MDaaS module, possibly due to 
   a need for backwards-compatibility, the user never needs to worry about that.
3. Using the registry for importing later (rather than providing a link to a module), means that modules
   are only loaded when they are needed.

It is point 1 that provides the coding principle above.

### The JSON API

At the moment, GEMS is designed to Python 3.9.17 and Pydantic 1.10.2. These are old and are not as 
security-aware as more modern implementations. 

We do want to upgrade, and will do so ASAP. It will be a complex task, especially because there are
significant differences between Pydantic v1 and v2.

In the meantime, these rules should be followed:

- All simple types must be `str`. Do not use `int`, `bool`, etc.
- Complex types, such as Dict or a reference to another Pydanti class, are allowed.

There are places where a stray `bool`, etc., snuck in. Please do not follow that precedent.

Once we have upgraded the codebase, this requirement will be revisited and possibly revised.

---

## Variables Related To I/O

### Variables that are part of the Python code

Conventions for variables that inhabit the client-facing API or that inhabit the scientific-software-facing Tasks.

- Client-Facing API Variables: snake case, for example: `project_dir`.
- Scientific-Software-Facing Task Variables (inlcuding APIs used only in Tasks): camel case, for example: `projectDir`.
- Prefer long-form to short-form

Doing this makes it easier for coders to identify the expected scope of a specific variable. 
This ability is also valuable in finding workflow-related bugs.

Another important benefit is to help communicate variable type. For example, in the API, `project_dir` can only be
a string: JSON does not allow the Python notion of 'Path'. If `project_dir` is only used in relation to the API,
then a coder can be sure that it is always a string. Similarly, a coder knows that `projectDir` is used by a Task.
Because the Tasks exist for the purpose of interfacing other software, the coder knows that it might be of whatever 
variable type is convenient to the particular Task.

### Variables that are not part of the Python code

This section has in mind situations like command-line arguments and SBATCH directives.

- Prefer the long form to the short form where possible

Example:

In arguments given to Slurm on the command line or as #SBATCH directives in a file, these are equivalent:

```
-D <working_directory>
--chidr <working_directory>
```

To make these purpose of these as unambiguous as possible, always prefer the longer `--chdir` variant.

---

## Syntactic Sugar

There is some built-in sugar. Where it exists, please use it. Feel free to add your own.

Currently, most of it exists in `gemsModules/systemoperations` and `gemsModules/common`. 

### Rationales

#### Readability

The most obvious rationale is to make code more readable, _particularly to folks unfamiliar with Python_.

We need non-coders to understand the code because they need to be able to inspect the scientific methods.

Example 1:

_More readable by non-Python-coders:_

```
from gemsModules.systemoperations.filesystem_ops import directory_exists

if directory_exists(directory_path):
```

_Less readable by non-Python-coders:_

```
import os

if os.path.isdir(directory_path):
```

Example 2:

Here is the code for `gemsModules.systemoperations.filesystem_ops.directory_is_writable`:

```
def directory_is_writable(directory_path, make_if_needed:bool = False):
    """Checks if a directory is writable by attempting to create a temporary file."""
    try:
        # If directory does not exist, and if asked to do so, try to make the directory:
        if make_if_needed:
            check_make_directory(directory_path)
        # Create a temporary file in the directory
        with tempfile.TemporaryFile(dir=directory_path) as temp_file:
            # Try writing to the file
            temp_file.write(b"test write")
        return True
    except PermissionError:
        return False
    except FileNotFoundError:
        # Parent directory does not exist
        return False
    except OSError as e:
        # Catch other potential OS errors (e.g., full disk, specific Windows issues)
        print(f"An OS error occurred: {e}")
        return False
```

The sugar (`directory_is_writable`) is much better than writing that code all over the place.

#### Searching and Maintenance

It is also useful to have the underlying code defined once and then referenced using a locally-sweet variable.

This helps for these reasons:

- There are many ways to do the same thing in Python. This assures one easily-searched method.
- The import statement informs the reader/coder where the sugar's code can be found.
- We often need only a few behaviors from a library (e.g., os.path) rather than all the possible options.
- If a sugared method must be altered, it needs only be altered in a single location.
- It is easy to find all instances where the sugar is used.

_Use case example:_

During an upgrade of the Python version used by the code, the default behavior of a file operation changed. 
This operation happened to be important and widely-used. In places where sugar had been used, the update
was simple: update a single defined function. But, the other uses had to be found one at a time by looking 
at every import of the relevant Python library.

---

## BASH

This is only about BASH. It might not apply to other shells.

### Sourcing: use 'source' or use a dot?

These two operations are identical in BASH:

```
source somefile.bash
. somefile.bash
```

#### A general use convention

- Use `source` when the information in `somefile.bash` is to be used by the code that follows it in the calling script.
  This is mainly used when `somefile.bash` contains definitions or configurations.
- Use a dot when the code in `somefile.bash` should be treated as code inserted into the calling script - that is, 
  the code in `somefile.bash` is likely to depend on the code that preceded it in the calling script.

That is:

```
source file_containing_definitions.bash

some_lines_of_code # do things that use the info in the sourced file.

. file_using_results_from_some_lines_of_code.bash
```

_Use case example:_ 

Assume that a file, `file.bash`, contains code that is to be used in several scripts. Rather than copy 
the code into all the scripts, you can just use `. file.bash`. Using the dot tells the user how the code 
is being used.

#### The general use convention doesn't always apply

When this convention doesn't apply, or could cause confusion, defaulting to `source` is better for readability.

For example, in the tests, the main script `run_tests.sh` contains this function definition:

```
run_test() 
{
    source $1
    return $?
}
`
```

In this case, the use of `source` emphasizes sourcing as a delibrate choice and improves readability. Importantly, it 
signals that `$1` should not contain the command 'exit'.  The preference for 'source' as opposed to running it as a shell 
script is explained below. 

### Executing other BASH files: use source/return or run/exit?

This mostly concerns the tests in GEMS, but the behavior information is general.

#### Brief Overview

Assume you have these three BASH scripts:

- `main_script.bash`
- `child_sript.bash`
- `separate_script.bash`

Also assume that `main_script.bash` must cause the other two to be executed. 

There are two ways that this can happen. Main can source the other script or can call it like a command.

The code looks something like:

```
source file.bash    # source file.bash as if it were lines of code
## or
bash file.bash      # run file.bash like a regular script or separate executable
```

The difference is important for two reasons: external script completion and variable passing to the external script.

#### External script completion

If file.bash contains an `exit` command, different things happen when that command is accesed.

The following will cause the calling script to also exit (cease processing) immediately:

```
source file.bash
```

But, this will not cause the calling script to exit:

```
bash file.bash
```

!! For this reason, files that are intended to be sourced should only `return` and never `exit`.

If exit is used, it causes everything that sourced the exiting file to also exit immediately.

#### Variable passing to the external script

Variables can be used by sourced scripts without using `export`. However, variables must be exported 
to scripts that are executed. This provides a method for having 'private' variables. 

Example:

Here is the calling script:
```
$ cat parent.bash 
#!/usr/bin/env bash

privatevariable="keepmelocal"
export exportedvariable="exportme"

echo "sourcing child.bash"
source child.bash

echo "executing child.bash"
bash child.bash
```

Here is the script that is called:
```
$ cat child.bash 
#!/usr/bin/env bash

echo "The value of privatevariable is ${privatevariable}"
echo "The value of exportedvariable is ${exportedvariable}"
```

Here is the result of running parent.bash:
```
$ bash parent.bash 
##
# sourcing child.bash
The value of privatevariable is keepme
The value of exportedvariable is exportme
##
# executing child.bash
The value of privatevariable is 
The value of exportedvariable is exportme
```

Note that `privatevariable` is only visible to child.bash if child.bash is sourced.

##### How this is useful

Assume that you are running tests. 

In the tests, you want `testchild.bash` to use `SpecialVariable` as defined in `parent.bash`.  But, you 
also must execute another file, `otherchild.bash`, that needs `SpecialVariable` to be defined somewhere 
else (possibly a pre-existing default). You can use this difference to achieve that.

```
$ cat parent.bash
#!/usr/bin/env bash

SpecialVariable="test value"

source testchild.bash   # will see SpecialVariable="test value"
bash otherchild.bash    # will see SpecialVariable as defined elsewhere (or as undefined if not)
```

---

## Artifacts

The use of Resources to describe Artifacts is preferred. Resources abstract location and format to simplify
storage, transmission and retrieval. 

For example, if your code needs a PDB file for input, the code that handles the PDB file does not need to
know where the PDB file is or the format it is in. That is, whether the file is at rcsb.org or on a local 
disk or in an object store, the local code does not need to know how to handle all those storage locations. 

Instead it can look like:

```
def manage_pdb_file(Resource Artifact_in) :
    ...
    pdb_file = Artifact_in.copy_to_path(Path(file_destination))
    ...
```

The Resource knows how to turn its payload into a file at a certain path.

This functionality is new, so it is a little limited. Please add to it if you can.
