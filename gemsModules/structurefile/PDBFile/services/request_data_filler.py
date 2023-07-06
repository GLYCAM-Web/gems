#!/usr/bin/env python3
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project

from gemsModules.structurefile.PDBFile.services.AmberMDPrep import api

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> List[AAOP]:
        this_Project: PDBFile_Project = self.project

        for i, aaop in enumerate(self.aaop_list):
            # Get the filename from the aaop inputs (originating from an actual "inputs": {} field in the service request.)
            if "pdb_filename" in aaop.The_AAO.inputs:
                if "outputDirPath" in aaop.The_AAO.inputs:
                    outDir = aaop.The_AAO.inputs["outputDirPath"]
                else:
                    outDir = this_Project.upload_path + "output/"

                if "inputFilesPath" in aaop.The_AAO.inputs:
                    inDir = aaop.The_AAO.inputs["inputFilesPath"]
                else:
                    inDir = this_Project.upload_path

                self.aaop_list[i].The_AAO.inputs = api.AmberMDPrep_Inputs(
                    pdb_file=aaop.The_AAO.inputs["pdb_filename"],
                    pUUID=this_Project.pUUID,
                    # Use defaults for now.
                    outputDirPath=outDir,
                    inputFilesPath=inDir,
                )
                log.debug("Found 'pdb_filename' in aaop.The_AAO.inputs: %s", aaop)
            # Lets use the project's pdb_filename if it exists.
            elif hasattr(
                this_Project, "pdb_filename" and len(this_Project.pdb_file_name) > 0
            ):
                self.aaop_list[i].The_AAO.inputs = api.AmberMDPrep_Inputs(
                    pdb_file=this_Project.pdb_filename,
                    pUUID=this_Project.pUUID,
                    # TODO: create project directory and update inputFile selection.
                    outputDirPath=this_Project.upload_path + "/output",
                    inputFilesPath=this_Project.upload_path,
                )
                log.debug("Found 'pdb_filename' in this_Project: %s", aaop)
            # If we can't find a pdb_filename, then we can't do anything. Can we?
            else:
                pass

        log.debug(
            "Project with pUUID: %s processed by AmberMDPrep Request Data filler",
            this_Project.pUUID,
        )

        return self.aaop_list
