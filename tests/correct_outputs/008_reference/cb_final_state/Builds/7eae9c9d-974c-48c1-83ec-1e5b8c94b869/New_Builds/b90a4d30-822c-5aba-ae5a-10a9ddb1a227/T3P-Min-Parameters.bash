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
PRMTOP='unminimized-t3p.parm7'
INPCRD='unminimized-t3p.rst7'
coordOutputFormat="NetCDF"  ## ntwo=2 - much smaller files; not human readable
restrtSuffix='restrt.nc'
mdSuffix='nc'
outputFileName='t3p-minimization.log'

mdEngine=pmemd
useMPI=Y
numProcs=4
useCUDA=N
allowOverwrite=N

writeCommands=Yes

runPrefix[0]='min-t3p'
runDescription[0]='T3P-solvated minimization'
