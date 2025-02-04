import subprocess
import os

from gemsModules.logging.logger import Set_Up_Logging
from ..services.common_api import Modification_Position


log = Set_Up_Logging(__name__)


# Path to the evaluate_wrapper.sh script which is used to run the GM/Evaluation step.
EVALUATE_WRAPPER = os.path.join(os.path.dirname(__file__), "evaluate_wrapper.sh")

# substitute for actual API types
CondensedSequence = str

# custom exception to indicate no positions found for GEMS error logic.
class NoPositionsFoundError(Exception):
    pass


def parse_eval_output(buffer):
    # line 1 should indica(te if valid or not
    valid = False
    if buffer[0].startswith("Valid"):
        valid = buffer[0].split(":")[1].strip() == "True"
    else:
        raise ValueError("Unexpected data format during GM/Evaluation step, missing valid flag")
    
    # line 2 should be a Reason: message
    reason = None
    if buffer[1].startswith("Reason"):
        reason = buffer[1].split(":")[1].strip()
    else:
        raise ValueError("Unexpected data format during GM/Evaluation step, missing reason message")
    
    # from line 3 onwards, we need to delimit by "Oligosaccharide" to take the condensed sequences with their modification positions.
    cbuffer = buffer[2:]

    condensed_sequences = []
    # split at lines containing "Oligosaccharide"
    oligo_lines = []
    for idx, line in enumerate(cbuffer):
        if line.startswith("Oligosaccharide"):
            oligo_lines.append(idx)
    
    # grab all lines between two "Oligosaccharide" lines
    for i, idx  in enumerate(oligo_lines):
        condensed_seq = cbuffer[idx].split(":")[1].strip()
        if i == len(oligo_lines) - 1:
            # last oligo line, grab all lines from idx to end
            condensed_sequences.append((condensed_seq, cbuffer[idx+1:]))
        else:
            # grab all lines from idx to next oligo line
            condensed_sequences.append((condensed_seq, cbuffer[idx+1:oligo_lines[i+1]]))
    
    return valid, reason, condensed_sequences
    
    
def parse_avail_positions(condensed_sequences_and_options):
    all_available_positions = {}
    for seq, options in condensed_sequences_and_options:        
        available_positions = []
        for line in options:
            mp = line.split('-')
            if len(mp) != 8:
                raise ValueError(f"Unexpected data format during GM/Evaluation step, invalid modification position found: {line}")
            
            available_positions.append(Modification_Position(
                Residue_Name=mp[0],
                Chain_Identifier=mp[1],
                Residue_Number=mp[2],
                Moiety_Attachment_Atom=mp[3],
                Atom_Number=mp[4],
                Residue_Name_Glycam=mp[5],
                Residue_Number_Glycam=mp[6],
                Atom_Number_Glycam=mp[7]
            ))
            
        if len(available_positions) == 0:
            raise NoPositionsFoundError("No available modification positions found during GM/Evaluation step")
        
        all_available_positions[seq] = available_positions

    condensed_sequences = [s[0] for s in condensed_sequences_and_options]
    return condensed_sequences, all_available_positions


def execute(parent_dir: str, pdb_filename: str) -> tuple[list[CondensedSequence], list[Modification_Position]]:
    os.chdir(parent_dir)
    
    # Run the GM/Evaluation step
    result = subprocess.run([EVALUATE_WRAPPER, parent_dir, pdb_filename])
    if result.returncode != 0:
        log.debug(f"Error running GM/Evaluation step, return code: {result.returncode}")
        # raise RuntimeError(f"Error running GM/Evaluation step, return code: {result.returncode}")
    
    # Check if the output file is present
    output_file = os.path.join(parent_dir, "available_atoms.txt")
    if not os.path.exists(output_file):
        evaluate_err_file = os.path.join(parent_dir, "evaluate.err")
        if os.path.exists(evaluate_err_file):
            with open(evaluate_err_file) as f:
                err_msg = f.read().strip()
            if err_msg:
                log.error(f"Error during GM/Evaluation step: {err_msg}, raising RuntimeError")
                raise RuntimeError(f"Error during GM/Evaluation step: {err_msg}")
        # Will be raised if outputfile is not found and no error message is present.
        raise FileNotFoundError(f"Output file not found: {output_file}")
    
    with open(output_file) as f:
        buffer = f.read().splitlines()
    
    if len(buffer) == 0:
        raise ValueError("No Evaluation output found, GM/Evaluation step failed for an unknown reason")

    # Assuming there are at least 2 lines for the valid flag and the reason.
    if len(buffer) < 2:
        raise ValueError("Unexpected data format during GM/Evaluation step, not enough data")  
    
    valid, reason, condensed_sequences_and_options = parse_eval_output(buffer)
        
    if len(condensed_sequences_and_options) == 0:
        raise ValueError("Unexpected data format during GM/Evaluation step, missing condensed sequence")

    # Now parse the available positions for each condensed sequence
    condensed_sequences, all_available_positions = parse_avail_positions(condensed_sequences_and_options)
    
    return valid, reason, condensed_sequences, all_available_positions