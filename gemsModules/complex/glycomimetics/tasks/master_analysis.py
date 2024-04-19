import os
import subprocess
import sys


from gemsModules.complex.glycomimetics.tasks.score_trajectory import (
    execute as score_trajectory,
)
from gemsModules.complex.glycomimetics.tasks.extract_selected_frames import (
    execute as extract_frames,
)
from gemsModules.complex.glycomimetics.tasks.write_frames import execute as write_frames


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def manage_gbsa_summary(subdirs, base_dir):
    summary_dir = os.path.join(base_dir, "summary")
    os.makedirs(summary_dir, exist_ok=True)

    with open(os.path.join(summary_dir, "gbsa_summary.txt"), "w") as f:
        for subdir in subdirs:
            gbsa_info = analyze_gbsa(subdir)
            f.write(f"{subdir}\t{gbsa_info}\n")
            print(f"{subdir}\t{gbsa_info}")

    sort_summary(summary_dir)


def analyze_gbsa(subdir):
    gbsa_file = os.path.join(subdir, "4_gbsa", "mmgbsa.out")
    try:
        with open(gbsa_file) as file:
            for line in file:
                if "DELTA TOTAL" in line:
                    return "\t".join(line.split()[2:4])
    except FileNotFoundError:
        pass
    return "Failed"


def sort_summary(summary_dir):
    summary_file = os.path.join(summary_dir, "gbsa_summary.txt")
    sorted_file = os.path.join(summary_dir, "gbsa_summary_sorted.txt")
    with open(summary_file) as file:
        lines = sorted(file.readlines(), key=lambda x: x.split()[0])

    with open(sorted_file, "w") as file:
        file.writelines(lines)


# TODO: this task might be a GEMS server.py or logic.py instead.
def execute(simulation_workdir):
    num_frames = 1000
    interval = 5
    scoring_interval = 1

    os.chdir(os.path.join(simulation_workdir, "simulation"))

    log.info("Begin writeframe")
    write_frames(num_frames, interval)

    os.chdir("frames")
    # TODO: pass vars through instead of the hardcoding/env vars
    extract_frames()
    os.chdir("..")

    log.info("Begin scoretraj")
    # TODO: as above
    score_trajectory(interval)

    log.info("Finally, GBSA dG:")
    subdirs = [d for d in os.listdir() if d.startswith("analog_") or d == "natural"]
    manage_gbsa_summary(subdirs, "frames")


if __name__ == "__main__":
    execute(sys.argv[1])
