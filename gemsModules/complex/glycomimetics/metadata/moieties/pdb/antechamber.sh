count=0
cd done1
for i in 10_4_*.pdb;do
    let "count = count + 1"
    echo "processing $i, file $count"
    x=$(echo $i | sed 's/.pdb//')
    read -p "Enter net charge: " nc
    antechamber -i $i -fi pdb -o ${x}.mol2 -fo mol2 -c bcc -s 2 -nc $nc
    parmchk -i ${x}.mol2 -f mol2 -o ${x}.frcmod
done

rm ANTECHAMBER_* sqm.* ATOMTYPE.INF
cd ..
    
