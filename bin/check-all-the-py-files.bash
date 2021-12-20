#!/usr/bin/env bash
# Remove any previous output files
for i in SUCCESS-dot-py-file-results.txt FAIL-dot-py-file-results.txt all-dot-py-file-results.txt ; do
	if [ -e ${i} ] ; then
		rm -f ${i}
	fi
done

# find all the dot-py files in this tree
find ./ -name "*.py" > All-the-dot-py-files.txt

# run them all with python3 file.py unless in a git-ignore-me situation
for i in $(cat All-the-dot-py-files.txt) ; do 
	if [[ "${i}" == *"git-ignore-me"* ]] ; then
		continue
	fi
	echo "Working on ${i}"
	python3 ${i} > /dev/null 2>&1
	result=$?
	echo "${result}     ${i}" >> all-dot-py-file-results.txt
	if [ "${result}" == "0" ] ; then
		echo ${i} >> SUCCESS-dot-py-file-results.txt
	elif [ "${result}" == "139" ] ; then
		if [[ "${i}" == *"isegfault"* ]] ; then
			echo ${i} >> SUCCESS-dot-py-file-results.txt
		else
			echo ${i} >> FAIL-dot-py-file-results.txt
		fi
	else
		echo ${i} >> FAIL-dot-py-file-results.txt
	fi

done
