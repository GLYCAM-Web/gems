#!/usr/bin/env python3
from gemsModules.status.main_settings import WhoIAm
from pydantic import validator, typing
from gemsModules.common import main_api
from gemsModules.common import main_api_entity

##
#@detail write me
class Status_Entity(main_api_entity.Entity):

    def getEntityType(self):
        return WhoIAm

##
#@detail write me
class Status_API(main_api.Common_API):    
    entity : Status_Entity

##
#@detail write me
class Status_Transaction(main_api.Transaction):
    def get_API_type(self):
        return Status_API