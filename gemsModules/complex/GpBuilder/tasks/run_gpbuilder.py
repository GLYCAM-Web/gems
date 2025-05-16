import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig

log = logging.getLogger(__name__)
ic = InstanceConfig()


def execute(input_file: Path, project_dir: Path):
    try:
        #project_dir = Path(ic.get_filesystem_path("GpBuilder")) / job_id
                    
        # TODO: Use $GEMSHOME
        GP_BUILDER = "/programs/gems/gmml2/bin/gpBuilder"
        
        cmd = [GP_BUILDER, str(input_file), str(project_dir)]
        log.info(f"Running command: {' '.join(cmd)}")
        
        log_file = project_dir / "gpbuilder.log"
        err_file = project_dir / "gpbuilder.err"
        with open(log_file, "w") as log_out, open(err_file, "w") as err_out:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=log_out,
                stderr=err_out,
                timeout=120,
            )
        log.info(f"gpBuilder output: {result.stdout.decode()}")
        log.info(f"gpBuilder error: {result.stderr.decode()}")
    
    except subprocess.CalledProcessError as e:
        # Handle process errors
        error_message = "Process error"
        if err_file.exists():
            error_message += f": {err_file.read_text()}"
        if log_file.exists():
            error_message += f"\nLog output: {log_file.read_text()}"
        log.error(error_message)

def gpbt_wrapper(project_pdb_file: Path, output_txt_file: Path):
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
    with open(output_txt_file, "w") as out_file:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=out_file,
            stderr=subprocess.PIPE
        )
    log.info(f"gpBuilderTable error: {result.stderr.decode()}") 
    
    
if __name__ == "__main__":
    """Simplification of the GpBuilder workflow for testing purposes."""
    logging.basicConfig(level=logging.DEBUG)
    
    from gemsModules.complex.GpBuilder.tasks.generate_input_file import execute as generate_input_file
    from gemsModules.complex.GpBuilder.services.Build.api import BuildService_Inputs, BuildOptions, GlycanMapping
    
    # handle inputs and project dirs
    test_input_pdb = Path("/programs/gems/gmml2/tests/tests/inputs/017.GlycoproteinBuilder/1eer_eop_Asn.pdb")
    test_project_dir = Path("test_project_dir")
    outputs_dir = test_project_dir / "outputs"
    possible_glycosylation_sites = test_project_dir / Path("possible_sites.csv")
    test_input_file = test_project_dir / "builder_input.txt"

    test_project_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)
    
    # Generate the input file with GpBuilderTable
    gpbt_wrapper(test_input_pdb, possible_glycosylation_sites)
    
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
    inputs = BuildService_Inputs(
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
    execute(test_input_file, outputs_dir)
    
    