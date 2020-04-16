#!/bin/bash

SourceCode="reorderSequence.cc"
Executable="reorderSequence_git-ignore-me"
OutputFile="Reordered_Output_git-ignore-me"

SequenceOne="DManpa1-3[DGalpb1-4DGalpb1-4DGalpb1-4DGalpb1-4]LRhapa1-OH"

if [ ! -e ${Executable} ] ; then

g++ -std=c++0x \
       	-I $GEMSHOME/gmml/includes/ \
       	-L$GEMSHOME/gmml/bin/ \
       	-Wl,-rpath,$GEMSHOME/gmml/bin/ \
       	${SourceCode}  \
       	-lgmml -o ${Executable}

fi


./${Executable} ${SequenceOne}  > "${OutputFile}"  2>&1
