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
            # This may belong part of the WM, IT, or RDF.
            if service.typename == "RunMD":
               self.__handle_runmd_service(service)
            if hasattr(service, "options") and service.options is not None:
                if "sim_length" in service.options:
                    if not self.response_project.sim_length:
                        self.response_project.sim_length = str(
                            service.options["sim_length"]
                        )

    def __handle_runmd_service(self, service):
        # The problem with setting the files here is that then they have their full paths,
        # and we still need the full paths for the RDF...
        if service.inputs["parameter-topology-file"]["locationType"] in [
            "File",
            "filesystem-path-unix",
        ]:
            parm_path = Path(
                service.inputs["parameter-topology-file"]["payload"]
            )
            self.response_project.parm7_file_name = str(parm_path.name)
        else:
            # TODO: Either set no path, or copy the payloaded input files to the project directory on run by PM.
            # None for now
            parm_path = None
            self.response_project.parm7_file_name = "MdInput.parm7"

        if service.inputs["input-coordinate-file"]["locationType"] in [
            "File",
            "filesystem-path-unix",
        ]:
            rst_path = Path(service.inputs["input-coordinate-file"]["payload"])
            self.response_project.rst7_file_name = str(rst_path.name)

            # Part of a temporary MdProject.upload_path hack. TODO: Remove upload path? Hardcode full file paths in project?
            if parm_path and rst_path.parent != parm_path.parent:
                log.warning(
                    "Parm7/rst7 upload paths do not agree! Response upload path may be incorrect!"
                )
        else:
            # TODO: Like above, this is just for response project metadata.
            rst_path = None
            self.response_project.rst7_file_name = "MdInput.rst7"

        self.response_project.upload_path = str(
            rst_path.parent
            if rst_path
            else parm_path.parent if parm_path else None
        )

def testme() -> MdProject:
    the_entity = MDaaS_Entity(type="MDaaS")
    the_project = MdProject()
    the_manager = mdaas_Project_Manager(entity=the_entity, incoming_project=the_project)
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
