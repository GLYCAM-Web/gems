#!/usr/bin/env bash

################################################################################
##
## This file performs the standard build and minimization for glycans
## built using the tools at GLYCAM-Web and associated software.
##
## AMBERHOME must be either:
##     *  set as an environment variable.
##     *  set in a file called 'Minimize-Parameters.bash'
##
## The following parameters may be overridden in Minimize-Parameters.bash
WORKDIR="$(pwd)"
LOGFILE="${WORKDIR}/Sequence_Prep_details.log"  ## Log file is very chatty, for tracking problems
STATUSFILE="${WORKDIR}/Sequence_Prep_status.log"  ## Status file is terse, with date/time stamps each line
##
## The following parameters may be overridden:
##     *  in Minimize-Parameters.bash
##     *  by setting an environment variable.
##           Note that the environment variable has a different name.
##
## If vars must be reset or commands run after the AMBER workflows, put them in a
## file with this name:
##     Amber-Prolog.bash
##
# Set this one to 'Yes' if you don't want to perform a full simulation but
# just want to make sure the workflow functions.  This makes the MD sims only
# run for a single step each.
testWorkflow=No   ## Environment variable:  MDUtilsTestRunWorkflow
# testWorkflow=Yes   
##
################################################################################

MAKE_GW_ZIPS="False" # can be overridden in Minimize-Parameters.bash as needed
if [ ! -z GW_DOMAIN ] ; then
	MAKE_GW_ZIPS="True" # can be overridden in Minimize-Parameters.bash as needed
	conformer_dir_name="$(basename ${WORKDIR})"
	cd ../../
	PROJECT_DIR="$(pwd)"
	project_dir_name="$(basename ${PROJECT_DIR})"
	PROJECT_STATLOG="${PROJECT_DIR}/zip_status.log"
	PROJECT_DEETLOG="${PROJECT_DIR}/zip_details.log"
	pUUID="$(grep pUUID logs/response.json | tail -1 | tr -d ' ' | tr -d '"' | tr -d ',' | cut -d ':' -f2)"
	if [ "${project_dir_name}" != "${pUUID}" ] ; then
		echo "INFO : The project directory name is not the same as the pUUID." >> ${LOGFILE}
	        echo "INFO : Using the directory name for naming the zip archive.">> ${LOGFILE}
	        echo "INFO : pUUID is given as: ${pUUID}">> ${LOGFILE}
	        echo "INFO : project directory name is: ${project_dir_name}">> ${LOGFILE}
	        echo "INFO : This message may be benign if this conformer processed before response.json exists.">> ${LOGFILE}
		project_ID_name="${project_dir_name:0:8}"
	else
		project_ID_name="${pUUID:0:8}"
	fi
	project_zipname="CB_project_${project_ID_name}_all.zip"
	conformer_zip_prefix="CB_conformer_${conformer_dir_name}"
	cd ${WORKDIR}
fi

# things can be overridden in this file if needed
if [ -f Minimize-Parameters.bash ] ; then
	. Minimize-Parameters.bash
fi


# Pass workflow information along if needed
if [ "${MDUtilsTestRunWorkflow}" == "Yes" ] ; then
	export MDUtilsTestRunWorkflow=Yes
fi
if [ "${testWorkflow}" == "Yes" ] ; then
	export MDUtilsTestRunWorkflow=Yes
fi

# If we should make zip files, declare the name of the project-level zip file
if [ "${MAKE_GW_ZIPS}" == "True" ] ; then
	echo "Project zipname is >>>${project_zipname}<<<" >> ${LOGFILE}
fi

