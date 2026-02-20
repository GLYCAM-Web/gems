#!/usr/bin/env python3
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

# TODO: Replace with PM_Resource
from gemsModules.common.main_api_resources import Resource

from gemsModules.conjugate.glycoprotein.main_api import GlycoProtein_Entity
from gemsModules.conjugate.glycoprotein.main_api_project import GlycoProteinProject

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class GlycoProtein_Request_Data_Filler(Request_Data_Filler):
    def process(self, transaction) -> List[AAOP]: 
        log.info("GlycoProtein_Request_Data_Filler process was called")
        if self.transaction.inputs.project is None:
            log.error("!! The incoming project is None. This could be a problem")
            raise ValueError("Data filler requires the transaction's project to be initialized by now.")
        this_Project = self.transaction.inputs.project.copy(deep=True)
        
        log.debug(f"GpB/Request_Data_Filler now filling data for the request.")
        log.debug(f"GpB/Request_Data_Filler: {this_Project.project_dir=}")
        # We fill in the data in reverse, as dependents are at the end of the list.
        for i, aaop in enumerate(reversed(self.aaop_list)):
            log.debug(f"GpB/Request_Data_Filler: {i}: {aaop.AAO_Type=}")
            
            if aaop.The_AAO.inputs.pUUID is None:
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
            else:
                # if the pUUID is already set, we assume it's from a previous Evaluation request.
                # Honestly, it should never happen that the aaop's pUUID is different
                # and, the pUUID from the project should win anyway
                if aaop.The_AAO.inputs.pUUID != this_Project.pUUID :
                    log.debug(f"Build AAO.inputs has a pre-filled pUUID that is not the same as the project pUUID.")
                    log.debug(f"the The_AAO.inputs.pUUID: {aaop.The_AAO.inputs.pUUID}")
                    log.debug(f"the Project pUUID: {this_Project.pUUID}")
                    log.debug("This is unexpected and might cause trouble.")
#                this_Project.pUUID = aaop.The_AAO.inputs.pUUID
#                this_Project.add_filesystem_info()
#                log.debug(f"Updated project directory: {this_Project.project_dir=}")
            
            aaop.The_AAO.inputs.projectDir = this_Project.project_dir

            if aaop.AAO_Type=='Build':
                # copy inputs to resources
                aaop.The_AAO.inputs.force_serial_execution = self.transaction.inputs.entity.procedural_options.force_serial_execution
                aaop.The_AAO.inputs.uploadsPath = this_Project.uploads_path
                self.__fill_build_input_resources(aaop, this_Project.project_dir)
            elif aaop.AAO_Type=='Evaluate':
                aaop.The_AAO.inputs.uploadsPath = this_Project.uploads_path
                self.__fill_evaluate_input_resources(aaop)
            elif aaop.AAO_Type=='ProjectManagement':
                aaop.The_AAO.inputs.uploadsPath = this_Project.uploads_path
                self.__fill_projectman_input_resources(aaop)
                # copy resources from requester
                self.fill_resources_from_requester_if_exists(aaop, deep_copy=True)
