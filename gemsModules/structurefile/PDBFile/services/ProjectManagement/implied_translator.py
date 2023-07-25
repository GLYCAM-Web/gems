#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP

# from gemsModules.common.services.implied_requests import Implied_Services_Inputs
from gemsModules.structurefile.PDBFile.services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Inputs,
)
from gemsModules.common.services.each_service.implied_translator import (
    Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class ProjectManagement_Implied_Translator(Implied_Translator):
    """Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
    Bundle resulting services into a service request package list (List[AAOP]).
    """

    def process(self, input_object: ProjectManagement_Inputs) -> List[AAOP]:
        self.aaop_list = []

        log.debug(
            "In ProjectManagement_Implied_Translator.process, \n\ninput_object=%s\n\n",
            input_object.json(indent=2),
        )

        # TODO/Q: It seems that we could instead add a Dependency to AmberMDPrep, but I don't think they get resolved yet.
        # It appears the only references to Dependencies are the class definition and deep copy at the moment.
        if input_object.services.is_present("AmberMDPrep"):
            log.debug(
                "Implicitly adding a ProjectManagement service request, needed by the AmberMDPrep service."
            )
            this_aaop = AAOP(
                AAO_Type="ProjectManagement",
                The_AAO=None,
                ID_String=uuid.uuid4(),
                Dictionary_Name="ProjectManagement_Request",
            )

            # TODO/Q: I think if we want to run this service before AmberMDPrep, we need to
            # add a dependency to AmberMDPrep and fill this Request with that service ID to
            # build the aaop tree correctly.
            self.aaop_list.append(this_aaop)

        return self.get_aaop_list()
