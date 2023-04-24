#!/usr/bin/env python3
from typing import List, Callable
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.service_packages_list import Services_Package_List_Utilities

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Duplicate_Requests_Manager(ABC):

    def __init__(self, aaop_list : List[AAOP]):
        self.incoming_aaop_list = aaop_list
        self.new_aaop_list : List[AAOP] = []
        self.package_utils=Services_Package_List_Utilities(aaop_list)
    
    @abstractmethod
    def get_available_services(self) -> List[str]:
        pass

    @abstractmethod
    def get_duplicates_manager(self, service : str) -> Callable:
        pass

    def process(self) -> List[AAOP]:  
        """ Process the AAOP list to handle any duplicate requests.  Return the resulting list.
        """
        for service in self.get_available_services():
            this_aaop_list = self.package_utils.get_all_of_type_in_AAOP_list(service)
            if len(this_aaop_list) > 1 :
                this_manager = self.get_duplicates_manager(service)
                this_manager.process(aaop_list = this_aaop_list)
                self.new_aaop_list.extend(this_manager.get_aaop_list())
            else:
                self.new_aaop_list.extend(this_aaop_list)

        return self.get_aaop_list()  # need to not lose error aaops

    def get_aaop_list(self) -> List[AAOP]:
        # for now we are not processing multiple error aaops.  One day we may want to do that.
        error_aaops = self.package_utils.get_all_of_type_in_AAOP_list('Error')
        self.new_aaop_list.extend(error_aaops)
        return self.new_aaop_list


class common_Duplicate_Requests_Manager(Duplicate_Requests_Manager):

    def get_available_services(self) -> List[str]:
        return super().get_available_services()
    
    def get_duplicates_manager(self, service : str) -> Callable:
        pass

