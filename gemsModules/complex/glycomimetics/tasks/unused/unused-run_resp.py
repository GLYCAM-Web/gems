import subprocess
import os
import sys


# TODO: move to common utils
def read_and_filter(file_path, keyword, output_file):
    """
    Reads from a specified file and writes lines containing a specific keyword to an output file.

    Args:
        file_path (str): Path to the input file.
        keyword (str): Keyword to filter lines by.
        output_file (str): Path to the output file for filtered lines.
    """
    with open(file_path, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if keyword in line:
                outfile.write(line)


def get_npoints(file_path):
    """
    Extracts the number of points used for fitting atomic charges from a Gaussian log file.

    Args:
        file_path (str): Path to the Gaussian log file.

    Returns:
        str: Number of points or None if not found.
    """
    with open(file_path, "r") as file:
        for line in file:
            if "points will be used for fitting atomic charges" in line:
                return line.split()[0]
    return None


def run_external_program(script_path):
    """
    Executes an external compiled program.

    Args:
        script_path (str): Path to the executable to run.
    """
    subprocess.run(script_path, shell=True, check=True)


def run_resp(inputs):
    """
    Executes the RESP program with the specified configuration.

    Args:
        inputs (dict): Contains paths for input, output, pch, qin, esp, and charge files.
    """
    resp_command = [
        "/cm/shared/apps/amber20/bin/resp",
        "-O",
        "-i",
        inputs["resp_input_file"],
        "-o",
        inputs["resp_output_file"],
        "-p",
        inputs["pch_output_file"],
        "-q",
        "qin",
        "-e",
        "esp.dat",
        "-t",
        inputs["charge_output_file"],
    ]
    subprocess.run(resp_command, check=True)


def cleanup(files):
    """
    Removes specified files if they exist.

    Args:
        files (list): List of file names to be removed.
    """
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def execute(
    gaussian_log_file,
    num_atoms,
    resp_input_file,
    resp_output_file,
    pch_output_file,
    charge_output_file,
    glycomimetic_scripts_dir,
):
    """
    Main function that orchestrates file processing and running of the RESP program based on command-line arguments.
    """

    # Cleanup temporary files
    cleanup(["a", "b", "c", "esp.dat", "count", "esout"])

    # Process Gaussian log file to extract points and write to 'count'
    npoints = get_npoints(gaussian_log_file)
    with open("count", "w") as count_file:
        count_file.write(f"{npoints}\n{num_atoms}\n")

    # Extract necessary data from Gaussian log file
    read_and_filter(gaussian_log_file, "Atomic Center ", "a")
    read_and_filter(gaussian_log_file, "ESP Fit", "b")
    read_and_filter(gaussian_log_file, "Fit    ", "c")

    # Uncomment below line to compile and run the Fortran code
    # compile_and_run_fortran(f"{glycomimetic_scripts_dir}/readit.f")

    # Run external compiled Fortran program if it exists
    run_external_program(f"{glycomimetic_scripts_dir}/a.out")

    # Execute RESP with the given configuration
    run_resp(
        {
            "resp_input_file": resp_input_file,
            "resp_output_file": resp_output_file,
            "pch_output_file": pch_output_file,
            "charge_output_file": charge_output_file,
        }
    )

    # Cleanup temporary files
    cleanup(["count", "esout", "a", "b", "c"])


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(
            "Usage: python script.py <gaussian_log_file> <num_atoms> <resp_input_file> <resp_output_file> <pch_output_file> <charge_output_file>"
        )
    else:
        glycomimetic_scripts_dir = "/home/yao/glycomimetic_simulations/scripts"
        execute(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3],
            sys.argv[4],
            sys.argv[5],
            sys.argv[6],
            glycomimetic_scripts_dir,
        )
