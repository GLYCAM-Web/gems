The image below outlines the current status of workflow in GEMS.

![[../img/GEMS - Application Flow.png]]

Start with Delegator, middle-left.  Head up from there.  

- Delegator assigns the Entity and sends the JSON request to the Entity.
- Entity receives the request and calls the Json String Manager to instantiate the Transaction and validate the JSON string.
- The Json String Manager then sends the Transaction to the Transaction Manager.
- The Transaction Manager (TM) performs a series of other management tasks.
	- At the moment, it does project management first, but that's a kluge.  Project management should happen later, as shown and as described below.
	- First, the TM invokes the Request Manager.  Overall, the job of the request manager is to inspect all the data in the incoming API and make a list of all the Services that are being requested or that must happen as a result of a request.  Keep in mind that a Service might be implied by the presence of user-convenience inputs.  Specifically, the Request Manager does these things:
		- Makes a list of Service Packages corresponding to each explicitly requested Service.  
			- Explicit requests come in the form of Service objects contained in the API.  
			- A Service Package ('AAOP' in the code) contains the Service Request itself plus some metadata for keeping up with information about how the service should run or how it did run.
		- Ensures that each explicitly requested Service is known to the Entity.  If any unknown services are found, it requests an Error Service.  The Error Service will ensure that the returned JSON includes information about the unknown services.
		- Adds to the current AAOP list any implied Service Requests.  Service Requests can be implied by these mechanisms:
			- Data in the user convenience sections of the API might imply a Service Request.
			- A requested Service might have pre-requisite services.
		- Sends the entire list to a Multiples Manager.  It is possible - and in many cases very legitimate - that a user might request a Service explicitly and implicitly.  Up to this point, all explicit or implicit services have been cast as separate requests.  The Multiples Manager determines what to do with multiple requests for the same service.  Possible actions are currently:
			- Return an error - that is, do  not allow any multiples at all.  
			- Act on the first one in the list.
			- Act on the last one in the list.
			- Run them all as separate requests.
			- Attempt to merge them into one request, or, depending on circumstances, into a smaller number of requests.  If this option is chosen, it is necessary to indicate what should happen if the merge is conflicted. 
		- The Request Manager then returns the resulting AAOP list to the TM.
	- Second, the TM sends the AAOP list to the Service Package Tree Pair Manager.  The job of this manager is to arrange the AAOP list according to the required order of operations.  Notably, the order of operations could be a tree-like structure, hence the name.  Ultimately, a pair of trees is generated.  The first tree holds the AAOPs for the Service Requests.  An equivalent tree holds spaces to recieve corresponding AAOPs for the Service Responses.
	- Third, the TM invokes the Project Manger.  The Project Manager handles information related to where data relevant to the service should be stored, sent, etc.  It also keeps up with UUIDs, session information, etc.  The Project Manager ensures that the outgoing Project contains all the information it needs and that the information is correct.
	- Next, the TM sends project and Entity information to the Data Filler.  The job of the Data Filler is to ensure that each Service Request has all the information it needs contained within itself.  Each Service Request should be able to run independently of the rest of the transaction.  It is possible to require that dependencies have run successfully, but the Service Request should not need to consult the Entity or the Transaction for information. 
	- Now that each Service Request has all the data it needs, the TM sends the AAOP Tree Pair to the Servicer.  The sole job of the Servicer is to run every Service Request and to store the output (possibly with some metadata) in a Service Response Package.  
	- Once all the Services have been run, the Response Manager is invoked.  It is the job of the response manager to do these things:
		- Make a serial list of all the Service Requests, complete with all the information they needed, and store those into a Services object to be included in the outgoing JSON.  
		- Make a serial list of all the Service Responses, complete with all output information, and store those into a Responses object to be included in the outgoing JSON.  
			- Note that the AAOP Tree Pair object, itself, actually generates the linear lists of Requests and Responses.  But, the Response Manager ensures that all the relevant pieces are stored properly in the JSON object.
		- Translate - using code specific to each Service - the Responses into any appropriate user-convenience data in the outgoing JSON. 
		- Generate any desired summary data.  For example, summary data might contain numbers of errors and warnings, links for download, etc.
		- Return the data to the Transaction Manager.
	- Next, the Transaction Manager ensures that all the data returned from the Response Manager is included in the outgoing Transaction. 
	- Finally, the Transaction Manger generates and returns the outgoing JSON string.
- The JSON string manager then returns the outgoing string to the Delegator.
- The Delegator returns the string to the user who initiated the process.