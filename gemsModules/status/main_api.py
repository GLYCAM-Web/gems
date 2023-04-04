#!/usr/bin/env python3
from pydantic import validator, typing, Field
from typing import Literal

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.status.main_settings import WhoIAm

## CLARIFY
#@brief 
# extends main_api_entity.Entity 
class Status_Entity(main_api_entity.Entity):

    entityType : Literal['Status'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )  

## CLARIFY
#@brief 
# extends main_api.Transaction
# define Status services here
class Status_API(main_api.Common_API):    
    entity : Status_Entity


##
#@detail 
# write me
class Status_Transaction(main_api.Transaction):
    def get_API_type(self):
        return Status_API
    





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