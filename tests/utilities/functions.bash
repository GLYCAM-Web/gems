#!/bin/bash

## This file should be sourced from the tests directory.

remove_file_if_found()
{
	if [ -f ${1} ] ; then
		rm ${1}
	fi
}

# See if a returned object is proper JSON and no other data
###
### This method will fail eventually!!!
###
check_output_is_only_json() 
{
	### The following will stop working eventually and will need to be replaced
	commonServicerResponse="$(cat ${1} | python ../gemsModules/deprecated/common/utils.py)"
	###
	###
	if ( echo ${commonServicerResponse} | grep -q CommonServices ) ; then
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		echo "  The returned data is not a proper JSON Object"
		echo "  This will cause the test to fail even if the builds work."
		echo "  The Common Servicer has this to say about the data:"
		echo ""
		echo "${commonServicerResponse}"
		echo ""
		echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		echo ""
		return 1
	else
		echo "The data response appears to be ok"
		return 0
	fi
}
get_seqID_from_json() 
{
	theseqID=$(grep -m 1  seqID ${1} | cut -d '"' -f4)
	export theseqID
}
get_pUUID_from_json() 
{
	thepUUID=$(grep -m 1  pUUID ${1} | cut -d '"' -f4)
	export thepUUID
}
do_files_exist()
{
	files=${1}
	#echo "checking on the file(s): ${files}"
	result=0
	for file in ${files} ; do
		if [ ! -e ${file} ] ; then
			result=1
		fi
	done
	#echo "returning ${result}"
	return ${result}
}
wait_for_files()
{
	### the sleep duration info is in common_environment.bash and that should be included before this file
	files=${1}
	#echo "waiting for the file(s): ${files}"
	count=0
	while ! do_files_exist ${files}
       	do
                echo "about to sleep"
                sleep ${oneSleepTimeDuration} 
                count=$((count+1))
                echo "Waited $((count*oneSleepTimeDuration)) seconds so far. Still missing one or more files."
                if [ "${count}" -eq "${maxSleepTimeCount}" ] ; then
                        echo "Waited $((count*oneSleepTimeDuration)) seconds so far. One or more files missing." 
                        return 1
                fi
        done
	return 0
}

