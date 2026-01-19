#!/usr/bin/env bash
# TODO: abstract the root_dir
# Main generation script for glycomimetics simulations.
root_dir="/home/yao"


export dirname=$1
export autogen_input_path="${root}/glycomimetics/autogen_md_input_files"
export autogen_input_path="${root}/glycomimetics/autogen_md_input_files"
export interface_glycam_gaff_path="${root}/glycomimetics/glycam_gaff_interfacing"
export glycomimetic_program_dir="${root}/glycomimetics"
export glycomimetics_scripts_dir="${root}/glycomimetic_simulations/scripts"
export num_cpus_emin=7
export num_cpus_gbsa=7
export num_mem_gaussian="1024MB"
export g16root="/programs/gaussian/16"


if [[ ${dirname} == "natural_ligand" ]]; then
    analog_name="natural"
else
    analog_name=$(echo ${dirname} | sed "s/analog_//")
fi
echo "Processing ${analog_name}"

export ligand_pdb="${analog_name}_ligand.pdb"


./make_1_slurm.sh
./make_2_md.sh
./make_3_emin.sh
./make_4_gbsa.sh