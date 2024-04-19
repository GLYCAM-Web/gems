gaussian_log_file=$1
num_atoms=$2
resp_input_file=$3
resp_output_file=$4
pch_output_file=$5
charge_output_file=$6
glycomimetic_scripts_dir="/home/yao/glycomimetic_simulations/scripts"

#${glycomimetics_scripts_dir}/run_resp.sh ${analog_name}_ligand_g16.log ${num_atoms} ${analog_name}_resp.in ${analog_name}_resp.out ${analog_name}_resp.pch ${analog_name}_resp_charges.out

rm -f a b c esp.dat count esout

npoints=$(grep "points will be used for fitting atomic charges" ${gaussian_log_file} | awk '{print $1}')
echo " ${npoints}" > count
echo ${num_atoms} >> count

#gfortran ${glycomimetic_scripts_dir}/readit.f >& /dev/null

grep "Atomic Center " ${gaussian_log_file} > a
grep "ESP Fit" ${gaussian_log_file} > b
grep "Fit    " ${gaussian_log_file} > c
#sed -n '/ESP charges:/,/Sum of ESP charges/p' ${gaussian_log_file} |tail -n +3 | head -n -1 | awk '{print $3}' | paste -sd" " > qin
${glycomimetic_scripts_dir}/a.out
#rm -f a b c a.out readit.o

#Call resp
/cm/shared/apps/amber20/bin/resp -O \
    -i ${resp_input_file} \
    -o ${resp_output_file} \
    -p ${pch_output_file} \
    -q qin \
    -e esp.dat \
    -t ${charge_output_file}

#rm count esout
