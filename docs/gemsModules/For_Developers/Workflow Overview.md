The image below outlines the current status of workflow in GEMS.

![[../img/GEMS - Application Flow.png]]

Start with Delegator.  Head up from there.  

- Delegator assigns the Entity and sends the JSON request to the Entity.
- Entity calls the Json String Manager to instantiate the Transaction and validate the JSON string.
- The Json String Manager then sends the Transaction to the Transaction Manager.
- The Transaction Manager performs a series of other management tasks.
	- At the moment, it does project management first, but that's a kluge.  It should not be that way.
	- (doc in progress)