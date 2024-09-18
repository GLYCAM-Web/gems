#!/bin/bash

# We must use a bash wrapper so that change directory works as intended.

PROJECT_DIR=$1
PDB_FILE=$2
#EVALUATE_EXE=$3
EVALUATE_EXE="$GLYCOMIMETICS_WEBTOOL/internal/glycomimetics/validation/main.exe"
if [ ! -f $EVALUATE_EXE ]; then
    exit 2
fi 

# cd $PROJECT_DIR
# echo "PROJECT_DIR: $PROJECT_DIR" >> $GEMSHOME/gems_error.log
# echo "CWD: $(pwd)" >> $GEMSHOME/gems_error.log

$EVALUATE_EXE $PDB_FILE $PROJECT_DIR/available_atoms.txt >$PROJECT_DIR/evaluation.log 2>$PROJECT_DIR/evaluate.err
if [ $? -ne 0 ]; then
    exit 1
fi