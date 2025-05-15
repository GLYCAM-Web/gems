import subprocess
import logging
from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig

log = logging.getLogger(__name__)
ic = InstanceConfig()

GP_BUILDER = ""

def execute(input_file: Path, project_dir: Path):
    try:
        #project_dir = Path(ic.get_filesystem_path("GpBuilder")) / job_id
        
        if not project_dir.exists():
            project_dir.mkdir()
            
        log_file = project_dir / "gpbuilder.log"
        err_file = project_dir / "gpbuilder.err"

        # Run gpBuilder with timeout
        with open(log_file, "w") as log_out, open(err_file, "w") as err_out:
            subprocess.run(
                [str(GP_BUILDER), str(input_file), str(project_dir / "output")],
                text=True,
                check=True,
                stdout=log_out,
                stderr=err_out,
                cwd=str(project_dir),
                timeout=300  # 5 minute timeout
            )

        # Update job status in database
        # job.status = "completed"
        # job.completed_at = datetime.now()
        # job.output_path = str(project_dir / "output")
        # db.commit()

    except subprocess.CalledProcessError as e:
        # Handle process errors
        error_message = "Process error"
        if err_file.exists():
            error_message += f": {err_file.read_text()}"
        if log_file.exists():
            error_message += f"\nLog output: {log_file.read_text()}"

        # job.status = "failed"
        # job.error = error_message
        # db.commit()

    except Exception as e:
        pass
        # log.error(f"Error processing job {job_id}: {str(e)}")
        # job.status = "failed"
        # job.error = str(e)
        # db.commit()


def gpb_wrapper(input_file: Path, project_dir: Path):
    """
    Wrapper function to execute the gpBuilder process.
    """
    import subprocess
    GP_BUILDER = "/programs/gems/gmml2/bin/gpBuilder"
    
    cmd = [GP_BUILDER, str(input_file), str(project_dir)]
    log.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    log.info(f"gpBuilder output: {result.stdout.decode()}")
    

def gpbt_wrapper(project_pdb_file: Path, output_txt_file: Path):
    """
    Wrapper function to execute the gpBuilderTable process.
    
    This is used to generate the possible glycosylation sites for
    the given PDB file. We choose to output as csv here.
    
    This will be requested by the website.
    
    ./bin/gpBuilderTable /programs/gems/gmml2/tests/tests/inputs/018.4mbzEdit.pdb --format csv > someout.txt
    """
    import subprocess
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
    #log.info(f"gpBuilderTable error: {result.stderr.decode()}") 
    
    
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
    gpb_wrapper(test_input_file, outputs_dir)
    
    