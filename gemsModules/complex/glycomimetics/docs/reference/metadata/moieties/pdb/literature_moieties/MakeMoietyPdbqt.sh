count=0
for i in *.pdb;do
    let "count = count + 1"
    echo "processing $i, file $count"
    x=$(echo $i | sed 's/.pdb//')
    /home/yao/programs_src/MGLTools-1.5.4/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r $i -A None -U None -o ${x}.pdbqt

    sed -i '/REMARK/d' ${x}.pdbqt
    sed -i '1s;^;REMARK DUMMY_ATOM=\n;' ${x}.pdbqt
    sed -i '1s;^;REMARK REAL_HEAD_ATOM=\n;' ${x}.pdbqt
    sed -i '1s;^;REMARK FAKE_HEAD_ATOM=\n;' ${x}.pdbqt
    sed -i '1s;^;MODEL 0\n;' ${x}.pdbqt
    sed -i '$s/$/\nENDMDL/' ${x}.pdbqt
done
