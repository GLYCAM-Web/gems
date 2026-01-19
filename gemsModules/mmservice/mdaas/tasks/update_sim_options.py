

def execute(
    sim_length, projectDir
):
    sim_length = float(sim_length)
    nstlim = int(sim_length * 500000)  # 500k because dt=0.002
    with open(projectDir + "/10.produ.in", "r") as f:
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

    with open(projectDir + "/10.produ.in", "w") as f:
        f.writelines(lines)