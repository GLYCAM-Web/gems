#!/bin/bash

project_dir=$1
project_zipname=$2
if [ -z "$project_dir" ] || [ -z "$project_zipname" ]; then
    exit 1
fi

project_dir_name="$(basename ${project_dir})"

# cd to parent of project_dir
OLDPWD=$(pwd)
cd $(dirname ${project_dir})
#cd ${project_dir_name}
if [ $? -ne 0 ]; then
    cd ${OLDPWD}
    exit 2
fi

echo "INFO: Zipping ${project_dir_name} to ${project_zipname}" >> ${project_dir}/logs/zip.log
zip -ru ${project_dir_name}/${project_zipname} ${project_dir_name}/Requested_Builds ${project_dir_name}/logs -x "/*.zip"
if [ $? -ne 0 ]; then
    cd ${OLDPWD}
    exit 3
fi
cd ${OLDPWD}