#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
from pathlib import Path

from gemsModules.common.project_manager import Project_Manager

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class mdaas_Project_Manager(Project_Manager):
    def process(self) -> MdProject:
        self.instantiate_response_project()
        # Broken:
        # self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity()

        return self.response_project

    def instantiate_response_project(self) -> MdProject:
        self.response_project = self.instantiate_new_project()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> MdProject:
        """This is a static method that returns a new project."""
        project = MdProject()
        project.add_temporary_info()
        return project

    # TODO: can probably be generalized and just pass the Project type.
    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            # need to combine instead of create new
            # self.response_project = MdProject(**self.incoming_project.dict())
            if self.response_project is None:
                self.response_project = self.instantiate_new_project()

            for key, value in self.incoming_project.dict().items():
                if key in self.response_project.dict().keys():
                    self.response_project.dict()[key] = value
                else:
                    log.warning("Key %s not in response project", key)

    def fill_response_project_from_response_entity(self):
        log.debug("fill_response_project_from_response_entity %s", self.incoming_entity)
        # Note: incoming entity may be wrong to use here.
        for service in self.incoming_entity.services.__root__.values():
            log.debug("fill_response_project_from_response_entity %s", service)
            
            #  Note: This may belong part of the WM, IT, or RDF.
            if service.typename == "RunMD":
                # TODO: Validate the service correctly within GEMS architecture...
               self.__handle_runmd_service(service)

            # Add request options to resposne project
            if hasattr(service, "options") and service.options is not None:
                if "sim_length" in service.options:
                    if not self.response_project.sim_length:
                        self.response_project.sim_length = str(
                            service.options["sim_length"]
                        )

    def __handle_runmd_service(self, service):
        # TODO: We don't do any actual fs operations until we finally service ProjectManagement.
        # There is a problem here in that files have their full paths throughout much of GEMS execution.
        # We currently have the full paths for the RDF which makes convenient use of them. 

        log.debug(f"project manager about to handle service: {service}")
        rst_path, parm_path = self.__handle_runmd_service_resources(service)

        if rst_path is None or parm_path is None:
            log.warning("RunMD service did not provide input resources, checking direct inputs...")
            rst_path, parm_path = self.__handle_runmd_service_inputs(service)

        self.response_project.upload_path = str(
            Path(rst_path).parent
            if rst_path
            else Path(parm_path).parent if parm_path else None
        )
    
    def __handle_runmd_service_inputs(self, service):
        # TODO/I: service.inputs aren't properly validated. This is not run_md_Inputs and it doesn't have these fields. It should be and it should define them.
        # TODO: This logic probably belongs in the Implicit Translator and should be translated to resources.
        log.debug(f"runmd inputs: {service.inputs}")
        if hasattr(service.inputs, "parameter-topology-file"):
            parm_path = Path(service.inputs["parameter-topology-file"])
            self.response_project.parm7_file_name = parm_path
        else:
            # TODO: Either set no path, or copy the payloaded input files to the project directory on run by PM.
            # We should be depending on Resource methods for this sort of logic.
            parm_path = None
            self.response_project.parm7_file_name = "MdInput.parm7"
            

        if hasattr(service.inputs, "input-coordinate-file"):
            rst_path = Path(service.inputs["input-coordinate-file"])
            self.response_project.rst7_file_name = rst_path

            # Part of a temporary MdProject.upload_path hack. TODO: Remove upload path? Hardcode full file paths in project?
            if parm_path and rst_path.parent != parm_path.parent:
                log.warning(
                    "Parm7/rst7 upload paths do not agree! Response upload path may be incorrect!"
                )
        else:
            # TODO: Like above, this is just for response project metadata.
            rst_path = None
            self.response_project.rst7_file_name = "MdInput.rst7"

        return rst_path, parm_path
    
    def __handle_runmd_service_resources(self, service):
        for resource in service.inputs.resources:
            if resource.resourceRole == "parameter-topology":
                self.response_project.parm7_file_name = resource.filename
            if resource.resourceRole == "input-coordinate":
                self.response_project.rst7_file_name = resource.filename
            if resource.resourceRole == "unminimized-gas":
                self.response_project.unsolvated_parm7_file_name = resource.filename

        return (
            self.response_project.rst7_file_name,
            self.response_project.parm7_file_name,
        )

def testme() -> MdProject:
    the_entity = MDaaS_Entity(type="MDaaS")
    the_project = MdProject()
    the_manager = mdaas_Project_Manager(entity=the_entity, incoming_project=the_project)
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
