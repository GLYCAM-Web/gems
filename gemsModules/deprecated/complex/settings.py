#!/usr/bin/env python3
from enum import Enum

## Who I am
WhoIAm='complex'

##Status Report
status = "Dev"
moduleStatusDetail = "Setting up gems module architecture."

servicesStatus = [
    {
        "service" : "Evaluate",
        "status" : "Queued for dev",
        "statusDetail" : "Will need to write this."
    },
    {
        "service" : "Status",
        "status" : "Queued for dev",
        "statusDetail" : "Will need to write this."
    },
    {
        "service" : "Glycomimetics",
        "status" : "Queued for dev",
        "statusDetail" : "Will need to write this."
    }
]

serviceModules = {
    'Evaluate' : 'evaluate',
    'Check_Status' : 'check_status',
    'Glycomimetics' : 'glycomimetics'
}

# ## Services
# ##
class Services(str,Enum):
    evaluate = 'Evaluate'
    check_status = 'Check_Status'
    your_new_service = 'Your_New_Service'

