import shutil
import os
import glob


# TODO: directory prep should be handled by ProjectManagement
def setup_directory(directory):
    """
    Remove the directory if it exists and then recreate it.

    Args:
        directory (str): The path of the directory to setup.
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def copy_selected_files(source_pattern, frame_indices, destination_folder):
    """
    Copies selected frame files from source directories matching a pattern to a destination folder.

    Args:
        source_pattern (str): Pattern to match source directories.
        frame_indices (list): List of frame indices to copy.
        destination_folder (str): Destination folder where files are copied.
    """
    for source_dir in glob.glob(source_pattern):
        for index in frame_indices:
            source_file = f"{source_dir}/{index}.pdb"
            destination_file = f"{destination_folder}/{source_dir}_{index}.pdb"
            if os.path.exists(source_file):
                print(f"cp {source_file} {destination_file}")
                shutil.copy(source_file, destination_file)


def execute():
    """
    Main function to setup directory and copy selected files.
    """
    selected_frames_dir = "selected_frames"
    frame_indices = [1, 50, 100, 150, 200]
    source_pattern = "analog_*"

    setup_directory(selected_frames_dir)
    copy_selected_files(source_pattern, frame_indices, selected_frames_dir)
    copy_selected_files(
        "natural", frame_indices, selected_frames_dir
    )  # Special case for 'natural' directory


if __name__ == "__main__":
    execute()
