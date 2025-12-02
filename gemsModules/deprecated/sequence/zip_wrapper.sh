#!/bin/bash

project_dir=$1
project_zipname=$2
if [ -z "$project_dir" ] || [ -z "$project_zipname" ]; then
    exit 1
fi

project_dir_name="$(basename ${project_dir})"

cd $(dirname ${project_dir})
if [ $? -ne 0 ]; then
    exit 2
fi

zip -ru ${project_dir_name}/${project_zipname} ${project_dir_name}/Requested_Builds ${project_dir_name}/logs -x "/*.zip" > ${project_dir_name}/zip_details.log 2>&1
EXIT_CODE=$?
if [ "${EXIT_CODE}" -ne "0" ]; then
    echo "Failed to create the project level zip" >> ${project_dir}/zip_details.log
    echo "[ERROR] : $(date) : Failed to zip project" >> ${project_dir}/zip_status.log
else
    # See: https://github.com/GLYCAM-Web/MD_Utils/blob/feature_add-zipfile-creation/protocols/Glycan/Prep_and_Minimization/Sequence-Prep.bash#L339
    # For info on where these patterns come from.
    echo "Processing completed on $(date) " >> ${project_dir}/zip_details.log
    echo "[INFO] : $(date) : Project completed" >> ${project_dir}/zip_status.log
fi

exit ${EXIT_CODE}
