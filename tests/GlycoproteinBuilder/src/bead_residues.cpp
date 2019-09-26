#include "../includes/bead_residues.h"

void beads::Add_Beads(MolecularModeling::Assembly &glycoprotein, GlycosylationSiteVector &glycosites)
{
    /*
    / This function creates atoms with large radii called "beads" for the protein and glycans
    / The beads are added directly in glycoprotein and put in the AtomNode connection network
    / Within each glycosite an atomvector (vector of pointers to each bead) is added.
    / Each glycosite will have atomvectors of protein beads, glycan beads, and other glycan beads.
    / Other glycan beads are beads from glycans attached to other glycosites.
    */
    // Add beads to protein atoms first.
    AtomVector protein_beads = Add_Beads_To_Protein(glycoprotein);
    // Go through all glycosite glycans, add bead to each residue, attach it to one other atom in residue.
    for (GlycosylationSiteVector::iterator it1 = glycosites.begin(); it1 != glycosites.end(); ++it1)
    {
    	GlycosylationSite *glycosite = &(*it1);
        Atom *cb_atom = glycosite->GetResidue()->GetAtom("CB");
        // This needs to be updated/scrapped if we start adjusting the glycosidic angles after this step, as that can change max distance
        double distance = ( GetMaxDistanceBetweenAtoms(glycosite->GetAttachedGlycan()->GetAllAtomsOfAssembly()) + 5); // added 5 to account for CB-C1(glycan) distance
        AtomVector close_protein_beads = selection::AtomsWithinDistanceOf(cb_atom, distance, protein_beads);
        glycosite->SetProteinBeads(&close_protein_beads);
        AtomVector self_glycan_beads = Add_Beads_To_Glycan(glycosite->GetAttachedGlycan());
        glycosite->SetSelfGlycanBeads(&self_glycan_beads);
    }
    // Now find beads from other glycans and add them to list of other_glycan_beads for each glycosite
   Set_Other_Glycan_Beads(glycosites);
}

void beads::Set_Other_Glycan_Beads(GlycosylationSiteVector &glycosites)
{
    for (GlycosylationSiteVector::iterator it1 = glycosites.begin(); it1 != glycosites.end(); ++it1)
    {
        GlycosylationSite *glycosite1 = &(*it1);
        AtomVector other_glycan_beads;
        for (GlycosylationSiteVector::iterator it2 = glycosites.begin(); it2 != glycosites.end(); ++it2)
        {
            GlycosylationSite *glycosite2 = &(*it2);
            if(glycosite1 != glycosite2) // Check if same site
            {
                // append each other glycosite's beads to list of other_glycan_beads: a.insert(std::end(a), std::begin(b), std::end(b));
                AtomVector temp = glycosite2->GetSelfGlycanBeads();
                other_glycan_beads.insert(std::end(other_glycan_beads), std::begin(temp), std::end(temp));
                //std::cout << "Adding beads of glycosite " << glycosite2->GetResidue()->GetId() << " to " << glycosite1->GetResidue()->GetId() << std::endl;
            }
        }
        glycosite1->SetOtherGlycanBeads(&other_glycan_beads);
    }
}

AtomVector beads::Add_Beads_To_Protein(MolecularModeling::Assembly &assembly)
{
    // sfat stands for sidechain fat atom. mfat stands for mainchain fat atom. fat atoms are now called beads, but the name stayed.
    // Different names allow for easy selection in VMD visualisation problem. They serve no other purpose.
    // The beads should completely envelope all atoms in the protein. I first did all CA atoms in the mainchain, then visualized in VMD
    // and manually selected sidechain atoms that would cover the rest of the protein.
    // The code below adds to CA atoms and then selected other atoms based on their name and sometimes also the residue name.
    AtomVector protein_beads;
    ResidueVector protein_residues = assembly.GetAllProteinResiduesOfAssembly();
    for (ResidueVector::iterator it1 = protein_residues.begin(); it1 != protein_residues.end(); ++it1)
    {
        Residue *residue = *it1;
        AtomVector atoms = residue->GetAtoms();
        for (AtomVector::iterator it2 = atoms.begin(); it2 != atoms.end(); ++it2)
        {
            Atom *atom = *it2;
            if (atom->GetName().compare("CA")==0) // Main chain (mfat) CA atoms
            {
                //std::cout << "Adding bead to protein " << residue->GetId() << std::endl;
                Atom* bead_atom = new Atom(residue, "mfat", atom->GetCoordinates());
                residue->AddAtom(bead_atom);
                protein_beads.push_back(bead_atom);
            }
            else if ( (atom->GetName().compare("NZ")==0) || // Sidechain (sfat) atoms I've manually selected
                      (atom->GetName().compare("CZ")==0) ||
                      (atom->GetName().compare("NE2")==0) ||
                      (atom->GetName().compare("OD1")==0) ||
                      (atom->GetName().compare("SD")==0)  ||
                      ( (atom->GetName().compare("CE2")==0) && residue->GetName().compare("TRP")==0 ) ||
                      ( (atom->GetName().compare("CD1")==0) && ( residue->GetName().compare("LEU")==0 || residue->GetName().compare("ILE")==0 ) ) ||
                      ( (atom->GetName().compare("CD")==0) && residue->GetName().compare("GLU")==0 )
                    )
            { // sfats should move when a chi1, chi2 is moved, so make sure they are connected to something for the SetDihedral function to move them.
                Atom* bead_atom = new Atom(residue, "sfat", atom->GetCoordinates());
                residue->AddAtom(bead_atom);
                protein_beads.push_back(bead_atom);
            }
        }
    }
    return protein_beads;
}

