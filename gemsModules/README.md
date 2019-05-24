# The GEMS Modules

The main purpose of these modules is to provide services via a JSON-based
API via GLYCAM-Web (glycam.org).  However, for simplicity and transparency,
the actual work of the API - and eventually all of the website services - 
happens here in these gemsModules.  That is, if you send an API request to
GLYCAM-Web, what really happens is that GLYCAM-Web sends that JSON object
down here.  These modules process it and send back a JSON object.  You can
do the same thing right here, on the command line, or from a python script
you write.  

The GEMS Modules:

* Use JSON objects as input and response.
  * As needed, inside the input and response there can be references to one
    or more external _Resources_, like a URL or directory.  
* Rely on the _Delegator_ to assign tasks.
* They are each, including the Delegator, called _Entities_.
  * Entities are things like sequences, files and glycoproteins.
  * Consider them to be objects.
* Each Entity can perform certain _Services_.
  * When needed, Entities can direct other Entities to perform Services.

The Delegator can be called as a module inside a python script or it can
be called on the command line.

You can find the JSON Schema in the $GEMSHOME/gemsModules/Schema directory.

## Prerequisites

* GEMS - https://github.com/GLYCAM-Web/gems 
* GMML - https://github.com/GLYCAM-Web/gmml
* Python 3.7 
* Pydantic - https://pydantic-docs.helpmanual.io/
* jsonpickle - https://jsonpickle.github.io/
* PYTHONPATH set to contain GEMSHOME
  * GEMSHOME is the main gems directory, above where you find this file.

### Possible other requirements

Depending on what you want to do, these other packages might be required:

* AMBER and/or AmberTools - http://ambermd.org/
* Slurm - https://slurm.schedmd.com/documentation.html
* GRPC - https://grpc.io/

## Usage

### On the command line:

>  $GEMSHOME/gemsModules/delegator/entity.py inputfile.json

If you feel like making that easier to do, go for it and send us a patch!

### In a python program:

> from gemsModules.delegator.entity import delegate
> jsonObjectOutputString = delegate(jsonObjectInputString)

## Adding new Entities and Services

Please see the files in:

> gemsModules/Docs/Delegator-Entities-Services/
