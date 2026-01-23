from pydantic import BaseModel, Field
from typing import List
from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging

from ..services.Build.api import Build_Inputs, BuildOptions, GlycanMapping

log = Set_Up_Logging(__name__)



def execute(input_file_string, inputs, options) -> Path:
    log.debug(f"Creating GP Builder input file at: {input_file_string}")

    input_file = Path(input_file_string)

    with input_file.open("w") as f:
        f.write(f"Protein:{inputs.protein_file}\n")
        f.write(f"numberOfSamples:{options.number_of_samples}\n")
        f.write(f"persistCycles:{options.persist_cycles}\n")
        f.write(f"rngSeed:{options.rng_seed}\n")
        f.write(f"overlapRejectionThreshold:{options.overlap_rejection_threshold}\n")
        f.write(f"prepareForMD:{str(options.prepare_for_md).lower()}\n")
        f.write(f"useInitialGlycositeResidueConformation:{str(options.use_initial_glycosite_residue_conformation).lower()}\n")
        f.write(f"moveOverlappingSidechains:{str(options.move_overlapping_sidechains).lower()}\n")
        f.write(f"deleteUnresolvableGlycosites:{str(options.delete_unresolvable_glycosites).lower()}\n")
        f.write("\n")
        
        f.write("ProteinResidue, GlycanName:\n")
        for mapping in inputs.glycan_mappings:
            f.write(f"{mapping.Chain}_{mapping.ResidueNumber}{mapping.InsertionCode}|{mapping.Sequence}\n")
        f.write("END\n")

    return input_file


@staticmethod
def parse_input_file(file_path: Path):
    """Parse a GP Builder input file into a GPBuilderInput object"""
    with open(file_path) as f:
        lines = f.readlines()

    b_inputs = Build_Inputs()
    b_options = BuildOptions()
    
    in_mappings = False
    
    for line in lines:
        line = line.strip()
        if not line or line == "END":
            continue
            
        if ":" in line:
            key, value = line.split(":", 1)
            if key == "Protein":
                b_options.protein_file = value.strip()
            elif key == "numberOfSamples":
                b_options.number_of_samples = int(value)
            elif key == "persistCycles":
                b_options.persist_cycles = int(value)
            elif key == "rngSeed":
                b_options.seed = int(value)
            elif key == "prepareForMD":
                b_options.prepare_for_md = value.strip().lower() == "true"
            elif key == "useInitialGlycositeResidueConformation":
                b_options.use_initial_glycosite_residue_conformation = value.strip().lower() == "true"
            elif key == "moveOverlappingSidechains":
                b_options.move_overlapping_sidechains = value.strip().lower() == "true"
            elif key == "ProteinResidue, GlycanName":
                in_mappings = True
            continue
        elif in_mappings and "|" in line:
            residue, sequence = line.split("|", 1)
            residue_parts = residue.split("_")
            if len(residue_parts) == 2:
                chain, residue_number = residue_parts
                glycan_mapping = GlycanMapping(
                    Chain=chain,
                    ResidueNumber=residue_number,
                    Sequence=sequence.strip()
                )
                b_inputs.glycan_mappings.append(glycan_mapping)
        else:
            log.warning(f"Unrecognized line in GP Builder input file: {line}")
        
    return b_inputs, b_options


if __name__ == "__main__":
    # Example usage
    job_dir = Path(".") / "gpbuilder_job"
    job_dir.mkdir(parents=True, exist_ok=True)
    
    inputs = Build_Inputs(protein_file="/programs/gems/gmml2/tests/tests/inputs/017.GlycoproteinBuilder/1eer_eop_Asn.pdb")
    options = BuildOptions(number_of_samples=2, seed=42)
    
    input_file = execute(job_dir, inputs, options)
    print(f"Input file created at: {input_file}")
