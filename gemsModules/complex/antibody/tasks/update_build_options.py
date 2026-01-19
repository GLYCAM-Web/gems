from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def execute(options, workdir):
    """Executes the service."""
    
    replacements = {}
    
    if "Number_of_Replicas" in options:
        # TODO: Ensure this is an int, add notice if not.
        replacements["Number_of_Replicas"] = str(options["Number_of_Replicas"])
    else:
        log.warning("Number_of_Replicas not found in AntibodyDocking/Build options")
        raise ValueError("Number_of_Replicas not found in AntibodyDocking/Build options")
    if "Glycan_Flexibility" in options:
        g_flex = str(options["Glycan_Flexibility"])
        replacements["Glycan_Flexibility"] = g_flex
        if g_flex not in ["Rigid", "Flexible", "Partial"]:
            log.warning(f"Invalid Glycan_Flexibility value: {g_flex}")
            raise ValueError(f"Invalid Glycan_Flexibility value: {g_flex}")
    else:
        log.warning("Glycan_Flexibility not found in AntibodyDocking/Build options")
        raise ValueError("Glycan_Flexibility not found in AntibodyDocking/Build options")
        
    replace_bash_variable_in_file(f"{workdir}/ad2config", replacements)