#
# Eveything for Status should already exist.
#            elif aaop.AAO_Type=='Status':
#                if aaop.The_AAO.inputs.pUUID is None:
#                    log.error("GpB/Request_Data_Filler: Status service requires pUUID to be set.")
#                    raise ValueError("GpB/Request_Data_Filler: Status service requires pUUID to be set.")
#                else:
#                    this_Project.pUUID = aaop.The_AAO.inputs.pUUID
#                    this_Project.add_filesystem_info()
#                    aaop.The_AAO.inputs.projectDir = this_Project.project_dir
            
            log.debug(f"GpB/Request_Data_Filler filled: {aaop.The_AAO.inputs=}")
        
        return self.aaop_list

    def __fill_build_input_resources(self, aaop: AAOP, project_dir: str):
        log.info("GlycoProtein_Request_Data_Filler __fill_build_input_resources was called")
        log.debug(f" Filling build input resources for {aaop=}")
        if aaop.The_AAO.inputs.protein_file not in (None, ""):
            log.debug(f"Protein file found in inputs: {aaop.The_AAO.inputs.protein_file}")
            # if the protein file is set, we add it as a resource
            protein = Resource(
                payload=aaop.The_AAO.inputs.protein_file,
                resourceFormat="PDB",
                resourceRole="protein-file",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(protein)
        else:
            # See if there is a file already in the directory with a sym link
            log.debug(f"Protein file not set in inputs, trying to find OriginalInput.pdb in project directory {project_dir}.")
            # try to grab from the project dir by seeing what OriginalInput.pdb points to
            default_pdb = Path(project_dir) / "OriginalInput.pdb"
            if default_pdb.exists():
                # resolve the symlink to get the actual file
                if default_pdb.is_symlink():
                    default_pdb = default_pdb.resolve()
                log.debug(f"OriginalInput.pdb found at {default_pdb}, setting as protein file.")
                protein = Resource(
                    payload=default_pdb,
                    resourceFormat="PDB",
                    resourceRole="protein-file",
                    locationType="filesystem-path-unix"
                )
                aaop.The_AAO.inputs.resources.add_resource(protein)
                aaop.The_AAO.inputs.protein_file = str(default_pdb)
                log.debug(f"Set protein file to {aaop.The_AAO.inputs.protein_file} from OriginalInput.pdb.")
            else:
                log.debug(f"OriginalInput.pdb not found in project directory {project_dir}, looking for protein file by PDB ID.")
                ## TODO - this is a kluge. An evaluate service should be added (implied by Build, especially without a protein_file already).
                ##        At the moment, the handling of implied services (and responses) is not mature.
                ##        Earlier services should download the PDB file (if not already present) and copy it to the working directory.
                for service in self.transaction.inputs.entity.services.__root__.values():
                    if "rcsb_id" in service.inputs.keys() :
                        log.debug("Found rcsb_id in incoming request:")
                        log.debug(str(service.inputs))
                        if service.inputs["rcsb_id"] not in (None, "") :
                            log.debug(f"Setting the protein_file to {service.inputs['rcsb_id']}")
                            rcsb_id = service.inputs["rcsb_id"].strip().lower()
                            aaop.The_AAO.inputs.resources.add_resource( 
                                    Resource( 
                                        payload=rcsb_id, 
                                        resourceFormat="RCSB-ID", 
                                        resourceRole="rcsb-id", 
                                        locationType="Payload"
                                        )
                                    )
                            log.debug(f"Attempting to download the PDB file {service.inputs['rcsb_id']}")
                            from gemsModules.conjugate.glycoprotein.tasks import download_pdb_from_rcsb_by_id
                            the_protein_file = download_pdb_from_rcsb_by_id.execute(
                                pdb_id=rcsb_id,
                                output_dir=aaop.The_AAO.inputs.projectDir,
                                #output_dir=aaop.The_AAO.inputs.uploadsPath,
                                compressed=False
                                )
                            if the_protein_file is None :
                                log.debug("Could not download the PDB from the RCSB.")
                            else :
                                aaop.The_AAO.inputs.protein_file = the_protein_file
                                aaop.The_AAO.inputs.resources.add_resource(
                                    Resource(
                                        payload=the_protein_file,
                                        resourceFormat="PDB",
                                        resourceRole="protein-file",
                                        locationType="filesystem-path-unix"
                                    )
                                )

        if aaop.The_AAO.inputs.glycan_mappings is not None:
            mappings = Resource(
                payload=aaop.The_AAO.inputs.glycan_mappings,
                resourceFormat="python-dict",
                resourceRole="glycan-mappings",
                locationType="Payload"
            )
            aaop.The_AAO.inputs.resources.add_resource(mappings)

    def __fill_evaluate_input_resources(self, aaop: AAOP):
        log.info("GlycoProtein_Request_Data_Filler __fill_evaluate_input_resources was called")
        log.debug(f" Filling evaluate input resources for {aaop=}")
        
        rcsb_id = aaop.The_AAO.inputs.rcsb_id
        if rcsb_id:
            rcsb_id = rcsb_id.strip().lower()
        
        given_protein_file = aaop.The_AAO.inputs.protein_file
        
        if given_protein_file is None and rcsb_id is None:
            log.warning("Neither protein_file nor rcsb_id is set in inputs, no protein file will be set in resources.")
        else:
            log.warning("Both protein_file and rcsb_id are set in inputs, keeping RCSB ID and updating protein_file.")

        if rcsb_id:
            log.debug(f"RCSB ID found in inputs: {rcsb_id}")
            # if the rcsb_id is set, we assume the protein file will be downloaded later
            aaop.The_AAO.inputs.resources.add_resource(
                Resource(
                    payload=rcsb_id,
                    resourceFormat="RCSB-ID",
                    resourceRole="rcsb-id",
                    locationType="Payload"
                )
            )
            given_protein_file = None
            
        if given_protein_file:
            log.debug(f"Protein file found in inputs: {given_protein_file}")
            aaop.The_AAO.inputs.resources.add_resource(
                Resource(
                    payload=given_protein_file,
                    resourceFormat="PDB",
                    resourceRole="protein-file",
                    locationType="filesystem-path-unix"
                )
            )


        
        
    def __fill_projectman_input_resources(self, aaop: AAOP):
        log.info("GlycoProtein_Request_Data_Filler __fill_projectman_input_resources was called")
        log.debug(f" Filling project management input resources for {aaop=}")

        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "request.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)
