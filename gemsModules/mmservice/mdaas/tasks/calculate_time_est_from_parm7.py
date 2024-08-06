from pathlib import Path
import re

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


# TODO: Where should this go? systemoperations seems like the spot until you consider this is an amber specific function. Tasks might be better interpreted as common library utilities for an Entity.
def parse_amber_parm7_pointers(content, flag_section="POINTERS"):
    """
    Parse the POINTERS section of an AMBER parm7 file.
    
    Args:
    content (str): The content of the parm7 file.
    
    Returns:
    tuple: A tuple containing (format_string, parsed_data_list)
    """
    pointers_regex = re.compile(f'%FLAG {flag_section}' + r'\s*\n%FORMAT\s*\((\d+[Ii]\d+)\)\s*(.*?)(?=\n%FLAG|\Z)', re.DOTALL)
    
    match = pointers_regex.search(content)
    if not match:
        raise ValueError("POINTERS section not found in the content")
    
    format_str, data_str = match.groups()
    
    # Parse the format string
    num_per_line, char_per_num = map(int, re.findall(r'\d+', format_str))
    log.debug(f"num_per_line: {num_per_line}, char_per_num: {char_per_num}")

    # remove newlines
    data_str = data_str.replace('\n', '')
    data = [data_str[i:i+char_per_num - 1].strip() for i in range(0, len(data_str), char_per_num)]
    log.debug(f"POINTERS data: {data}")

    # Convert to integers
    try:
        pointers = list(map(int, data))
    except:
        log.debug(f"Could not convert POINTERS data to integers: {data}")
        raise ValueError(f"Could not convert POINTERS data to integers: {data}")
    return format_str, pointers


def parse_amber_parm7_natoms(content):
    """
    Return the number of atoms (NATOMS) from an AMBER parm7 file.
    
    Args:
    path (Path or str): Path to the parm7 file.
    
    Returns:
    int: The number of atoms (NATOMS) in the system.
    """

    
    try:
        _, pointers = parse_amber_parm7_pointers(content, flag_section="POINTERS")
    except ValueError as e:
        log.debug(f"Could not parse the POINTERS section for the content.")
        raise ValueError(f"Could not parse the POINTERS section: {e}")
    # NATOMS is the first value in the POINTERS section
    natoms = pointers[0]
    
    return natoms


def execute(content: str, sim_length: float) -> float:
    """
    Calculate the time prediction for a given number of residues and simulation length.

    Args:
    parmfile (Path): Path to the AMBER parm7 file.
    sim_length (int): The length of the simulation in ns.
    """
    number_of_particles = parse_amber_parm7_natoms(content)
    
    # Return a time prediction in days per ns.
    # N.B. This line was fit using data gathered from GLYCAM-Web around July 18, 2024.
    days_per_ns = 1.50724e-07 * number_of_particles + -0.000544733
    log.debug(f"Predicted time: {days_per_ns:.6f} days per ns for {number_of_particles} particles")

    sim_time_est_days = days_per_ns * sim_length
    sim_time_est_hours = sim_time_est_days * 24
    #sim_time_est = sim_time_est_hours * 3600  # convert to seconds
    #log.debug(f"Predicted time: {sim_time_est:.6f} seconds")
    return sim_time_est_hours, number_of_particles


# Example usage: python calculate_days_per_ns.py parm7_file_path
if __name__ == "__main__":
    import sys
    parm_file_path = Path(sys.argv[1])
    try:
        days_per_ns = execute(parm_file_path, 10)
        print(f"Predicted time: {days_per_ns:.6f} days per ns")
    except ValueError as e:
        print(f"Error: {e}")