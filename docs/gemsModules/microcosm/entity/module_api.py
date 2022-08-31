#!/usr/bin/env python3
from Pydantic import AnyOf
from gemsModules.docs.microcosm.common import entity_api
from gemsModules.docs.microcosm.common import services_api
from gemsModules.docs.microcosm.entity import module_api
from gemsModules.docs.microcosm.entity import settings 


class Module_Service(services_api.Service):
    typename : settings.All_Available_Services
    inputs : Union [ all the service types inputs...]

class Module_Response(services_api.Response):
    typename: settings.All_Available_Services
    outputs : Union [ all the service types outputs...]

class Module_User_Friendliness_Inputs :
    pass

class Module_User_Friendliness_Outputs :
    pass
