#!/usr/bin/env python3
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.main_api_services import Service, Services
from gemsModules.common.settings_main import All_Available_Services
from gemsModules.common.settings_main_servicer import All_Service_Modules

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Servicer:
   
    def __init__(self, incoming_tree: AAOP_Tree):
        self.incoming_tree = incoming_tree

    def invoke_servicer(self):
##  Move all this to a servicer - let services fill in prereqs (service chain??  sigh...)
        self.instantiate_AAOP_Tree_Set(self)
        self.merge_explicit_and_implicit(self) # Logic should live in service management
        self.add_requisite_service_packages(self) ## this should be done by the services' managers.
        self.build_service_request_package_tree(self)
        self.build_skeleton_service_response_tree(self)
        self.build_service_tree_set(self)
        self.call_servicer(self)

    def build_service_request_package_tree(self):
        pass

    def build_skeleton_service_response_tree(self):
        pass

    def build_service_tree_set(self):
        pass

    def call_servicer(self):
        pass
