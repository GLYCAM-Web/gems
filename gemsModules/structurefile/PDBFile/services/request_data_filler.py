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
        this_Project: PDBFile_Project = self.project

        for i, aaop in enumerate(self.aaop_list):
            log.debug(f"i: {i}, {aaop.AAO_Type=}")
            if aaop.AAO_Type == "AmberMDPrep":
                root = this_Project.project_dir
                if (
                    "inputFilePath" in aaop.The_AAO.inputs
                    and aaop.The_AAO.inputs["inputFilePath"] is not None
                ):
                    root = aaop.The_AAO.inputs["inputFilePath"]

                self.aaop_list[i].The_AAO.inputs = mdprep_api.AmberMDPrep_Inputs(
                    pdb_file=aaop.The_AAO.inputs["pdb_filename"],
                    outputFileName=f"preprocessed.{aaop.The_AAO.inputs['pdb_filename']}",
                    outputFilePath=this_Project.project_dir,
                    inputFilePath=root,
                )
                log.debug(
                    "\tFinished building AmberMDPrep_Inputs, %s aaop_list[%s]",
                    self.aaop_list[i].The_AAO.inputs,
                    i,
                )
            elif aaop.AAO_Type == "ProjectManagement":
                self.__manage_pm_aaop(i, aaop)

        return self.aaop_list

    def __manage_pm_aaop(self, i: int, aaop: AAOP):
        # TODO: Resources need conversion methods.
        # fill in the project management service request with the resources to copy
        input_json = Resource(
            locationType="File",
            resourceFormat="json",
            payload=self.entity.schema_json(),
        )

        if aaop.Requester is not None:
            # If we were using an AAOP_Tree we could use aaop_tree.get_aaop_by_id(aaop.Requester)
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)

            input_pdb = Resource(
                locationType="File",
                resourceFormat="pdb",
                payload=requester_aaop.The_AAO.inputs["pdb_filename"],
            )
        else:
            log.debug(
                "No requester found for aaop_list[%s], PM service request will not have a pdb file resource.",
                i,
            )
            input_pdb = None

        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.project.pUUID,
            projectDir=self.project.project_dir,
            resources=[input_json, input_pdb],
        )

        log.debug(
            "\tFinished building ProjectManagement_Inputs, %s aaop_list[%s]",
            self.aaop_list[i].The_AAO.inputs,
            i,
        )

        # TODO/O: How do we get the input filename from the ambermdprep service request to it's implied dependency, the project management service?
