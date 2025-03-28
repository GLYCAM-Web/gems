from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file

def execute(options, workdir):
    replacements = {
        "Number_of_Replicas": str(options['count']),
        "Glycan_Flexibility": str(options['flexibility']),
    }
    replace_bash_variable_in_file(f"{workdir}/ad2config", replacements)