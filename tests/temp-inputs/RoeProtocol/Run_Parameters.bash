#!/usr/bin/env bash

################################################################################
##
## This file holds parameters to be read into Run_Multi-Part_Simulation.bash
##
## Please see that script for documentation.
##
## Here, all parameters are explicitly set, even those left at defaults.
##
################################################################################

thisAMBERHOME='DETECT'
PRMTOP='mol_min_t3p.parm7'
INPCRD='mol_min_t3p.restrt.nc'
coordOutputFormat="NetCDF"  ## ntwo=2 - much smaller files; not human readable
restrtSuffix='restrt.nc'
mdSuffix='nc'
outputFileName='run_simulation.out'

mdEngine=pmemd
useMPI=Y
numProcs=4
useCUDA=N
allowOverwrite=N

writeCommands=Only

runPrefix[0]='1.min'
runPrefix[1]='2.relax'
runPrefix[2]='3.min'
runPrefix[3]='4.min'
runPrefix[4]='5.min'
runPrefix[5]='6.relax'
runPrefix[6]='7.relax'
runPrefix[7]='8.relax'
runPrefix[8]='9.relax'
runPrefix[9]='10.produ'
runDescription[0]='Water-only min'
runDescription[1]='Water-only min'
runDescription[2]='Water-only min'
runDescription[3]='Water-only min'
runDescription[4]='Water-only min'
runDescription[5]='Water-only relax'
runDescription[6]='Water-only relax'
runDescription[7]='Glycan rings and protein backbone restrained relax'
runDescription[8]='Full system relaxation (no restraints)'
runDescription[9]='MD production run'
