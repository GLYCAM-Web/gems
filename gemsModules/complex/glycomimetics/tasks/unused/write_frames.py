import os
import subprocess
import glob
import shutil
import sys


def ensure_directory_exists(path):
    """Ensures that a directory exists; if not, it creates it."""
    if not os.path.exists(path):
        os.makedirs(path)


def clean_directory(directory):
    """Removes all files in the specified directory."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def write_cpptraj_input(input_filename, directory, num_frames, interval, path_prefix):
    """Writes the CPPTRAJ input file for processing."""
    content = f"""
parm {directory}/1_leap/cocomplex_nowat_noion.prmtop
trajin {directory}/3_md/md.nc 1 {num_frames} {interval}
autoimage
trajout {path_prefix} pdb multi nobox
go
"""
    with open(input_filename, "w") as file:
        file.write(content)


def execute_cpptraj(input_file):
    """Executes CPPTRAJ with the provided input file."""
    subprocess.run(["cpptraj", "<", input_file], shell=True)


def rename_files(path_prefix):
    """Renames files to remove prefix and add .pdb extension."""
    for filename in glob.glob(f"{path_prefix}*"):
        new_name = filename.replace(path_prefix, "") + ".pdb"
        os.rename(filename, new_name)


def execute(num_frames, interval):
    """Main function to orchestrate the workflow."""
    ensure_directory_exists("frames/summary")

    for directory in glob.glob("analog_*") + ["natural"]:
        frame_dir = os.path.join("frames", directory)

        ensure_directory_exists(frame_dir)
        clean_directory(frame_dir)

        path_prefix = os.path.join(frame_dir, "frame_")
        input_file = os.path.join("frames", "cpptraj_writeframes.in")
        write_cpptraj_input(input_file, directory, num_frames, interval, path_prefix)

        execute_cpptraj(input_file)
        rename_files(path_prefix)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <num_frames> <interval>")
        sys.exit(1)

    num_frames = sys.argv[1]
    interval = sys.argv[2]
    execute(num_frames, interval)
