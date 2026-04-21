# Conventions and Normal Practices for gemsModules

Unless something here contradicts a widely-adopted practice, then use a widely-adopted practice.

## Imports

Goal: minimize the number of imports to greatly reduces the possibility of head-scratcher bugs.

It also makes the code faster.

### Leave `__init__.py` empty.

Keep all imports purposeful, local, and targeted to the need.

### Use Full Paths

Don't use relative paths (start with dots). Please just accept this and hope you never need to know why.
As of this writing, this is also the recommended best practice for Python.

The gemsModules refer to each other, and sometimes to deprecated code. Each one is a 'package', and they
often have identical names other than their paths. Be verbose and unambiguous.

### Place imports as close to the imported code as possible. 

Top-level (file-level) imports should be reserved for:

- File-level imports, e.g., logging utilities.
- Requirements for defining classes or definitions, e.g., `class MyChildClass(ParentClass):`. 
  In the latter, it is appropriate to import ParentClass at the file-level.

It is also ok to use them for this:

- Imports that are used in multiple places by many defs/classes.
- Especially lower-level imports like 'os'.

... but avoid it even then. 

Regarding lower-level imports, see also Syntactic Sugar, below.

## Variables Related To I/O

Conventions for variables that inhabit the client-facing API or that inhabit the scientific-software-facing Tasks.

- Client-Facing API Variables: snake case, for example: `project_dir`.
- Scientific-Software-Facing Task Variables (inlcuding APIs used only in Tasks): camel case, for example: `projectDir`.

Doing this makes it easier for coders to identify the expected scope of a specific variable. 
This ability is also valuable in finding workflow-related bugs.

Another important benefit is to help communicate variable type. For example, in the API, `project_dir` can only be
a string: JSON does not allow the Python notion of 'Path'. If `project_dir` is only used in relation to the API,
then a coder can be sure that it is always a string. Similarly, a coder knows that `projectDir` is used by a Task.
Because the Tasks exist for the purpose of interfacing other software, the coder knows that it might be of whatever 
variable type is convenient to the particular Task.

Currently, there is no convention for non-API/non-Task naming. For example, `def do_this_thing():` has no predetermined
convention. It might be useful to add one. Spelling/naming conventions can be added as needed. 

## Use Syntactic Sugar

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

See the code for `gemsModules.systemoperations.filesystem_ops.directory_is_writable`. The sugar is much 
better than writing that all over the place.

#### Searching and Maintenance

It is also useful to have the underlying code defined once and then referenced using a locally-sweet variable.

This helps for these reasons:

- There are many ways to do the same thing in Python. This assures one easily-searched method.
- The import statement informs the reader/coder where the sugar's code can be found.
- We often need only a few behaviors from a library (e.g., os.path) rather than all the possible options.
- If a sugared method must be altered, it needs only be altered in a single location.
- It is easy to find all instances where the method is used.

_A use-case example:_

During an upgrade of the Python version used by the code, the default behavior of a file operation changed. 
This operation happened to be important and widely-used. In places where sugar had been used, the update
was simple: update a single defined function. But, the other uses had to be found one at a time by looking 
at every import of the relevant Python library.


