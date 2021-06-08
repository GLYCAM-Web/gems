#include "../includes/glycoprotein_builder.h"

/*******************************************/
/* Functions                               */
/*******************************************/

void glycoprotein_builder::AttachGlycansToGlycosites(MolecularModeling::Assembly &glycoprotein, GlycosylationSiteVector &glycosites, const std::string glycanDirectory)
{
    // Find protein residues in Glycoprotein that will get a glycan added. Set Residue in Glycosite.
    // Often there are multiple chains with the same residue number. If the input file repeats a residue number, it will go on the next instance (next chain)
    // of that residue number. This is not a good long term solution, as users will want to select chains.
    ResidueVector protein_residues = glycoprotein.GetResidues();
    for(GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
    {
        bool stop = false;
        std::string glycosite_number = glycosite->GetResidueNumber();
        ResidueVector::iterator it2 = protein_residues.begin();
        while ( (!stop) && (it2 != protein_residues.end()) )
        {
            MolecularModeling::Residue *protein_residue = *it2;
            std::string id = protein_residue->GetId();
            std::string formatted_glycosite_number = "_" + glycosite_number + "_";
            if( id.compare(3, formatted_glycosite_number.size(), formatted_glycosite_number) == 0)
            {
                //std::cout << "glycosite: " << glycosite_number << std::endl;
                std::cout << "glycosite id:" << id << std::endl;
                glycosite->SetResidue(protein_residue);
                stop = true;
                // Remove residue from list, so if user has listed same residue name twice, it will go on next instance (i.e. on next chain) of residue number
                protein_residues.erase(std::remove(protein_residues.begin(), protein_residues.end(), *it2), protein_residues.end()); // Note need #include <algorithm>
            }
            ++it2;
        }
    }
//    // Find protein residues in Glycoprotein that will get a glycan added. Set Residue in Glycosite.
//    ResidueVector protein_residues = glycoprotein.GetResidues();
//    for (ResidueVector::iterator it2 = protein_residues.begin(); it2 != protein_residues.end(); ++it2)
//    {
//        Residue *protein_residue = *it2;
//        std::string id = protein_residue->GetId();
//        for(GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
//        {
//            std::string glycosite_number = glycosite->GetResidueNumber();
//            std::string formatted_glycosite_number = "_" + glycosite_number + "_";
//            if( id.compare(5, formatted_glycosite_number.size(), formatted_glycosite_number) == 0)
//            {
//                //std::cout << "glycosite: " << glycosite_number << std::endl;
//                std::cout << "glycosite id:" << id << std::endl;
//                glycosite->SetResidue(protein_residue);
//            }
//        }
//    }
    // Load glycan files from directory
    //std::cout << "Glycan directory: " << glycanDirectory << std::endl;
    std::string filepath;
    DIR *dp; // A directory stream
    struct dirent *dirp; // Contains file serial number and name (char d_name[])
    struct stat filestat; // Contains info about file, such as device ID, user ID, access time etc

    dp = opendir( glycanDirectory.c_str() ); //.c_str adds a null character to the end.
    if (dp == NULL)
    {
        std::cout << "Error(" << errno << ") opening " << glycanDirectory << std::endl;
        return;
    }
    while ((dirp = readdir ( dp )))
    {
        filepath = glycanDirectory + "/" + dirp->d_name;
        // If the file is a directory (or is in some way invalid) we'll skip it
        if (stat( filepath.c_str(), &filestat )) continue; // Is it a valid file?
        if (S_ISDIR( filestat.st_mode ))         continue; // Is it a directory?
        for (GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
        {
            //std::cout << "Glycan is " << glycosite->GetGlycanName() << ". d_name is " << dirp->d_name << std::endl;
            if (glycosite->GetGlycanName().compare(0, glycosite->GetGlycanName().size(), dirp->d_name, 0, glycosite->GetGlycanName().size()) == 0 )
            {
                MolecularModeling::Assembly input_glycan(filepath, gmml::InputFileType::PDB);
                input_glycan.BuildStructureByDistance();
                glycosite->AttachGlycan(input_glycan, glycoprotein);
                //std::cout << "Added " << glycosite->GetGlycanName() << " to " << glycosite->GetResidueNumber();
            }
        }
    }
    closedir( dp );
}

void glycoprotein_builder::Read_Input_File(GlycosylationSiteVector &glycosites, std::string &proteinPDB, std::string &glycanDirectory, const std::string working_Directory)
{
    std::string buffer;
    std::ifstream infile (working_Directory + "/input.txt");
    if (!infile)
    {
        std::cerr << "Uh oh, input file could not be opened for reading!" << std::endl;
        std::exit(1);
    }
    while (infile) // While there's still stuff left to read
    {
        std::string strInput;
        getline(infile, strInput);
        if(strInput == "Protein:")
        {
            getline(infile, proteinPDB);
        }
        if(strInput == "Glycans:")
        {
            getline(infile, glycanDirectory);
            glycanDirectory = working_Directory + "/" + glycanDirectory;
        }
        if(strInput == "Protein Residue, Glycan Name:")
        {
            getline(infile, buffer);
            while(buffer != "END")
            {
                StringVector splitLine = split(buffer, ',');
                glycosites.emplace_back(splitLine.at(1), splitLine.at(0)); // Creates GlycosylationSite instance on the vector. Love it.
                getline(infile, buffer);
            }
        }
    }
}

void glycoprotein_builder::PrintDihedralAnglesAndOverlapOfGlycosites(GlycosylationSiteVector &glycosites)
{
    for(GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
    {
        std::cout << "site: " << glycosite->GetResidueNumber() << " chi1: " << glycosite->GetChi1Value() << ", chi2: " << glycosite->GetChi2Value() << ", overlap: " <<  glycosite->GetOverlap() << "\n";
    }
    return;
}

void glycoprotein_builder::SetReasonableChi1Chi2Values(GlycosylationSiteVector &glycosites)
{
    for(GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
    {
        glycosite->SetChi1Value(180);
        glycosite->SetChi2Value(180);
        std::cout << "Setup for " << glycosite->GetResidue()->GetId() << " chi1: " << glycosite->GetChi1Value() << " chi2: " << glycosite->GetChi2Value() << "\n";
    }
//    Statistical analysis of the protein environment of N-glycosylation sites: implications for occupancy, structure, and folding
//    Andrei-J. Petrescu  Adina-L. Milac  Stefana M. Petrescu  Raymond A. Dwek Mark R. Wormald
//    Glycobiology, Volume 14, Issue 2, 1 February 2004, Pages 103–114,
    return;
}

void glycoprotein_builder::SetRandomChi1Chi2Values(GlycosylationSiteVector &glycosites)
{
    srand(time(NULL)); // Actually maybe random.
    for(GlycosylationSiteVector::iterator glycosite = glycosites.begin(); glycosite != glycosites.end(); ++glycosite)
    {
        glycosite->SetChi1Value(glycoprotein_builder::RandomAngle_360range());
        glycosite->SetChi2Value(glycoprotein_builder::RandomAngle_360range());
        std::cout << "Setup for " << glycosite->GetResidue()->GetId() << " chi1: " << glycosite->GetChi1Value() << " chi2: " << glycosite->GetChi2Value() << "\n";
    }
    return;
}



double glycoprotein_builder::GetGlobalOverlap(GlycosylationSiteVector &glycosites)
{
    //std::cout << "Calculating global overlap\n";
    double global_overlap = 0.0;
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        global_overlap += current_glycosite->GetOverlap();
        //std::cout << "Current site is " << current_glycosite->GetResidueNumber() << ", overlap: " << current_glycosite->GetOverlap() << ", making global: " << global_overlap << "\n";
    }
    return global_overlap;
}

// random number generator; allows full range rotation
double glycoprotein_builder::RandomAngle_360range()
{
    return (rand() % 360) + 1 - 180;
}

double glycoprotein_builder::RandomAngle_range(int min, int max)
{
   // double angle = rand() % (max + 1 - min) + min;
    //std::cout << "Angle in range " << min << " - " << max << " is " << angle << "\n";
    // return angle;
    return rand() % (max + 1 - min) + min;
}

// random number generator; specify a maximum step size relative to a start point
double glycoprotein_builder::RandomAngle_PlusMinusX(double start_point, int max_step_size)
{
    return start_point + (rand() % (max_step_size * 2) + 1) - max_step_size;
}

double glycoprotein_builder::GetNewAngleScaledToDegreeOfOverlap(double current_angle, double overlap, int number_of_atoms)
{
    int max_step_size = 1 + std::round( 180 * ( overlap / number_of_atoms ) ); // Always allow at least 1 degrees of movement
    return RandomAngle_PlusMinusX(current_angle, max_step_size);
}

void glycoprotein_builder::write_pdb_file(Assembly *glycoprotein, int cycle, std::string summary_filename, double score)
{
    std::stringstream ss;
    ss << summary_filename << "_cycle_" << cycle << "overlap_" << score << ".pdb";
    PdbFileSpace::PdbFile *outputPdbFile = glycoprotein->BuildPdbFileStructureFromAssembly(-1,0);
    outputPdbFile->Write(ss.str());
//    std::ofstream summary;   // write a file that describes the best conformations found
//    summary.open(summary_filename, std::ios::out | std::ios::app);
//    summary << score << "\t" << "cycle_" << cycle << ".pdb\n";
//    summary.close();
}

void glycoprotein_builder::PrintOverlaps(GlycosylationSiteVector &glycosites)
{
    std::cout << "      Site        |  Total | Protein | Glycan \n";
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        current_glycosite->Print_bead_overlaps();
    }
}

void glycoprotein_builder::PrintOverlaps(GlycosylationSitePointerVector &glycosites)
{
    std::cout << "      Site        |  Total | Protein | Glycan \n";
    for (GlycosylationSitePointerVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        (*current_glycosite)->Print_bead_overlaps(); // Good old pointers to pointers.
    }
}



void glycoprotein_builder::CalculateAndPrintOverlaps(GlycosylationSiteVector &glycosites)
{
    std::cout << "      Site        |  Total | Protein | Glycan \n";
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        current_glycosite->Calculate_and_print_bead_overlaps();
    }
}

void glycoprotein_builder::CalculateOverlaps(GlycosylationSiteVector &glycosites)
{
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        current_glycosite->Calculate_bead_overlaps();
    }
}

