#!/usr/bin/env python3
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project

from gemsModules.structurefile.PDBFile.services.AmberMDPrep import api as mdprep_api
from gemsModules.structurefile.PDBFile.services.ProjectManagement import api as pm_api

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> list[AAOP]:
        this_Project: PDBFile_Project = self.project

        for i, aaop in enumerate(self.aaop_list):
            if aaop.AAO_Type == "AmberMDPrep":
                # I believe this should be done by the ProjectManagement service, but we currently give these inputs to AmberMDPrep.
                #
                # Also,  Q: should we be using the entity inputs and filling the service inputs here?
                # Not doing so means in the implied translator we have to know about services.
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
                    "Finished building AmberMDPrep_Inputs, %s",
                    self.aaop_list[i].The_AAO.inputs,
                )
            elif aaop.AAO_Type == "ProjectManagement":
                this_service = pm_api.ProjectManagement_Request()
                this_service.inputs = pm_api.ProjectManagement_Inputs(
                    pUUID=this_Project.pUUID,
                    projectDir=this_Project.project_dir,
                )

                # TODO/O: How do we get the project directory from the ProjectManagement service to AmberMDPrep?
                self.aaop_list[i].The_AAO = this_service

        return self.aaop_list
