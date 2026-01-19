The title (the file name) is super vague and overly wordy.  Feel free to change it.

This doc was inspired by Dan's request to be able to get a list of valid file formats for a given service, particularly a service offered by a sub-entity of a meta-entity.  But, the basic infrastructure can apply to other situations.

Herein is documentation for a possible way to handle doing this.

This method has the following attributes:
- The meta-entity can specify a set of file formats that all sub-entities will accept.
- These file formats can also be used by pydantic as the sub-entities validate incoming json.
- If needed, the sub-entity's service can completely override whatever the meta-entity had set.

Caveats and other things to note:
- This method is applied to mmservice (the meta-entity) and mdaas (the sub-entity)
- The file formats assigned by mmservice might not be actually usable by mdaas.  The point here is to show how it can be done.
- It is not applied to any given service of mdaas yet in any case.

# Important files:

## How to do the basics:

	   gemsModules/mmservice/each_service/known_available.py  
       gemsModules/mmservice/each_service/service_io.py  
       gemsModules/mmservice/each_service/tests/service_io_tester.py  

## Extending the Enum

       gemsModules/mmservice/mdaas/services/settings/known_available.py  

## Returning a list of services

       gemsModules/delegator/tasks/get_services_list.py

## Files you might also want to check out:

       gemsModules/common/main_api_resources.py  
       gemsModules/delegator/services/settings/known_available.py

# The Walk Through

Start here:

	   gemsModules/mmservice/each_service/known_available.py  

- This file contains an enum that defines a list of allowed input file types.  
- Files with this name generally contain what is known to be available.  See the one down in Delegator for one with more content ("Files you might also want to check out").
- The name of the enum should probably be "...allowed INPUT file formats" because the output formats might differ.  Put that on the to-do list.
- The GemsStrEnum just defines some methods with names that are convenient for us.  For example, `get_json_list`, which gives the list in the format most useful for comparing to the incoming JSON.

Now check out this:

       gemsModules/mmservice/each_service/service_io.py  

- The validator is set as an abstract method.  This forces it to be defined in any child classes.
- Those child classes can then validate against whatever list of files is correct for them.
- Having the others be ABCs might not be necessary, but it makes plain that something below them requires special input.  
	- If I were to want to change anything, it would be this need to define everything above the thing you need to change.  There is probably a way to not do that, but this is low priority as it isn't really a ton of work and it works.

Then, see this: 

       gemsModules/mmservice/each_service/tests/service_io_tester.py  

- Here, you can see the validation part put into action.
- To prove it, try chaning the resourceFormat in the test json.
- This file should be made compatible with doctest one day.

Regarding doctest,  this file is an example:

       gemsModules/delegator/services/settings/known_available.py

To see how the enum defined in mmservice can be extended in mdaas, see this:

       gemsModules/mmservice/mdaas/services/settings/known_available.py  

- See also the doctest-ref file just above.  It does the same thing for available services.

To see how you might define a task that can return the info, see this:

       gemsModules/delegator/tasks/get_services_list.py

- The same logic could `get_known_file_formats` and so forth.

