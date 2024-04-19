import os
import sys
import subprocess


def check_for_restart_conditions(gaussian_opt_output):
    """
    Check if the optimization should be restarted based on the output file contents.
    """
    if os.path.exists(gaussian_opt_output):
        with open(gaussian_opt_output, "r") as file:
            content = file.read()
            if "Number of steps exceeded" in content and "Error termination" in content:
                return True
    return False


def write_newzmat(
    input_file_type,
    net_charge,
    check_file,
    num_mem,
    num_cpus,
    gaussian_opt_output,
    gaussian_input,
    old_chk=None,
):
    """
    Writes newzmat content based on the type of input file.
    """
    if input_file_type == "0":
        with open("newzmat_here.txt", "w") as file:
            file.write(f"{net_charge},1\n")
            file.write(f"%Chk={check_file}\n")
            file.write(f"%mem={num_mem}\n")
            file.write(f"%NProcShared={num_cpus}\n")
            if check_for_restart_conditions(gaussian_opt_output):
                file.write("#HF/6-31+G* Opt(restart,maxcycle=1000) geom=connectivity\n")
            else:
                file.write("#HF/6-31+G* Opt(maxcycle=1000) geom=connectivity\n")
            file.write("\nOpt then ESP\n\n")
            file.write(f"{net_charge},1\n")
        subprocess.run(
            ["newzmat", "-ipdb", "-ozmat", "-prompt", gaussian_input],
            input=open("newzmat_here.txt", "r"),
        )

    elif input_file_type == "1":
        with open("newzmat_here_esp.txt", "w") as file:
            file.write(f"%OldChk={old_chk}\n")
            file.write(f"%Chk={check_file}\n")
            file.write(f"%mem={num_mem}\n")
            file.write(f"%NProcShared={num_cpus}\n")
            file.write("#HF/6-31+G* pop=chelpg iop(6/33=2) geom=(connectivity)\n")
            file.write("\nESP calculation of the optimized ligand structure\n\n")
            file.write(f"{net_charge},1\n")
        subprocess.run(
            ["newzmat", "-ichk", "-ozmat", "-prompt", old_chk, gaussian_input],
            input=open("newzmat_here_esp.txt", "r"),
        )


def execute(
    ligand_pdb,
    check_file,
    gaussian_input,
    net_charge,
    num_cpus,
    num_mem,
    gaussian_opt_output,
    input_file_type,
):
    """
    Main execution function.
    """
    old_chk = check_file.replace("_esp", "") if input_file_type == "1" else None
    write_newzmat(
        input_file_type,
        net_charge,
        check_file,
        num_mem,
        num_cpus,
        gaussian_opt_output,
        gaussian_input,
        old_chk,
    )


if __name__ == "__main__":
    if len(sys.argv) < 9:
        print(
            "Usage: python script.py <ligand_pdb> <check_file> <gaussian_input> <net_charge> <num_cpus> <num_mem> <gaussian_opt_output> <input_file_type>"
        )
        sys.exit(1)
    execute(*sys.argv[1:])
