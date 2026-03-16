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
###         service_organizational_unit(s)
###                         =   These are any sub-directories or trees of 
###                             sub-directories, that are needed by the entity
###                             while performing the requested service.
###
###                             For example, the Build3DStructure service uses
###                             'Builds' and 'Sequences', each of which contain
###                             multiple trees of sub-directories.
###

default_versions_file_name = "VERSIONS.sh"

# Default user paths are set in the main_api.py file. They are not enforced, so are not listed here.

# Default standalone filesystem paths
default_standalone_filesystem_output_path = '/work/' 
default_standalone_filesystem_uploads_path = '/work/uploads/' 
default_standalone_filesystem_testing_path = '/work/TESTS/'
default_standalone_versions_file_path = default_standalone_filesystem_output_path

# Default website filesystem paths - these are generally enforced in a website environment
default_website_filesystem_output_path = '/website/userdata/' 
default_website_filesystem_uploads_path = '/website/uploads/' 
default_website_filesystem_testing_path = '/website/TESTS/'
default_website_filesystem_prepush_testing_path = '/website/TESTS/git-ignore-me/pre-push/'
default_website_versions_file_path = default_website_filesystem_output_path
# For allowing easy restriction
allowed_website_filesystem_paths = [default_website_filesystem_output_path,
                            default_website_filesystem_testing_path,
                            default_website_filesystem_prepush_testing_path]

