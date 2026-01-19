import subprocess
import os
import sys
import glob

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def run_resp_calculations(
    gaussian_log_file,
    resp_input_file,
    resp_output_file,
    pch_output_file,
    charge_output_file,
    glycomimetic_scripts_dir,
):
    # Cleanup previous run files if any
    cleanup_files = ["a", "b", "c", "a.out", "readit.o", "esp.dat", "count", "esout"]
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)

    # List and process each Gaussian log file
    for log_file in glob.glob(gaussian_log_file):
        log.info(f"Getting ESP charges on {log_file}")

        # Generate ESP data from Gaussian log
        subprocess.run(["espgen", "-i", log_file, "-o", "esp.dat"])

        # Run RESP
        resp_executable = os.path.join(glycomimetic_scripts_dir, "resp-2.2", "resp")
        resp_command = [
            resp_executable,
            "-O",
            "-i",
            resp_input_file,
            "-o",
            resp_output_file,
            "-p",
            pch_output_file,
            "-e",
            "esp.dat",
            "-t",
            charge_output_file,
        ]
        subprocess.run(resp_command)

        # Optionally remove temporary files created during processing
        # os.remove('esp.dat')
        # os.remove('count')
        # os.remove('esout')


def execute(
    gaussian_log_file,
    atoms,
    resp_input_file,
    resp_output_file,
    pch_output_file,
    charge_output_file,
):
    glycomimetic_scripts_dir = "/home/yao/glycomimetic_simulations/scripts"
    run_resp_calculations(
        gaussian_log_file,
        resp_input_file,
        resp_output_file,
        pch_output_file,
        charge_output_file,
        glycomimetic_scripts_dir,
    )


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "Usage: python script.py <gaussian_log_file_pattern> <atoms> <resp_input_file> <resp_output_file> <pch_output_file> <charge_output_file>"
        )
    else:
        execute(
            sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        )
