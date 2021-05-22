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


###  Filesystem Paths Information
###  
###  The format for the path is : 
###   
###      /filesystem_path/entity_ID/service_ID/service_organizational_unit(s)
###
###         filesystem_path =   the path above anything defined within this code.
###                             this allows the user to specicy output location
###
###         entity_ID       =   an identifier for the entity.  If the entity name
###                             is long, etc., this might be an abbreviation
###
###         service_ID      =   Like entity_ID but for the service.  For example,
###                             rather than 'Build3DStructure', we use 'cb'
###
###
###  service_organizational_unit(s) are defined at the entity/service level, and they may
###     be defined in different ways in different entities/services.
###
###         service_ortanizational_unit(s)
###                         =   These are any sub-directories or trees of 
###                             sub-directories, that are needed by the entitu
###                             while performing the requested service.
###
###                             For example, the Build3DStructure service uses
###                             'Builds' and 'Sequences', each of which contain
###                             multiple trees of sub-directories.
###

# Default filesystem path
output_data_dir = '/website/userdata/'  ## Being deprecated
default_filesystem_output_path = '/website/userdata/' ## Use this instead of output_data_dir
default_versions_file_path = default_filesystem_output_path
default_versions_file_name = "VERSIONS.sh"

# Default entity IDs
output_entity_id = {
        'Sequence'      : 'sequence',
        'Conjugate'     : 'conjugate',
        'Query'         : 'query',
        'StructureFile' : 'structureFile'
        }

output_entity_service_id = {
        'Sequence'      :   {
            'Validate'          : 'cb',
            'Evaluate'          : 'cb',
            'Build3DStructure'  : 'cb',
            'DrawGlycan'        : 'cb'
            },
        'Conjugate'     :   {
            'BuildGlycoprotein' : 'gp'
            },
        'StructureFile'         :   {
            'PreprocessPDB'     : 'pdb'
            }
        }


# Default subdirectories per project type.  Typically, these go
# under whatever is defined for project_path
##
##  Old and being deprecated
##
toolPathIdentifier = {
#        'cb'   :  'tools/cb/git-ignore-me_userdata',
        'pdb'  :  'tools/pdb/git-ignore-me_userdata',
        'gp'   :  'tools/gp/git-ignore-me_userdata'
        }