write_return_value_info_to_log_status()
{
	Write_Project_Logs="False"
	Val="${1}"  ## the return value
	Mess="${2}"  ## the action message
	if [ ! -z "${3}" ] ; then
		Write_Project_Logs="${3}"
	fi
	if [ "${Val}" == "18" ] ; then
		echo "...${Mess} failed with code ${Val}.  Ignoring" >> ${LOGFILE}
		echo "[WARNING] : $(date) : ${Mess} for conformer ${conformer_dir_name} failed with code ${Val}" >> ${STATUSFILE}
		if [ "${Write_Project_Logs}" == "True" ] ; then
			echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
			echo "...${Mess} failed with code ${Val}.  Ignoring" >> ${PROJECT_DEETLOG}
			echo "[WARNING] : $(date) : ${Mess} for conformer ${conformer_dir_name} failed with code ${Val}" >> ${PROJECT_STATLOG}
		fi
	elif [ "${Val}" != "0" ] ; then
		echo "...${Mess} failed with code ${Val}.  Exiting" >> ${LOGFILE}
		echo "[ERROR] : $(date) : ${Mess} for conformer ${conformer_dir_name} failed with code ${Val}" >> ${STATUSFILE}
		if [ "${Write_Project_Logs}" == "True" ] ; then
			echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
			echo "...${Mess} failed with code ${Val}.  Exiting" >> ${PROJECT_DEETLOG}
			echo "[ERROR] : $(date) : ${Mess} for conformer ${conformer_dir_name} failed with code ${Val}" >> ${PROJECT_STATLOG}
		fi
		exit 1
	else
		echo "...${Mess} completed on $(date)" >> ${LOGFILE}
		echo "[INFO] : $(date) : ${Mess} completed" >> ${STATUSFILE}
		if [ "${Write_Project_Logs}" == "True" ] ; then
			echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
			echo "...${Mess} for conformer ${conformer_dir_name} completed on $(date)" >> ${PROJECT_DEETLOG}
			echo "[INFO] : $(date) : ${Mess} for conformer ${conformer_dir_name} completed" >> ${PROJECT_STATLOG}
		fi
	fi
}
run_command_and_log_results()
{
	echo "${1} " >> ${LOGFILE}
        eval "${2}  >> ${LOGFILE} 2>&1"
	returnValue=$?
	write_return_value_info_to_log_status "${returnValue}" "${3}" "${4}"
}
generate_current_directory_zipfile()
{
	(cd ../ && zip -r \
		${conformer_dir_name}/${conformer_zip_prefix}_all.zip \
		${conformer_dir_name} \
		-x "/*.zip")
}
generate_current_directory_solventfiles_zipfile()
{
	(cd ../ && zip -r \
		${conformer_dir_name}/${conformer_zip_prefix}_solvent_${1^^}_simfiles.zip \
		${conformer_dir_name}/unminimized-${1,,}*   \
		${conformer_dir_name}/min-gas.mol2 \
		${conformer_dir_name}/response.json \
		-x "/*.zip")
}
am_I_the_last()
{
	## Get the list of New Builds
	echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
	echo "Processing of conformer ${conformer_dir_name} completed on $(date)" >> ${PROJECT_DEETLOG}
	echo "[INFO] : $(date) : Processing for conformer ${conformer_dir_name} completed" >> ${PROJECT_STATLOG}
	# Ensure that response.json exists
	seconds_waited="0"
	max_seconds="20"
	grep_string="^}"
	while [ "${seconds_waited}" -le "${max_seconds}" ] ; do
		grep -q ${grep_string} ../../logs/response.json
		if [ "$?" == "0" ] ; then
			echo "about to break"
			break
		fi
		seconds_waited="$((seconds_waited+1))"
		if [ "${seconds_waited}" -ge "${max_seconds}" ] ; then
			echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
			echo "Conformer ${conformer_dir_name} timed out waiting for response.json" >> ${PROJECT_DEETLOG}
			echo "Unable to generate the project-level zip file" >> ${PROJECT_DEETLOG}
			echo "This warning might be benign for requests of large numbers of conformers" >> ${PROJECT_DEETLOG}
			echo "[WARNING] : $(date) : ${conformer_dir_name} timed out waiting (${max_seconds} s) for response.json" >> ${PROJECT_STATLOG}
			export I_Am_Last="False"
			return 
		fi
	done
#	echo "found response.json after ${seconds_waited} seconds"
	Requested_Confs="$(grep conformerID ../../logs/response.json | tr -d ' ' | tr -d '"' | tr -d ',' | cut -d ':' -f2)"
#	echo "Requested confs is: "
#	echo ">>>${Requested_Confs}<<<"
	Existing_Confs="$(/bin/ls -1 ../../Existing_Builds/ | grep -vw logs)"
#	echo "Existing confs is: "
#	echo ">>>${Existing_Confs}<<<"
	# Get the list of conformers that are not expected to already exist
	check_confs=""
	for conformer in ${Requested_Confs} ; do
#		echo "checking conformer >>>${conformer}<<<"
#		echo "Checking against Existing Confs: >>>${Existing_Confs}<<<"
		if [[ ${Existing_Confs} != *${conformer}* ]] ; then
#			echo "found a not-match"
			check_confs="${check_confs} ${conformer}"
		fi
	done
#	echo "check confs is: "
#	echo ">>>${check_confs}<<<"
	# Get the last conformer in the zip status file that declared an end to processing (successful or not)
	grep_string="Processing for conformer"
#	echo "grep string is >>>${grep_string}<<<"
	COMMAND="grep '${grep_string}' ${PROJECT_STATLOG}  | tail -1"
#	echo "command is >>>${COMMAND}<<<"
	Last_Conformer="$(eval ${COMMAND})"
#	echo "Last Conformer is: "
#	echo ">>>${Last_Conformer}<<<"
	COMMAND="grep '${grep_string}' ${PROJECT_STATLOG}"
	Done_Conformers="$(eval ${COMMAND})"
#	echo "Done Conformers is: "
#	echo ">>>${Done_Conformers}<<<"
	# See if this one is the last one
	I_Am_Last="False"
#	echo "checking for ${conformer_dir_name} in ${Last_Conformer}"
	if [[ ${Last_Conformer} == *${conformer_dir_name}* ]] ; then
		I_Am_Last="True"
#		echo "setting I am last to true"
	fi
	# still here? see if all the conformers have finished
	for conformer in ${check_confs} ; do
#		echo "checking for ${conformer} in ${Done_Conformers}"
		if [[ ${Done_Conformers} != *${conformer}* ]] ; then
			I_Am_Last="False"
			break
		fi
	done
	echo "Process ${0} sends this message:" >> ${PROJECT_DEETLOG}
	echo "Conformer ${conformer_dir_name} was the last to finish? ${I_Am_Last}" >> ${PROJECT_DEETLOG}
	export I_Am_Last
	return 
}
update_project_level_zipfile()
{
	sleep 1 # allows other processes to finish writing log file entries
	(cd ../../../ && zip -ru \
		${project_dir_name}/${project_zipname} \
		${project_dir_name}/Requested_Builds \
		${project_dir_name}/logs  \
		-x "/*.zip")
}


