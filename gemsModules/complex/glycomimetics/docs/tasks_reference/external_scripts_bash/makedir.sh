glycomimetic_output_dir=$1 #Absolute path
simulation_workdir=$2 #Absolute path

cd ${simulation_workdir}

prefix="analog"

if [[ ! -d natural ]];then
    mkdir natural
    mkdir natural/1_leap  natural/2_min  natural/3_md natural/4_gbsa
fi


cd ${glycomimetic_output_dir}
for i in *_ligand.pdb; do
    #echo $i
    x=$(echo ${i} | sed 's/_ligand.pdb//')
    if [[ -f *${x}*clash* ]];then
        echo "${i} is too large to fit in the binding site. Won't run it through MD"
        continue
    fi

    if [[ ${i} != "natural"* ]]; then
        dirname=${prefix}_${x}
        full_path=${simulation_workdir}/${dirname}
    else
        full_path=${simulation_workdir}/${x}
    fi

    mkdir -p ${full_path}/1_leap  ${full_path}/2_min  ${full_path}/3_md ${full_path}/4_gbsa
    cp ${i} ${x}_receptor.pdb ${x}_pdb2glycam.log ${full_path}/1_leap
    sed '/CONECT/d' ${i} > ${full_path}/1_leap/${x}_ligand_noconect.pdb
        
done

