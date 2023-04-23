#!/usr/bin/env python3
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class AAOP_Tree_Pair_Manager(ABC):
    def __init__(self, aaop_request_list : List[AAOP]):
        self.aaop_request_list = aaop_request_list

    def process(self) -> AAOP_Tree_Pair:
        self.transform_aaop_list_to_aaop_tree()
        self.generate_tree_pair()
        return self.aaop_tree_pair

    @abstractmethod
    def transform_aaop_list_to_aaop_tree(self):
        pass

    @abstractmethod
    def generate_tree_pair(self):
        pass


