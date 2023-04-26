#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Callable

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Servicer(ABC):
   
    def __init__(self, tree_pair: AAOP_Tree_Pair):
        self.tree_pair = tree_pair
        log.debug(f'In servicer, tree_pair = {tree_pair}')

    @abstractmethod
    def get_module_for_this_request(self, this_request_aaop : AAOP) -> Callable:
        from gemsModules.common.services.settings.service_modules import service_modules
        return service_modules[this_request_aaop.AAO_Type]

    def serve(self) -> AAOP_Tree_Pair:
        I_am_done = False
        while I_am_done == False :
            log.debug("In servicer, about to serve")
            try: 
                log.debug("In servicer, about to get next AAOP")
                this_request_aaop : AAOP = self.tree_pair.get_next_AAOP_incoming()
                log.debug(f'In servicer, this_request_aaop = {this_request_aaop}')
            except StopIteration:
                I_am_done = True
                break
            log.debug(f'In servicer, this_request_aaop = {this_request_aaop}')
            this_callable = self.get_module_for_this_request(this_request_aaop)
            this_request=this_request_aaop.The_AAO.copy(deep=True)
            this_response_aaop : AAOP = this_request_aaop.make_skeleton_copy()
            this_response = this_callable(this_request)
            this_response_aaop.The_AAO = this_response.copy(deep=True)
            log.debug(f'In servicer, this_response_aaop = {this_response_aaop}')
            self.tree_pair.put_next_AAOP_outgoing(this_response_aaop)
        log.debug("In servicer, about to return this tree_pair:")
        log.debug(self.tree_pair)
        return self.tree_pair

class commonservices_Servicer(Servicer):

    # def __init__(self, tree_pair: AAOP_Tree_Pair):
    #     super().__init__(tree_pair)

    def get_module_for_this_request(self, this_request_aaop: AAOP) -> Callable:
        from gemsModules.common.services.settings.service_modules import service_modules
        return service_modules[this_request_aaop.AAO_Type]
       
