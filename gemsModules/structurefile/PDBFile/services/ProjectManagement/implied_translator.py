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
        # TODO: This should not be here, but in a dependency manager.
        if input_object.services.is_present("AmberMDPrep"):
            log.debug(
                "Implicitly adding a ProjectManagement service request, needed by the AmberMDPrep service."
            )
            this_aaop = AAOP(
                AAO_Type="ProjectManagement",
                The_AAO=ProjectManagement_Request(),
                ID_String=uuid.uuid4(),
                Dictionary_Name="ProjectManagement_Request",
            )

            # TODO/Q: I think if we want to run this service before AmberMDPrep, we need to
            # add a this AAOP as a dependency to the AmberMDPrep AAOP. I think we need to use something like:

            # for service in input_object.services.get_services_of_type("AmberMDPrep"):
            #    this_aaop = AAOP( ... )
            #    service.add_dependency(this_aaop.ID_String)
            #
            # But, then we need to actually execute the PM service first by resolving dependenices...
            # - Also fill the PM request from the associated mdprep request.
            #
            #  After directory creation:
            # - One thing the PM service needs to be able to do is copy the input file given to AmberMDPrep to the project.
            #   - This way AmberMDPrep only has to look for an input.pdb file in the project directory no matter how we got it there.
            # - We also need to be able to dump the incoming request.json() to the project directory

            #  > These things mean that when we run PM service to resolve a dependency for AmberMDPrep, we need to be able to resolve the
            #  > pUUID of the associated mdprep service request, rather than an arbitrary or any default created for PM service.
            #
            # get index of all AmberMDPrep requests and prepend an aaop for each:
            self.aaop_list.append(this_aaop)

        return self.get_aaop_list()