AtomVector beads::Add_Beads_To_Glycan(MolecularModeling::Assembly *assembly)
{
    AtomVector glycan_beads;
    ResidueVector glycan_residues = assembly->GetResidues();
    for (ResidueVector::iterator it2 = glycan_residues.begin(); it2 != glycan_residues.end(); ++it2)
    {
        Residue *residue = *it2;
        if ( residue->GetName().at(1) != 'S' ) // don't add a bead to a sialic acid in this section (see "else" below). Middle character of resname is always S for sialic acid.
       // if ( residue->GetName().compare(1, 2, "SA") != 0) // don't add one to a sialic acid (see below)
        {
            // std::cout << (*resi_iter)->GetName() << "\tG\t" << (*resi_iter)->CheckIfProtein() << endl;
           // std::cout << "Adding bead to self glycan " << residue->GetId() << std::endl;
            Atom* bead_atom = new Atom(residue, "gfat", residue->GetGeometricCenter());
            residue->AddAtom(bead_atom);
            glycan_beads.push_back(bead_atom);
            //Bond bead_atom to any other atom in residue so when glycan is moved, bead_atom moves too.
            Atom *any_atom = residue->GetAtoms().at(0); // 0 is arbitrary, any atom would do.
            any_atom->GetNode()->AddNodeNeighbor(bead_atom);
            AtomVector temp = {any_atom};
            AtomNode *node = new AtomNode(); // DELETE IS FOR LOSERS.
            bead_atom->SetNode(node);
            bead_atom->GetNode()->SetNodeNeighbors(temp);
            AtomVector atoms = residue->GetAtoms();
            for (AtomVector::iterator it3 = atoms.begin(); it3 != atoms.end(); ++it3)
            {
                Atom *atom = *it3;
                if ( (atom->GetName().compare("C2N") == 0) || (atom->GetName().compare("C6") == 0) )
                {
                    bead_atom = new Atom(residue, "gfat", atom->GetCoordinates().at(0));
                    residue->AddAtom(bead_atom);
                    glycan_beads.push_back(bead_atom);
                    any_atom->GetNode()->AddNodeNeighbor(bead_atom);
                    AtomNode *node1 = new AtomNode(); // DELETE IS FOR LOSERS.
                    bead_atom->SetNode(node1);
                    bead_atom->GetNode()->SetNodeNeighbors(temp);
                }
            }
        }
        else // if it is sialic acid
        {
            AtomVector atoms = residue->GetAtoms();
            for (AtomVector::iterator it3 = atoms.begin(); it3 != atoms.end(); ++it3)
            {
                Atom *atom = *it3;
                if ( (atom->GetName().compare("C2") == 0) || (atom->GetName().compare("N5") == 0) || (atom->GetName().compare("C8") == 0) )
                {
                    Atom* bead_atom = new Atom(residue, "gfat", atom->GetCoordinates().at(0));
                    residue->AddAtom(bead_atom);
                    glycan_beads.push_back(bead_atom);
                    Atom *any_atom = residue->GetAtoms().at(0);
                    any_atom->GetNode()->AddNodeNeighbor(bead_atom);
                    AtomVector temp = {any_atom};
                    AtomNode *node = new AtomNode(); // DELETE IS FOR LOSERS.
                    bead_atom->SetNode(node);
                    bead_atom->GetNode()->SetNodeNeighbors(temp);
                }
            }
        }
    }
    return glycan_beads;
}

void beads::Remove_Beads(MolecularModeling::Assembly &glycoprotein)
{
    // Removes all bead atoms from the assembly.
    // Based on having "fat" in the name.
    // When finished, assembly should look the same as before Add_Beads was called.
    ResidueVector all_residues = glycoprotein.GetAllResiduesOfAssembly();
    for (ResidueVector::iterator it1 = all_residues.begin(); it1 != all_residues.end(); ++it1)
    {
        Residue *residue = *it1;
        AtomVector atoms = residue->GetAtoms();
        for (AtomVector::iterator it2 = atoms.begin(); it2 != atoms.end(); ++it2)
        {
            Atom *atom = *it2;
            if (atom->GetName().find("fat")==1)
            {
                residue->RemoveAtom(atom);
            }
        }
    }
}

double GetMaxDistanceBetweenAtoms(AtomVector atoms)
{
    double max_distance = 0.0;
    for(AtomVector::iterator it1 = atoms.begin(); it1 != atoms.end(); ++it1)
    {
        Atom *atom1 = (*it1);
        for(AtomVector::iterator it2 = it1; it2 != atoms.end(); ++it2)
        {
            Atom *atom2 = (*it2);
            if (atom1->GetDistanceToAtom(atom2) > max_distance)
            {
                max_distance = atom1->GetDistanceToAtom(atom2);
            }
        }
    }
    return max_distance;
}



