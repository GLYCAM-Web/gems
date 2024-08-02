echo "#!/bin/bash
#SBATCH -D ${dirname}/1_leap
#SBATCH -J E-${analog_name}
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=${num_cpus_emin}


source /etc/profile.d/modules.sh
source ${AMBERHOME}/amber.sh


#srun hostname -s | sort -u >slurm.hosts
bash ../../simulation_${analog_name}_Emin.sh

echo \"Slurm script ends\"
" > slurm_submit_${dirname}.sh

