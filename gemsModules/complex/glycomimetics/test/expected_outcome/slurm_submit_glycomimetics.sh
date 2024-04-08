#!/bin/bash
#SBATCH -D /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library
#SBATCH -J glycomimetics
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node=8

source /etc/profile.d/modules.sh

cd /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library/glycomimetics
#/home/yao/glycomimetics/main.exe -f /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library/glycomimetics/sample_input_file.txt

#Now make simulation directories, one for each analog
cd /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library
glycomimetic_output_dir_with_slash="/home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library/glycomimetics/output"

#/home/yao/glycomimetic_simulations/scripts/makedir.sh ${glycomimetic_output_dir_with_slash} /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library/simulation
#exit 1

cd /home/yao/glycomimetic_simulations/virtual_screening/flu_3ubq_N5_aldehyde_library/simulation
#for i in analog_* natural; do
for i in natural; do
    /home/yao/glycomimetic_simulations/scripts/make_simulation_scripts.sh ${i}
    sbatch slurm_submit_${i}.sh
    sleep 1
done
echo 'Slurm glycomimetic script reaches end'

