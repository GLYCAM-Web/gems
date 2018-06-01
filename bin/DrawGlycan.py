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

## Declare and define the main function.
def main():
    ## Default Configuration Values
    data = {
        "show_config_labels": True,
        "show_edge_labels": False,
        "show_position_labels": True,
        "dpi": 72,
        "svg_directory_path": "/programs/gw_misc/SNFG/V1/",
        "dot_file_name": "oligosaccharide.dot",
        "sequence": ""
    }
    sequence = False

    ## Why doesn't Python have a conditional for-loop like other languages?
    index = 1
    while index < len(sys.argv):
        tmp = sys.argv[index]

        ## Print USAGE statement and exit.
        if tmp == "-h" or tmp == "--help":
            print(USAGE)
            sys.exit(0)
        ## Write Default Config File and exit.
        elif tmp == "-w" or tmp == "--write":
            with open('drawglycan.json', 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            sys.exit(0)
        ## Try to read a User Defined Config File.
        elif tmp == "-c" or tmp == "--config":
            index += 1
            ## Make sure there is another argument to get.
            if len(sys.argv) > index:
                file = Path(sys.argv[index])
                ## Test if the argument is actually a file.
                if file.is_file():
                    with open(sys.argv[index]) as json_file:
                        ## Override the Default Config values.
                        data = json.load(json_file)
                else:
                    print(SCRIPT + ": File Error: \'" + sys.argv[index] + "\' is not a file.")
                    print(USAGE)
                    sys.exit(1)
            ## Print USAGE statement because there isn't another argument to use with option.
            else:
                print(SCRIPT + ": Please provide a config JSON file.")
                print(USAGE)
                sys.exit(1)
        else:
            sequence = True
            arg_sequence = tmp

        index += 1

    ## If a sequence was passed as an argument then override the one in the config file.
    if sequence:
        data['sequence'] = arg_sequence

    ## If we have come to this point and we still don't have a sequence then something is wrong.
    if data['sequence'] == "":
        print(SCRIPT + ": Error: No sequence to draw.")
        sys.exit(1)

    ## Initialize a GMML CondensedSequenceSpace::GraphVizDotConfig
    configs = gmml.GraphVizDotConfig()

    ## Set it's values from the JSON object data.
    configs.show_edge_labels_ = data['show_edge_labels']
    configs.show_config_labels_ = data['show_config_labels']
    configs.show_position_labels_ = data['show_position_labels']
    configs.dpi_ = data['dpi']
    configs.svg_directory_path_ = data['svg_directory_path']
    configs.file_name_ = data['dot_file_name']

    ## Intialize a GMML CondensedSequenceSpace::CondensedSequence
    condensed_sequence = gmml.CondensedSequence(data['sequence'])

    ## Call the WriteGraphVizDotFile function.
    condensed_sequence.WriteGraphVizDotFile(configs)

    ## We made it! :)
    sys.exit(0)

## Now we call main function.
if __name__ == "__main__":
    main()
