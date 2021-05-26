#!/bin/bash


if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo  "GEMSHOME is undefined. Exiting."
	exit 1
fi
OUTFILE="${GEMSHOME}/UserSpace/VERSIONS.sh"
if [ ! -d "${GEMSHOME}/UserSpace" ] ; then
	mkdir -p  "${GEMSHOME}/UserSpace"
fi

echo "#!/bin/bash
# Versions information updated on:  $(date)
#" > ${OUTFILE}

##
## Set Git versioning info
##
# GEMS
if ! cd ${GEMSHOME} ; then
	print_error_and_exit "Could not cd to gems directory"
fi
echo """
GEMS_GIT_BRANCH=\"$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')\"
GEMS_GIT_COMMIT_HASH=\"$(git rev-parse HEAD)\"
""" >> ${OUTFILE}
# MD_Utils
if ! cd "${GEMSHOME}/External/MD_Utils" ; then
	print_error_and_exit "Could not cd to MD Utils directory"
fi
echo """
MD_UTILS_GIT_BRANCH=\"$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')\"
MD_UTILS_GIT_COMMIT_HASH=\"$(git rev-parse HEAD)\"
""" >> ${OUTFILE}
# GMML
if ! cd ${GEMSHOME}/gmml ; then
	print_error_and_exit "Could not cd to gmml directory"
fi
echo """
GMML_GIT_BRANCH=\"$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')\"
GMML_GIT_COMMIT_HASH=\"$(git rev-parse HEAD)\"
""" >> ${OUTFILE}

## TODO - add other externals as needed, such as the glycoprotein builder
