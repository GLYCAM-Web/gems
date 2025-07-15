#!/usr/bin/env bash
# archive a target dir zip and it's contents, write to top level of project dir.
# ignore archives when archiving
# Usage: ./create_project_archive.sh <project_dir> <archive_pUUID>

project_dir="$1"
archive_pUUID="$2"

if [ -z "$project_dir" ] || [ -z "$archive_pUUID" ]; then
    echo "Usage: $0 <project_dir> <archive_pUUID>" >&2
    exit 1
fi

# Check if the project directory exists
if [ ! -d "$project_dir" ]; then
    echo "Project directory '$project_dir' does not exist." >&2
    exit 2
fi

# Based on File Naming Conventions in DevEnv's mkdocs.
archive_name="GP_project_${archive_pUUID:0:8}_all.zip"

# Create the archive
archive_path="${project_dir}/${archive_name}"

if zip -r "$archive_path" "$project_dir" -x "*.zip"; then
    echo "Project archive created successfully." >> "${project_dir}/status.log"
else
    echo "Failed to create project archive." >> "${project_dir}/status.log"
    exit 3
fi