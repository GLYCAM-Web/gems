#!/usr/bin/env python3
import importlib

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

## Leaving out:     "GpBuilder": glycoprotein, # for backwards compatibility
##                  replace if needed
MODULE_REGISTRY = {
    "MDaaS": "gemsModules.mmservice.mdaas.receive",
    "MmService": "gemsModules.mmservice.receive",
    "Status": "gemsModules.status.receive",
    "PDBFile": "gemsModules.structurefile.PDBFile.receive",
    "AntibodyDocking": "gemsModules.complex.antibody.receive",
    "Glycomimetics": "gemsModules.complex.glycomimetics.receive",
    "GlycoProtein": "gemsModules.conjugate.glycoprotein.receive",
    # Deprecated
    "BatchCompute": "DeprecatedDelegator",
    "Conjugate": "DeprecatedDelegator",
#    "DeprecatedDelegator": "DeprecatedDelegator", # generally not useful
    "DrawGlycan": "DeprecatedDelegator",
    "Query": "DeprecatedDelegator",
    "Sequence": "DeprecatedDelegator",
    "StructureFile": "DeprecatedDelegator",
}

def get_known_entities():
    return list(MODULE_REGISTRY.keys())

def get_receive_module(choice):
    module_path = MODULE_REGISTRY.get(choice)

    ############## I HAVE NOT TESTED THIS YET
    #
    # It allows a developer to use an environment variable to override the 
    #    module associated with an Entity. This allows easy A/B comparison
    #    between an old module and a new one. 
    #
    # Example Use: 
    #    You are updating the 'Status' module, working in this dev directory:
    #      ${GEMSHOME}/gemsModules/dev/status/
    #
    #    Be able to run GEMS code in two terminals. 
    #      * In one terminal, use the default behavior as defined above.
    #      * In the other, set this:
    #        export GEMS_OVERRIDE_Status="gemsModules.dev.status.receive"
    #
    #     !! Use `unset GEMS_OVERRIDE_Status` to stop the override.
    import os
    override = os.getenv(f"GEMS_OVERRIDE_{choice}")
    if override:
        log.info(f"Using DEV OVERRIDE for {choice}: {override}")
        module_path = override
    ############## END of untested part

    if not module_path:
        raise ValueError(f"No module found for choice: {choice}")

    try:
        # Dynamic import only happens here
        # Subsequent calls for the same choice are fast because 
        # Python caches imported modules in sys.modules.
    
        # If the module is deprecated, forward to the deprecated code
        if module_path == "DeprecatedDelegator" :
            module = importlib.import_module("gemsModules.deprecated.delegator.receive")
            return getattr(module, "delegate")
        
        # Otherwise, import as usual
        module = importlib.import_module(module_path)
        # Extract the 'receive' function from the loaded module and return that
        return getattr(module, "receive")
    except ImportError as e:
        log.error(f"Failed to load module for {choice} at {module_path}: {e}")
        raise
