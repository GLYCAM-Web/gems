#!/usr/bin/env bash
AllDotPyFilesList='All-the-dot-py-files.txt'
FullDotPyOutputFILE='Full-dot-py-output.txt'
AllDotPyExitCodesFile='all-dot-py-file-results.txt'
SuccessFile='SUCCESS-dot-py-file-results.txt'
FailFile='FAIL-dot-py-file-results.txt'
AllFiles=( 
	${AllDotPyFilesList} 
	${FullDotPyOutputFILE}
	${AllDotPyExitCodesFile} 
	${SuccessFile}
	${FailFile}
)
USAGE="""
Usage:

	check-all-the-py-files.bash [ full | remove | help ] 

	where:

		full = keep all the output from all the scripts
			- this is optional. 
		        - Normally, these go to /dev/null

		remove = remove any previously generated files

		help = display this message
			- this is optional

What the script does:

	It begins by removing any old output files it finds.

	Starting from the current working directory, it finds all files that
	end in '.py'.  This list is saved in ${AllDotPyFilesList}

	From that list, it ignores any files with 'git-ignore-me'
	in the name.  

	For all other files ('filename.py'), it runs this:

		python3 filename.py > OUTFILE 2>&1

		where OUTFILE is /dev/null unless the word 'full'
		is given as an argument on the command line. In the 
		latter case, the results go to: ${FullDotPyOutputFILE}

	After running filename.py, the script captures the exit code.
	All files, with their exit code, are listed in the file:
	${AllDotPyExitCodesFile}


	Based on the exit code, the filename is copied into one of the
	two files below as described:
		
		${SuccessFile} :  If the exit code is 0 or if the exit
				code indicates a segmentation fault and
				filename.py contains the string 'isegfault'.

		${FailFile} :  Any other result.

"""

if [ "${1}" == "help" ] ; then
	echo "${USAGE}"
	exit 0
fi

if [ "${1}" == "remove" ] ; then
	for file in ${AllFiles[@]} ; do
		rm -f ${file}
	done
	exit 0
fi

if [ "${1}" == "full" ] ; then
	FullOutputDestination="${FullDotPyOutputFILE}"
else
	FullOutputDestination='/dev/null'
fi
echo "The output from the scripts will go to ${FullOutputDestination}"

# Remove any previous output files
echo "${AllFiles[@]}"
for i in "${AllFiles[@]}" ; do
	if [ -e ${i} ] ; then
		rm -f ${i}
	fi
done

# find all the dot-py files in this tree
find ./ -name "*.py" >  ${AllDotPyFilesList}

# run them all with python3 file.py unless in a git-ignore-me situation
for i in $(cat ${AllDotPyFilesList}) ; do 
	if [[ "${i}" == *"git-ignore-me"* ]] ; then
		continue
	fi
	if [ "${1}" == "full" ] ; then
echo "
===========================================================================
===========================================================================
Next file:  ${i} 
===========================================================================
===========================================================================
" >> ${FullOutputDestination}
	fi
	echo "Working on ${i}"
	python3 ${i} >> ${FullOutputDestination} 2>&1
	result=$?
	echo "${result}     ${i}" >> ${AllDotPyExitCodesFile}
	if [[ "${i}" == *"isegfault"* ]] ; then
		if [ "${result}" == "139" ] ; then
			echo ${i} >>  ${SuccessFile}
		else
			echo ${i} >> ${FailFile}
		fi
	else
		if [ "${result}" == "0" ] ; then
			echo ${i} >> ${SuccessFile}
		else
			echo ${i} >>  ${FailFile}
		fi
	fi
done
