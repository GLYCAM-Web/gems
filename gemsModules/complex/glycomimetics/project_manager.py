#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
from pathlib import Path
import os

from gemsModules.common.project_manager import Project_Manager

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from gemsModules.systemoperations.filesystem_ops import check_make_directory

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Project_Manager(Project_Manager):
    def process(self) -> GlycomimeticsProject:
        log.info("Project management for Glycomimetics_Project_Manager is begun")

        if self.incoming_project is not None:
            foundUUID = None
            serviceType = None
            for service in self.incoming_entity.services.__root__.values():
                log.debug("The current service looks like:")
                log.debug(str(service))
                if service.inputs.pUUID not in (None, "") :
                    log.debug("Found pUUID in incoming request:")
                    log.debug(str(service.inputs))
                    if service.inputs["pUUID"] not in (None, "") :
                        log.debug(f"Setting the pUUID to {service.inputs['pUUID']}")
                        if foundUUID in (None, "") :
                            foundUUID = service.inputs['pUUID']
                            serviceType = service.typename
                        else :
                            log.error("Conflicting pUUID values found in services. They are:")
                            log.error(f"service: {serviceType} - pUUID {foundUUID}")
                            log.error(f"service: {service.typename} - pUUID {service.inputs['pUUID']}")
                            raise ValueError ("Service inputs have conflicting pUUIDs")
                        self.incoming_project.pUUID = foundUUID

            self.incoming_project.setProjectDir(noClobber=False)
            self.incoming_project.logs_dir = str(os.path.join(self.incoming_project.project_dir, "logs"))

            self.fill_response_project_from_incoming_project()
            log.debug("The incoming project is:")
            log.debug(self.incoming_project.json(indent=2))
            log.debug("The response project is:")
            log.debug(self.response_project.json(indent=2))
        else:
            self.response_project = GlycomimeticsProject()
        if self.incoming_project.project_dir not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.project_dir)
        else:
            log.error("Project directory not specified")
        if self.incoming_project.uploads_path not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.uploads_path)
        else:
            log.error("Uploads path not specified")
        if self.incoming_project.logs_dir not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.logs_dir)
        else:
            log.error("Logging directory for the project is not specified")
        return self.response_project


        # log.debug("Glycomimetics_Project_Manager.process")
        # log.debug("incoming_entity: %s", self.incoming_entity)
        # log.debug("incoming_project: %s", self.incoming_project)
        
#        self.instantiate_response_project()
#        # Broken:
#        # self.fill_response_project_from_incoming_project()
#        # self.fill_response_project_from_response_entity()
#
#        return self.response_project
#
#    def instantiate_response_project(self) -> GlycomimeticsProject:
#        self.response_project = self.instantiate_new_project()
#
#        return self.response_project
#
#    @staticmethod
#    def instantiate_new_project() -> GlycomimeticsProject:
#        """This is a static method that returns a new project."""
#        project = GlycomimeticsProject()
#        project.add_filesystem_info()
#        return project
#
#    # TODO: can probably be generalized and just pass the Project type.
#    def fill_response_project_from_incoming_project(self):
#        pass
#        if self.incoming_project is not None:
#            # need to combine instead of create new
#            # self.response_project = GlycomimeticsProject(**self.incoming_project.dict())
#            if self.response_project is None:
#                self.response_project = self.instantiate_new_project()
#
#            for key, value in self.incoming_project.dict().items():
#                if key in self.response_project.dict().keys():
#                    self.response_project.dict()[key] = value
#                else:
#                    log.warning("Key %s not in response project", key)

    def fill_response_project_from_response_entity(self, responseProject: GlycomimeticsProject, responseEntity: Glycomimetics_Entity):
        # TODO: incoming entity may be wrong to use here.
        log.debug("fill_response_project_from_response_entity %s", self.incoming_entity)
        self.response_project = responseProject
        for response in responseEntity.responses.__root__.values():
            if response.typename == "Status" :
                self.response_project.status = response.outputs.status
        return self.response_project

        # # Bad hack... # TODO: Ensure the IT fills inputs from resources before the PM? and ignore resources here?
        # inputs_needed = ["complex", "receptor", "ligand"]
        # for service in self.incoming_entity.services.__root__.values():
        #     log.debug("fill_response_project_from_response_entity %s", service)
        #     if hasattr(service.inputs, "complex_PDB_Filename"):
        #         self.response_project.complex = service.inputs.complex_PDB_Filename
        #         inputs_needed.remove("complex")
        #     if hasattr(service.inputs, "receptor_PDB_Filename"):
        #         self.response_project.receptor = service.inputs.receptor_PDB_Filename
        #         inputs_needed.remove("receptor")
        #     if hasattr(service.inputs, "ligand_PDB_Filename"):
        #         self.response_project.ligand = service.inputs.ligand_PDB_Filename
        #         inputs_needed.remove("ligand")
        #     if not len(inputs_needed):
        #         break

        # if len(inputs_needed):
        #     # Do we need to try to get from inputs.resources?
        #     # for resource in service.inputs.resources.__root__:
        #     #     if resource.resourceRole == "cocomplex":
        #     #         self.response_project.cocomplex = resource.payload
        #     #         inputs_needed.remove("cocomplex")
        #     #     elif resource.resourceRole == "moiety":
        #     #         self.response_project.moiety = resource.payload
        #     #         inputs_needed.remove("moiety")
        #     #     if not len(inputs_needed):
        #     #         break
        #     log.warning(f"Could not find all inputs: {inputs_needed}. ")


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
