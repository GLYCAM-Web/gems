# Installing GEMS (GLYCAM Extensible Modeling Script)

This document is likely somewhat out of date.  We're working on that.

[Prerequisites](#prerequisites)  
[Obtaining the software](#obtaining-the-software)  
[Compiling and Installing](#compiling-and-installing)  
[Testing the Installation](#testing-the-installation)  
[Example Use](#example-use)  
[Documentation](#documentation)  

## Prerequisites

In order to install GEMS, you will need to have the following software available on your system: 

* `openssl` 
* `git` 
* `python`   
* `python-dev` (you need the Python header files for your Linux distro, which may not be part of your existing Python package)
* `swig` 
* Kernel headers (the source code for the Linux kernel, which may not be installed on your system)
* `qmake`
* `qt4-dev-tools`
* `boost`

**NOTE** - installing some prerequisites may require `root` access.

Installation instructions will vary according to the package management software your distro uses.  If you use Ubuntu or any other Debian based system, you should be able to use a command like this:

```bash
sudo apt-get install openssl git python3 python3-dev swig build-essential qt4-qmake qt4-dev-tools libboost-all-dev 
```
For other Linux distros, please follow the instructions for the package management software included with your system. 

---

## Obtaining the software

Once you have installed the prerequisites, you can install the GEMS software. 

**NOTE** - installing GEMS **does not** require `root` access. 

Change to the directory where you will install GEMS, and clone the GEMS repo from Github: 

`git clone https://github.com/GLYCAM-Web/gems.git`

This will create a *`gems`* directory. Change to the *`gems`* directory, and clone the GMML repo from Github: 

```bash
cd gems/
git clone https://github.com/GLYCAM-Web/gmml.git
```

---

## Compiling and Installing

To compile the software, make sure you are still in the *`gems`* directory: 

```bash
pwd
/gems
```

Set your **`PYTHON_HOME`** environment variable to the location of the `Python.h` file for your Python version. For Ubuntu, use something like one of the following: 

`export PYTHON_HOME=/usr/include/python3.4`   
or   
`setenv PYTHON_HOME /usr/include/python3.4`  

Make sure to use the correct path to your Python version, and the correct version of Python. 

For other Linux distros, please follow the instructions to set environment variables specific to your system. 

To control the number of processors used during the *`make`* process, set the GEMSMAKEPROCS environment variable.  
The default value of 4 will be used if you do not set this variable. For exmaple, a command like one of the 
will set the number of processors to be used during *`make`* to 8:

`export GEMSMAKEPROCS=8`   
or   
`setenv GEMSMAKEPROCS 8`  

After setting the `PYTHON_HOME`, run the makefile in order to compile `gmml` and create the `gems` interface. 

```bash
./make.sh
```
---

## Testing the Installation

Make sure you are still in the *`gems`* directory, and run the following command to test the installation: 

```bash
./test_installation.bash
```
The output will tell you whether the installation was successful or not and will look similar to this:

```bash
$ ./test_installation.bash

This test should take less than 10 seconds to run on most modern computers.

This test will compare these files:
        updated_pdb.txt -- this is the file the test should generate
        test_pdb.txt.save -- this is the file to which it should be identical

Beginning test.

Checking for diffeences between test output and the standard output.

The test passed.
```        

**NOTE** - the test suite is a Bash shell script. Bash is generally installed by default on most Linux distros. If you try to run the test suite and get any errors, make sure that Bash is installed with the **`which bash`** command. This should return the `$PATH` variable for the `bash` executable, such as `/bin/bash`. If you get nothing back, you will need to either install Bash (which is far outside the scope of this README) or contact your system administrator for assistance. 

---

## Example Use

Make sure you are still in the *`gems`* directory, and run the following command, which is all on one line:   

```bash
python3 test_installation.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -prep "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -pdb "gmml/example/pdb/Small_to_test.pdb" > testing.log 2&> testing.error
```
**NOTE** - make sure to use your version of Python. 

There are also sample commands located at the top of the `*.py` files. Look in the comments for a line that says `# SAMPLE COMMAND` and use the examples found below there. 

You can also use the available help for most GEMS functions. 

```bash
$ python3 test_installation.py --help
Available options:
-amino_libs : amino acid library file(s) (e.g. gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib)
-glycam_libs: glycam library file(s)
-other_libs : other kinds of library files
-prep       : prep file(s) (e.g. gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep)
-pdb        : pdb file (e.g. gmml/example/pdb/1RVZ_New.pdb)
-cnf        : configuration file as an argument. sample file format:
amino_libs
gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib
gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib
glycam_libs
other_libs
prep
gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep
pdb
gmml/example/pdb/1RVZ_New.pdb
```

---

## Documentation

The official documentation for both GEMS and GMML can be found on the main GLYCAM website: 

GEMS - [http://glycam.org/gems](http://glycam.org/gems "GEMS")  
GMML - [http://glycam.org/gmml](http://glycam.org/gmml "GMML")

