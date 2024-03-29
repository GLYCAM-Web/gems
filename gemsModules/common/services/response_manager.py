#!/usr/bin/env python3
from abc import ABC, abstractmethod

from gemsModules.common.main_api_entity import Entity
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Response_Manager(ABC):
    def __init__(self, aaop_tree_pair: AAOP_Tree_Pair):
        self.response_entity = None
        self.aaop_tree_pair = aaop_tree_pair

    def process(self) -> Entity:
        self.generate_response_entity()
        return self.response_entity

    @abstractmethod
    def generate_response_entity(self):
        pass


class common_Response_Manager(Response_Manager):
    def generate_response_entity(self):
        self.response_entity = Entity(entity_type="Common")
