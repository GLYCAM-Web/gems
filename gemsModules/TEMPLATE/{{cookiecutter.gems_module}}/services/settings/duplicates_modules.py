from typing import Dict, Callable

from gemsModules.common.services.error.manage_multiples import error_Multiples_Manager 
from gemsModules.common.services.marco.manage_multiples import marco_Multiples_Manager 
from gemsModules.common.services.status.manage_multiples import status_Multiples_Manager

from gemsModules.{{cookiecutter.gems_module}}.services.list_services.manage_multiples import list_services_Multiples_Manager
from gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.manage_multiples import {{cookiecutter.service_name}}_Multiples_Manager 

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

duplicates_modules : Dict[str, Callable] = {
    'Error': error_Multiples_Manager, 
    'ListServices': list_services_Multiples_Manager, 
    'Marco': marco_Multiples_Manager, 
    'Status': status_Multiples_Manager,
    '{{cookiecutter.service_name}}': {{cookiecutter.service_name}}_Multiples_Manager
    }
