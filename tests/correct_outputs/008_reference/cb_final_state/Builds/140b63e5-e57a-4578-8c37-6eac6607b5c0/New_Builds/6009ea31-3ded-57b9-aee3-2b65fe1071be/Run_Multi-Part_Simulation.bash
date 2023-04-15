#!/usr/bin/env bash

################################################################################
## File:  Run_Multi-Part_Simulation.bash
################################################################################
##
## This script will run one or more MD simulations for you using AMBER
##
## Look below this section to see the script defaults. 
##
## All defaults can be overridden by specifying new values in a separate file.
##
## By default, the script expects to find the file in your current directory 
## and expects it to be 'Run_Parameters.bash'. 
##
## You may change this behavior by:
##
##      - Setting the environment variable called 'GW_RUN_PARAMETERS' so 
##        that it points to whatever file you like.
##
##      - Adding the file name (with path if needed) as an argument on the
##        command line
##
if [ "${GW_RUN_PARAMETERS}zzz" == "zzz" ] ; then
	GW_RUN_PARAMETERS="./Run_Parameters.bash"
fi
if [ "${1}zzz" != "zzz" ] ; then
	GW_RUN_PARAMETERS="${1}"
fi
##
##
################################################################################
## Parameters that can be overridden in the Run Parameters file start here.
################################################################################
##
## Tell the script how to get your AMBERHOME:
## Set thisAMBERHOME to DETECT if you want the script to try to detect it.
## Otherwise, set thisAMBERHOME to your AMBERHOME absolute path.
thisAMBERHOME='DETECT'
#thisAMBERHOME='/path/to/your/amber'
#
## Replace these with the names of your prmtop and inpcrd files
PRMTOP='structure.parm7'
INPCRD='structure.rst7'
#
## Choose the output format for coordinates
## NOTE !  Make sure this matches the ntwo entry in your input files.  To use
##         this script, all files must use the same coordinate output format.
coordOutputFormat="NetCDF"  ## ntwo=2 - much smaller files; not human readable
#coordOutputFormat="ASCII"  ## ntwo=1 - larger file sizes; is human readable
#
## Choose either sander or pmemd as your MD engine
##    - sander is freely distributed with AmberTools, but isn't fast
##    - pmemd requires an AMBER license (prices are generally reasonable)
##      pmemd is much faster than sander, so use it if you have the choice
## Note - there can be only one mdEngine for a given call of this script.
mdEngine=pmemd
# mdEngine=sander
##
## Will you be running your simulation in parallel ('useMPI')?
## NOTE! This is not the same as using CUDA (below).  It is possible to be
##      only parallel, only CUDA, both, or neither.
useMPI=Y
# useMPI=N
#
# If you chose Y for useMPI, specify the number of processors
# Replace '4' with your number of processors, if that is a different number
numProcs=4
##
## Will you be running your simulation using CUDA?
## We expect that more users will have ready access to plain MPI than to CUDA,
##       so we set the default to be no.
useCUDA=N
# useCUDA=Y
##
## Would you like this script to print out the job submission commands?
## These will be printed to outputFileName, below.
##     - Yes  = print the job submisison commands
##     - No   = do not print the job submisison commands
##     - Only = only print the job submisison commands; do NOT actually run 
##              the simulations (for troubleshooting)
writeCommands=Yes
# writeCommands=No
# writeCommands=Only
##  
## You can change the name of the output file if you like. 
## This file will contain a log from the point of view of this script.
outputFileName='run_simulation.log'
##  
## The allowOverwrite variable controls whether the simulation will 
##      overwrite any pre-existing files.
## It is useful to set it to 'N' if you don't want a restarted simulation
##      to overwrite files that were already begun. 
allowOverwrite=Y
# allowOverwrite=N
##
## Change these if you want to alter the number of consecutive runs and
##      their prefixes.  Please also update the descriptive texts.
##
## NOTE - these prefixes are important, and your filenames must match.
##
##        Make sure that your run control ('mdin') files are named like:
##
##                  runPrefix[i].in
##
##        For example, if left unchanged, this script expects that 
##        the mdin files for the three simulations are called:
##            relax1.in  relax2.in  md.in
##
declare -a runPrefix
runPrefix[0]='gp_min'
declare -a runDescription
runDescription[0]='Gas-Phase Minimization'
declare -a runEngine
runEngine[0]='sander'
##
##
## If you are so inclined, you can change the output suffix, but these
## options are pretty standard, so leaving them as-is should be good for
## most applications.
if [ "${coordOutputFormat}" == "NetCDF" ] ; then
	restrtSuffix='restrt.nc'
	mdSuffix='nc'
