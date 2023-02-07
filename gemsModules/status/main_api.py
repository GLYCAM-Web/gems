#!/usr/bin/env python3
from gemsModules.status.main_settings import WhoIAm
from pydantic import validator, typing
from gemsModules.common import main_api
from gemsModules.common import main_api_entity

##
#@detail
# Holds information about the main object responsible for a service.
class Status_Entity(main_api_entity.Entity):

    def getEntityType(self):
        return WhoIAm

class Status_API(main_api.Common_API):    
    entity : Status_Entity