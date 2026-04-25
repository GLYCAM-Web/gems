#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    'Error' : ModuleData('gemsModules.common.services.error.server', 'Serve'),
    'ListServices': ModuleData('gemsModules.common.services.list_services.server', 'Serve'),
    'Marco': ModuleData('gemsModules.common.services.marco.server', 'Serve'),
    'Status': ModuleData('gemsModules.common.services.status.server', 'Serve'),
    '{{cookiecutter.service_name}}' : ModuleData('gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.server ', 'Serve'),
    }


module_loader = ModuleLoader(REGISTRY)

