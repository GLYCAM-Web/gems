"""
The GEMS Modules are designed to serve as a JSON-based
interface to the capabilities of GEMS and GMML.

These modules are also used by the molecular modeling
services at GLYCAM-Web (glycam.org and, for the
adventuresom, dev.glycam.org).

The main point of entry is the delegator submodule. To
learn how it works, try using the 'delegate' script
found in $GEMSHOME/bin.  Start off with:

    $GEMSHOME/bin/delegate --help

The other modules that are generally important are
the common and project modules as they provide core
services to the others.

See also our JSON schema documentation in the Schema
subdirectory.
"""
from . import batchcompute
#from . import common
from . import conjugate
from . import delegator
from . import mmservice
from . import project
from . import query
from . import sequence
from . import graph
from . import status
from . import structureFile

## Deprecating_2022_12
from Deprecating_2022_12 import common