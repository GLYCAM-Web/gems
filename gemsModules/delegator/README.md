# Readme for the delegator

The delegator entity is responsible for directing incoming requests to other GEMS entities.   Because of this, delegator offers only a few services.

## Services

- `known_entities` - return a list of entities to which the delegator can forward requests.
- `list_services` - return a list of services offered by the delegator
- `marco` - return an affirmation that connection to the delegator is working

## Request redirection

_explain the basic workflow for delegator's job of delegating_

## To-Do

Currently working on this workflow:
1. Entity receives incoming JSON string
2. Entity transforms it into a transaction
3. Entity translates top-level directives into Procedural Options
4. Entity sends only the Entity portion of the transaction to each Service
5. Each Service inspects the requested services, the inputs, and the Procedural Options.  From these, the Service generates a big list of all service requests that are explicit or implied.
6. Each Service then generates a list of pre-requisite service requests, if any (only from the current entity - services from other entities happen elsewhere)
7. Each service request is placed into an AAOP (this can happen at service request creation or later, depending on which is simpler.  At this moment, I think at creation time is easier.)
8. Each Service sends back to the Entity the list of AAOPs that it generated.
9. Entity collects together all AAOPs relevant to each Service and sends only that group back to the Service.  
10. This time, the service inspects the multiple service requests.  Based on its rules for service requests, it might merge some (or all), might keep them all as individual services, or it might return a special "error" service request that contains options to be later turned into Notices.
11. Service returns the resulting AAOP list.

So far, I drafted code for doing part of the above.  I need to move it to better places.

After this workflow is done, the following should happen:
1. Entity sends the AAOP list and any Project info to each Service.
2. Each Service fills in each service_request with all the information that the service request needs.
3. The AAOP list is returned to Entity.
4. Entity collects together all the AAOP lists from the Services into a single list.
5. Entity sends the list to the Workflow Manager.  Workflow Manager arranges AAOP objects into an AAOP Tree and instantiates an AAOP Tree Pair object.
6. Figure out how the tree pair object will be managed and some hack way to make it work quickly.

- [ ] Finish writing these docs
- [ ] Finish writing the code for managing delegator's services 
	- [x] Write all the tasks that are needed
	- [ ] Write mechanism for each service to perform each task in order
	- [ ] Write mechanism for services to be performed in order
	- [ ] Refine and expand mechanism for converting top-level input into service requests
	- [ ] Write mechanism for converting service responses into top-level output
- [ ] Move the parts that can be abstracted over to common
- [ ] Test the generalization by making an MD as a service module