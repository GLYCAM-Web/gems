#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
import os

from gemsModules.common.project_manager import Project_Manager

from gemsModules.conjugate.glycoprotein.main_api import GlycoProtein_Entity
from gemsModules.conjugate.glycoprotein.main_api_project import GlycoProteinProject

from gemsModules.systemoperations.filesystem_ops import check_make_directory

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class GlycoProtein_Project_Manager(Project_Manager):

    def process(self) -> GlycoProteinProject:
        log.info("Project management for GlycoProtein_Project_Manager is begun")

        if self.incoming_project is not None:
            foundUUID = None
            serviceType = None
            for service in self.incoming_entity.services.__root__.values():
                if "pUUID" in service.inputs.keys() :
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
            self.response_project = GlycoProteinProject()
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


    # This happens at the very end of the transaction's processing
    def fill_response_project_from_response_entity(self, responseProject: GlycoProteinProject, responseEntity: GlycoProtein_Entity):
        log.info("Final fill of response project for GlycoProtein_Project_Manager is begun")
        self.response_project = responseProject
        for response in responseEntity.responses.__root__.values():
            if response.typename == "Status" :
                self.response_project.status = response.outputs.status
        return self.response_project



def testme() -> GlycoProteinProject :
    the_entity=GlycoProtein_Entity(type="GlycoProtein")
    the_project=GlycoProteinProject()
    the_manager=GlycoProtein_Project_Manager(entity=the_entity, project=the_project)
    return the_manager.instantiate_new_project()

if __name__ == "__main__":
    project=testme()
    print(project.json(indent=2))
