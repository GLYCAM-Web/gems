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
            # Theoretically, we're duplicating explicit_requests.py logic here, Is this how we should wrap inputs?
            if "pdb_filename" in aaop.The_AAO.inputs:
                if "outputDirPath" in aaop.The_AAO.inputs:
                    # I don't think we should be grabbing inputs from the aaop like this?
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
        log.debug(
            "Project with pUUID: %s processed by AmberMDPrep Request Data filler",
            this_Project.pUUID,
        )

        return self.aaop_list
