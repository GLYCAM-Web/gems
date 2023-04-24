#!/usr/bin/env python3

from gemsModules.common.services.response_manager import Response_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class delegator_Response_Manager(Response_Manager):

    def generate_response_entity(self):
        pass
