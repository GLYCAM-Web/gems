#!/usr/bin/env python3
from gemsModules.systemoperations.module_import import ModuleData, ModuleLoader

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


REGISTRY = {
    "MDaaS": ModuleData('gemsModules.mmservice.mdaas.receive', 'receive'),
    "MmService": ModuleData('gemsModules.mmservice.receive', 'receive'),
    "Status": ModuleData('gemsModules.status.receive', 'receive'),
    "PDBFile": ModuleData('gemsModules.structurefile.PDBFile.receive', 'receive'),
    "AntibodyDocking": ModuleData('gemsModules.complex.antibody.receive', 'receive'),
    "Glycomimetics": ModuleData('gemsModules.complex.glycomimetics.receive', 'receive'),
    "GlycoProtein": ModuleData('gemsModules.conjugate.glycoprotein.receive', 'receive'),
    # Deprecated
    "BatchCompute": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
    "Conjugate": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
    "DrawGlycan": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
    "Query": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
    "Sequence": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
    "StructureFile": ModuleData('gemsModules.deprecated.delegator.receive', 'delegate'),
}


module_loader = ModuleLoader(REGISTRY)


def get_known_entities():
    return list(REGISTRY.keys())


####################################################################################
##  Add the following if possible
####################################################################################
#    # This might have mechanical or other errors.
#    #
#    # It allows a developer to use an environment variable to override the 
#    #    module associated with an Entity. This allows easy A/B comparison
#    #    between an old module and a new one. 
#    #
#    # Example Use: 
#    #    You are updating the 'Status' module, working in this dev directory:
#    #      ${GEMSHOME}/gemsModules/dev/status/
#    #
#    #    Be able to run GEMS code in two terminals. 
#    #      * In one terminal, use the default behavior as defined above.
#    #      * In the other, set this:
#    #        export GEMS_OVERRIDE_module_Status="gemsModules.dev.status.receive"
#    #        export GEMS_OVERRIDE_attr_Status="receive"
#    #
#    #     !! To stop the override, use
#    #        unset GEMS_OVERRIDE_module_Status 
#    #        unset GEMS_OVERRIDE_attr_Status 
#    import os
#    override_module = os.getenv(f"GEMS_OVERRIDE_module_{choice}")
#    override_attr = os.getenv(f"GEMS_OVERRIDE_attr_{choice}")
#    if override:
#        log.info(f"Using DEV OVERRIDE for {choice}: {override_module}.{override_attr}")
#        module_path = override_module
#     .... get the attr ... (How? see the imported file, above, and delegator's receive)
####################################################################################
##  End of add if possible
####################################################################################

