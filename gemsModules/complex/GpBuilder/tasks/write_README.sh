#!/bin/bash

projectDir="$1"
if [ -z "$projectDir" ]; then
    echo "Usage: $0 <project_directory>"
    exit 1
fi

# Function to check if file/dir exists and format the description
check_and_format() {
    local item="$1"
    local description="$2"
    description=$(echo "$description" | fold -s -w 80 | sed 's/^/\t/')

    local full_path="${projectDir}/${item}"
    
    if [ -e "$full_path" ]; then
        echo -e "${item}\t(Found)\n${description}"
    else
        echo -e "${item}\t(Missing)\n${description}"
    fi
}

# Function to check for zip files with glob pattern (Should only ever find one for GpBuilder)
check_zip_files() {
    local description="$1"
    local zip_files=("${projectDir}"/*.zip)
    
    if [ -e "${zip_files[0]}" ]; then
        for zip_file in "${zip_files[@]}"; do
            local basename=$(basename "$zip_file")
            echo -e "${basename}\t(Found)\n\t${description}"
        done
    else
            echo -e "GP_project_*.zip\n\t${description}"
    fi
}

{
    check_and_format "OriginalInput.pdb" "A consistently named symlink to the user uploaded PDB file."
    check_and_format "the_input.txt" "The input file for the glycoprotein builder program in gmml2."
    check_and_format "the_glycosites.csv" "A list of sites found by gmml2 for the website to display to the user on the options page."
    echo ""
    check_and_format "start_build.sh" "Shell script that runs the gmml2 gpBuilder program and writes status/errors to the logs."
    check_and_format "gpBuilder.err" "Errors from the gpBuilder program's execution."
    check_and_format "gpBuilder.log" "Logs from the gpBuilder program's execution."
    check_and_format "status.log" "Status file for the website to know what steps have been completed."
    echo ""
    check_and_format "outputs/" "A folder containing the outputs from the gmml2 gpBuilder program."
    check_and_format "outputs/default.pdb" "The resulting glycosylated structure that is shown to the user in Mol*. It uses original residue numbering by default and serialized residue numbering with MD prep enabled."
    check_and_format "outputs/unresolved.pdb" "The initial glycosylated structure before any overlap resolution is performed. It keeps the original residue numbering."
    check_and_format "outputs/structures.csv" "A list of each of the generated structures information about failed glycosites, highest overlap, etc."
    check_and_format "outputs/summary.html" "A summary of input information and site specific results from the gpBuilder."
    check_and_format "outputs/summary.txt" "Same as summary.html but in text format."
    check_and_format "outputs/samples/" "A folder containing either rejected (too high overlaps) or good samples of the shapes that can be adopted by the glycans at each site. The code will produce as many samples as requested in the input file. Will use serialized residue numbering if MD prep is enabled, otherwise uses original residue numbering."
    echo ""
    check_zip_files "The zip file containing these project files."
} >> "${projectDir}/README.txt"