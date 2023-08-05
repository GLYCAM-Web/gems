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
        for i, aaop in enumerate(self.aaop_list):
            log.debug(f"i: {i}, {aaop.AAO_Type=}")

            if aaop.AAO_Type == "AmberMDPrep":
                self.__fill_ambermdprep_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)

        return self.aaop_list

    def __fill_ambermdprep_aaop(self, i: int, aaop: AAOP):
        root = self.response_project.project_dir
        if (
            "inputFilePath" in aaop.The_AAO.inputs
            and aaop.The_AAO.inputs["inputFilePath"] is not None
        ):
            root = aaop.The_AAO.inputs["inputFilePath"]

        self.aaop_list[i].The_AAO.inputs = mdprep_api.AmberMDPrep_Inputs(
            pdb_file=aaop.The_AAO.inputs["pdb_filename"],
            outputFileName=f"preprocessed.{aaop.The_AAO.inputs['pdb_filename']}",
            outputFilePath=self.response_project.project_dir,
            inputFilePath=root,
        )

        log.debug(
            "\tFinished building AmberMDPrep_Inputs, aaop_list[%s].The_AAO.inputs: %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        # Fill in the project management service request
        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
        )

        # Add the resources to copy to the project management service request
        input_json = pm_api.PM_Resource.from_payload(
            self.transaction.incoming_string, "input", "json"
        )
        aaop.The_AAO.inputs.resources.append(input_json)

        # Lets try to get inputs from the requesting AAOP for ProjectManagement
        if aaop.Requester is not None:
            # If we were using an AAOP_Tree we could use aaop_tree.get_aaop_by_id(aaop.Requester)
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)

            input_pdb = pm_api.PM_Resource(
                name=Path(requester_aaop.The_AAO.inputs["pdb_filename"]).stem,
                res_format="pdb",
                location=str(requester_aaop.The_AAO.inputs["inputFilePath"]),
                locationType="File",
            )
            log.debug(
                "Adding input_pdb resource to ProjectManagement_Inputs: %s", input_pdb
            )
            aaop.The_AAO.inputs.resources.append(input_pdb)
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