###  Initialize the log and status files
echo "Run log begun on $(date) " > ${LOGFILE}
echo "[INFO] : $(date) : Status log opened." > ${STATUSFILE}

###  If we seem to be in a Slurm cluster, record some info
( 
command -V srun >/dev/null 2>&1 &&
  ( 
  echo "This build appears to be running in a Slurm cluster.:" >> ${LOGFILE} 
  echo "The current host is $(hostname):" >> ${LOGFILE} 
  echo "The build will run on these hosts:" >> ${LOGFILE} 
  echo "[INFO] : $(date) : This job is running in a Slurm cluster." >> ${STATUSFILE}
  srun hostname -s | sort -u >slurm.hosts
  cat slurm.hosts >> ${LOGFILE}
  )
)

run_command_and_log_results \
	"Sourcing amber.sh from ${AMBERHOME}" \
	"source ${AMBERHOME}/amber.sh" \
	"Sourcing of AMBERHOME[now=${AMBERHOME}]/amber.sh"

echo "
Building and minimizing the gas-phase system.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to generate gas-phase input files." \
	"tleap -f unminimized-gas.leapin" \
	'Gas-phase tleap processing'

run_command_and_log_results \
	"Running the Gas-Phase Minimization"  \
	"bash Run_Multi-Part_Simulation.bash Run-Gas-Min-Parameters.bash" \
	'Gas-phase minimization'

