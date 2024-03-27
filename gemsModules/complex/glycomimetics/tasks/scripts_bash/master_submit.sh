glycomimetic_program_dir="/home/yao/glycomimetics"
glycomimetic_scripts_dir="/home/yao/glycomimetic_simulations/scripts"
job_workdir=$1
cd ${job_workdir}
job_workdir_absolute=$(pwd)

glycomimetic_reldir="glycomimetics"
glycomimetic_dir="${job_workdir_absolute}/${glycomimetic_reldir}"
input_filename="sample_input_file.txt"
#input_filename="sample_input_file_11_to_13.txt"
#input_filename="sample_input_file_no_O2.txt"
#input_filename="sample_input_file_with_O2.txt"
#input_filename="sample_input_file_no_R2_R3_H.txt"
#input_filename="sample_input_file_no_R2_R3_Cl.txt"
#input_filename="sample_input_file_with_R2_R3_Cl.txt"
#input_filename="sample_input_file_no_R2_R3_H.txt"

glycomimetic_input_file="${glycomimetic_dir}/${input_filename}"
#glycomimetic_output_dir=$(grep "OutputPath:" ${glycomimetic_input_file} | sed 's/OutputPath://')
#num_cpus_glycomimetics=$(grep "NumThreads:" ${glycomimetic_input_file} | sed 's/NumThreads://')

glycomimetic_output_dir="output"
num_cpus_glycomimetics=4

simulation_reldir="simulation"
simulation_dir="${job_workdir_absolute}/${simulation_reldir}"

#SBATCH --partition=CPU
#SBATCH -D ${job_workdir_absolute}


#Glycomimetics
echo "#!/bin/bash
#SBATCH -D ${job_workdir_absolute}
#SBATCH -J glycomimetics
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=${num_cpus_glycomimetics}

source /etc/profile.d/modules.sh

cd ${glycomimetic_dir}
#${glycomimetic_program_dir}/main.exe -f ${glycomimetic_input_file}
#exit 1

#Now make simulation directories, one for each analog
cd ${job_workdir_absolute}
glycomimetic_output_dir_with_slash=\"${glycomimetic_dir}/${glycomimetic_output_dir}\"

{glycomimetic_scripts_dir}/makedir.sh \${glycomimetic_output_dir_with_slash} ${simulation_dir}
#exit 1

cd ${simulation_dir}
#for i in analog_* natural; do
for i in analog_30 analog_37; do
    ${glycomimetic_scripts_dir}/make_simulation_scripts.sh \${i}
    sbatch slurm_submit_\${i}.sh
    sleep 1
done
echo 'Slurm glycomimetic script reaches end'
" > slurm_submit_glycomimetics.sh

sbatch slurm_submit_glycomimetics.sh



