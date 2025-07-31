import os
import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

ic = InstanceConfig()


def execute_gpb(project_dir: Path, pUUID) -> bool:
    """
    Executes the GpBuilder process using the provided input file and project directory.

    Args:
        input_file (Path): The path to the input file for GpBuilder.
        project_dir (Path): The directory where the project files are located.

    Returns:
        bool: Returns True if something failed while trying to run GpBuilder.
              Check produced status.log file for execution status.
    """
    log.debug(
        f"Executing GpBuilder for this project directory: {project_dir}"
    )
    
    GP_BUILDER = f"$GEMSHOME/gmml2/bin/gpBuilder"

    input_file = project_dir / "the_input.txt"
    if not input_file.exists():
        log.error(f"Input file does not exist: {input_file}")
        return True

    # Create an outputs directory if it doesn't exist
    outputs_dir = project_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    # Set up log files
    status_file = project_dir / "status.log"
    log_file = project_dir / "gpBuilder.log"
    err_file = project_dir / "gpBuilder.err"

    # Create bash script to run GpBuilder in background
    # TODO: parameterize/don't write to project dir
    bash_script = project_dir / "start_build.sh"
    
    gpbuilder_cmd = f"{GP_BUILDER} \"{input_file}\" \"{outputs_dir}\""
    build_script_str = f"""#!/bin/bash
# GpBuilder program execution script
echo "Working directory: {project_dir}" >>"{log_file}"
echo "Running command: {gpbuilder_cmd}" >>"{log_file}"
echo "GpBuilder execution started." >>"{status_file}"

# ensure $GEMSHOME is set
if [ -z "$GEMSHOME" ]; then
    echo "GEMSHOME environment variable is not set." >>"{err_file}"
    echo "Cannot run GpBuilder without GEMSHOME, please set it and run this script again." >>"{status_file}"
    exit 1
fi

# Run GpBuilder and capture output
{gpbuilder_cmd} >>"{log_file}" 2>>"{err_file}"
exit_code=$?

bash "$GEMSHOME/gemsModules/complex/GpBuilder/tasks/write_README.sh" "{project_dir}"

# Check for success message in run log
if grep -q "Program got to end ok" "{log_file}"; then
    echo "GpBuilder finished with: Success" >>"{status_file}"
else
    echo "GpBuilder finished with: Failure" >>"{status_file}"
    
    echo "GpBuilder exit code: $exit_code" >>"{err_file}"
fi

# Archive project
bash "$GEMSHOME/gemsModules/complex/GpBuilder/tasks/create_project_archive.sh" "{project_dir}" "{pUUID}"
zip_error=$?
if [ $zip_error -ne 0 ]; then
    echo "Failed to create project archive." >>"{status_file}"
    exit_code=$((exit_code + zip_error))
else
    echo "Project archive completed." >>"{status_file}"
fi    

# Final status message (Bug: The archive will not include these final messages.)
if [ $exit_code -eq 0 ]; then
    echo "All complete" >>"{status_file}"
else
    echo "Completed with errors. ($exit_code)" >>"{status_file}"
fi

exit $exit_code
"""

    with open(bash_script, "w") as f:
        f.write(build_script_str)

    bash_script.chmod(0o755)

    log.info(
        f"Submitting command to background: {gpbuilder_cmd}"
    )

    # Run the bash script in background, detached from parent
    subprocess.Popen(
        [str(bash_script)],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    log.info("GpBuilder submitted to background execution")


def execute_gpbt_wrapper(project_pdb_file: Path, output_file: Path):
    """
    Wrapper function to execute the gpBuilderTable program.

    This is used to generate the possible glycosylation sites for
    the given PDB file. We choose to output as csv here.

    This will be requested by the website.

    ./bin/gpBuilderTable /programs/gems/gmml2/tests/tests/inputs/018.4mbzEdit.pdb --format csv > someout.txt
    """
    GP_BUILDER_TABLE = os.path.expandvars("$GEMSHOME/gmml2/bin/gpBuilderTable")

    cmd = [GP_BUILDER_TABLE, str(project_pdb_file), "--format", "csv"]
    log.info(f"Running command: {' '.join(cmd)}")
    with open(output_file, "w") as out_file:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=out_file,
        )

    failed = result.returncode != 0
    
    if failed:
        log.error(f"gpBuilderTable failed with return code {result.returncode}")
    else:
        log.info(f"gpBuilderTable completed successfully, output written to {output_file}")
        
    return failed


if __name__ == "__main__":
    """Simplification of the GpBuilder workflow for testing purposes."""
    logging.basicConfig(level=logging.DEBUG)

    from gemsModules.complex.GpBuilder.tasks.generate_input_file import (
        execute as generate_input_file,
    )
    from gemsModules.complex.GpBuilder.services.Build.api import (
        Build_Inputs,
        BuildOptions,
        GlycanMapping,
    )

    # handle inputs and project dirs
    test_input_pdb = Path(
        "/programs/gems/gmml2/tests/tests/inputs/017.GlycoproteinBuilder/1eer_eop_Asn.pdb"
    )
    test_project_dir = Path("test_project_dir")
    possible_glycosylation_sites = test_project_dir / Path("possible_sites.csv")
    test_input_file = test_project_dir / "the_input.txt"

    test_project_dir.mkdir(exist_ok=True)

    # Generate the input file with GpBuilderTable
    execute_gpbt_wrapper(test_input_pdb, possible_glycosylation_sites)

    # select the first 3 possible glycosylation sites
    sites_to_select = 3
    sites = []
    with open(possible_glycosylation_sites) as f:
        lines = f.readlines()
        for line in lines[1 : 1 + sites_to_select]:
            line = line.strip()
            sites.append("_".join(line.split(",")[:2]))

    # Note: The website will have to allow users to select sites and
    # generate the sequences and send them to us.
    inputs = Build_Inputs(
        protein_file=str(test_input_pdb),
        glycan_mappings=[
            GlycanMapping(residue=site, sequence="DManpa1-OH") for site in sites
        ],
    )
    options = BuildOptions(number_of_samples=1, persist_cycles=1, seed=0)

    # Generate the input file for GpBuilder
    generate_input_file(test_project_dir, inputs, options)

    # Run GpBuilder with the generated input file
    execute_gpb(test_input_file, test_project_dir)
