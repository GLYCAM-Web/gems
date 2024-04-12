#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
from pathlib import Path

from gemsModules.common.project_manager import Project_Manager

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Project_Manager(Project_Manager):
    def process(self) -> GlycomimeticsProject:
        self.instantiate_response_project()
        # Broken:
        # self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity()

        return self.response_project

    def instantiate_response_project(self) -> GlycomimeticsProject:
        self.response_project = self.instantiate_new_project()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> GlycomimeticsProject:
        """This is a static method that returns a new project."""
        project = GlycomimeticsProject()
        project.add_temporary_info()
        return project

    # TODO: can probably be generalized and just pass the Project type.
    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            # need to combine instead of create new
            # self.response_project = GlycomimeticsProject(**self.incoming_project.dict())
            if self.response_project is None:
                self.response_project = self.instantiate_new_project()

            for key, value in self.incoming_project.dict().items():
                if key in self.response_project.dict().keys():
                    self.response_project.dict()[key] = value
                else:
                    log.warning("Key %s not in response project", key)

    def fill_response_project_from_response_entity(self):
        # Lets try updating from Build inputs for now... # TODO: incoming entity may be wrong to use here.
        log.debug("fill_response_project_from_response_entity %s", self.incoming_entity)
        for service in self.incoming_entity.services.__root__.values():
            log.debug("fill_response_project_from_response_entity %s", service)
            if service.typename == "Build":
                ...
                # # THe problem with setting the files here is that then they have their full paths,
                # # and we still need the full paths for the RDF...
                # parm_path = Path(service.inputs["parameter-topology-file"]["payload"])
                # rst_path = Path(service.inputs["input-coordinate-file"]["payload"])

                # # Part of a temporary GlycomimeticsProject.upload_path hack. TODO: Remove upload path? Hardcode full file paths in project?
                # if rst_path.parent != parm_path.parent:
                #     log.warning(
                #         "Parm7/rst7 upload paths do not agree! Response upload path may be incorrect!"
                #     )
                # self.response_project.upload_path = str(rst_path.parent)

                # self.response_project.parm7_file_name = str(parm_path.name)
                # self.response_project.rst7_file_name = str(rst_path.name)
                # if hasattr(service, "options") and service.options is not None:
                #     if "sim_length" in service.options:
                #         self.response_project.sim_length = str(
                #             service.options["sim_length"]
                #        )


def testme() -> GlycomimeticsProject:
    the_entity = Glycomimetics_Entity(type="Glycomimetics")
    the_project = Glycomimetics_Entity()
    the_manager = Glycomimetics_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
