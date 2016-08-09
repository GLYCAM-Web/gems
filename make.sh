#!/bin/bash
MOOD="$1"
CLEAN="$2"
TARGET_MAKE_FILE="Makefile-main"
echo $TARGET_MAKE_FILE
if [ "$CLEAN" == "-cm" ]; then
	echo "Clean and make"
elif [ "$CLEAN" == "-m" ]; then
	echo "Make only"
else
	echo "Compilation is set to default: make only"
	CLEAN="-m"
fi
echo $MOOD
if [ -z "$PYTHON_HOME" ] ; then
	echo "PYTHON_HOME is not set."
	echo "Cannot automatically set PYTHON_HOME environment variable.."
	echo "Your PYTHON_HOME should be set to the location of Python.h for your python3 installation."
	echo "Exiting."
	exit 1
fi

cd gmml
if [ -f $TARGET_MAKE_FILE ]; then
	if [ "$MOOD" == "Qt" ]; then
		echo "Compile compatible with Qt"
		if [ "$CLEAN" == "-cm" ]; then
			make -f $TARGET_MAKE_FILE distclean
			rm -rf gmml.pro*
			qmake -project -t lib -o gmml.pro "OBJECTS_DIR = build" "DESTDIR = bin"
			qmake -o Makefile
			make -j 4
		elif [ "$CLEAN" == "-m" ]; then
			make -j 4
		fi
	else
		echo "Qt independent compilation"
		if [ "$CLEAN" == "-cm" ]; then
			make -f $TARGET_MAKE_FILE distclean
			rm -rf gmml.pro*
			make -j 4 -f $TARGET_MAKE_FILE
		elif [ "$CLEAN" == "-m" ]; then
			make -j 4 -f $TARGET_MAKE_FILE
		fi
	fi
else
	if [ "$MOOD" == "Qt" ]; then
		if [ "$CLEAN" == "-cm" ]; then
			make distclean
			rm -rf gmml.pro*
			qmake -project -t lib -o gmml.pro "OBJECTS_DIR = build" "DESTDIR = bin"
			qmake -o Makefile
			make -j 4
		elif [ "$CLEAN" == "-m" ]; then
			make -j 4
		fi
	else
		echo "Qt independent make file does not exist"
	fi
fi
cd ..
if [ -f "gmml.i" ]; then
	echo "Wrapping gmml library in python ..."
	swig -c++ -python gmml.i
else
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
if [ -f "gmml_wrap.o" ]; then
	echo "Building python interface ..."
	g++ -shared gmml/build/*.o gmml_wrap.o -o _gmml.so
else
	echo "gmml has not been compiled correctly"
fi
