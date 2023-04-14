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
	seqID=$(grep -m 1  seqID ${1} | cut -d '"' -f4)
	return seqID
}
get_pUUID_from_json() 
{
	pUUID=$(grep -m 1  pUUID ${1} | cut -d '"' -f4)
	return pUUID
}
check_string_against_standard()
{
	test_string="${1}"
	standard="${2}"

}
check_file_contents_against_standard()
{
	test_contents="${1}"
	standard="${2}"
	cmp ${test_content} ${standard} > /dev/null 2>&1;
}

