# GlycoProteinBuilder
Uses GEMS/GMML to add and adapt 3D structures of N-glycans and O-glycans onto glycoproteins. It can do this for Asn, Ser, Thr and Tyr.

## Schematic
![schematic](schematic/schematic.png)

### Notes
Project is under development, contact olivercgrant "at" uga.edu with queries. 
This code will replace the glycoprotein builder currently available on glycam.org/gp.
Has been tested on linux, but should install on both Mac and Windows with appropriate C++ complilers.

### Prerequisites

You'll need GMML. See here for installation instructions: http://glycam.org/docs/gems/download-and-install/.

### Installation of GlycoProteinBuilder
export GEMSHOME=<Your Path To Gems > # eg: export GEMSHOME=/home/oliver/Programs/gems

#### Makefile:
Some commands defined in the Makefile are:
$ make
$ make all
$ make bin/gp_builder
$ make build/<file_name>.o
$ make clean

#### Comand line:
g++ -std=c++0x -I $GEMSHOME/gmml/includes/ -I includes/ -L$GEMSHOME/gmml/bin/ -Wl,-rpath,$GEMSHOME/gmml/bin/ src/*.cpp -lgmml -o gp_builder

### Setup
Edit or create an input.txt file and place in a folder called tests/. See tests/input.txt for an example.

If running outside of the program directory, create a directory called outputs/

You must provide:

    a protein 3D structure

    glycan 3D structure(s)

    input.txt, which contains:

        protein file name

        name of the folder containing the glycans e.g. glycans

        the protein residue numbers you want to attach to (no automatic detection of sequons)

        the name of the glycan you want to attach. Be careful that the name matches the start of the name of the glycan file.

        e.g. m9 will match to m9* in the glycan folder, while m9-gtgt will cause just that rotamer to be added.

        Note that for each protein residue number provided a glycan must be detailed. Allowing you to add different glycans to different sites

### Bead based overlap calculation
In order to speed up the overlap calculation, certain atoms in the glycan and protein are replaced with large spheres that encompass the neighbouring atoms. The overlap calculation only looks at the beads, and as there are much fewer of them, it will be faster. The downside is that it is not as accurate and may be unncessarily optimizing. However, as the beads will encompass all atoms in the protein/glycan, if the bead overlap reaches zero, the per atom overlap will be zero.
Here is a figure showing the atoms being replaced by beads:
![bead replacment](schematic/beads.png)

## Monte Carlo - Protein First Algorithm
Only chi1 and chi2 angles are manipulated (for now).

A strict tolerance of 0.1 and a loose tolerance of 1.0 (square angstrom) are used for overlap cutoffs.

Starting with sites that have protein overlaps, chi1 and chi2 are adjusted (see below) until the overlap gets below the strict tolerance.

At the end of max_cycles, any sites with overlap greater than the loose tolerance are deleted. A glycan cannot be placed there.

Continuting with sites that have overlaps, chi1 and chi2 are adjusted until the overlap gets below the strict tolerance. A site can get below the tolerance and drop off the list of sites that are being considered, but another glycan can move and overlap with that site, and it must now be moved again. 

The set of chi1 and chi2 that produce the lowest overlaps score for a site are recorded.

At the end of max_cycles, the best chi1 and chi2 are set for each site. Sites where overlap did not get below the loose tolerance are deleted.

### Angle adjustment
The amount to change the torsion angle by is scaled to the degree of overlap. i.e. small overlap = small adjustment, large overlap = large adjustment.

### Known problems
At the end, should delete the highest overlapping site, and then reassess all sites before deleting another.

Setting the best chi1 and chi2 for two sites may cause them to overlap with each other, as the other can be in different orientations when the lowest overlap was found for each one. I need to track the overlap of local groups of sites. Looking at global won't work.




