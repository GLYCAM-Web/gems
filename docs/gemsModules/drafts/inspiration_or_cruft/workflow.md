# General Workflow for the GEMS Modules

## Common
Contains many abstract base classes, protocols and such.

Mostly, things in common are not meant to be used directly.

All other modules inherit from common in some way.  This is the base module.

## Delegator

Delegator is special.

## Normal Modules

Actually... this includes the Delegator module.

Workflow is as follows:
 1. Receive a json string.
 2. Parse the json string into a transaction.inputs object.
 3. If #2 fails, return an error.
 4. Hand the transaction object off to the Servicer.
 5. The Servicer will hand the transaction off to services. 
 


