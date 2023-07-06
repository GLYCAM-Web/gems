#!/usr/bin/env python3
from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import (
    AmberMDPrep_Request,
    AmberMDPrep_Response,
)

from gemsModules.systemoperations.filesystem_ops import separate_path_and_filename

# from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory
# from gemsModules.mmservice.mdaas.tasks import initiate_build
from gemsModules.structurefile.PDBFile.services.AmberMDPrep.logic import execute
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: AmberMDPrep_Request) -> AmberMDPrep_Response:
    # set_up_prepare_pdb_directory.execute(
    #     protocol_files_dir=service.inputs.protocolFilesPath,
    #     output_dir_path=service.inputs.outputDirPath,
    #     uploads_dir_path=service.inputs.inputFilesPath,
    #     parm7_real_name=service.inputs.amber_parm7,
    #     rst7_real_name=service.inputs.amber_rst7,
    # )
    # initiate_build.execute(
    #     pUUID=service.inputs.pUUID,
    #     outputDirPath=service.inputs.outputDirPath,
    #     use_serial=True,
    # )

    response = AmberMDPrep_Response()
    response.outputs.message = execute(service.inputs)
    # response.outputs.outputDirPath = separate_path_and_filename(
    #     service.inputs["output_filename"]
    # )[0]

    log.debug(f"AmberMDPrep prepare_pdb_Response: {response}")
    return response
