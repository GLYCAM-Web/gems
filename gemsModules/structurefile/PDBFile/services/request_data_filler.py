#!/usr/bin/env python3
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project

from gemsModules.structurefile.PDBFile.services.AmberMDPrep import api

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> list[AAOP]:
        this_Project: PDBFile_Project = self.project

        for i, aaop in enumerate(self.aaop_list):
            # Use the pUUID to get a project
            if (
                "pUUID"
                in aaop.The_AAO.inputs  #  Should we make a utility function for optional keys or do this check another way?
                and aaop.The_AAO.inputs["pUUID"] is not None
            ):
                # TODO: get the project by pUUID
                root = this_Project.project_dir
                output_root = root
            # Attempt to use the inputFilePath and outputFilePath otherwise use the general project directory
            else:
                root = this_Project.project_dir
                if (
                    "inputFilePath" in aaop.The_AAO.inputs
                    and aaop.The_AAO.inputs["inputFilePath"] is not None
                ):
                    root = aaop.The_AAO.inputs["inputFilePath"]

                output_root = this_Project.project_dir
                if (
                    "outputFilePath" in aaop.The_AAO.inputs
                    and aaop.The_AAO.inputs["outputFilePath"] is not None
                ):
                    # Q: deprecate this ability to write to arbitrary paths?
                    output_root = aaop.The_AAO.inputs["outputFilePath"]

            # update output file name
            if (
                "outputFileName" in aaop.The_AAO.inputs
                and aaop.The_AAO.inputs["outputFileName"] is not None
            ):
                out_filename = aaop.The_AAO.inputs["outputFileName"]
            else:
                out_filename = f"preprocessed.{aaop.The_AAO.inputs['pdb_filename']}"

            # create actual request inputs
            self.aaop_list[i].The_AAO.inputs = api.AmberMDPrep_Inputs(
                pdb_file=aaop.The_AAO.inputs["pdb_filename"],
                outputFileName=out_filename,
                pUUID=this_Project.pUUID,  # Q: Should we just pass the project_dir? That way we can copy the file to the project dir in a task. (w/o some pUUID project registry)
                outputFilePath=output_root,
                inputFilePath=root,
            )

        return self.aaop_list
