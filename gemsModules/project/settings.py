#!/usr/bin/env python3

## Who I am
WhoIAm='Project'

##Status Report
status = "Stable"
moduleStatusDetail = "Creates Gems Projects for MMService, Sequence, and StructureFile."

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

# Default project path - see also getProjectPath()
output_data_dir = '/website/userdata/'

# Default subdirectories per project type.  Typically, these go
# under whatever is defined for project_path
project_subdirectory = {
        'cb'   :  'tools/cb',
        'pdb'  :  'tools/pdb',
        'gp'   :  'tools/gp'
        }
