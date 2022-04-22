#!/usr/bin/env python3
from enum import Enum

## Who I am
WhoIAm='gems_module_template'

##Status Report
status = "Queued for dev"
moduleStatusDetail = "Setting up gems module architecture."

servicesStatus = [
    {
        "service" : "Evaluate",
        "status" : "Queued for dev",
        "statusDetail" : "Will need to write this."
    },
    {
        "service" : "YourNewService",
        "status" : "Queued for dev",
        "statusDetail" : "Will need to write this."
    }
]

serviceModules = {
    'Evaluate' : 'evaluate',
    'YourNewService' : 'YourNewService'
}

# ## Services
# ##
class Services(str,Enum):
    evaluate = 'Evaluate'
    status = 'Status'
    your_new_service = 'YourNewService'

