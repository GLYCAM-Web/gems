#!/bin/bash

: << '=cut'
COMMENT - Requirements and Known Issues.

# Python 3 is required.
# These are known to work: 3.6.6 :: Anaconda custom and 3.7.3.

# Python.h is required.
# In some cases Python.h does not live in PYTHON_HOME.
# Users can run this command to find it and set PYTHON_HEADER_HOME accordingly:
## python3-config --cflags

# Based on practice SWIG version 3 or later is recommended.
# These are known to work: 3.0.10 and 3.0.12.
# These are known to fail: 2.0.10.
# SWIG Version 2.0.10 fails due to this issue:
# https://sourceforge.net/p/swig/bugs/1331/
# Here's part of a typical failure:
##gmml_wrap.cxx: In function 'PyObject* _wrap_pdbmatrixn_vector_vector_erase__SWIG_0(PyObject*, PyObject*)':
##gmml_wrap.cxx:202628:30: error: no matching function for call to 'std::vector<std::vector<PdbFileSpace::PdbMatrixNCard*>
##>::erase(SwigValueWrapper<__gnu_cxx::__normal_iterator<std::vector<PdbFileSpace::PdbMatrixNCard*>*, std::vector<std::vector<PdbFileSpace::PdbMatrixNCard*> > > >>&)'
##   result = (arg1)->erase(arg2);

=cut

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
        #try checking the inode in case there is a problem with symlinks
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

check_pull_mdutils() {
    theDir="$GEMSHOME/External/MD_Utils"
    if [ ! -d "${theDir}" ]; then
	    mkdir -p ${theDir}
    fi
    if [ "${GW_GRPC_ROLE}" == "Swarm" ] ; then
        echo "Swarm deployment detected.  MD_Utils should be controlled by upstream processes. "
        echo "!!!  NOT ALTERING MD_Utils  !!!"
	return 0;
    elif [ "${GW_GRPC_ROLE}" == "Developer" ] ; then
	echo "Developer environment detected; pulling MD_Utils from md-test."
	mdBranch="md-test"
	inDevEnv="true"
    else
        mdBranch="stable"
	inDevEnv="false"
    fi
    if [ ! -d "${theDir}/.git" ]; then
        echo ""
        echo "MD_Utils repo does not exist. Attempting to clone."
	git clone -b ${mdBranch} https://github.com/GLYCAM-Web/MD_Utils.git ${theDir}
    	if [ ! -d "${theDir}/.git" ]; then
        	echo ""
        	echo "Error:  Unable to clone MD_Utils.  Some functions will be unavailable."
        	echo "You can try again on your own using the following command."
        	echo "You will not need to remake GEMS or GMML after cloning."
        	echo ""
		echo "git clone -b ${mdBranch} https://github.com/GLYCAM-Web/MD_Utils.git ${theDir}"
		return 1
	fi
	echo "Cloning of MD_Utils was successfil"
	return 0
    fi
    ## Still here?  If on the correct branch, pull and return.
    currentBranch="$( cd ${theDir} && git branch | grep ^* | cut -d ' ' -f2)"
    if [ "${currentBranch}" == "${mdBranch}" ] ; then
        echo "Attempting to update MD_Utils"
	##  Ensure upstream is tracked properly, then pull
	( cd ${theDir} \
		&& git branch -u origin/${mdBranch} \
		&& git pull )
        returnValue=$?
        if [ "${returnValue}" != 0 ] ; then
            echo ""
            echo "Error!  Unable to update MD_Utils. "
            echo "You can try again on your own using the command below."
            echo ""
            echo "cd ${theDir} && git pull origin ${mdBranch}"
	    return 1
        else
	    return 0
        fi
    fi
    ## Still here?  Ask what to do about it.
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "Your MD_Utils repo (\$GEMSHOME/External/MD_Utils) is not on the expected branch."
    echo "    Expected branch:  ${mdBranch}"
    echo "    Current branch:   ${currentBranch}"
    echo ""
    echo "What do you want to do? "
    echo "   p  (pull)       :  Issue 'git pull' in the repo on the current branch "
    echo "   s  (skip)       :  Don't do anything in the repo.  Carry on with make. "
    echo "   a  (abort)      :  Don't do anything in the repo.  Exit make. "
    echo "   just hit enter  :  Change to the expected branch and update the repo. "
    echo ""
    echo "If you don't know what to do, you should probably just htt enter."
    echo ""
    read -p "Your response:  " branchResponse
    if [[ $branchResponse == [sS] ]]; then
        printf "Skipping update of MD_Utils repo.\n"
        return 0;
    elif [[ $branchResponse == [aA] ]]; then
        printf "Abort!\n"
        exit 1;
    elif [[ $branchResponse == [pP] ]]; then
        printf "Pulling from within the current branch\n"
	( cd ${theDir} && git pull )
        returnValue=$?
        if [ "${returnValue}" != 0 ] ; then
            echo ""
            echo "Error!  Unable to update MD_Utils within the current branch. "
            echo "You can try again on your own using the command below."
            echo "Exiting for now."
            echo ""
            echo "cd ${theDir} && git pull"
	    return 1
        else
	    return 0
        fi
    else
        echo "Changing to branch ${mdBranch}, ensuring proper upstream, and pulling"
	COMMAND="( cd ${theDir} &&  git branch | grep -q ${mdBranch} )"
	echo "running :  ${COMMAND}"
	if ! eval ${COMMAND} ; then
            echo "The expected branch does not already exist.  Setting it up now."
	    COMMAND="( cd ${theDir} \
	        && git remote set-branches --add origin ${mdBranch} \
		&& git fetch \
		&& git checkout -b ${mdBranch}  origin/${mdBranch} )"
	    eval ${COMMAND}
            returnValue=$?
            if [ "${returnValue}" != 0 ] ; then
                echo ""
                echo "Error!  Unable to change branches and update MD_Utils. "
                echo "You can try again on your own using the command below."
                echo "Exiting for now."
                echo ""
                echo "${COMMAND}"
	        return 1
            else
	        return 0
            fi
        else
	    ##  Check out the branch, ensure upstream is tracked properly, then pull
	    COMMAND="( cd ${theDir} \
		&& git checkout ${mdBranch} \
		&& git branch -u origin/${mdBranch} \
		&& git pull )"
	    eval ${COMMAND}
            returnValue=$?
            if [ "${returnValue}" != 0 ] ; then
                echo ""
                echo "Error!  Unable to update MD_Utils. "
                echo "You can try again on your own using the command below."
                echo ""
                echo "${COMMAND}"
	        return 1
            else
	        return 0
            fi
	fi
    fi
}

