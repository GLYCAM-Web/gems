echo "#Antechamber
nc=\$(grep \"\b${analog_name}:\" ../../charges.txt | sed \"s/${analog_name}://\")
echo \"Net charge: \${nc}\"

#Remove old temp file from last timee
#rm -rf /local/yao/${analog_name}

#If don't need to run Gaussian to calculate resp charges, turn on the comment out section to skip
<<\"comment\"
#Make Gaussian input file for optimization
${glycomimetics_scripts_dir}/make_gaussian_input_file.sh ${analog_name}_ligand.pdb ${analog_name}.chk ${analog_name}_ligand.com \${nc} ${num_cpus_emin} ${num_mem_gaussian} 0


#Gaussian 16
export g16root=${g16root}
source ${g16root}/g16/bsd/g16.profile
mkdir -p /local/yao/${analog_name}
export PBS_O_WORKDIR=\".\"
cd \${PBS_O_WORKDIR}
export GAUSS_SCRDIR=/local/yao/${analog_name}
export GAUSS_RUNDIR=\${PBS_O_WORKDIR}


#Run optimization
/programs/gaussian/16/g16/g16 \${GAUSS_RUNDIR}/${analog_name}_ligand.com \${GAUSS_RUNDIR}/${analog_name}_ligand_g16.log

#exit 1

#Make Gaussian input file for ESP calculation
${glycomimetics_scripts_dir}/make_gaussian_input_file.sh ${analog_name}_ligand.pdb ${analog_name}_esp.chk ${analog_name}_ligand_esp.com \${nc} ${num_cpus_emin} ${num_mem_gaussian} 1

#Run ESP calculation
/programs/gaussian/16/g16/g16 \${GAUSS_RUNDIR}/${analog_name}_ligand_esp.com \${GAUSS_RUNDIR}/${analog_name}_ligand_esp_g16.log


#exit 1

#Make RESP input file
${glycomimetic_program_dir}/autogen_resp_input/main.exe ${analog_name}_ligand_noconect.pdb \${nc} ${analog_name}_resp.in
#Do RESP calculation
num_atoms=\$(grep -c \"ATOM\" ${analog_name}_ligand.pdb)
num_het_atoms=\$(grep -c \"HETATM\" ${analog_name}_ligand.pdb)
let "num_atoms+=\${num_het_atoms}"
echo \"Num atoms : \${num_atoms}\"
${glycomimetics_scripts_dir}/Run.resp ${analog_name}_ligand_esp_g16.log \${num_atoms} ${analog_name}_resp.in ${analog_name}_resp.out ${analog_name}_resp.pch ${analog_name}_resp_charges.out 

#exit 1
comment


echo \"antechamber -i ${analog_name}_ligand.pdb -fi pdb -o corona.mol2 -fo mol2 -c bcc -s 2 -nc \${nc}\"
antechamber -i ${analog_name}_ligand.pdb -fi pdb -o corona.mol2 -fo mol2 -at gaff

#Frcmod
parmchk2 -i corona.mol2 -f mol2 -o corona.frcmod

#Interfacing
mol2=corona.mol2
ligand_pdb=${ligand_pdb}
pdb2glycam_log=${analog_name}_pdb2glycam.log
amber_gaff_dat=\"${interface_glycam_gaff_path}/gaff.dat\"
antechamber_frcmod=corona.frcmod
output_glycam_gaff_frcmod=${analog_name}_glycam_gaff.frcmod
output_glycam_gaff_off=${analog_name}_glycam_gaff.off
resp_output_file=${analog_name}_resp_charges.out

if [[ ! -f \${pdb2glycam_log} ]];then
    pdb2glycam_log=\"none\"
fi
if [[ ! -f \${resp_output_file} ]];then
    resp_output_file=\"none\"
fi

echo \"Calling interface\"
#Use this when calculating RESP charges of R groups. 
${interface_glycam_gaff_path}/main.exe \${mol2} ${analog_name}_ligand_noconect.pdb \${pdb2glycam_log} \${amber_gaff_dat} \${antechamber_frcmod} ${analog_name}_resp_charges.out \${output_glycam_gaff_frcmod} \${output_glycam_gaff_off} \${nc}

#Use this for virtual screening.
#${interface_glycam_gaff_path}/main.exe \${mol2} ${analog_name}_ligand_noconect.pdb \${pdb2glycam_log} \${amber_gaff_dat} \${antechamber_frcmod} none \${output_glycam_gaff_frcmod} \${output_glycam_gaff_off} \${nc}

#exit 1

#tleap
if [[ -f \${pdb2glycam_log} ]];then
    ${glycomimetics_scripts_dir}/tleap.sh ${analog_name} "true"
else
    ${glycomimetics_scripts_dir}/tleap.sh ${analog_name} "false"
fi


#Make input files
${autogen_input_path}/main.exe receptor_nowat_noion.pdb cocomplex_nowat_noion.pdb ../2_min/min_H.in ../2_min/min_solvent.in ../2_min/min_all.in ../3_md//heat.in ../3_md/equi_restraint.in ../3_md/equi.in ../3_md/md.in ../4_gbsa/mmgbsa.in ../4_gbsa/_MMPBSA_gb_decomp_com.mdin  ../4_gbsa/_MMPBSA_gb_decomp_lig.mdin  ../4_gbsa/_MMPBSA_gb_decomp_rec.mdin
#exit 1



#Energy minimization
cd ../2_min
export pmemd=\"mpirun -np ${num_cpus_emin} \${AMBERHOME}/bin/pmemd.MPI\"
wallclock=\"Total wall time\"

#<<\"comment\"
#Minimize all hydrogen atoms only
\${pmemd} -O \\
 -p ../1_leap/cocomplex.prmtop \\
 -c ../1_leap/cocomplex.rst7 \\
 -i min_H.in \\
 -o min_H.out \\
 -r min_H.rst7 \\
 -ref ../1_leap/cocomplex.rst7

if grep -q \"\${wallclock}\" min_H.out ; then
#Solvent minimization
    \${pmemd} -O \\
     -p ../1_leap/cocomplex.prmtop \\
     -c min_H.rst7 \\
     -i min_solvent.in \\
     -o min_solvent.out \\
     -r min_solvent.rst7 \\
     -ref min_H.rst7
fi

if grep -q \"\${wallclock}\" min_solvent.out ; then
    #all atom minimization
    \${pmemd} -O \\
     -p ../1_leap/cocomplex.prmtop \\
     -c min_solvent.rst7 \\
     -i min_all.in \\
     -o min_all.out \\
     -r min_all.rst7 \\
     -ref min_solvent.rst7
fi


cd ../3_md
#Heating
if grep -q \"\${wallclock}\" ../2_min/min_all.out ; then
    \${pmemd} -O \\
     -p ../1_leap/cocomplex.prmtop \\
     -c ../2_min/min_all.rst7 \\
     -i heat.in \\
     -o heat.out \\
     -r heat.rst7 \\
     -ref ../2_min/min_all.rst7
fi

#comment
#Temporary, remember to remove
cd ../3_md

if grep -q \"\${wallclock}\" heat.out ; then
    sbatch ../../simulation_${analog_name}_md.sh
fi
" > simulation_${analog_name}_Emin.sh

