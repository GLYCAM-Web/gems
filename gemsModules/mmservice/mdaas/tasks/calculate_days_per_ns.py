from pathlib import Path
import re

def parse_amber_parm7_pointers(content):
    """
    Parse the POINTERS section of an AMBER parm7 file.
    
    Args:
    content (str): The content of the parm7 file.
    
    Returns:
    tuple: A tuple containing (format_string, parsed_data_list)
    """
    pointers_regex = re.compile(r'%FLAG POINTERS\s*\n%FORMAT\s*\((\d+[Ii]\d+)\)\s*(.*?)(?=\n%FLAG|\Z)', re.DOTALL)
    
    match = pointers_regex.search(content)
    if not match:
        raise ValueError("POINTERS section not found in the content")
    
    format_str, data_str = match.groups()
    
    # Parse the format string
    num_per_line, char_per_num = map(int, re.findall(r'\d+', format_str))
    
    # Remove newlines and extra spaces, then split the data
    data_str = data_str.replace('\n', '').strip()
    data = [data_str[i:i+char_per_num].strip() for i in range(0, len(data_str), char_per_num)]
    
    # Convert to integers
    pointers = list(map(int, data))
    
    return format_str, pointers


def parse_amber_parm7_natoms(path):
    """
    Return the number of atoms (NATOMS) from an AMBER parm7 file.
    
    Args:
    path (Path or str): Path to the parm7 file.
    
    Returns:
    int: The number of atoms (NATOMS) in the system.
    """
    with open(path, 'r') as f:
        content = f.read()
    
    _, pointers = parse_amber_parm7_pointers(content)
    
    # NATOMS is the first value in the POINTERS section
    natoms = pointers[0]
    
    return natoms


def execute(parmfile: Path, sim_length: int) -> float:
    """
    Calculate the time prediction for a given number of residues and simulation length.

    Args:
    parmfile (Path): Path to the AMBER parm7 file.
    sim_length (int): The length of the simulation in ns.
    """
    number_of_particles = parse_amber_parm7_natoms(parmfile)
    
    # Return a time prediction in days per ns.
    # N.B. This line was fit using data gathered from GLYCAM-Web around July 18, 2024.
    days_per_ns = 1.50724e-07 * number_of_particles + -0.000544733

    sim_time_est = days_per_ns * sim_length
    return sim_time_est


# Example usage: python calculate_days_per_ns.py parm7_file_path
if __name__ == "__main__":
    import sys
    parm_file_path = Path(sys.argv[1])
    try:
        days_per_ns = execute(parm_file_path)
        print(f"Predicted time: {days_per_ns:.6f} days per ns")
    except ValueError as e:
        print(f"Error: {e}")