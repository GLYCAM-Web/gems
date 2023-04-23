#!/usr/bin/env python3
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Servicer:
   
    def __init__(self, tree_pair: AAOP_Tree_Pair):
        self.tree_pair = tree_pair

    def serve(self) -> AAOP_Tree_Pair:
        this_request_aaop : AAOP = self.tree_pair.get_next_AAOP_incoming()
        while this_request_aaop is not None :
            this_callable = this_request_aaop.get_callable()
            this_response_aaop = this_callable(this_request_aaop)
            self.tree_pair.put_next_AAOP_outoing(this_response_aaop)
            this_request_aaop = self.tree_pair.get_next_AAOP_incoming()

