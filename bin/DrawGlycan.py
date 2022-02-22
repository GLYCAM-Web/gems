#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

# check out the environment
GemsPath = os.environ.get('GEMSHOME')
if GemsPath == None:
    print("""

Must set GEMSHOME environment variable

    BASH:  export GEMSHOME=/path/to/gems
    SH:    setenv GEMSHOME /path/to/gems

""")
    sys.exit(1)

# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

## Defining the Usage Statement
USAGE="""

DrawGlycan.py [ OPTIONS ] [ SEQUENCE ]

OPTIONS:
    -v, --verbose           Will be verbose on what is happening. (For Debugging)
    -h, --help              Show this help message and exit.
    -w, --write             Write out a default config file(JSON) and exit.
    -c CONFIG_FILE          CONFIG_FILE is the path to the config file(JSON) used.
    --config CONFIG_FILE    Same as -c option.

CONFIG_FILE:
    This is a JSON file used to set some parameters for how the Graph Viz dot file
    is generated. If the -c or --config OPTIONS are not used then the program will
    look for a config file called \"drawglycan.json\".

SEQUENCE:
    The Condensed Sequence the program will use to generate a Graph Viz dot file.
    If the SEQUENCE doesn't exists as an argument, then the program will look
    for the sequence in the config file(JSON). If the sequence isn't present in the
    config file, then the program will inform the user of the problem.

"""

## Store the name of the Program. (Why? Because.)
SCRIPT=sys.argv[0]

## Declare and define the convert2bool function.
def convert2bool(arg):
    if isinstance(arg, bool):
        return arg
    else:
        if arg.lower() == "true":
            return True
        elif arg.lower() == "false":
            return False

## Declare and define the conver2str function.
def convert2str(arg):
    if isinstance(arg, str):
        return arg
    else:
        return str(arg)

## Declare and define the convert2int function.
def convert2int(arg):
    if isinstance(arg, int):
        return arg
    else:
        return int(arg)

## Declare and define the main function.
def main():
    ## Default Configuration Values
    data = {
        "show_config_labels": True, # bool
        "show_edge_labels": False, # bool
        "show_position_labels": True, # bool
        "dpi": 72, # int
        "svg_directory_path": "/programs/gems/gmml/includes/MolecularMetadata/Sugars/SNFG_Symbol_Images/", # string
        "dot_file_name": "oligosaccharide.dot", # string
        "sequence": "" # string
    }
    sequence = False
    verbose = False

    ## Why doesn't Python have a conditional for-loop like other languages?
    index = 1
    while index < len(sys.argv):
        if verbose:
            print("Next command line argument is " + sys.argv[index])
        tmp = sys.argv[index]

        ## Print USAGE statement and exit.
        if tmp == "-h" or tmp == "--help":
            if verbose:
                print("-h or --help OPTION found. Printing USAGE.")
            print(USAGE)
            if verbose:
                print("Exiting with Success(0)")
            sys.exit(0)
        ## Write Default Config File and exit.
        elif tmp == "-w" or tmp == "--write":
            try:
                if verbose:
                    print("-w or --write OPTION found. Trying to open drawglycan.json for writing.")
                outfile = open('drawglycan.json', 'w')
            except OSError as err:
                print(err, file=sys.stderr)
            else:
                if verbose:
                    print("Dumping JSON Data into drawglycan.json.")
                json.dump(data, outfile, sort_keys=True, indent=4)
            if verbose:
                print("Exiting with Success(0)")
            sys.exit(0)
        ## Try to read a User Defined Config File.
        elif tmp == "-c" or tmp == "--config":
            if verbose:
                print("-c or --config OPTION found. Looking for next command line argument.")
            index += 1
            ## Make sure there is another argument to get.
            if len(sys.argv) > index:
                try:
                    if verbose:
                        print("Found another command line argument. Trying to open the file for reading")
                    json_file = open(sys.argv[index], 'r')
                except OSError as err:
                    print(err, file=sys.stdout)
                    if verbose:
                        print("Exiting with Failure(1)")
                    sys.exit(1)
                else:
                    if verbose:
                        print("Loading data from " + sys.argv[index] + " to data Object.")
                    data = json.load(json_file)
            ## Print USAGE statement because there isn't another argument to use with option.
            else:
                if verbose:
                    print("Didn't find another command line argument after the OPTION.")
                print(SCRIPT + ": Please provide a config JSON file.", file=sys.stderr)
                print(USAGE)
                if verbose:
                    print("Exiting with Failure(1)")
                sys.exit(1)
        ## Turn on verbosity.
        elif tmp == "-v" or tmp == "--verbose":
            if verbose:
                print("-v or --verbose OPTION was found after Verbosity was turned on.")
            else:
                verbose = True
                print(SCRIPT + ": Verbosity has been turned on. From now on.")
        ## Looking for other command line argument. This script current assumes if it is not one of
        ## the above OPTIONS then it is a SEQUENCE. The script also current uses the last SEQUENCE
        ## command line argument to create the dot file.
        else:
            if verbose:
                print("Found a SEQUENCE command line argument. " + tmp + " Assigning it to arg_sequence")
            sequence = True
            arg_sequence = tmp

        index += 1

    ## If a sequence was passed as an argument then override the one in the config file.
    if verbose:
        print("Checking if a command line SEQUENCE was passed.")
    if sequence:
        if verbose:
            print("Command line SEQUENCE was passed. Storing it to data[\'sequence\'] as a string.")
        data['sequence'] = convert2str(arg_sequence)

    ## If we have come to this point and we still don't have a sequence then something is wrong.
    if verbose:
        print("Checking to make sure we have a SEQUENCE to create a dot file from.")
    if data['sequence'] == "":
        print(SCRIPT + ": Error: No sequence to draw.", file=sys.stderr)
        if verbose:
            print("Exiting with Failure(1)")
        sys.exit(1)

    ## Need to make sure all the data types are the valid data types we need.
    if verbose:
        print("Checking to make sure input is valid data types and converting, if not.")
    data['show_edge_labels'] = convert2bool(data['show_edge_labels'])
    data['show_config_labels'] = convert2bool(data['show_config_labels'])
    data['show_position_labels'] = convert2bool(data['show_position_labels'])
    data['svg_directory_path'] = convert2str(data['svg_directory_path'])
    data['dot_file_name'] = convert2str(data['dot_file_name'])
    data['dpi'] = convert2int(data['dpi'])
    data['sequence'] = convert2str(data['sequence'])

    ## Initialize a GMML CondensedSequenceSpace::GraphVizDotConfig
    if verbose:
        print("Initializing a default GMML CondensedSequenceSpace::GraphVizDotConfig Object.")
    configs = gmml.GraphVizDotConfig()

    ## Set it's values from the JSON object data.
    if verbose:
        print("Assigning input values to GMML CondensedSequenceSpace::GraphVizDotConfig Object.")
    configs.show_edge_labels_ = data['show_edge_labels']
    configs.show_config_labels_ = data['show_config_labels']
    configs.show_position_labels_ = data['show_position_labels']
    configs.dpi_ = data['dpi']
    configs.svg_directory_path_ = data['svg_directory_path']
    configs.file_name_ = data['dot_file_name']

    ## Call the WriteGraphVizDotFile function.
    if verbose:
        print("Calling CondensedSequence::DrawGlycan to generate the dot file.")
    gmml.DrawGlycan(configs, data['sequence'])

    if verbose:
        print("We made it to the end. Congratulations!")
    ## We made it! :)
    sys.exit(0)

## Now we call main function.
if __name__ == "__main__":
    main()
