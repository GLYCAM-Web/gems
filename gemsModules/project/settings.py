#!/usr/bin/env python3

## Who I am
WhoIAm='Project'

##Status Report
status = "In development"
moduleStatusDetail = "Building module framework."

servicesStatus = [
    {
        "service" : "StartProject",
        "status" : "In development.",
        "statusDetail" : "Currently in focus."
    }
]

serviceModules = {
    "StartProject" : "startProject"
}

##This is the directory where projects should place their output,
## Note that the project.project_root is not included here, but is appended
## in project instantiation.
output_data_dir = '/website/userdata/'
