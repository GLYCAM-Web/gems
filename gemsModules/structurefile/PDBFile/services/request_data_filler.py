#!/usr/bin/env python3
import json
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_resources import Resource
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project

from gemsModules.structurefile.PDBFile.services.AmberMDPrep import api as mdprep_api
from gemsModules.structurefile.PDBFile.services.ProjectManagement import api as pm_api

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> list[AAOP]:
        """Fill in any data required in the service request aaop_list."""
        for i, aaop in enumerate(reversed(self.aaop_list)):
            log.debug(f"i: {i}, {aaop.AAO_Type=}")

            if aaop.AAO_Type == "AmberMDPrep":
                self.__fill_ambermdprep_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)

        return self.aaop_list

    def __fill_ambermdprep_aaop(self, i: int, aaop: AAOP):
        root = self.response_project.project_dir
        if aaop.The_AAO.inputs.inputFilePath is not None:
            root = aaop.The_AAO.inputs.inputFilePath

        # TODO: "projectDir" API instead
        aaop.The_AAO.inputs.outputFilePath = self.response_project.project_dir
        aaop.The_AAO.inputs.inputFilePath = root
        aaop.The_AAO.inputs.outputFileName = f"preprocessed.{aaop.The_AAO.inputs.pdb_filename}"
        
        log.debug(
            "\tFinished building AmberMDPrep_Inputs, aaop_list[%s].The_AAO.inputs: %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )

    # TODO: PDBFile and MDaaS PM data fillers are very similar, can we generalize them?
    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        # Fill in the project management service request
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        
        # Add the resources to copy to the project management service request
        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "input.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)

        # Lets try to get inputs from the requesting AAOP for ProjectManagement
        if aaop.Requester is not None:
            # If we were using an AAOP_Tree we could use aaop_tree.get_aaop_by_id(aaop.Requester)
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
            log.debug(
                "Found requester aaop[%s] for aaopreversed_list[%s], %s",
                requester_aaop,
                i,
                requester_aaop.The_AAO.inputs,
            )

            input_pdb = Resource(
                payload=Path(requester_aaop.The_AAO.inputs.inputFilePath)
                / requester_aaop.The_AAO.inputs.pdb_filename,
                resourceFormat="chemical/pdb",
                locationType="filesystem-path-unix",
                resourceRole="input-pdb"
            )
            log.debug(
                "Adding input_pdb resource to ProjectManagement_Inputs: %s", input_pdb
            )
            aaop.The_AAO.inputs.resources.add_resource(input_pdb)
        else:
            log.debug(
                "No requester found for aaop_list[%s], PM service request will not have a pdb file resource.",
                i,
            )

        log.debug(
            "\tFinished building ProjectManagement_Inputs, aaop_list[%s].inputs filled with %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )
