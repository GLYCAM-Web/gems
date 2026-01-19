# The GEMS Modules

## Overview
The gemsModules contain entities. Entities provide services.  Not all sub-folders in the gemsModules are Entities, but most are.

One key gemsModule, delegator, receives a json-formatted request that
defines one entity, and a list of requested services. The delegator validates 
this request, and if all goes well, requests a service from the requested
entity's gemsModule, or returns a json-formatted error. 

GemsModules receive the request in the form of a transaction object,
which is designed to contain the original request, and any output that 
will be returned. The services defined in each gemsModule are responsible 
for creating any output.


## Adding A New Entity
It is likely very helpful to refer to the sequence gemsModule to see 
examples.

1. Add a new folder for your gemsModule. Begin lowercase, and use camelcase
if necessary.
2. Add an `__init__.py` and in it, list __helpme.py, receive.py,__ and __settings.py__, 
along with any other files you need to include in your package.
3. Write each of those files. 
4. Register your service in the delegator settings.py subentities.
5. Register your service in the common settings.py subentities.
6. In your gemsModule's settings.py, list your service in serviceModules.
7. In gemsModule's settings.py, add a status for your service.
8. Define your classes in io.py. Use pydantic.

## Adding A New Service
1. Add the new service to settings.py, in the serviceModules enum. 
Key should be capitalized, and represents what users will request. 
Value should begin with a lowercased letter, then be camel-cased.
2. Add a servicesStatus element, with service, status, and status detail. 
3. In the io.py for your gemsModule, create an Output class for your
service response. In this class, you must provide an __init__() function
for constructing your response object. This will be used by common.logic.py's
updateResponse() to prepare for calling thisTransaction.build_outgoing_string().
4. Add your new Output class to the ServiceResponse Outputs list.