echo "
NOT building and minimizing the solvated systems.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running cpptraj to convert gas-phase output to convenient formats"  \
	"cpptraj -i min-gas.cpptrajin" \
	'Post-gas-phase cpptraj processing'

echo "
Working on TIP3P solvated version.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to build the Tip3P solvated structures"  \
	"tleap -f unminimized-t3p.leapin" \
	'Solvent-phase (T3P) tleap processing'

#run_command_and_log_results \
#	"Running the Tip3P-Solvated Minimization" \
#	"bash Run_Multi-Part_Simulation.bash T3P-Min-Parameters.bash" \
#	'Solvent-phase (T3P) minimization'

#run_command_and_log_results \
#	"Running cpptraj to convert t3p-solvated output to convenient formats"  \
#	"cpptraj -i min-t3p.cpptrajin" \
#	'Post-t3p-solvated cpptraj processing'

echo "
Working on TIP5P solvated version.
" >> ${LOGFILE}

run_command_and_log_results \
	"Running tleap to build the Tip5P solvated structures"  \
	"tleap -f unminimized-t5p.leapin " \
	'Solvent-phase (T5P) tleap processing'

#run_command_and_log_results \
#	"Running the Tip5P-Solvated Minimization" \
#	"bash Run_Multi-Part_Simulation.bash T5P-Min-Parameters.bash" \
#	'Solvent-phase (T5P) minimization'

#run_command_and_log_results \
#	"Running cpptraj to convert t5p-solvated output to convenient formats"  \
#	"cpptraj -i min-t5p.cpptrajin" \
#	'Post-t5p-solvated cpptraj processing'


# If post-amber processing must happen, put them in this file
if [ -f Amber-Epilog.bash ] ; then
	. Amber-Epilog.bash
fi


# Generate zipfiles for the website if indicated
if [ "${MAKE_GW_ZIPS}" == "True" ] ; then
	# simulation files (parm7/rst7 only) for the water models
	if [ ! -e response.json ] ; then
		ln -s ../../logs/response.json
	fi
	for solvent in "T3P" "T5P" ; do
		run_command_and_log_results \
			"Generating/updating the zip file for ${solvent} simulation files."  \
			"generate_current_directory_solventfiles_zipfile ${solvent}" \
			'Simulation files for solvent zip-file creation/updating'
	done
	# all files for this conformer
	run_command_and_log_results \
		"Generating the zip file for the current directory: ${WORKDIR}"  \
		"generate_current_directory_zipfile" \
		'Conformer-level zip-file creation'
	# check if this process should make the top-level zip file
	# I_Am_Last="False"
	run_command_and_log_results \
		"Checking if this process is the last one finished in the project."  \
		"am_I_the_last" \
		'Check for being the last sub-process'

#echo "I am Last is ${I_Am_Last}"

	if [ "${I_Am_Last}" == "True" ] ; then 
		# create or update the files for the entire project
		run_command_and_log_results \
			"Generating/updating the zip file for the entire project."  \
			"update_project_level_zipfile" \
			'Project-level zip-file creation/updating' \
			'True'

		echo "Processing completed on $(date) " >> ${PROJECT_DEETLOG}
		echo "[INFO] : $(date) : Project completed" >> ${PROJECT_STATLOG}
	fi
fi


echo "
Got to end of $0
" >> ${LOGFILE}

