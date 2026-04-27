#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error' : ModuleData('gemsModules.common.services.error.server', 'Serve'),
    'Marco': ModuleData('gemsModules.common.services.marco.server', 'Serve'),
    'ListServices': ModuleData('gemsModules.common.services.list_services.server', 'Serve'),
    'ProjectManagement': ModuleData('gemsModules.conjugate.glycoprotein.services.ProjectManagement.server', 'Serve'),
    'Evaluate': ModuleData('gemsModules.conjugate.glycoprotein.services.Evaluate.server', 'Serve'),
    'Build' : ModuleData('gemsModules.conjugate.glycoprotein.services.Build.server ', 'Serve'),
    'Status': ModuleData('gemsModules.conjugate.glycoprotein.services.Status.server', 'Serve'),
}


module_loader = ModuleLoader(REGISTRY)

