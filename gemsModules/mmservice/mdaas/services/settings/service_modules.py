#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = { 
    "Error": ModuleData('gemsModules.common.services.error.server', 'Serve'),
    "Marco": ModuleData('gemsModules.common.services.marco.server', 'Serve'),
    "ListServices": ModuleData('gemsModules.common.services.list_services.server', 'Serve'),
    "Status": ModuleData('gemsModules.common.services.status.server', 'Serve'),
    "RunMD": ModuleData('gemsModules.mmservice.mdaas.services.run_md.server', 'Serve'),
    "Evaluate": ModuleData('gemsModules.mmservice.mdaas.services.Evaluate.server', 'Serve'),
    "ProjectManagement": ModuleData('gemsModules.mmservice.mdaas.services.ProjectManagement.server', 'Serve'),
}


module_loader = ModuleLoader(REGISTRY)

