#!/usr/bin/env python3
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Servicer:
   
    def __init__(self, tree_pair: AAOP_Tree_Pair):
        self.tree_pair = tree_pair
        log.debug(f'In servicer, tree_pair = {tree_pair}')

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
            this_callable = this_request_aaop.get_callable()
            this_response_aaop = this_callable(this_request_aaop)
            log.debug(f'In servicer, this_response_aaop = {this_response_aaop}')
            log.debug("In servicer, the response aaop type is" + str(type(this_response_aaop)))
            self.tree_pair.put_next_AAOP_outoing(this_response_aaop)
        log.debug("In servicer, about to return this tree_pair:")
        log.debug(self.tree_pair)
        return self.tree_pair
