# Notable Services

This is a listing of certain services that are generally available across all
the modules or that are important to them all.  The services listed here are
also likely to be of use generally to users of the modules.

## `marco`

This is the old game Marco Polo.  We chose that rather than 'ping' because of
how the modules work, especially in view of our use of gRPC.  If you ping a
computer, you are asking if a specific machine, more precisely address, is
listening and able to respond.  But, with the modules, it's a lot more like 
calling "Marco" into the void and listening for an answer from someone, anyone.

This service tells you if a given entity is working, accessible and able 
to respond.  It's not an exhaustive test.  It doesn't check that the entity
or its services function as needed.

Here is what it checks:

  -  That the entity can be found by delegator.
  -  That the entity can find the common servicer.
  -  That the common servicer can also find the entity.

If all of these things can happen, a JSON object that requests the 'Marco' 
service will receive a response of 'Polo', also in a JSON object.

## `receive`

All the entities work by receiving a JSON object and by returning one.  This
is the name of the service that receives the JSON object and then figures out
what to do with it.

## `list_entities`

If asked of the delegator, this returns a list of all the entities that the 
delegator knows about.  If asked of any other entity, it is sort-of the same
except that it returns a list of all the other entities that might be contacted
by the entity you are asking.

## `list_services`

This lists all the services that are offered by the entity being asked.

