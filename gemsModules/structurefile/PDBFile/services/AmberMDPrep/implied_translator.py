#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.implied_requests import Implied_Services_Inputs
from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import (
    AmberMDPrep_Request,
)
from gemsModules.common.services.each_service.implied_translator import (
    Implied_Translator,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmbderMDPrep_Implied_Translator(Implied_Translator):
    """Inspect the Implied_Services_Inputs to figure out if this service needs to be run, and if so, how many times.
    Bundle resulting services into a service request package list (List[AAOP]).
    """

    def process(self, input_object: Implied_Services_Inputs) -> List[AAOP]:
        if input_object is not None and input_object.inputs is not None:
            the_inputs = input_object.inputs
            if "pdb_filename" not in the_inputs.keys():
                service_request = AmberMDPrep_Request()
                # service_request.options = {}
                # service_request.options["pdb"] = the_inputs["pdb"]
                service_request.inputs = {
                    "pdb_filename": "016.AmberMDPrep.4mbzEdit.pdb",
                    "inputFilesPath": "/programs/gems/tests/inputs/",
                    "outputDirPath": "/programs/gems/tests/outputs/",
                }
                this_aaop = AAOP(
                    Dictionary_Name="implied_PDBFile_AmberMDPrep",
                    ID_String=uuid.uuid4(),
                    The_AAO=service_request,
                    AAO_Type="prepare_pdb",
                )
                self.aaop_list.append(this_aaop)

                log.debug(
                    "Implicitly adding AmberMDPrep service request with prepare_pdb task"
                )
        else:
            pass

        return self.get_aaop_list()
