#!/bin/bash

################################################################
#########                 FUNCTIONS                    #########
################################################################

check_pythonhome() {
    if [ -z "$PYTHON_HOME" ]; then
        printf "PYTHON_HOME is not set.\n"
        printf "Set PYTHON_HOME to the location of Python.h for a python 3 installation,\n"
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
        printf "PYTHON_HOME is not set to a directory.\n" 
        printf "It is currently %s\n" $PYTHON_HOME
        printf "Perhaps try     %s\n" $guess
        echo "Exiting."
        exit 1
    fi
}

check_gemshome() {
   if [ -z "$GEMSHOME" ]; then
      echo ""
      echo "Your GEMSHOME environment variable is not set! It should be set to"
      echo "$1"
      exit 1
   elif [ ! -d $GEMSHOME ]; then
      echo ""
      echo "Your GEMSHOME environment variable is set to $GEMSHOME -- this does"
      echo "not appear to be a directory. It should be set to"
      echo "$1"
      exit 1
   elif [ ! "$GEMSHOME" = "$1" -a ! "$GEMSHOME" = "${1}/" ]; then
      #try checking the inode incase there is a problem with symlinks
       if [ `stat -c "%i" $GEMSHOME` != `stat -c "%i" ${1}` ]; then
           echo ""
           echo "ERROR: GEMSHOME is expected to be $1 but it is currently"
           echo "$GEMSHOME    This will cause problems!"
           exit 1
       fi
   fi
}

check_gmmldir() {
    if [ ! -d "$1" ]; then
        echo ""
        echo "Your gmml directory does not exist. If your GEMSHOME is set correctly,"
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
#########                SET UP DEFAULTS               #########
################################################################

#Changing the following options are for developers.
TARGET_MAKE_FILE="Makefile-main"
IDE="None"
CLEAN="No"
WRAP_GMMML="Wrap"

################################################################
#########               COMMAND LINE INPUTS            #########
################################################################

if [[ $# -eq 2 ]]; then 
    CLEAN="$1"
elif [[ $# -eq 3 ]]; then
    CLEAN="$1"
    WRAP_GMMML="$2"
elif [[ $# -eq 4 ]]; then
    CLEAN="$1"
    WRAP_GMMML="$2"
    IDE="$3"
fi

if [[ "$1" == "-help" ]] || [[ "$1" == "-h" ]]; then
    printf "\nUsage: $0 clean_gmml? wrap_gmml? ide?\n"
    printf "Example $0 clean no_wrap Qt\n" 
    printf "This 1. Cleans gmml before making\n" 
    printf "     2. Does not wrap up via swig (required only for Gems)\n"
    printf "     3. Prepares a .pro file for Qt to read\n"
    echo "Exiting."
    exit 1
fi


################################################################
#########                  COMPILE GMML                #########
################################################################

#If wrapping later, check if PYTHON_HOME is set before compiling GMML
if [[ "$WRAP_GMML" != "no_wrap" ]]; then
    check_pythonhome
fi

cd gmml
if [ -f $TARGET_MAKE_FILE ]; then
    if [ "$CLEAN" == "clean" ]; then
        make -f $TARGET_MAKE_FILE distclean
        rm -rf gmml.pro*
    fi
    if [ "$IDE" == "Qt" ]; then
        qmake -project -t lib -o gmml.pro "OBJECTS_DIR = build" "DESTDIR = bin"
        qmake -o Makefile 
    fi
    echo "Compiling gmml"
    make -j 4 -f $TARGET_MAKE_FILE
fi
cd ../

################################################################
#########              WRAP UP TO GEMS                 #########
################################################################

if [[ "$WRAP_GMML" != "no_wrap" ]]; then

    if [[ -f "gmml.i" ]]; then
        echo "Wrapping gmml library in python ..."
        swig -c++ -python gmml.i
    elif [[ -z "gmml.i" ]]; then
        echo "Interface file for swig does not exist"
    fi

    PYTHON_FILE="$PYTHON_HOME/Python.h"
    if [ -f $PYTHON_FILE ]; then
        if [ -f "gmml_wrap.cxx" ]; then
            echo "Compiling wrapped gmml library in python ..."
            g++ -O3 -fPIC -c gmml_wrap.cxx -I"$PYTHON_HOME"
        else
            echo "gmml_wrap.cxx does not exist"
        fi
    else
        echo "PYTHON_HOME variable has not been set"
    fi

    if [[ -f "gmml_wrap.o" ]]; then
        echo "Building python interface ..."
        g++ -shared gmml/build/*.o gmml_wrap.o -o _gmml.so
    elif [[ -z "gmml_wrap.o" ]]; then
        echo "gmml has not been compiled correctly"
    fi

fi
