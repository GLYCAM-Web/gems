#!/usr/bin/env python3
from pathlib import Path
import sys
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs
from ..common_api import Modification_Position


log = Set_Up_Logging(__name__)


# Not working.
@validate_arguments
def execute(inputs: Evaluate_Inputs) -> Evaluate_Outputs:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    # TODO: Handle pUUID
    # if inputs.pUUID:
    #     pass

    receptor_pdb_resource = None
    for resource in inputs.resources:
        if resource.resourceRole == "Receptor":
            receptor_pdb_resource = resource
            

    if not receptor_pdb_resource:
        # Append a notice, we can do nothing else.
        service_notices.addNotice(
            Brief="No Receptor PDB Resource",
            Scope="Service",
            Messenger="Glycomimetics",
            Type="Info",
            Code="600",
            Message="No Receptor PDB was provided to Glycomimetics, nothing to do.",
        )
    else:
        # Evaluation
        result = None
        if receptor_pdb_resource.locationType != "filesystem-path-unix":
            service_notices.addNotice(
                Brief="current Receptor PDB Resource Location type not supported",
                Scope="Service",
                Messenger="Glycomimetics",
                Type="Error",
                Code="601",
                Message="Receptor PDB Resource must be a filesystem path.",
            )
        else:   
            pdb_fpath = receptor_pdb_resource.payload
            if Path(pdb_fpath).exists():
                log.debug(f"Receptor PDB file found: {pdb_fpath}")
                try:
                    # TODO: Properly include glycomimetic external programs and wrappers with DevENv.
                    # We need Yao's "Validation" for this service.
                    sys.path.append("/programs/gems/External/GM_Utils/external_programs/validation/evaluate_swig")
                    from evaluate_pdb import evaluate_pdb

                    result = evaluate_pdb(pdb_fpath)
                    for atom in result.available_atoms:
                        log.debug(f"atom: {atom}")
                        posmod = Modification_Position(
                            Residue_Identifier=atom.residue_index_str_,
                            Residue_Name=atom.resname_,
                            Chain_Identifier=atom.chain_id_,
                            Attachment_Atom=atom.atom_name_,
                            Replaced_Atom=atom.atom_to_replace_,
                        )
                        service_outputs.Available_Modification_Options.append(posmod)
                except Exception as e:
                    service_notices.addNotice(
                        Brief="Error during Evaluation",
                        Scope="Service",
                        Messenger="Glycomimetics",
                        Type="Error",
                        Code="602",
                        Message=f"Error during Evaluation: {e}",
                    )
                log.debug(f"Evaluation Result: {result}")
            else:
                log.debug(f"Receptor PDB file not found: {pdb_fpath}")

    log.debug(f"service_outputs: {service_outputs}")
    return service_outputs, service_notices