################################################################
#########                CHECK SETTINGS                #########
################################################################

echo "Starting installation of GEMS at `date`".

gemshome=`pwd`
check_gemshome $gemshome
check_gmmldir $GEMSHOME/gmml
check_pull_mdutils
get_numprocs

################################################################
#########              CREATE CLIENT HOOKS             #########
################################################################

#Cannot use server side hooks when hosting on git-hub.
#Stuff in .git/hooks is ignored by git.
#Solution: The folder .hooks is tracked by git.
# Copy .hooks to .git/hooks during installation.
cp -r $GEMSHOME/.hooks/* $GEMSHOME/.git/hooks/
# gmml hooks are similarly copied in its make.sh.  SRB Jul 2019.
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
#printf "# (1) Location of the installation\n\n" >> config.h

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
    printf "Usage: $0 clean_gmml? debug_gmml wrap_gmml?\n"
    printf "Example: $0 clean no_wrap\n"
    printf "Default: $0 no_clean wrap\n"
    printf "*************************************************************\n"
    printf "If selected the options do this:\n"
    printf "     1. Cleans gmml before making.\n"
    printf "     2. Build gmml with debugging options.\n"
    printf "     3. Wrap up via swig (wrapping required only for GEMS).\n"
    printf "*************************************************************\n"
    printf "These environment variables are also used:\n"
    printf "GEMSHOME: The path of the top level directory of GEMS.\n"
    printf "GEMSMAKEPROCS: The parallelism of make; optional, default is 4.\n"
    printf "PYTHON_HOME: The path of the top level directory of Python 3.\n"
    printf "PYTHON_HEADER_HOME: The path of Python.h; optional, default is PYTHON_HOME.\n"
    printf "*************************************************************\n"
    echo "Exiting."
    exit 1
fi

################################################################
#########                SET UP DEFAULTS               #########
################################################################

#Changing the following options are for developers.
CLEAN=""
BUILD_LEVEL="O2"
TARGET_MAKE_FILE="Makefile"
WRAP_GMML="-w"

################################################################
#########               COMMAND LINE INPUTS            #########
################################################################
i=1
while [ ${i} -le $# ]; do
    argument="${!i}"
    if [ "$argument" = "clean" ]||[ "$argument" = "no_clean" ];then
        if [ "$argument" = "clean" ]; then
			CLEAN="-c"
	fi
    elif [ "$argument" = "wrap" ]||[ "$argument" = "no_wrap" ];then
        if [ "$argument" = "no_wrap" ]; then
			WRAP_GMML=""
	fi
    elif [ "$argument" = "optimize" ]||[ "$argument" = "no_optimize" ]||[ "$argument" = "O1" ]||[ "$argument" = "O2" ]||[ "$argument" = "debug" ]||[ "$argument" = "no_debug" ];then

	if [ "$argument" = "O1" ]||[ "$argument" = "O2" ]||[ "$argument" = "optimize" ]; then
		BUILD_LEVEL=O2
	elif [ "$argument" = "no_optimize" ]; then
		BUILD_LEVEL=O0
	elif [ "$argument" = "debug" ];then
		BUILD_LEVEL=OG
        fi
    elif [ "$argument" = "jobs" ];then
	i=$[$i+1]
	NMP="${!i}"		
    fi
    i=$[$i+1]
done

# if [[ $# -eq 1 ]]; then
#     CLEAN="$1"
# elif [[ $# -eq 2 ]]; then
#     CLEAN="$1"
#     WRAP_GMML="$2"
# fi

printf "\nBuilding with these settings:\n"
printf "GEMSHOME: $GEMSHOME\n"
printf "TARGET_MAKE_FILE: $TARGET_MAKE_FILE\n"
printf "CLEAN: $CLEAN\n"
printf "BUILD_LEVEL: $BUILD_LEVEL\n"
printf "WRAP_GMML: $WRAP_GMML\n\n"

################################################################
#########                  COMPILE GMML                #########
################################################################

cd gmml/
./make.sh $CLEAN $WRAP_GMML -o $BUILD_LEVEL -j $NMP
cd ../

################################################################
#########              WRAP UP TO GEMS                 #########
################################################################
                #WRAPPING DONE IN GMML


#if [[ "$WRAP_GMML" != "no_wrap" ]]; then
#
#    check_pythonhome
#
#    echo ""
#    if [[ -f "gmml.i" ]]; then
#        echo "Wrapping gmml library in python ..."
#        swig -version
#        swig -c++ -python gmml.i
#    else
#        echo "Warning:  Interface file for swig does not exist."
#    fi
#
#    echo ""
#    # In some cases Python.h does not live in PYTHON_HOME; allow user control.
#    if [ -z "$PYTHON_HEADER_HOME" ]; then
#        PYTHON_HEADER_HOME="$PYTHON_HOME"
#    fi
#    PYTHON_FILE="$PYTHON_HEADER_HOME/Python.h"
#    if [ -f $PYTHON_FILE ]; then
#        echo "Using $PYTHON_FILE header file."
#        if [ -f "gmml_wrap.cxx" ]; then
#            echo "Compiling wrapped gmml library in python ..."
#            g++ -std=c++17 -O3 -fPIC -c gmml_wrap.cxx -I"$PYTHON_HEADER_HOME" -I gmml/
#        else
#            echo "Warning:  gmml_wrap.cxx does not exist."
#        fi
#    else
#        echo "Warning:  $PYTHON_FILE not found !"
#    fi
#
#    echo ""
#    if [[ -f "gmml_wrap.o" ]]; then
#        echo "Building python interface ..."
#        g++ -std=c++17 -shared gmml/build/*.o gmml_wrap.o -o _gmml.so
#    else
#        echo "Warning:  gmml python interface has not been compiled correctly."
#    fi
#fi

echo ""
echo "GEMS compilation is finished at `date`".
exit

