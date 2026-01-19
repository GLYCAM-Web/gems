echo "#!/bin/bash
#SBATCH -D ../4_gbsa
#SBATCH -J G-${analog_name}
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=${num_cpus_gbsa}

source /etc/profile.d/modules.sh
source ${AMBERHOME}/amber.sh
srun hostname -s | sort -u >slurm.hosts

echo \"parm ../1_leap/cocomplex_nowat_noion.prmtop
trajin ../3_md/md.nc
strip :WAT
trajout md_no_receptor_water.nc
go
clear all

parm ../1_leap/cocomplex_nowat_noion.prmtop
parmstrip :WAT
parmwrite out cocomplex_nowat_noion_no_receptor_water.prmtop
go
clear all

parm ../1_leap/receptor_nowat_noion.prmtop
parmstrip :WAT
parmwrite out receptor_nowat_noion_no_receptor_water.prmtop
go\" > cpptraj_strip_receptor_water.in

cpptraj < cpptraj_strip_receptor_water.in

mmpbsa=\"mpirun -np ${num_cpus_gbsa} ${AMBERHOME}/bin/MMPBSA.py.MPI\"

\${mmpbsa} -O \\
 -i mmgbsa.in \\
 -cp cocomplex_nowat_noion_no_receptor_water.prmtop \\
 -rp receptor_nowat_noion_no_receptor_water.prmtop \\
 -lp ../1_leap/ligand_nowat_noion.prmtop \\
 -y md_no_receptor_water.nc \\
 -o  mmgbsa.out \\
 -do decom_gbsa.dat \\
 -eo per_frame_breakdown.dat \\
 -use-mdins
" > simulation_${analog_name}_gbsa.sh

