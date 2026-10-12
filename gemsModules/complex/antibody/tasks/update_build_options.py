from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def execute(options, workdir):
    """Executes the service."""
    
    replacements = {}
    
    num_replicas = options.get("Number_of_Replicas", options.get("count"))
    if num_replicas is not None:
        replacements["Number_of_Replicas"] = str(num_replicas)
    else:
        log.warning("Number_of_Replicas not found in AntibodyDocking/Build options")
        raise ValueError("Number_of_Replicas not found in AntibodyDocking/Build options")

    glycan_flex = options.get("Glycan_Flexibility", options.get("flexibility"))
    if glycan_flex is not None:
        raw_val = glycan_flex.value if hasattr(glycan_flex, "value") else str(glycan_flex)
        g_flex = raw_val.capitalize()
        replacements["Glycan_Flexibility"] = g_flex
        if g_flex not in ["Rigid", "Flexible", "Partial"]:
            log.warning(f"Invalid Glycan_Flexibility value: {g_flex}")
            raise ValueError(f"Invalid Glycan_Flexibility value: {g_flex}")
    else:
        log.warning("Glycan_Flexibility not found in AntibodyDocking/Build options")
        raise ValueError("Glycan_Flexibility not found in AntibodyDocking/Build options")
        
    replace_bash_variable_in_file(f"{workdir}/ad2config", replacements)