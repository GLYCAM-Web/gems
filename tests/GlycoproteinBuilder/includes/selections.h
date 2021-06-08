#ifndef SELECTIONS_H
#define SELECTIONS_H

#include "gmml.hpp"

namespace selection
{
AtomVector AtomsWithinDistanceOf(MolecularModeling::Atom *query_atom, double distance, AtomVector atoms);
}

#endif // SELECTIONS_H
