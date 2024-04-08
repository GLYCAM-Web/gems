#!/bin/bash
vina_score_traj_program_dir="/home/yao/glycomimetics/rescoring"
interval=$1
if [ ! -z $1 ]; then
    echo "Interval argument supplied as $1"
    interval=$1
fi

cd frames
rm -f summary/*
if [[ ! -d cocomplex_pdbqts ]]; then
    mkdir cocomplex_pdbqts
fi

for i in analog_* natural; do
#for i in analog_39; do
    moiety_name=$(echo ${i} | sed 's/analog_//')
    echo "moiety name: ${moiety_name}"

    /home/yao/programs_src/MGLTools-1.5.4/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r ../${i}/1_leap/cocomplex_nowat_noion.pdb -A None -U None -o cocomplex_pdbqts/cocomplex_${i}.pdbqt
    if [[ ! -f "cocomplex_pdbqts/cocomplex_${i}.pdbqt" ]]; then
        echo "Warning: failed to generate cocomplex pdbqt file for ${i}. Skipping"
        continue;
    fi

    cd ${i}
    ${vina_score_traj_program_dir}/scoretraj.exe ../cocomplex_pdbqts/cocomplex_${i}.pdbqt . ${interval}

    if [[ -f output.csv ]];then
        mv output.csv ../summary/${moiety_name}.csv
    else
        echo "Scoring of ${i} failed, output.csv missing"
    fi
    cd ..
done

cd summary
for i in *.csv;do
    x=$(echo ${i} | sed 's/.csv//')
    tail -n 1 ${i} | awk -v moiety="${x}" '{print moiety"\t"$2"\t"$3}' >> summary_csv.txt
done

echo ""
cat summary_csv.txt
