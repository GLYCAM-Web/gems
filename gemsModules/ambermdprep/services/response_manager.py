#!/usr/bin/env python3

from gemsModules.common.services.response_manager import Response_Manager
from gemsModules.common.main_api_notices import Notices

from gemsModules.ambermdprep.main_api import AmberMDPrep_Entity
from gemsModules.ambermdprep.tasks import create_default_entity_aaop_tree_pair

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Response_Manager(Response_Manager):
    def generate_response_entity(self):
        self.response_entity = AmberMDPrep_Entity(type="AmberMDPrep")
        self.response_entity.notices = Notices()

        create_default_entity_aaop_tree_pair.execute(self)

        return self.response_entity
