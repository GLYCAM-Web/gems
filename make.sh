#!/bin/bash

################################################################
#########                 FUNCTIONS                    #########
################################################################

check_pythonhome() {
    if [ -z "$PYTHON_HOME" ]; then
        printf "\nError:  PYTHON_HOME is not set.\n"
        printf "Set PYTHON_HOME to the location of Python.h for a python 3 installation.\n"
        printf "Searching for locations of Python.h:\n"
        if locate_test="$(type -p "locate")" || [ -z "locate" ]; then
            num_Pythons=`locate -ce Python.h`
            if [[ $num_Pythons -gt 0 ]]; then
            {
                printf "Here are the current locations of Python.h on your machine:\n\n"
                locate -e Python.h
                printf "\n"
            }
            else
                printf "locate could not find any instances of Python.h\n"

            fi
        fi
        echo "Exiting."
        exit 1
    elif [ ! -d $PYTHON_HOME ]; then
        guess=`dirname $PYTHON_HOME`
        printf "\nError:  PYTHON_HOME is not set to a directory.\n"
        printf "It is currently %s\n" $PYTHON_HOME
        printf "Perhaps try     %s\n" $guess
        echo "Exiting."
        exit 1
    fi
}

get_numprocs() {
    if [ -z "$GEMSMAKEPROCS" ]; then
        NMP=4
    elif ! [[ $GEMSMAKEPROCS =~ ^[0-9]+$ ]] ; then
        echo "Warning:  GEMSMAKEPROCS is not a valid integer; setting to 4"
        NMP=4
    elif [ "$GEMSMAKEPROCS" -eq "0" ] ; then
        echo "Warning:  GEMSMAKEPROCS cannot be zero; setting to 4"
        NMP=4
    else
        NMP=$GEMSMAKEPROCS
    fi
}

check_gemshome() {
    if [ -z "$GEMSHOME" ]; then
        echo ""
        echo "Error:  GEMSHOME environment variable is not set! It should be set to"
        echo "$1"
        exit 1
    elif [ ! -d $GEMSHOME ]; then
        echo ""
        echo "Error:  GEMSHOME environment variable is set to $GEMSHOME -- this does"
        echo "not appear to be a directory. It should be set to"
        echo "$1"
        exit 1
    elif [ ! "$GEMSHOME" = "$1" -a ! "$GEMSHOME" = "${1}/" ]; then
        #try checking the inode incase there is a problem with symlinks
        if [ `stat -c "%i" $GEMSHOME` != `stat -c "%i" ${1}` ]; then
            echo ""
            echo "Error:  GEMSHOME is expected to be $1 but it is currently"
            echo "$GEMSHOME"
            echo "        This will cause problems!"
            exit 1
        fi
    fi
}

check_gmmldir() {
    if [ ! -d "$1" ]; then
        echo ""
        echo "Error:  gmml directory does not exist. If your GEMSHOME is set correctly,"
        echo "it should be here: $GEMSHOME/gmml"
        exit 1
    fi
}

################################################################
#########                CHECK SETTINGS                #########
################################################################

gemshome=`pwd`
check_gemshome $gemshome
check_gmmldir $GEMSHOME/gmml
get_numprocs

################################################################
#########              CREATE CLIENT HOOKS             #########
################################################################

