import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

ic = InstanceConfig()


def execute_gpb(input_file: Path, project_dir: Path):
    GP_BUILDER = "/programs/gems/gmml2/bin/gpBuilder"

    outputs_dir = project_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    cmd = [GP_BUILDER,str(input_file), str(outputs_dir)]
    log.info(f"Running command: {' '.join(cmd)}")
    
    log_file = project_dir / "gpbuilder.log"
    err_file = project_dir / "gpbuilder.err"
    with open(log_file, "w") as log_out, open(err_file, "w") as err_out:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
        )
        log_out.write(result.stdout.decode())
        if result.stderr:
            err_out.write(result.stderr.decode())
            
    if result.returncode != 0:
        log.error(f"gpBuilder failed with return code {result.returncode}. Check {err_file} for details.")
    else:
        log.info(f"gpBuilder completed successfully.")



def execute_gpbt_wrapper(project_pdb_file: Path, output_file: Path):
    """
    Wrapper function to execute the gpBuilderTable process.
    
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
    
    
if __name__ == "__main__":
    """Simplification of the GpBuilder workflow for testing purposes."""
    logging.basicConfig(level=logging.DEBUG)
    
    from gemsModules.complex.GpBuilder.tasks.generate_input_file import execute as generate_input_file
    from gemsModules.complex.GpBuilder.services.Build.api import Build_Inputs, BuildOptions, GlycanMapping
    
    # handle inputs and project dirs
    test_input_pdb = Path("/programs/gems/gmml2/tests/tests/inputs/017.GlycoproteinBuilder/1eer_eop_Asn.pdb")
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
        for line in lines[1:1+sites_to_select]:
            line = line.strip()
            sites.append("_".join(line.split(",")[:2]))
            
    # Note: The website will have to allow users to select sites and 
    # generate the sequences and send them to us.
    inputs = Build_Inputs(
        protein_file=str(test_input_pdb),
        glycan_mappings=[
            GlycanMapping(residue=site, sequence="DManpa1-OH") for site in sites
        ]
    )
    options = BuildOptions(
        number_of_samples=1,
        persist_cycles=1,
        seed=0
    )
    
    # Generate the input file for GpBuilder
    generate_input_file(test_project_dir, inputs, options)
    
    # Run GpBuilder with the generated input file        
    execute_gpb(test_input_file, test_project_dir)
    
    