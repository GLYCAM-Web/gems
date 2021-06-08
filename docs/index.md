# Overview

There are three main components to GEMS:

1. An interface to GMML
2. The GEMS Modules
3. Scripts in the `bin` directory

## The GMML Interface

GMML (GLYCAM Molecular Modeling Library) is a C++ library designed to 
simplify molecular modelign tasks.  It is built to be especially good at
modeling carbohydrates (aka sugars, glycans), but it is also designed to
handle all the things carbohydrates interact with.  So, it is pretty good
at modeling molecules in general.

Whenever you type "make.sh" in GEMS, a program called [SWIG](http://www.swig.org/)
builds an interface between GMML and Python 3.  This interface makes it possible 
to directly access the GMML library.  That is, you can use the components of 
the library without needing to learn (much) C++ or to compile a program.

## The GEMS Modules

The primary purpose of these modules is to serve as an interface between
[GLYCAM-Web](dev.glycam.org) and other software.  The other software includes
GMML (via the SWIG interface), but is not liminted to that.  

The input to the modules is primarily in the form of a JSON object.  The
output is also in that form.  

The GEMS Modules are designed to ensure that the user can obtain exactly 
the same output whether the user interacts via:

* GLYCAM-Web using a browser
* The JSON API
* The command line

## The `bin` Directory

The scripts in this directory perform common tasks.  Notable among these
is the `delegate` script.  All website and API traffic is handled by this
script.  This script can also be used on the command line, e.g.:

	$GEMSHOME/bin/delegate my_input.json

Here, `GEMSHOME` is the path to your GEMS installation and `my_input.json` is
a file containing a JSON object to be used as input to the delegator module.
The delegator inspects your JSON object and, based on what it finds, either
hands the input to the appropriate entity or, if something has gone wrong, 
returns an error message.
