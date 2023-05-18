Because we are in the process of adding MD as a service (MDaaS) to GEMS at the time of this writing, the examples herein will be drawn from that process.

## Before starting:

- Think carefully about what the service should do.
- Think even more carefully about what it should not do.
- Seek input from the various stakeholders.   These might include:
	- Users of the service.  Keep in mind that some users might be other services, other software, etc.
	- Maintainers of the service - not just the parts you will write but all the software parts on both sides of the GEMS interface.
	- Systems folks who might need to configure storage, networks, etc.
- Also seek input from people who have done work similar to what your service will provide.
- Make a list of all the software, data or systems that the new service must interface.
- Keep in mind that the primary role of GEMS is to be an interface.  

**Example**

>Regarding what the software should and should not do:  MDaaS should perform molecular dynamics simulations.  But, it should do only that.  It should not be tasked with determinining which systems to simulate.  At first, at least, it will also not determine which force field to use.  MDaaS will require a parameter-topology file and an input-coordinate file as input.  Those files have the force field already defined within.  In this case, we are also requiring that the simulation software be AMBER.  One day, MDaaS might be more powerful, but  not yet.

We will get to the other items in the list above in due time.  But, for now, we have enough to begin.

## Become familiar with the API

The image below shows a Service-centered view of the API.  Note especially the two groupings titled "User Convenience".  Everything inside those groupings could potentially need to be copied into a Service_Request or out from a Service_Response.  This doesn't mean you should make things hard on the user by avoiding using the components that are convenient to the user.  But, you can also minimize how hard you make things for yourself.

![[../img/GEMS - API Overview.png]]

Also find the notes that start with "Form varies by".  Inputs and outputs at the Entity level apply to the entire Entity and, potentially, all of its services.  The same goes for the Project (which is on the same level with Entity).  Note that the Service-level inputs, outputs, options and notices are specific to each Service.  

Each Service_Request and Service_Response must be completely self-contained.  There might be user-convenience information that is copied into multiple services.  Be careful how you include information at higher levels if it might differ from one service to another.   Generally, it is best to avoid having data that will vary in this way.  

Inside the code, the translation into a Service_Request is handled by a Request_Manager.  The translation back out from a Service_Response is handled by a Response_Manager.  These two managers allow each Service to specify - and deide - which parts of the User-Convenience data apply to them.  

**Example**

> Below, we will see that two of the desired services are called 'Evaluate' and 'Run_MD'.  Each of these services will need to know the location of the input files.  In the first case, the Evaluate service will inspect the files and return information about them to the user.  In the second case, the files will be used to run a molecular dynamics simulation.  Because this Entity is concerned entirely with running molecular dynamics simulations, it makes sense to require that the user only write this information once, at the Entity level's inputs.  Of course, it should also be acceptable for users to write the information directly into a Service Request.  

**Example**

> Considering those same two services, it would be best to keep any output written to a filesystem inside a single parent directory.  Outputs from the two Services could be placed in separate subdirectories, of course.  But, it would be best to avoid, for example, having to provide an 'evaluation parent path' that is separate from the 'md parent path'. 

## Start with the user story

The user is the reason we bother to write software.  We want to make things easy for the user.  So, we start off by considering what the user wants and needs.

But do not be so sidetracked by the user's interests that you forget that you will need to build software capable of providing the service.

### Start small

Don't forget any complexity that you know will come later.  That knowledge is useful.  But, at the start, consider a minimal implementation.

- What are the minimum inputs required for the service?
- Are there any ancillary services that might be needed or immediately usefu?  (other than the standards, like 'Marco')
- What are the outputs expected from each service?
	- Will any special actions be needed for returning these outputs?

**Example**

>From the example above, we know that we will require as input:
>- a parameter-topology file
>- an input-coordinate file
. ..both in AMBER format.  
>
 Optionally, users willing to pay a fee for longer simulations might enter:
>- desired simulation length
>- authentication information
>
 From conversations with stakeholders, we learned that the following services are desirable for MDaaS:
>
>- Evaluate:  
	- Perform some evaluation of the inputs.  
	- Expected output:  
		- confirmation that the files are appropriate
		- expected ns/day simulation speed
		- total ns expected from the requested simulation
>- Run MD:
	- Perform the MD simulation for the default amount of time.
	- Expected output:  
		- zipped directory containing all the simulation files.
>- Run MD longer for a fee:
	- Extend the default simulation to the desired length of time.
	- Additional input:
		- simulation length
		- authentication data
	- Expected output:
		- zipped directory containing all the simulation files
	- Special actions:
		- Very large output files might need to be omitted from the zip file and transferred separately using special methods.
>- Convert trajectory from NetCDF to ASCII:
	- Windows users cannot open NetCDF files in VMD (a popular visualization software), and other older codes cannot handle NetCDF, so we add a service that will convert the default NetCDF files to the older, ASCII format.
	- Expected output:
		- Single trajectory file in mdcrd format.
	- Special actions:
		- Very large files might need special transfer methods.
>- Status:
>	- The behavior of the Status service will need to change depending on the information it is given.
>- List acceptable inputs:
>	- what types, sizes, etc.
>- Analyze the MD output:
	- Users will eventually want the MD analyzed. 
	- This is tabled for now.
	- This service should possibly be performed by a different entity.


As  you can see, a seemingly-simple service can have complex needs. 


## Design an interface

