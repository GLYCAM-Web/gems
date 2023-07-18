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
            self.aaop_list[i].The_AAO.inputs = api.AmberMDPrep_Inputs(
                pdb_file=aaop.The_AAO.inputs["pdb_filename"],
                pUUID=this_Project.pUUID,
                outputDirPath=aaop.The_AAO.inputs["outputDirPath"],
                inputFilesPath=aaop.The_AAO.inputs["inputFilesPath"],
            )

        return self.aaop_list
