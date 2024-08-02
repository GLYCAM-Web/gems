import sys

# import numpy as np


def execute(project_dir):
    unit = 0.529177249
    count_path = f"{project_dir}/count"
    a_path = f"{project_dir}/a"
    b_path = f"{project_dir}/b"
    c_path = f"{project_dir}/c"
    esp_dat_path = f"{project_dir}/esp.dat"

    # Reading file count
    with open(count_path, "r") as f:
        lines = f.readlines()
        i = int(lines[0].strip())  # Number of atoms
        j = int(lines[1].strip())  # Number of esp points

    # Initialize output file
    with open(esp_dat_path, "w") as esp_file:
        esp_file.write(f"{i:6d}{j:6d}\n")

        # Read and transform coordinates for atoms
        with open(a_path, "r") as file_a:
            for _ in range(i):
                line = file_a.readline()
                a, b, c = map(float, line[32:].split())
                esp_file.write(f"{a/unit:16.6e}{b/unit:16.6e}{c/unit:16.6e}\n")

        # Read and transform coordinates and ESP values
        with open(b_path, "r") as file_b, open(c_path, "r") as file_c:
            for _ in range(j):
                line_b = file_b.readline()
                a, b, c = map(float, line_b[32:].split())
                line_c = file_c.readline()
                esp = float(line_c[14:].strip())
                esp_file.write(
                    f"{esp:16.6e}{a/unit:16.6e}{b/unit:16.6e}{c/unit:16.6e}\n"
                )


if __name__ == "__main__":
    project_directory = str(sys.argv[1])
    execute(project_directory)
