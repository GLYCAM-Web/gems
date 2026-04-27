#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = { 
    "Error": ModuleData('gemsModules.common.services.error.server', 'Serve')
    "ListServices": ModuleData('gemsModules.common.services.list_services.server', 'Serve')
    "Marco": ModuleData('gemsModules.common.services.marco.server', 'Serve')
    "Status": ModuleData('gemsModules.complex.glycomimetics.services.Status.server', 'Serve')
    "Evaluate": ModuleData('gemsModules.complex.glycomimetics.services.Evaluate.server', 'Serve')
    "Validate": ModuleData('gemsModules.complex.glycomimetics.services.Validate.server', 'Serve')
    "ProjectManagement": ModuleData('gemsModules.complex.glycomimetics.services.ProjectManagement.server', 'Serve')
    "Build_Selected_Positions": ModuleData('gemsModules.complex.glycomimetics.services.Build_Selected_Positions.server', 'Serve')
    "Analyze": ModuleData('gemsModules.complex.glycomimetics.services.Analyze.server', 'Serve')
}


module_loader = ModuleLoader(REGISTRY)

