#!/usr/bin/env python3
from typing import List

from gemsModules.common.code_utils import Annotated_List
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class AAOP_Tree_Pair_Generator():
    def __init__(self, aaop_request_list : List[AAOP] = []):
        self.aaop_request_list : List[AAOP] = aaop_request_list
        self.incoming_aaop_tree : AAOP_Tree = None

    def process(self) -> AAOP_Tree_Pair:
        self.incoming_aaop_tree=self.transform_aaop_list_to_aaop_tree(the_list=self.aaop_request_list)
        log.debug("incoming_aaop_tree")
        log.debug(self.incoming_aaop_tree)
        self.aaop_tree_pair=self.generate_tree_pair()
        log.debug("aaop_tree_pair")
        log.debug(self.aaop_tree_pair)
        return self.aaop_tree_pair

    def transform_aaop_list_to_aaop_tree(self, the_list : List[AAOP]):
        the_annotated_list = Annotated_List(items=the_list)
        the_tree = AAOP_Tree(packages=the_annotated_list)
        return the_tree

    def generate_tree_pair(self):
        the_tree_pair = AAOP_Tree_Pair(input_tree=self.incoming_aaop_tree)
        return the_tree_pair