elif [ "${coordOutputFormat}" == "ASCII" ] ; then
	restrtSuffix='rst7'
	mdSuffix='mdcrd'
else
	echo "Value of coordOutputFormat variable unrecognized.  Exiting."
	exit
fi
##
## Check to see if we are just testing the overall workflow.
## This can be set using the input file as described above.
## It can also be set using the environment variable MDUtilsTestRunWorkflow
## If MDUtilsTestRunWorkflow disagrees with testWorkflow, the
## value assigned to MDUtilsTestRunWorkflow will be used.
##
## If set, the script will set:
##               maxcyc, ncyc, ntwr and nstlim to 1.
## WARNING: 
##       It will do this using sed.  The input files will be changed in place.  
##    
testWorkflow=No
#testWorkflow=Yes
##
################################################################################
## This is the end of the parameters that can be overridden.
##
## Normal users should not need to read anything below this line.
################################################################################
##
# Read in the Run Parameters file, if it exists.
FoundRunParameterFile=No
if [ -f "${GW_RUN_PARAMETERS}" ] ; then
	FoundRunParameterFile=Yes
	. ${GW_RUN_PARAMETERS}
fi
if [ "${MDUtilsTestRunWorkflow}" == "Yes" ] ; then
	testWorkflow=Yes
fi
##
# Start the ouput file
echo "Beginning MD simulations on $(date)" | tee ${outputFileName}
echo "Working directory is $(pwd)" | tee -a ${outputFileName}
if [ "${FoundRunParameterFile}" == "Yes" ] ; then
	echo "Using info from file: '${GW_RUN_PARAMETERS}'. " | tee -a ${outputFileName}
else
	echo "No file called '${GW_RUN_PARAMETERS}' found.  Using internal defaults. " | tee -a ${outputFileName}
fi

##
##
# Source needed information from AMBERHOME
##
# First, see if an AMBERHOME is defined in the environment
if [ "${AMBERHOME}zzz" == "zzz" ] ; then
	amberhomeDefined='No'
else
	amberhomeDefined='Yes'
fi
# If we were instructed to detect AMBERHOME, 
detectAMBERHOME='No'
if [ "${thisAMBERHOME}" == "DETECT" ] ; then 
	detectAMBERHOME='Yes'
	if [ "${amberhomeDefined}" == "Yes" ] ; then
		thisAMBERHOME=${AMBERHOME}
	else
		echo "Could not Detect AMBERHOME.  Exiting." | tee -a ${outputFileName}
		exit 1
	fi
fi
if [ ! -d ${thisAMBERHOME} ] ; then
echo "
!!!!!!!!!!!!!!!  
Strong Warning 
!!!!!!!!!!!!!!!  
Cannot find AMBERHOME.  This is likely to cause problems if this is an attempt 
to actually run a simulation (as opposed to a test of the script, for example).
The script thinks that the following is AMBERHOME:
${thisAMBERHOME}
" | tee -a ${outputFileName}
if [ "${detectAMBERHOME}" == "No" ] ; then
	if [ "${amberhomeDefined}" == "Yes" ] ; then
		echo "The environment defines AMBERHOME as: ${AMBERHOME}
		" | tee -a ${outputFileName}
	fi
fi
fi
AMBERHOME=${thisAMBERHOME}
if [ -e ${AMBERHOME}/amber.sh ] ; then
	source ${AMBERHOME}/amber.sh
fi

##
# Set the contents of checkText according to the MD Engine
if [ "${mdEngine}" == "pmemd" ] ; then 
	checkText='Total wall time'
	useLogFile=Y
elif [ "${mdEngine}" == "sander" ] ; then 
	checkText='wallclock() was called'
	useLogFile=N
