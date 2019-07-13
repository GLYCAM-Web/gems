

## TODO Make this not be a call to a compiled binary
def build3DStructure(thisTransaction : Transaction):
    # Check for environment variables that tell where things go
    # check out the environment
    OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_STRUCTURE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_SEQUENCE_PATH')
    if OutputPath == None:
        OutputPath = os.environ.get('GEMS_MODULES_PATH')
    if OutputPath == None:
        OutputPath = '.' 
    # Set up the location where output files will be stored
    # This next function should check for directory name prefix or
    # if the complete spec is known or if a UUID should be generated
    #    OutputDirectorySpecification = getOutputDirectorySpecification(thisTransaction: Transaction)
    # Set up the location of the MD5Sum directory
    # Set up the location of the prep file to be used
    # Generate directories as needed
    # Save output files to the directories as needed
    # Run the program to generate the files
    # Return the name of the directory where the files reside
    pass
    
