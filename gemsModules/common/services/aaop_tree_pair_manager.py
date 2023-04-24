#!/usr/bin/env python3
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class AAOP_Tree_Pair_Manager():
    def __init__(self):
        self.aaop_request_list : List[AAOP] = []

    def process(self, aaop_request_list : List[AAOP]) -> AAOP_Tree_Pair:
        self.transform_aaop_list_to_aaop_tree(aaop_request_list)
        self.generate_tree_pair()
        return self.aaop_tree_pair

    def transform_aaop_list_to_aaop_tree(self):
        pass

    def generate_tree_pair(self):
        pass

