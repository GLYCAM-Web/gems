#${glycomimetics_scripts_dir}/make_gaussian_input_file.sh ${analog_name}_ligand.pdb ${analog_name}_ligand.com ${nc}
ligand_pdb=$1
check_file=$2
gaussian_input=$3
net_charge=$4
num_cpus=$5
num_mem=$6
gaussian_opt_output=$7
#Input file type is either 0 (opt) or 1 (ESP)
input_file_type=$7

#echo "#HF/6-31G* Opt=(Tight,CalcFC,maxcycle=200) Freq SCF(Conver=8) Test" >> ${gaussian_input}


if [[ ${input_file_type} ==  "0" ]]; then
    #The 1st line below doesn't matter. I'm inputing the correct value, but it is effectively ignored.
    echo "${net_charge},1" > newzmat_here.txt
    echo "%Chk=${check_file}" >> newzmat_here.txt
    echo "%mem=${num_mem}" >> newzmat_here.txt
    echo "%NProcShared=${num_cpus}" >> newzmat_here.txt

    restart="false"
    if [[ -f ${gaussian_opt_output} ]];then
        if grep -q "Number of steps exceeded" ${gaussian_opt_output}; then
            if grep -q "Error termination" ${gaussian_opt_output}; then
                echo "#HF/6-31+G* Opt(restart,maxcycle=1000) geom=connectivity" >> newzmat_here.txt
                restart="true"
            fi
        fi
    fi

    if [[ ${restart} == "false" ]];then
        echo "#HF/6-31+G* Opt(maxcycle=1000) geom=connectivity" >> newzmat_here.txt
    fi

    echo "" >> newzmat_here.txt
    echo "Opt then ESP">> newzmat_here.txt
    echo "" >> newzmat_here.txt
    echo "${net_charge},1" >> newzmat_here.txt

    newzmat -ipdb -ozmat -prompt ${ligand_pdb} ${gaussian_input} < newzmat_here.txt

elif [[ ${input_file_type} ==  "1" ]]; then
    #Make input for ESP calculation
    echo "Entering elif"
    old_chk=$(echo ${check_file} | sed 's/_esp//')
    #echo "${net_charge},1" > newzmat_here_esp.txt
    echo "%OldChk=${old_chk}" > newzmat_here_esp.txt
    echo "%Chk=${check_file}" >> newzmat_here_esp.txt
    echo "%mem=${num_mem}" >> newzmat_here_esp.txt
    echo "%NProcShared=${num_cpus}" >> newzmat_here_esp.txt
    echo "#HF/6-31+G* pop=chelpg iop(6/33=2) geom=(connectivity)" >> newzmat_here_esp.txt
    echo "" >> newzmat_here_esp.txt
    echo "ESP calculation of the optimized ligand structure" >> newzmat_here_esp.txt
    echo "" >> newzmat_here_esp.txt
    echo "${net_charge},1" >> newzmat_here_esp.txt

    newzmat -ichk -ozmat -prompt ${old_chk} ${gaussian_input} < newzmat_here_esp.txt

else
    echo "Unknown file type requested. Must be 0 for opt and 1 for ESP"
fi


<<"comment"
#Make input for optimization
echo "%Chk=${check_file}" > ${gaussian_input}
echo "%mem=${num_mem}" >> ${gaussian_input}
echo "%NProcShared=${num_cpus}" >> ${gaussian_input}
echo "#HF/6-31+G* Opt(Cartesian,Restart,calcfc,maxcycle=500)" >> ${gaussian_input}
echo "" >> ${gaussian_input}
echo "Optimization of the ligand structure" >> ${gaussian_input}
echo "" >> ${gaussian_input}
echo "${net_charge} 1" >> ${gaussian_input}

grep "ATOM\|HETATM" ${ligand_pdb} | awk '{print substr($0,77,2)" "substr($0,31,24)}' >> ${gaussian_input}
echo -e "\n\n" >> ${gaussian_input}
comment

