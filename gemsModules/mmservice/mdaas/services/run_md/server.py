#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.services.run_md.api import run_md_Request, run_md_Response

from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory
from gemsModules.mmservice.mdaas.tasks import initiate_build

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : run_md_Request) -> run_md_Response:

    set_up_run_md_directory.execute(protocol_files_dir=service.inputs.protocolFilesPath, 
                                    output_dir_path=service.inputs.outputDirPath,  
                                    uploads_dir_path=service.inputs.inputFilesPath, 
                                    parm7_real_name=service.inputs.amber_parm7, 
                                    rst7_real_name=service.inputs.amber_rst7  
    )
    initiate_build.execute(pUUID=service.inputs.pUUID,
                           outputDirPath=service.inputs.outputDirPath, 
                           use_serial=True, 
                           )
                   
                                    

    