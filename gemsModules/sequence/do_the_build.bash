#!/bin/bash
export LD_LIBRARY_PATH=$GEMSHOME/gmml/lib


#Path used in development. Not in line with Django expectations.
SequenceModulePath="$GEMSHOME/gemsModules/sequence"

#This is the preferred output destination for sequence builds as expected by Django.
SeqPath="/website/userdata/tools/cb"

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

BuildMe="${SequenceModulePath}/buildFromSequence.py"
PrepFile="${SequenceModulePath}/GLYCAM_06j-1.prep"

OutOFF="${OutDir}/structure.off"
OutPDB="${OutDir}/structure.pdb"

echo "SequenceModulePath: ${SequenceModulePath}"
echo "BuildMe: ${BuildMe}"
echo "PrepFile: ${PrepFile}"
echo "OutOFF: ${OutOFF}"
echo "OutPDB: ${OutPDB}"
echo "The command: ${BuildMe} ${PrepFile} $1 ${OutOFF} ${OutPDB}"
echo "~~~Doing the build."

${BuildMe} ${PrepFile} $1 ${OutOFF} ${OutPDB}

echo "~~~Finished doing the build."