#!/usr/bin/env python3
from gemsModules.status.main_settings import WhoIAm
from pydantic import validator, typing
from gemsModules.common import main_api
from gemsModules.common import main_api_entity

##
#@detail 
# write me
class Status_Entity(main_api_entity.Entity):

    def getEntityType(self):
        return WhoIAm    

##
#@detail 
# write me
class Status_API(main_api.Common_API):    
    entity : Status_Entity
    
    # migrate these to a service-related module
    # The Pydantic classes should be focused on 
    # actions associated with the API itself, with 
    # the JSON object itself.
    #
    # ##
    # #@brief 
    # # determines local environment or production
    # # if production, get release name
    # def _get_environment_state(self):#rename this
    #     pass

    # ##
    # #@brief
    # # get branch names and commit hashes
    # def _get_git_meta_data(self):
    #     pass

    # ##
    # #@brief 
    # # get warnings associated with user behavior
    # # warnings will likely pertain scientific protocols
    # def _get_user_warning(self):
    #     pass

    # ##
    # #@brief 
    # # write me
    # def _get_module_error_notice(self):
    #     pass

    # ##
    # #@brief 
    # # get errors from test runners
    # def _get_test_error_notice(self):
    #     pass

    # ##
    # #@brief 
    # # get status of a given project
    # def poll_status(self):
    #     pass

##
#@detail 
# write me
class Status_Transaction(main_api.Transaction):
    def get_API_type(self):
        return Status_API