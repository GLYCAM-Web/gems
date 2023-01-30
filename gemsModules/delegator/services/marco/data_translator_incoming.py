#!/usr/bin/env python3

from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.main_api import Delegator_API
from gemsModules.delegator.main_api import Delegator_Entity

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

template_API = Delegator_API.construct(entity=Delegator_Entity.construct(entityType='Delegator'))
#self.outputs = self.get_API_type(self).construct(entity=Entity.construct(entityType=settings_main.WhoIAm))


JSON_to_Service_Request_mapping={
        template_API.entity.inputs['cake'] : "yay"
        }


class JSON_to_Service_Request_translator():
    pass



class Request_to_task_input_translator():
    pass



