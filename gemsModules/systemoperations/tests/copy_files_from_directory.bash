#!/usr/bin/env bash

python3 copy_files_from_directory.py

Diffs="$(diff -r inputs/A/ outputs/B/)"

if [ "${Diffs}zzz" != "zzz" ] ; then
	echo "The test failed!"
else
	echo "The test passed!"
	rm -rf outputs/B/
fi

