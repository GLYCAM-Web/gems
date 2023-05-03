#!/usr/bin/env python3
from pydantic import ValidationError
from gemsModules.common.receiver import Receiver
from gemsModules.TEMPLATE.main_settings import WhoIAm
from gemsModules.TEMPLATE.main_api import Template_Transaction
from gemsModules.TEMPLATE.transaction_manager import template_Transaction_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Template_Receiver(Receiver):

    def get_local_components(self):
        self.transaction = Template_Transaction()
        self.entityType = WhoIAm
        self.transaction_manager_type = template_Transaction_Manager