void glycoprotein_builder::SetBestChi1Chi2(GlycosylationSitePointerVector &glycosites, std::string overlap_type)
{
    /****
     * Ok, the problem here is that two sites that are close may independantly find a best set that when set together causes them to overlap. This can happen
     * when just looking at protein overlaps, as the sfat atom on the NLN is moving around. It's worse when you consider glycan overlaps.
     * When searching for the best overlaps, the monte_carlo function must always treat new low/equal overlaps as better. If it found zero for a site,
     * overlaps are reintroduced by another site moving, then when it finds a new zero for this site, the new one should take precedence. Going to check
     * that now.
     */
    for (GlycosylationSitePointerVector::iterator it = glycosites.begin(); it != glycosites.end(); ++it)
    {
        GlycosylationSite *current_glycosite = (*it);
        current_glycosite->SetChi1Value(current_glycosite->GetBestOverlapRecord(overlap_type).GetChi1());
        current_glycosite->SetChi2Value(current_glycosite->GetBestOverlapRecord(overlap_type).GetChi2());
        current_glycosite->Calculate_bead_overlaps();
    }
}

GlycosylationSitePointerVector glycoprotein_builder::DetermineSitesWithOverlap(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type)
{
    GlycosylationSitePointerVector sites_to_return;
    double overlap = 0.0;
    std::cout << "      Site        |  Total | Protein | Glycan " << std::endl;
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        overlap = current_glycosite->Calculate_bead_overlaps(overlap_type);
        if ( overlap > tolerance)
        {
//            std::cout << "Site " << current_glycosite->GetResidue()->GetId() << " is over tolerance with " << overlap << "\n";
            current_glycosite->Print_bead_overlaps();
            sites_to_return.push_back(&(*current_glycosite));
        }
    }
    return sites_to_return;
}

