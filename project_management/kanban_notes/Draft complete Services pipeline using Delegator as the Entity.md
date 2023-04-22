Currently working on this workflow:
- [x] Entity receives incoming JSON string
- [x] Entity transforms it into a transaction
- [x] Transaction translates top-level directives into Entity's Procedural Options
- [ ] Entity passes Entity portion of transaction to the Service Manager
- [ ] Service manager extracts all explicit services into an AAOP list 
	- [ ] DRAFTED
- [ ] Service manager collapses all unknown services into an error service 
	- [ ] DRAFTED
- [ ] Service manager sends the Entity info to each Service 
	- [ ] draft in flux
- [ ] Each Service inspects the requested services, the inputs, and the Procedural Options.  From these, the Service generates a list of all service requests that are implied and packs them into a list of AAOPs and returns them to the Service Manager 
	- [ ] prior code exists, needs to be moved / rewritten / expanded /wrapped
- [ ] Service manager collects all AAOPs for a specific service, explicit or implicit, and sends those to the service so the service can manage initial duplicates (merge, allow, error, etc.) 
	- [ ] prior code exists, needs to be moved / expanded / wrapped
- [ ] Each Service then generates a list of pre-requisite service requests, if any.  This step considers only service needs provided by the current entity - services requested from other entities get handled down in the tasks.
	- [ ] some settings info exists somewhere
- [ ] The service manager collects all the resulting service requests and sends them back to the services for a final merge.
- [ ] During merges, the service inspects the multiple service requests.  Based on its rules for service requests, it might merge some (or all), might keep them all as individual services, or it might return a special "error" service request that contains options to be later turned into Notices.
	- [ ] This is gonna be a hack for now
- [ ]  Service returns the resulting AAOP list.

So far, I drafted code for doing part of the above.  I need to move it to better places.  I keep changing my mind about where the better places are, but that is happening less often.

After this workflow is done, the following should happen:
- [ ] Entity sends the AAOP list and any Project info to each Service.
- [ ] Each Service fills in each service_request with all the information that the service request needs.
- [ ] The AAOP list is returned to Entity.
- [ ] Entity collects together all the AAOP lists from the Services into a single list.
- [ ] Entity sends the list to the Workflow Manager.  Workflow Manager arranges AAOP objects into an AAOP Tree and instantiates an AAOP Tree Pair object.
- [ ] Figure out how the tree pair object will be managed and some hack way to make it work quickly.

This old list is probably redundant, but check it:

- [ ] Finish writing the code for managing delegator's services 
	- [x] Write all the tasks that are needed
	- [ ] Write mechanism for each service to perform each task in order
	- [ ] Write mechanism for services to be performed in order
	- [ ] Refine and expand mechanism for converting top-level input into service requests
	- [ ] Write mechanism for converting service responses into top-level output