else
	echo "mdEngine other than pmemd or sander was specified.  Exiting." | tee -a ${outputFileName}
fi
echo "
The mdEngine is ${mdEngine} and the text to check for success is '${checkText}'." | tee -a ${outputFileName}

##
# Set the runs to use CUDA if requested
if [ "${useCUDA}" == "Y" ] ; then 
	if [ "${mdEngine}" != "pmemd" ] ; then 
		echo "mdEngine other than pmemd requested with CUDA.  Exiting." | tee -a ${outputFileName}
	fi
	mdEngine="${mdEngine}.cuda"
fi

##
# Set the runs to use MPI if requested
if [ "${useMPI}" == "Y" ] ; then 
	mdEngine="mpirun ${mdEngine}.MPI -np ${numProcs} "
fi

##
# Set the runs to allow overwriting if requested
if [ "${allowOverwrite}" == "Y" ] ; then 
	mdEngine="${mdEngine} -O "
fi

## Tell everyone what the complete command is:
echo "Complete mdEngine command is '${mdEngine}'." | tee -a ${outputFileName}

echo "
There will be ${#runPrefix[@]} phases to this simulation:
" | tee -a ${outputFileName}
i=0
while [ "${i}" -lt "${#runPrefix[@]}" ] ; do
	j=$((i+1))
	echo "Phase ${j} has prefix ${runPrefix[${i}]} and is described as: ${runDescription[${i}]}" | tee -a ${outputFileName}
	i=${j}
done

## build_run_command phase-index 
#    phase-index starts with zero
build_run_command() {
	thisi=${1}
	if [ "${thisi}" == "0" ] ; then
		thisRST=${INPCRD}
	else
		lasti=$((thisi-1))
		thisRST=${runPrefix[${lasti}]}.${restrtSuffix}
	fi
COMMAND="${mdEngine} \
 -i ${runPrefix[${thisi}]}.in \
 -o ${runPrefix[${thisi}]}.o \
 -e ${runPrefix[${thisi}]}.en \
 -p ${PRMTOP} \
 -c ${thisRST} \
 -r ${runPrefix[${thisi}]}.${restrtSuffix} \
 -x ${runPrefix[${thisi}]}.${mdSuffix} \
 -inf ${runPrefix[${thisi}]}.info \
 -ref ${INPCRD} "

if [ "${useLogFile}" == "Y" ] ; then
COMMAND="${COMMAND} \
 -l ${runPrefix[${thisi}]}.log "
fi
export COMMAND
}


##  Do the runs
#
i=0
while [ "${i}" -lt "${#runPrefix[@]}" ] ; do
	j=$((i+1))
	echo "
	Starting phase ${j}" | tee -a ${outputFileName}
	#
	#  Build the command for this phase
	build_run_command ${i}
	if [ "${testWorkflow}" == "Yes" ] ; then
		sed -i s/maxcyc\ *=\ *[1-9][0-9]*/maxcyc\ =\ 1/ ${runPrefix[${i}]}.in 
		sed -i s/ncyc\ *=\ *[1-9][0-9]*/ncyc\ =\ 1/ ${runPrefix[${i}]}.in 
		sed -i s/nstlim\ *=\ *[1-9][0-9]*/nstlim\ =\ 1/ ${runPrefix[${i}]}.in 
		sed -i s/ntwr\ *=\ *[1-9][0-9]*/ntwr\ =\ 1/ ${runPrefix[${i}]}.in 
	fi
	#
	#  Write it to a file if desired
	if [ "${writeCommands}" != "No" ] ; then
		echo "
		The command is:
		${COMMAND}

		" | tee -a ${outputFileName}
	fi
	#
	#  Run the command unless told not to 
	if [ "${writeCommands}" != "Only" ] ; then
		eval ${COMMAND}
		#
		# Check if the command worked
		if ! grep -q "$wallclock" ${runPrefix[${i}]}.o ; then
			echo "

Something went wrong for run phase $((thisi+1)).
The simulation cannot continue.  Exiting.

"  | tee -a ${outputFileName}
			exit 1
		fi
	fi

	i=${j}
done