At this point, begin to be of two minds.  Consider the user and how one might keep things simple from the user's perspective.  But, also consider the needs of GEMS.

Specifically, keep in mind that each Service, when implemented in GEMS, will ultimately be initiated with a Service Request and fullfilled by a Service Response.  No information outside the Service Request will be available to the service, and the service will not fill any information outside of a Service Response.  Whatever you design for the user will need to be translated into a Service Request.  Correspondingly, any friendly output you design will need to be tranlated from a Service Response.  Where possible, avoid making your life difficult.

Currently, a Service Request contains these components:

```
class Service_Request(BaseModel):  
   """  
   Holds information about a requested Service.  
   This object will have different forms in each Entity.  
   """  
   typename: Available_Services = Field(  
       'Status',  
       alias='type',  
       title='Common Services',  
       description='The service requested of the Common Servicer'  
   )  
   givenName: str = Field(  
       None,  
       title='The name given this object in the transaction',  
       description='A place for users to specify a name.'  
   )  
   myUuid: UUID = Field(  
       None,  
       title='My UUID',  
       description='ID to allow correlations between services and responses.'  
   )  
   inputs: typing.Any = None  
   options: Dict[str, str] = Field(  
       None,  
       description='Key-value pairs that are specific to each entity, service, etc'  
   )  
  
   class Config:  
       title = 'Service'
```

The _inputs_ and _options_ can be practically anything.   A Service Response has an equivalent form.

Consider infrastructure that is available to you in GEMS.  Reuse of common infrastructure reduces the need for code duplication.  

At the top level, each Entity has this definition:

```
class Entity(ABC, BaseModel):  
   """Holds information about the main object responsible for a service."""  
   entityType : str = Field(  # This is the only required field in all of the API  
           ...,  
           title='Type',  
           alias='type'  
           )  
   inputs : Union[Dict,Resource] = Field(  
           None,  
           title='Inputs',  
           description='User-friendly, top-level inputs to the services.'  
   )  
   outputs : Union[Dict,Resource] = Field(  
           None,  
           title='Inputs',  
           description='User-friendly, top-level outputs from the services.'  
   )  
   services : Service_Requests = Service_Requests()  
   responses : Service_Responses = Service_Responses()  
   notices : Optional[Notices] = Notices()  
   procedural_options : Procedural_Options = Procedural_Options()  
   options : Dict[str,str] = Field(  
           None,  
           description='Key-value pairs that are specific to each entity, service, etc'  
           )
```

The _inputs_ and _outputs_ are designed to be the user-friendly interface.  Of course, users can ignore those and instead directly specify services.  But, we expect them to only do that if they require very specialized behavior.

**Note to devs** - The definition of inputs and outputs in Entity might benefit from some tweaking.

The 'Resource' defined in both the inputs and outputs is an example of infrastructure that can facilitate abstraction.  Here is the Resource:

```
class Resource(BaseModel):  
   """Information describing a resource containing data."""  
   locationType: str = Field(  
           None,  
           title='Location Type',  
           description='Supported locations will vary with each Entity.'  
           )  
   resourceFormat: str = Field(  
           None,  
           title='Resource Format',  
           description='Supported formats will varu with each Entity.',  
           )  
   payload : Union[str,int,float] = Field(  
           None,  
           description='The thing that is described by the location and format'  
           )  
   notices : Notices = Notices()  
   options : Dict[str,str] = Field(  
           None,  
           description='Key-value pairs that are specific to each entity, service, etc'  
           )
```

It is designed to be adaptable.  Consider locationType: this could be filesystem or URL or database query or any other type of location.  The resourceFormat specifies how to interpret the data at that location.  The payload tells how to get the data.   Additoinal details can be added in the options (usually for inputs) and notices (usually for outputs). 

Here are two possible Resources.

This one is a path to an AMBER 7 restart file:

```
{"locationType" : "filesystem-path-unix",
 "resourceFormat" : "AMBER-7-restart",
  "payload" : "/path/to/my/file.rst7"}
```

This one is an mmCIF file to be retrieved from the wwPDB:

```
{"locationType" : "download-url",
 "resourceFormat" : "mmCIF",
  "payload" : "https://files.rcsb.org/download/1UBQ.cif"}
```


The Entity's inputs/outputs can also 

**Example**

> Let's consider the input files.   File formats change.  Right now, we are in the process of migrating from MD output being primarily in ASCII format to NetCDF format.  It will be useful to be able to tell the Service Request what sort of file is being used as input.  You might decide to detect the file format for the user (or you might not), but your sanity will be enhanced by not needing to add "file format detection" to the job of the "run MD" service.  
> 
> You might decide to make your Entity inputs for the run_MD service look like this dictionary where the values are of type Resource:
> 
```
{
  "parameter-topology-file" : {
    "locationType" : "filesystem-path-unix",
 ​   "resourceFormat" : "AMBER-7-restart",
    "payload" : "/path/to/my/file.rst7"
    },
  "input-coordinate-file" : {
    "locationType" : "filesystem-path-unix",
 ​￼​  "resourceFormat" : "AMBER-7-prmtop",
    "payload" : "/path/to/my/file.parm7"
    },
  "convert-trajectory-to-ascii" : false
}
```
>The last field would imply an additional service - the conversion of the trajectory to ascii.  Note that the use of the Resource here forces the user to specify the file type.  Furthermore, the entire Resource can be copied into each Service Request that needs it (evaluate, run md, etc.).


