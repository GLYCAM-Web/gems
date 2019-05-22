# Adding New Entities and Services to the Delegator

It should be pretty easy to do this, and you should be able to add in
pretty much any code you wrote.  

You will need to:
* Decide what to call your Entity and the Service(s) it provides.
  * Examples:
    * Is this a docking service?  Maybe your entity is a _Cocomplex_. 
    * If you are mutating a protein, then maybe the entity is a _Protein_.
    * Are you collecting info from databases?  Maybe call it a _Query_.
  * If the name for your Entity already exists, consider adding your
    code to that Entity as a new Service.
* If your code is not written in python, then wrap it in python.
* Find some way to encode your code's input in JSON. 
  * The simplest way will be to use the _tags_ in the Delegator schema.
* Put your code, along with certain files, in a directory alongside
  the Delegator.
* Add some info to the Delegator itself and to CommonServices.

## Files to place in your Entity's directory

Better docs should come later.  For now, look at these files in 
existing directories for format and content information.

* entity.py - A file containing high-level information about what your
  Entity does.  
  * It should at least include:
    * A main() function for use on the command line.
    * A receive() function for receiving a Transaction.  This function should
      decide what to do based on the incoming JSON information.
    * A doDefaultService() function.  This is the thing that your Entity 
      should do if no Service is explicitly requested.
  * It might also include other functions, but those can go in other files.
* helpme.py - A file containing various types of help in simple text format.
  * Note that the names of the types of help are standard, so be sure to
    stick to the naming convention.
* settings.py - A file mapping JSON requests to classes, funcitons and modules.
  * We do this because we don't want anything coming in over the web to 
    directly cause the execution of any code.  So, we make sure that the code
    on the back-end always performs actions _on behalf of_ a request rather 
    than performing commands in the request.
* schema.json - a symbolic link to the schema appropriate to the Entity.

Of course, your Entity's directory can contain other files as needed for the
Entity to perform its services.

## Additions to the Common Servicer

The Common Servicer (in the _common_ subdirectory) is responsible for 
containing and executing any Services that all Entites should perform.

* Add your entity to the EntityModules object in settings.py.
* In transaction.py:
  * Add the entity to EntityTypeEnum.
  * Add any non-common Services for your entity to a new Enum (see existing
    Enum's for examples - they should be right at the top).
  * Make a new EntityServices(BaseModel) class for your Entity's Services Enum 
    (again see existing classes as examples).
  * Add that new BaseModel to the Union at the top of the Service class.

# At this point, it should just work.

If not, please let us know by opening an issue:
https://github.com/GLYCAM-Web/gems/issues

