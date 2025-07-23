import os
import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

ic = InstanceConfig()


def execute_gpb(input_file: Path, project_dir: Path, pUUID) -> bool:
    """
    Executes the GpBuilder process using the provided input file and project directory.

    Args:
        input_file (Path): The path to the input file for GpBuilder.
        project_dir (Path): The directory where the project files are located.

    Returns:
        bool: Always returns False (success) since we don't wait for completion.
              Check produced status.log file for execution status.
    """
    log.debug(
        f"Executing GpBuilder with input file: {input_file} in project directory: {project_dir}"
    )

    GEMSHOME = os.getenv("GEMSHOME")
    if not GEMSHOME:
        log.error("GEMSHOME environment variable is not set. Please set it.")
        return True
    GP_BUILDER = f"{GEMSHOME}/gmml2/bin/gpBuilder"

    status_file = project_dir / "status.log"

    # Create an outputs directory if it doesn't exist
    outputs_dir = project_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    # Set up log files
    log_file = project_dir / "gpbuilder.log"
    err_file = project_dir / "gpbuilder.err"

    # Create bash script to run GpBuilder in background
    # TODO: parameterize/don't write to project dir
    bash_script = project_dir / "start_build.sh"
    script_content = f"""#!/bin/bash
echo "Running command: {GP_BUILDER} {input_file} {outputs_dir}" >> "{log_file}"
echo "Working directory: {project_dir}" >> "{log_file}"
echo "GpBuilder execution started." >> "{err_file}"
echo "GpBuilder execution started." >> "{status_file}"

# Run GpBuilder and capture output
"{GP_BUILDER}" "{input_file}" "{outputs_dir}" >> "{log_file}" 2>> "{err_file}"
exit_code=$?

# Check for success message in log
if grep -q "Program got to end ok" "{log_file}"; then
    echo "GpBuilder finished with: Success" >> "{status_file}"
else
    echo "GpBuilder finished with: Failure" >> "{status_file}"
fi

# Archive project
bash "$GEMSHOME/gemsModules/complex/GpBuilder/tasks/create_project_archive.sh" "{project_dir}" "{pUUID}"

# Write "Project archive completed."
echo "Project archive completed." >> "{status_file}"

# Write All complete to status log
echo "All complete" >> "{status_file}"

exit $exit_code
"""

    with open(bash_script, "w") as f:
        f.write(script_content)

    bash_script.chmod(0o755)

    log.info(
        f"Submitting command to background: {GP_BUILDER} {input_file} {outputs_dir}"
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
    return False  # Return immediately indicating successful submission


def execute_gpbt_wrapper(project_pdb_file: Path, output_file: Path):
    """
    Wrapper function to execute the gpBuilderTable program.

    This is used to generate the possible glycosylation sites for
    the given PDB file. We choose to output as csv here.

    This will be requested by the website.

    ./bin/gpBuilderTable /programs/gems/gmml2/tests/tests/inputs/018.4mbzEdit.pdb --format csv > someout.txt
    """
    # TODO: Use $GEMSHOME
    GP_BUILDER_TABLE = "/programs/gems/gmml2/bin/gpBuilderTable"

    cmd = [GP_BUILDER_TABLE, str(project_pdb_file), "--format", "csv"]
    log.info(f"Running command: {' '.join(cmd)}")
    with open(output_file, "w") as out_file:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=out_file,
        )
    log.info(f"gpBuilderTable completed successfully, output written to {output_file}")

    failed = result.returncode != 0
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
