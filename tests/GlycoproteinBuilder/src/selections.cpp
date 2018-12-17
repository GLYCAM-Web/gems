#include "../includes/selections.h"

AtomVector selection::AtomsWithinDistanceOf(MolecularModeling::Atom *query_atom, double distance, AtomVector atoms)
{
    AtomVector atoms_within_distance;
    for(AtomVector::iterator it1 = atoms.begin(); it1 != atoms.end(); ++it1)
    {
        MolecularModeling::Atom *atom1 = (*it1);
        if (atom1->GetDistanceToAtom(query_atom) < distance )
        {
            atoms_within_distance.push_back(atom1);
        }
    }
    return atoms_within_distance;
}

