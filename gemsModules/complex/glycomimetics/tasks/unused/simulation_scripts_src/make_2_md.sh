echo "#!/bin/bash
#SBATCH -D .
#SBATCH -J M-${analog_name}
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --gres=gpu:1

source /etc/profile.d/modules.sh
source ${AMBERHOME}/amber.sh
srun hostname -s | sort -u >slurm.hosts

#MD
pmemd_cuda=\"${AMBERHOME}/bin/pmemd.cuda\"

#<<\"comment\"
#First run a restrained equi on the cocomplex
\${pmemd_cuda} -O \\
 -p ../1_leap/cocomplex.prmtop \\
 -c heat.rst7 \\
 -i equi_restraint.in \\
 -o equi_restraint.out \\
 -r equi_restraint.rst7 \\
 -ref heat.rst7

#Then run an unrestrained equi on the cocomplex
if grep -q \"\${wallclock}\" equi_restraint.out ; then
    \${pmemd_cuda} -O \\
     -p ../1_leap/cocomplex.prmtop \\
     -c equi_restraint.rst7 \\
     -i equi.in \\
     -o equi.out \\
     -r equi.rst7 \\
     -ref equi_restraint.rst7
fi

#check if equilibration is complete
if grep -q \"\${wallclock}\" equi.out ; then

    #production
    \${pmemd_cuda} -O \\
     -p ../1_leap/cocomplex.prmtop \\
     -c equi.rst7 \\
     -i md.in \\
     -o md.out \\
     -r md.rst7 \\
     -x md.nc \\
     -ref equi.rst7
fi
#comment

#check if MD is complete
if grep -q \"\${wallclock}\" md.out ; then
    sbatch ../../simulation_${analog_name}_gbsa.sh
fi
" > simulation_${analog_name}_md.sh

