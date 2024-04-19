import os
import subprocess


def prepare_receptor(pdb_path, output_path):
    """Run prepare_receptor4.py on a PDB file."""
    cmd = f"/home/yao/programs_src/MGLTools-1.5.4/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r {pdb_path} -A None -U None -o {output_path}"
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0 and os.path.exists(output_path)


def score_trajectory(vina_dir, pdbqt_file, working_dir, interval):
    """Run scoretraj.exe on a pdbqt file."""
    os.chdir(working_dir)
    cmd = f"{vina_dir}/scoretraj.exe {pdbqt_file} . {interval}"
    result = subprocess.run(cmd, shell=True)
    os.chdir("..")
    return result.returncode == 0


def summarize_results(summary_dir):
    """Summarize the scoring results into a summary file."""
    summary_path = os.path.join(summary_dir, "summary_csv.txt")
    with open(summary_path, "w") as summary:
        for csv_file in os.listdir(summary_dir):
            if csv_file.endswith(".csv"):
                moiety = csv_file.replace(".csv", "")
                with open(os.path.join(summary_dir, csv_file)) as f:
                    last_line = f.readlines()[-1]
                    score = last_line.split()
                    summary.write(f"{moiety}\t{score[1]}\t{score[2]}\n")
    return summary_path


def execute(interval):
    """Currently equivalent to external_scripts_bash/scoretraj.sh logic.

    ## TODO:
    - should not make dirs on the fly here, should be prepared earlier

    """
    os.makedirs("frames/summary", exist_ok=True)
    os.makedirs("frames/cocomplex_pdbqts", exist_ok=True)

    vina_score_traj_program_dir = "/home/yao/glycomimetics/rescoring"

    for directory in os.listdir("frames"):
        if directory.startswith("analog_") or directory == "natural":
            moiety_name = directory.replace("analog_", "")
            pdb_path = f"frames/{directory}/1_leap/cocomplex_nowat_noion.pdb"
            pdbqt_path = f"frames/cocomplex_pdbqts/cocomplex_{directory}.pdbqt"

            if prepare_receptor(pdb_path, pdbqt_path):
                if score_trajectory(
                    vina_score_traj_program_dir,
                    pdbqt_path,
                    f"frames/{directory}",
                    interval,
                ):
                    if os.path.exists(f"frames/{directory}/output.csv"):
                        os.rename(
                            f"frames/{directory}/output.csv",
                            f"frames/summary/{moiety_name}.csv",
                        )
                    else:
                        print(f"Scoring of {directory} failed, output.csv missing")
                else:
                    print(f"Scoring failed for {directory}")
            else:
                print(
                    f"Warning: failed to generate cocomplex pdbqt file for {directory}. Skipping"
                )

    summary_file = summarize_results("frames/summary")
    with open(summary_file) as file:
        print(file.read())


if __name__ == "__main__":
    import sys

    interval = (
        int(sys.argv[1]) if len(sys.argv) > 1 else 30
    )  # Default to 30 if no interval is supplied
    execute(interval)
