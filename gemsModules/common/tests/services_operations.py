#!/usr/bin/env python3
from gemsModules.common import main_api_services as api

the_Services = api.Services()

this_service = api.Service()
this_service.typename="testme"

the_Services.add_service("newThing",this_service)

this_service = api.Service()
this_service.typename="testmeagain"

the_Services.add_service("newerThing",this_service)

print(the_Services.json(indent=2))

print("Checking if testmeagain is present.  Is it?")
print(the_Services.is_present("testmeagain"))
