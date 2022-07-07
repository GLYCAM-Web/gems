#!/bin/bash

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

check_website_status() {
	if [ "${GW_LIVE_SWARM}zzz" == "zzz" ] ; then
		echo ""
		echo "You do not appear to be inside a full DevEnv."
		echo "Pushing is not allowed."
		echo ""
		echo "You need to be in the grpc delegator container in a running site."
		echo ""
		echo "Exiting"
		exit 1
	elif [ "${GW_LIVE_SWARM}" == "true" ] ; then
		echo ""
		echo "This appears to be a live swarm."
		echo "Pushing is not allowed from a live swarm."
		echo ""
		echo "Exiting"
		echo ""
		exit 1
	else
		echo ""
		echo "This appears to be a full DevEnv that is not a live swarm."
		echo "Pre-push tests can be run."
		echo ""
	fi
}

gemshome=`pwd`
check_gemshome $gemshome 
## OG Oct 2021 have the hooks update themselves.
cp -r $GEMSHOME/.hooks/* $GEMSHOME/.git/hooks/

#### Allow skipping tests ####
branch=`git rev-parse --abbrev-ref HEAD`
if [[ "$branch" != "gems-dev" ]] && [[ "$branch" != "gems-test" ]]; then
    printf "Branch is %s\nSkipping tests is allowed.\nDo you want to skip them?\ns=skip\na=abort\nEnter anything to run tests.\n" $branch
    read -p "Enter response: " response < /dev/tty
    if [[ $response == [sS] ]]; then
        printf "Skipping tests!\n"
        exit 0;
    elif [[ $response == [aA] ]]; then
        printf "Abort!\n"
        exit 1;
    else
        printf "Running tests.\n"
    fi
fi
#### End Allow skipping tests ####


check_website_status



#Compile gmml if not compiled:
echo "Pulling gems AND gmml, and then compiling gmml if necessary with ./make.sh"
cd $GEMSHOME/gmml/
  git pull
cd $GEMSHOME
  git pull
 ./make.sh
cd - >> /dev/null 2>&1

echo "Running mandatory tests..."
cd $GEMSHOME/tests/
 bash run_tests.sh
 result=$? # record the exit status from compile_run_tests.bash
cd - >> /dev/null 2>&1
if [ $result -eq 0 ] ; then
    echo  "All tests have passed. Pushing is allowed."
    exit 0
else
    echo "
         *****************************************************************
         The tests have failed! 
         Push cancelled.
         *****************************************************************
         "
    exit 1
fi
