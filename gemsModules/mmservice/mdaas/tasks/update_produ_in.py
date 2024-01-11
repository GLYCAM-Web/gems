from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(sim_length: float, output_dir_path: str):
    sim_length = float(sim_length)
    nstlim = int(sim_length * 500000)  # 500k because dt=0.002
    with open(output_dir_path, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if "nstlim" in lines[i]:
                lines[i] = f"  nstlim = {nstlim},\n"
            if "ntwx" in lines[i]:
                lines[i] = f"  ntwx = {int(nstlim * 0.01)},\n"
            if "ntpr" in lines[i]:
                lines[i] = f"  ntpr = {int(nstlim * 0.01)},\n"
            if "ntwe" in lines[i]:
                lines[i] = f"  ntwe = {int(nstlim * 0.01)},\n"
            if "ntwr" in lines[i]:
                lines[i] = f"  ntwr = -{int(nstlim * 0.1)},\n"

    with open(output_dir_path, "w") as f:
        f.writelines(lines)

    log.debug(f"Updated {output_dir_path} with sim_length {sim_length} ns.")
