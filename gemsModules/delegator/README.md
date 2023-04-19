# Readme for the delegator

The delegator entity is responsible for directing incoming requests to other GEMS entities.   Because of this, delegator offers only a few services.

## Services

- `known_entities` - return a list of entities to which the delegator can forward requests.
- `list_services` - return a list of services offered by the delegator
- `marco` - return an affirmation that connection to the delegator is working

## Request redirection

_explain the basic workflow_

## To-Do

- [ ] Finish writing these docs
- [ ] Finish writing the code for managing delegator's services 
	- [x] Write all the tasks that are needed
	- [ ] Write mechanism for each service to perform each task in order
	- [ ] Write mechanism for services to be performed in order
	- [ ] Refine and expand mechanism for converting top-level input into service requests
	- [ ] Write mechanism for converting service responses into top-level output
- [ ] Move the parts that can be abstracted over to common
- [ ] Test the generalization by making an MD as a service module