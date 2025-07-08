from pydantic import BaseModel, Field
from typing import List
from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)



def execute(input_file, inputs, options) -> Path:
    log.debug(f"Creating GP Builder input file at: {input_file}")

    with input_file.open("w") as f:
        # we don't use inputs.protein_file here to simplify v1 considering the website must execute evaluate for it's own reasons first.
        # When we do start using the protein file, we will need to ensure to use it's filename, but path modified to the job directory after we copy the upload for them.
        f.write(f"Protein:Default.pdb\n")
        f.write(f"numberOfSamples:{options.number_of_samples}\n")
        f.write(f"persistCycles:{options.persist_cycles}\n")
        f.write(f"rngSeed:{options.seed}\n\n")
        
        f.write("ProteinResidue, GlycanName:\n")
        for mapping in inputs.glycan_mappings:
            f.write(f"{mapping.Chain}_{mapping.ResidueNumber}|{mapping.Sequence}\n")
        f.write("END\n")

    return input_file


@staticmethod
def parse_input_file(file_path: Path):
    """Parse a GP Builder input file into a GPBuilderInput object"""
    with open(file_path) as f:
        lines = f.readlines()

    config = {
        "glycan_mappings": []
    }
    
    in_mappings = False
    
    for line in lines:
        line = line.strip()
        if not line or line == "END":
            continue
            
        if ":" in line:
            key, value = line.split(":", 1)
            if key == "Protein":
                config["protein_file"] = value.strip()
            elif key == "numberOfSamples":
                config["number_of_samples"] = int(value)
            elif key == "persistCycles":
                config["persist_cycles"] = int(value)
            elif key == "seed":
                config["seed"] = int(value)
            elif key == "ProteinResidue, GlycanName":
                in_mappings = True
        elif in_mappings and "|" in line:
            residue, sequence = line.split("|", 1)
            config["glycan_mappings"].append({
                "residue": residue.strip(),
                "sequence": sequence.strip()
            })
    
    return config


if __name__ == "__main__":
    # Example usage
    job_dir = Path(".") / "gpbuilder_job"
    job_dir.mkdir(parents=True, exist_ok=True)
    
    inputs = {
        "protein_file": "/programs/gems/gmml2/tests/tests/inputs/017.GlycoproteinBuilder/1eer_eop_Asn.pdb",
    }
    options = {
        "number_of_samples": 2,
        "seed": 42
    }
    
    input_file = execute(job_dir, inputs, options)
    print(f"Input file created at: {input_file}")