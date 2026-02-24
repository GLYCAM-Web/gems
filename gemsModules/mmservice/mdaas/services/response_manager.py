#!/usr/bin/env python3

from gemsModules.common.services.response_manager import Response_Manager
from gemsModules.common.main_api_notices import Notices

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity

from gemsModules.common.tasks import create_default_entity_aaop_tree_pair

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class mdaas_Response_Manager(Response_Manager):

    def populate_response_entity(self, existing_response_entity):
        log.info("populate_response_entity for mdaas_Response_Manager is called")
        if self.response_entity is None:
            log.debug("in populate_response_entity, existing_response_entity cannot be None")
            raise ValueError ("In populate_response_entity, existing_response_entity cannot be None")
        if self.response_entity.notices is None:
            self.response_entity.notices = Notices()

        create_default_entity_aaop_tree_pair.execute(self)

        return self.response_entity


    def generate_response_entity(self):
        self.response_entity = MDaaS_Entity(type="MDaaS")


