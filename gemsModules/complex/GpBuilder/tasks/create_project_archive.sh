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

# Create the archive
# Based on File Naming Conventions in DevEnv's mkdocs.
folder_name="$(basename "$project_dir")"
archive_name="${project_dir}/GP_project_${archive_pUUID:0:8}_all.zip"

cd "$(dirname "$project_dir")" || exit 3
zip -r "$archive_name" "$archive_pUUID" -x "*.zip" || exit 4