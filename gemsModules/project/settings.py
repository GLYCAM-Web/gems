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
output_data_dir = '/website/userdata/'  ## Being deprecated
default_filesystem_output_path = '/website/userdata/' ## Use this instead of output_data_dir
default_versions_file_path = default_filesystem_output_path
default_versions_file_name = "VERSIONS.sh"

# Default subdirectories per project type.  Typically, these go
# under whatever is defined for project_path
toolPathIdentifier = {
        'cb'   :  'tools/cb/git-ignore-me_userdata',
        'pdb'  :  'tools/pdb/git-ignore-me_userdata',
        'gp'   :  'tools/gp/git-ignore-me_userdata'
        }
