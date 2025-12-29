#!/usr/bin/env python3
from typing import Optional
from pathlib import Path
from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices, Notice
from gemsModules.logging.logger import Set_Up_Logging

from .api import Status_Inputs, Status_Outputs, Status_Options


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Status_Inputs, options: Optional[Status_Options]) -> tuple[Status_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Status_Outputs()
    service_notices = Notices()
    
    status_file = inputs.projectDir + "/status.log"
    
    try:
        with open(status_file, 'r') as f:
            status_content = f.read()
            lines = status_content.strip().split('\n')
            
            # Get the last line as status
            if lines:
                service_outputs.status = lines[-1]
                log.info(f"Status found: {lines[-1]}")
            else:
                service_outputs.status = None
                log.warning("Status file is empty.")
            
            # Check for GpBuilder failure and add notice if needed
            success = True
            for line in lines:
                if "GpBuilder finished with: Failure" in line or "GpBuilder execution failed" in line:
                    success = False
                    error_file_path = inputs.projectDir + "/GpBuilder.err"
                    try:
                        with open(error_file_path, 'r') as err_f:
                            error_content = err_f.read().strip()
                            error_lines = error_content.split('\n')
                            last_error_line = error_lines[-1]
                            service_notices.append(Notice(
                                brief="GpBuilder failure detected",
                                message=f"GpBuilder execution failed with error: {last_error_line}",
                                scope="Service",
                                Messenger="GpBuilder",
                                type="Error",
                                code="500",
                            ))
                            log.error(f"GpBuilder failure detected. Error: {last_error_line}")
                    except FileNotFoundError:
                        log.error(f"GpBuilder.err file not found: {error_file_path}")
                    break
                elif "GpBuilder finished with: Success" in line:
                    success = True
                    break
            
            if success:
                service_notices.append(Notice(
                    brief="GpBuilder success",
                    message="GpBuilder completed without errors.",
                    scope="Service",
                    Messenger="GpBuilder",
                    type="Info",
                    code="200",
                ))
                log.info("GpBuilder finished successfully.")
                if service_outputs.status is None:
                    service_outputs.status = "GpBuilder finished successfully."
            else:
                service_notices.append(Notice(
                    brief="GpBuilder failure",
                    message="GpBuilder execution failed.",
                    scope="Service",
                    Messenger="GpBuilder",
                    type="Error",
                    code="500",
                ))
                log.error("GpBuilder execution failed.")
                if service_outputs.status is None:
                    service_outputs.status = "GpBuilder execution failed."
               
                    
    except FileNotFoundError:
        service_outputs.status = "Status file not found"
        log.error(f"Status file not found: {status_file}")
        
    return service_outputs, service_notices