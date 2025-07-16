#!/bin/bash

# Check if two arguments were provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 file1.zip file2.zip"
    exit 1
fi

# Check if both files exist
if [ ! -f "$1" ]; then
    echo "Error: File '$1' does not exist."
    exit 1
fi

if [ ! -f "$2" ]; then
    echo "Error: File '$2' does not exist."
    exit 1
fi

# Create unique temporary directories based on process ID
temp_dir1="/tmp/compare_zip_$(basename "$1")_$$"
temp_dir2="/tmp/compare_zip_$(basename "$2")_$$"

# Make sure temp directories don't exist
rm -rf "$temp_dir1" "$temp_dir2"
mkdir -p "$temp_dir1" "$temp_dir2"

echo "Extracting files..."

# Unzip both files into separate directories
if ! unzip -q "$1" -d "$temp_dir1"; then
    echo "Error extracting '$1'"
    rm -rf "$temp_dir1" "$temp_dir2"
    exit 1
fi

if ! unzip -q "$2" -d "$temp_dir2"; then
    echo "Error extracting '$2'"
    rm -rf "$temp_dir1" "$temp_dir2"
    exit 1
fi

echo "Comparing files..."

# Compare the directories recursively
if diff -r "$temp_dir1" "$temp_dir2" > /dev/null; then
    echo "✅ The zip files are identical."
    result=0
else
    echo "❌ The zip files are different."
    echo "Would you like to see the differences? (y/n)"
    read -r answer
    if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
        diff -r "$temp_dir1" "$temp_dir2" > zip_diff.txt
        echo "Differences saved to zip_diff.txt"
        cat zip_diff.txt
        echo 
    fi
    result=1
fi

# Clean up the temporary directories if equal
if [ $result -eq 0 ]; then
    echo "Cleaning up..."
    rm -rf "$temp_dir1" "$temp_dir2"
else
    echo "Temporary files are kept for inspection."
    echo "Temporary files are located in:"
    echo "  $temp_dir1"
    echo "  $temp_dir2"
    echo "Please remove them manually if no longer needed."
    echo "You can also use the command:"
    echo "  rm -rf $temp_dir1 $temp_dir2"
    echo "to remove them."
fi
exit $result