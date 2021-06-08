#ifndef BEAD_RESIDUES_H
#define BEAD_RESIDUES_H

#include "glycosylationsite.h"
#include "selections.h"
#include "glycoprotein_builder.h"

typedef std::vector<GlycosylationSite> GlycosylationSiteVector;
typedef std::vector<GlycosylationSite*> GlycosylationSitePointerVector;

namespace beads
{
void Add_Beads(MolecularModeling::Assembly &glycoprotein, GlycosylationSiteVector &glycosites);
void Set_Other_Glycan_Beads(GlycosylationSiteVector &glycosites);
void Remove_Beads(MolecularModeling::Assembly &glycoprotein);
AtomVector Add_Beads_To_Glycan(MolecularModeling::Assembly *assembly);
AtomVector Add_Beads_To_Protein(MolecularModeling::Assembly &assembly);
}

double GetMaxDistanceBetweenAtoms(AtomVector atoms);

#endif // BEAD_RESIDUES_H

