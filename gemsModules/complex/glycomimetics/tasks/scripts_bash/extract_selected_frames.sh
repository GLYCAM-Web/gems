rm -r selected_frames
mkdir -p selected_frames
for i in analog_* natural; do
    for j in 1 50 100 150 200; do 
        echo "cp ${i}/${j}.pdb selected_frames/${i}_${j}.pdb"
        cp ${i}/${j}.pdb selected_frames/${i}_${j}.pdb
    done
done
