#!/bin/bash
g++ -std=c++11 -I$GEMSHOME/gmml/includes -L$GEMSHOME/gmml/lib temp_build_default_structure.cpp -o buildFromSeq_Temp.exe -lgmml 
