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

    def process(self, existing_response_entity=None) -> Entity:
        log.info("process for Response_Manager is called.")
        if existing_response_entity is not None:
            log.debug("using the existing_response_entity")
            self.response_entity = existing_response_entity.copy(deep=True)
        else: 
            log.debug("existing_response_entity is None; making new")
            self.response_entity = self.generate_response_entity()

        self.response_entity=self.populate_response_entity(existing_response_entity=self.response_entity)
        return self.response_entity

    # making abstract for now. might remove that later.
    @abstractmethod 
    def generate_response_entity(self) -> Entity:
        # Should look something like this, but customize for your situation
        # TODO - make customization not be needed
        log.info("generate_response_entity for Response_Manager is called")
        self.response_entity = Entity(type="Common_API")

    @abstractmethod
    def populate_response_entity(self, existing_response_entity) -> Entity:
        pass


class common_Response_Manager(Response_Manager):
    def generate_response_entity(self):
        self.response_entity = Entity(entity_type="Common")
