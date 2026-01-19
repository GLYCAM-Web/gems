simulation_workdir=$1
glycomimetic_input_file="${simulation_workdir}/glycomimetics/sample_input_file.txt"
glycomimetic_output_dir=$(grep "OutputPath:" ${glycomimetic_input_file} | sed 's/OutputPath://')  #This needs to be absolute path
num_cpus_glycomimetics=4
glycomimetic_program_dir="/home/yao/glycomimetics"

#SBATCH --partition=CPU
#SBATCH -D ${simulation_workdir}

cd ${simulation_workdir}
#Glycomimetics
echo "#!/bin/bash
#SBATCH -D .
#SBATCH -J glycomimetics
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=${num_cpus_glycomimetics}

source /etc/profile.d/modules.sh

#${glycomimetic_program_dir}/main.exe -f ${glycomimetic_input_file}

#Now make simulation directories, one for each analog
#cd ${simulation_workdir}
glycomimetic_output_dir_with_slash=\"${simulation_workdir}/glycomimetics/${glycomimetic_output_dir}\"
simulation_workdir_with_slash=\"${simulation_workdir}/simulation\"

#../makedir.sh \${glycomimetic_output_dir_absolute_with_slash} \${simulation_workdir_absolute_with_slash}

for i in analog_* natural_ligand; do
    ../make_simulation_scripts.sh \${i}
    #sbatch slurm_submit_\${i}.sh
    sleep 1
done
echo 'Slurm glycomimetic script reaches end'
" > slurm_submit_glycomimetics.sh

sbatch slurm_submit_glycomimetics.sh