GlycosylationSitePointerVector glycoprotein_builder::GetSitesWithOverlap(GlycosylationSiteVector &glycosites, double tolerance)
{
    GlycosylationSitePointerVector sites_to_return;
    double overlap = 0.0;
    std::cout << "      Site        |  Total | Protein | Glycan " << std::endl;
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
    {
        overlap = current_glycosite->GetOverlap();
        if ( overlap > tolerance)
        {
//            std::cout << "Site " << current_glycosite->GetResidue()->GetId() << " is over tolerance with " << overlap << "\n";
            current_glycosite->Print_bead_overlaps();
            sites_to_return.push_back(&(*current_glycosite));
        }
    }
    return sites_to_return;
}

GlycosylationSitePointerVector glycoprotein_builder::DeleteSitesWithOverlaps(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type)
{
    GlycosylationSitePointerVector sites_to_return;
    double overlap = 0.0;
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end();)
    {
        overlap = current_glycosite->Calculate_bead_overlaps(overlap_type);
        // Delete site from list if overlap is greater than the tolerance value
        std::cout << "Site " << current_glycosite->GetResidueNumber() << ": " << overlap << " :";
        if ( overlap > tolerance)
        {
            std::cout << "Removed\n";
            ResidueVector glycan_residues = current_glycosite->GetAttachedGlycan()->GetResidues();
            for(ResidueVector::iterator it = glycan_residues.begin(); it != glycan_residues.end(); ++it)
            {
                current_glycosite->GetGlycoprotein()->RemoveResidue(*it);
                //glycoprotein.RemoveResidue(*it);
            }
            glycosites.erase(std::remove(glycosites.begin(), glycosites.end(), *current_glycosite), glycosites.end()); // Note need #include <algorithm>
        }
        else
        {
            std::cout << "Retained\n";
            sites_to_return.push_back(&(*current_glycosite));
            ++current_glycosite; // This will get you. Erase/Remove advances current_glycosite.
        }
    }
    return sites_to_return;
}

