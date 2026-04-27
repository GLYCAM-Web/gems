#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = { 
    "Error": serve_error, ModuleData('gemsModules.common.services.error.server', 'Serve'),
    "Marco": serve_marco, ModuleData('gemsModules.common.services.marco.server', 'Serve'),
    "ListServices": serve_list_services, ModuleData('gemsModules.common.services.list_services.server', 'Serve'),
    "Status": serve_status, ModuleData('gemsModules.common.services.status.server', 'Serve'),
    "AmberMDPrep": serve_prepare_pdb, ModuleData('gemsModules.structurefile.PDBFile.services.AmberMDPrep.server', 'Serve'),
    "ProjectManagement": serve_project_management, ModuleData('gemsModules.structurefile.PDBFile.services.ProjectManagement.server', 'Serve'),
}
