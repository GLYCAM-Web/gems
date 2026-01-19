glycomimetic_scripts_dir="/home/yao/glycomimetic_simulations/scripts"
vina_score_traj_program_dir="/home/yao/glycomimetics/rescoring"
num_frames=1000
interval=5
scoring_interval=1

simulation_workdir=$1
cd ${simulation_workdir}/simulation

echo "Begin writeframe"
${glycomimetic_scripts_dir}/writeframes.sh ${num_frames} ${interval}
cd frames
${glycomimetic_scripts_dir}/extract_selected_frames.sh
cd ..

echo "Begin scoretraj"
${glycomimetic_scripts_dir}/scoretraj.sh ${scoring_interval}

echo "Finally, GBSA dG:"
mkdir -p frames/summary
rm -f frames/summary/gbsa_summary.txt

for i in analog_* natural; do
#for i in analog_14_Rob; do
    gbsa_info=""
    if grep -q "DELTA TOTAL" ${i}/4_gbsa/mmgbsa.out; then
        gbsa_info=$(grep "DELTA TOTAL" ${i}/4_gbsa/mmgbsa.out | awk '{print $3"\t "$4}')
    else
        gbsa_info="Failed"
    fi

    echo -e "${i}\t ${gbsa_info}"
    echo -e "${i}\t ${gbsa_info}" >> frames/summary/gbsa_summary.txt
done

sort -nk1 frames/summary/gbsa_summary.txt > frames/summary/gbsa_summary_sorted.txt