void glycoprotein_builder::DeleteSitesWithOverlapRecordsAboveTolerance(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type)
{
    for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end();)
    {
        double overlap = current_glycosite->GetBestOverlapRecord(overlap_type).GetOverlap();
        std::cout << "Site " << current_glycosite->GetResidueNumber() << ": " << overlap << " :";
        if ( overlap > tolerance)
        {
            std::cout << "Removed\n";
            ResidueVector glycan_residues = current_glycosite->GetAttachedGlycan()->GetResidues();
            for(ResidueVector::iterator it = glycan_residues.begin(); it != glycan_residues.end(); ++it)
            {
                current_glycosite->GetGlycoprotein()->RemoveResidue(*it);
            }
            glycosites.erase(std::remove(glycosites.begin(), glycosites.end(), *current_glycosite), glycosites.end()); // Note need #include <algorithm>
        }
        else
        {
            std::cout << "Retained\n";
            ++current_glycosite; // This will get you. Erase/Remove advances current_glycosite.
        }
    }
}

void glycoprotein_builder::DeleteSitesIterativelyWithOverlapAboveTolerance(GlycosylationSiteVector &glycosites, double tolerance)
{
    bool continue_deleting = true;
    // While overlap for any site is > tolerance
    // Delete site with highest overlap.
    // Re-calculate overlaps.
    while (continue_deleting)
    {
        GlycosylationSite *worst_site = glycosites.data(); // Pointer to the first glycosite. Remember an erase/remove "advances"
        for (GlycosylationSiteVector::iterator current_glycosite = glycosites.begin(); current_glycosite != glycosites.end(); ++current_glycosite)
        {
            if  ( current_glycosite->GetOverlap() > worst_site->GetOverlap())
            {
                worst_site = &(*current_glycosite); // The C is strong with this one.
            }
        }
        if (worst_site->GetOverlap() > tolerance)
        {
            continue_deleting = true;
            std::cout << "Site " << worst_site->GetResidueNumber() << ": " << worst_site->GetOverlap() << " :" << "Removed\n";
            ResidueVector glycan_residues = worst_site->GetAttachedGlycan()->GetResidues();
            for(ResidueVector::iterator it = glycan_residues.begin(); it != glycan_residues.end(); ++it)
            {
                worst_site->GetGlycoprotein()->RemoveResidue(*it);
            }
            glycosites.erase(std::remove(glycosites.begin(), glycosites.end(), *worst_site), glycosites.end()); // Note need #include <algorithm>
            beads::Set_Other_Glycan_Beads(glycosites); // After "erasing", the actual atoms still exist and pointers to them are valid. Need to reset what beads are part of "other".
            glycoprotein_builder::CalculateOverlaps(glycosites); // After deleting, other sites will have lower values
        }
        else
        {
            continue_deleting = false;
        }
    }
    return;
}

void glycoprotein_builder::Overlap_Weighted_Adjust_Torsions_For_X_Cycles(GlycosylationSitePointerVector &sites, GlycosylationSiteVector &glycosites, int max_cycles, double tolerance, std::string overlap_type)
{
    int cycle = 0;
    bool stop = false;
    while ( (cycle < max_cycles) && (stop == false) )
    {
        ++cycle;
        std::cout << "Cycle " << cycle << " of " << max_cycles << ".\n";
        Overlap_Weighted_Adjust_Torsions(sites);
        std::cout << "Updating list of sites with overlaps.\n";
        sites = DetermineSitesWithOverlap(glycosites, tolerance, overlap_type);
        if (sites.size() == 0)
        {
            std::cout << "No more overlaps\n";
            stop = true;
        }
    }
    return;
}

void glycoprotein_builder::Overlap_Weighted_Adjust_Torsions(GlycosylationSitePointerVector &sites)
{
    double new_dihedral_angle = 0.0;
    for(GlycosylationSitePointerVector::iterator it1 = sites.begin(); it1 != sites.end(); ++it1)
    {
        GlycosylationSite *current_glycosite = (*it1);
        new_dihedral_angle = GetNewAngleScaledToDegreeOfOverlap(current_glycosite->GetChi1Value(), current_glycosite->GetProteinOverlap(), current_glycosite->GetAttachedGlycan()->GetAllAtomsOfAssembly().size());
        current_glycosite->SetChi1Value(new_dihedral_angle);
        new_dihedral_angle = GetNewAngleScaledToDegreeOfOverlap(current_glycosite->GetChi2Value(), current_glycosite->GetProteinOverlap(), current_glycosite->GetAttachedGlycan()->GetAllAtomsOfAssembly().size());
        current_glycosite->SetChi2Value(new_dihedral_angle);
    }
    return;
}
