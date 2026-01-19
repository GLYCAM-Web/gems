# List of the modules

If you are new here, you probably want to start with the 
[common](#common) and [delegator](#delegator) modules. 


## `batchcompute`

This module is responsible for getting longer jobs submitted to machines
that can handle the jobs.  It has some ability to query job status, but that
ability is limited to querying schedulers and such.  It is up to the module
that calls batchcompute to know how to check output from a job to ensure that
everything happened correctly.

Of note, this module employs gRPC.  At the moment, this ability is only written
into the Slurm submodule.  But, it should eventually be made more generally 
available.  It is set up so that the module does not need to know the location 
or identity of the machine that provides the batch computing (that is, the high 
performance compute cluster).  Environment variables control this information.
The module checks "am I on a machine that can accept job submissions?"  If the
answer is yes, then it submits the job.  If not, then it uses gRPC to send the
job on to whatever other machine answers.  

## `common`

The [common](#common) module is used by all the other modules.  It performs
many services that all modules are likely to need.  For example, it will check
the status of a file, make a symbolic link, and return the value of GEMSHOME.

Most importantly, this module contains the definitions of the parts of the API
that are common to all the other modules.  The other modules inherit from the
definitions in this module and make modifications as needed.

## `complex`

This module is a super-module for the modeling of any system containing a
glycan that is in complex with some other molecule.  Typically the other
molecule is large, but it need not be.  An example of such a system would 
be a complex of a spike protein from a flu virus in complex with the host
glycan that the spike latches onto.

Sub-modules include automated antibody docking, glyspec (grafting) and
glycomimetics.

## `conjugate`

This module is a super-module for the modeling of any system containing a
glycan that is conjugated (chemically bonded to) some other molecule.  
Typically the other molecule is large, but it need not be.  Examples of 
such a system include glycoproteins and glycolipids. These would also be
sub-modules.

## `delegator`

The delegator is the receptionist for the gemsModules.  Delegator doesn't 
do very much otherwise.  It looks into the incoming JSON object and, based
on what it finds, it sends the JSON on to wherever it needs to go.

The reason for this module's existence is to simplify the interface to
the gemsModules.  This is especially important for the interface to 
GLYCAM-Web.  It would be crazy for the website to have to know how to use
the gemsModules just to function.  Instead, the website always has to 
do exactly the same thing:  send the JSON object to the delegator and
collect the response.

Having the delegator also allows us to more easily try out new ideas and
new code, especially during development.  If a dev wants to try out a
shiny new newSequence module, then there is only a change in a settings
file.  The website will never know or care that there was a change.

## `Docs`

This isn't technically a module, but it is a directory in gemsModules.
It contains documentation.

## `drawglycan`

This module exists for generating graphic representations of glycans. 
Most visibly, this will be of the SNFG type.  But, any other graphic
representation that is needed will be handled here.

## `Examples`

This is also not a module.  This folder contains examples of how to 
use the modules.

## `gems_module_template`

This is a template designed to simplify starting new modules.  

## `graph`

This module should handle any graph-relevant tasks.  We're not sure we
really need it, though, because GMML handles most graph ops.  This one
might go away if it doesn't seem useful soon.

## `metadata`

This is a place for storing metadata, mostly molecular, that is of use to
other modules.  Need the mass of a carbon atom?  Look here.

## `mmservice`

This module handles interfaces to external molecular modeling softare.
Currently, that is primarily [AMBER](https://ambermd.org).   

## `project`

This module handles all the bureaucracy.  It makes directories, copies 
files, assigns UUIDs, assigns project IDs, etc.

## `query`

The query module handles interface to databases.  Currently, it only 
interfaces a triplestore DB served by Virtuoso, but other types of DB
queries will live here as they are needed.

## `Schema`

This isn't a module.  Its purpose is to store the schema for the API.  But,
we will probably move the schema somewhere else.  So, this is likely to 
go away eventually.

## `sequence`

The sequence module handles the generation of 3D models from sequence data.
Currently, it only handles glycan sequences in our condensed notation, but
it could handle other notations, and other types of molecules, for example
polymers, proteins, or DNA.

## `status`

This module is tasked with being able to figure out the status of all the 
other modules.  Are they working?  What serices do they offer?  Etc.

## `structureFile`

This module handles inspection, handling, and modification, as needed, of 
files containing molecular structure data.  

## `tests`

This is not a module.  It contains tests that can be run to assess the 
functionality of the various modules and their services.
