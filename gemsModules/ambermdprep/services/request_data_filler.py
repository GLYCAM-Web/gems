#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.ambermdprep.main_api import AmberMDPrep_Entity
from gemsModules.ambermdprep.main_api_project import AmberMDPrepProject

from gemsModules.ambermdprep.services.prepare_pdb import api

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> List[AAOP]:
        this_Project: AmberMDPrepProject = self.project

        for i, aaop in enumerate(self.aaop_list):
            if aaop.Dictionary_Name == "any_amber_prep":
                self.aaop_list[i].The_AAO.inputs = api.prepare_pdb_Inputs(
                    pdb_file=aaop.The_AAO.inputs["pdb_filename"],
                    pUUID=this_Project.pUUID,
                    # Use defaults for now.
                    outputDirPath=aaop.The_AAO.inputs["outputDirPath"],
                    inputFilesPath=aaop.The_AAO.inputs["inputFilesPath"],
                )
                log.debug("Found any_amber_prep: %s", aaop)
            elif aaop.Dictionary_Name == "web_amber_prep":
                self.aaop_list[i].The_AAO.inputs = api.prepare_pdb_Inputs(
                    pdb_file=this_Project.pdb_file_name,
                    pUUID=this_Project.pUUID,
                    # Use defaults for now.
                    # outputDirPath=this_Project.project_dir,
                    # inputFilesPath=this_Project.upload_path,
                )

        return self.aaop_list