#Cannot use server side hooks when hosting on git-hub.
#Stuff in .git/hooks is ignored by git
#Solution: The folder gmml/.hooks is tracked by git.
# Copy gmml/.hooks to gmml/.git/hooks during installation
cp -r $GEMSHOME/gmml/.hooks/* $GEMSHOME/gmml/.git/hooks/
cp -r $GEMSHOME/.hooks/* $GEMSHOME/.git/hooks/
#I don't think this is ideal, and is perhaps silly. OG Apr 2017.

################################################################
#########                WRITE CONFIG.H                #########
################################################################

# NOTE: Inactive for now

# Store the command
#command=`echo "$0 $*"`

# Write directories into config.h
#printf "# Gems configuration file, created with: %s\n\n" $command > config.h
#printf "###############################################################################\n\n" >> config.h
#printf "# (1) Location of the installtion\n\n" >> config.h

#printf "BASEDIR=%s\n" $GEMSHOME >> config.h
#printf "BINDIR=%s/bin\n" $GEMSHOME >> config.h
#printf "TESTDIR=%s/testbin\n" $GEMSHOME >> config.h
#printf "APPDIR=%s/apps\n" $GEMSHOME >> config.h
#printf "HOOKDIR=%s/hooks\n" $GEMSHOME >> config.h
#printf "GMMLDIR=%s/gmml\n" $GEMSHOME >> config.h

#printf "\n###############################################################################\n\n" >> config.h

################################################################
##########               Print help message         ############
################################################################

if [[ "$1" == "-help" ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    printf "*************************************************************\n"
    printf "Usage: $0 clean_gmml? wrap_gmml?\n"
    printf "Example: $0 clean no_wrap\n"
    printf "Default: $0 no_clean wrap\n"
    printf "*************************************************************\n"
    printf "If selected the options do this:\n"
    printf "     1. Cleans gmml before making\n"
    printf "     2. Wrap up via swig (wrapping required only for Gems)\n"
    printf "*************************************************************\n"
    echo "Exiting."
    exit 1
fi

################################################################
#########                SET UP DEFAULTS               #########
################################################################

#Changing the following options are for developers.
TARGET_MAKE_FILE="Makefile"
CLEAN="no"
WRAP_GMML="wrap"
DEBUG=""

################################################################
#########               COMMAND LINE INPUTS            #########
################################################################
i=1
while [ ${i} -le $# ]; do
    argument="${!i}"
    if [ "$argument" = "clean" ]||[ "$argument" = "no_clean" ];then
        CLEAN="${!i}"
    elif [ "$argument" = "wrap" ]||[ "$argument" = "no_wrap" ];then
        WRAP_GMML="${!i}"
    elif [ "$argument" = "debug" ];then
        DEBUG="-g"
    fi
    i=$[$i+1]
done

# if [[ $# -eq 1 ]]; then
#     CLEAN="$1"
# elif [[ $# -eq 2 ]]; then
#     CLEAN="$1"
#     WRAP_GMML="$2"
# fi

printf "\nTARGET_MAKE_FILE: $TARGET_MAKE_FILE, CLEAN: $CLEAN, WRAP_GMML: $WRAP_GMML\n"

################################################################
#########                  COMPILE GMML                #########
################################################################

cd gmml/
 # Always create a new gmml.pro and makefile
 ## This is going to be broken up to variables instead of being this long command. Just wanted to get a working version pushed up.
 qmake -project -t lib -o gmml.pro "QMAKE_CXXFLAGS += -Wall -W -std=c++11 ${DEBUG}" "QMAKE_CFLAGS += -Wall -W ${DEBUG}" "DEFINES += _REENTRANT" "CONFIG = no_lflag_merge" "unix:LIBS = -L/usr/lib/x86_64-linux-gnu -lpthread" "OBJECTS_DIR = build" "DESTDIR = lib" -r src/ includes/ -nopwd
 qmake -o $TARGET_MAKE_FILE

 if [ "$CLEAN" == "clean" ]; then
     make -f $TARGET_MAKE_FILE distclean
     qmake -o $TARGET_MAKE_FILE
 fi

 echo "Compiling gmml"
 make -j ${NMP} -f $TARGET_MAKE_FILE

cd ../

################################################################
#########              WRAP UP TO GEMS                 #########
################################################################

if [[ "$WRAP_GMML" != "no_wrap" ]]; then

    check_pythonhome

    if [[ -f "gmml.i" ]]; then
        echo "Wrapping gmml library in python ..."
        swig -c++ -python gmml.i
    elif [[ -z "gmml.i" ]]; then
        echo "Warning:  Interface file for swig does not exist."
    fi

    PYTHON_FILE="$PYTHON_HOME/Python.h"
    if [ -f $PYTHON_FILE ]; then
        if [ -f "gmml_wrap.cxx" ]; then
            echo "Compiling wrapped gmml library in python ..."
            g++ -std=c++11 -O3 -fPIC -c gmml_wrap.cxx -I"$PYTHON_HOME"
        else
            echo "Warning:  gmml_wrap.cxx does not exist."
        fi
    else
        echo "Warning:  $PYTHON_FILE not found !"
    fi

    if [[ -f "gmml_wrap.o" ]]; then
        echo "Building python interface ..."
        g++ -std=c++11 -shared gmml/build/*.o gmml_wrap.o -o _gmml.so
    elif [[ -z "gmml_wrap.o" ]]; then
        echo "Warning:  gmml python interface has not been compiled correctly."
    fi
fi
