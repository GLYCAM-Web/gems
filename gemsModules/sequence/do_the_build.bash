#!/bin/bash
export LD_LIBRARY_PATH=$GEMSHOME/gmml/lib
SeqPath="$GEMSHOME/gemsModules/sequence"
OutPath="${SeqPath}/git-ignore-me_userdata"
#uuid=$(uuidgen)
#uuid=${uuid,,}
#OutDir="${OutPath}/${uuid}"
OutDir="${OutPath}/${2}"
#echo "outdir is >>>${OutDir}<<<"
#exit
if [ ! -e ${OutPath} ] ; then
	mkdir ${OutPath}
fi
if [ ! -e ${OutDir} ] ; then
	mkdir ${OutDir}
fi
BuildMe="${SeqPath}/buildFromSeq_Temp.exe"
PrepFile="${SeqPath}/GLYCAM_06j-1.prep"
OutOFF="${OutDir}/structure.off"
OutPDB="${OutDir}/structure.pdb"

${BuildMe} ${PrepFile} $1 ${OutOFF} ${OutPDB}
