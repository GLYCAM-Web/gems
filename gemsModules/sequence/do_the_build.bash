#!/bin/bash
export LD_LIBRARY_PATH=$GEMSHOME/gmml/lib

echo "GEMSHOME: $GEMSHOME" 

SeqPath="/website/userdata/tools/cb"
#SeqPath="$GEMSHOME/gemsModules/sequence"
SeqModulePath="${GEMSHOME}/gemsModules/sequence"
echo "SeqModulePath: $SeqModulePath" 

OutPath="${SeqPath}/git-ignore-me_userdata"
#uuid=$(uuidgen)
#uuid=${uuid,,}
#OutDir="${OutPath}/${uuid}"
OutDir="${OutPath}/${2}"
echo "OutDIR is >>>${OutDir}<<<"
#exit
if [ ! -e ${OutPath} ] ; then
	mkdir - p ${OutPath}
fi
if [ ! -e ${OutDir} ] ; then
	mkdir  -p ${OutDir}
fi

BuildMe="${SeqModulePath}/buildFromSeq_Temp.exe"
echo "BuildMe: ${BuildMe}"
PrepFile="${SeqModulePath}/GLYCAM_06j-1.prep"
echo "PrepFile: ${PrepFile}"
OutOFF="${OutDir}/structure.off"
echo "OutOFF: ${OutOFF}"
OutPDB="${OutDir}/structure.pdb"
echo "OutPDB: ${OutPDB}"


${BuildMe} ${PrepFile} $1 ${OutOFF} ${OutPDB}
