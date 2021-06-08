#include "../includes/resolve_overlaps.h"

typedef std::vector<GlycosylationSite*> GlycosylationSitePointerVector;

using namespace gmml;
using namespace glycoprotein_builder;
/* New algorithm idea:
 * For each site that has overlap:
 1) Try to resolve all protein overlaps, ignoring glycan-glycan. Delete glycan from any site with unresolvable protein overlaps, report to user.
 2) Resolve glycan overlaps. Either
    a) Loop through and check every site each cycle, and move those with overlaps

    c) Create a tree structure for sites that overlap with each other.
        Could use assembly index/id of bead atom? Can work on individual trees and report nice info to users.


Note: Chi1 is 180,-60,60 +/- 30 degrees. Want a function that keeps the values within these states.
Note: Need to save best structure.
*/

void resolve_overlaps::weighted_protein_global_overlap_random_descent(GlycosylationSiteVector &glycosites, int max_cycles)
{
    int cycle = 1;
    bool stop = false;
    double previous_chi1;
    double previous_chi2;
    double previous_glycan_overlap, new_glycan_overlap, previous_protein_overlap, new_protein_overlap;
    double lowest_global_overlap = glycoprotein_builder::GetGlobalOverlap(glycosites);
    double new_global_overlap;
    double strict_tolerance = 0.1, loose_tolerance = 1.0;

    GlycosylationSitePointerVector sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance, "total");

    std::cout << "Initial torsions and overlaps:\n";
    glycoprotein_builder::PrintDihedralAnglesAndOverlapOfGlycosites(glycosites);
    while ( (cycle < max_cycles) && (stop == false) )
    {
        ++cycle;
        std::cout << "Cycle " << cycle << " of " << max_cycles << std::endl;
        std::random_shuffle (sites_with_overlaps.begin(), sites_with_overlaps.end());
        for(GlycosylationSitePointerVector::iterator it1 = sites_with_overlaps.begin(); it1 != sites_with_overlaps.end(); ++it1)
        {
            GlycosylationSite *current_glycosite = (*it1);
           // std::cout << "Checking " << current_glycosite->GetResidue()->GetId() << "\n";
            previous_glycan_overlap = current_glycosite->GetGlycanOverlap();
            previous_protein_overlap = current_glycosite->GetProteinOverlap();
            previous_chi1 = current_glycosite->GetChi1Value();
            current_glycosite->SetChi1Value(RandomAngle_360range());
            previous_chi2 = current_glycosite->GetChi2Value();
            current_glycosite->SetChi2Value(RandomAngle_360range());
            new_glycan_overlap = current_glycosite->Calculate_bead_overlaps_noRecord_noSet("glycan");
            new_protein_overlap = current_glycosite->Calculate_bead_overlaps_noRecord_noSet("protein");
            if ((new_glycan_overlap + (new_protein_overlap*5)) >= (previous_glycan_overlap + (previous_protein_overlap*5)))
            {
                current_glycosite->SetChi1Value(previous_chi1);
                current_glycosite->SetChi2Value(previous_chi2);
            }
//            else
//            {
//              //  std::cout << "Accepted a change of " << ((new_overlap) - (previous_overlap)) << "\n";
//            }
        }
        //std::cout << "Updating list of sites with overlaps." << std::endl;
        sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance); // Moved glycans may clash with other glycans. Need to check.
        if (sites_with_overlaps.size() == 0)
        {
            std::cout << "Stopping with all overlaps resolved.\n";
            stop = true;
        }

        new_global_overlap = glycoprotein_builder::GetGlobalOverlap(glycosites);
//        std::cout << "Lowest: " << lowest_global_overlap << ", Current: " << new_global_overlap << "\n";
        if ( lowest_global_overlap > new_global_overlap + 1 )
        {
            write_pdb_file(glycosites.at(0).GetGlycoprotein(), cycle, "best", new_global_overlap);
            lowest_global_overlap = new_global_overlap;
        }
    }
    std::cout << "Global overlap before deleting sites is " << glycoprotein_builder::GetGlobalOverlap(glycosites) << "\n";
    std::cout << "Finished torsions and overlaps:\n";
    glycoprotein_builder::PrintDihedralAnglesAndOverlapOfGlycosites(glycosites);
    DeleteSitesIterativelyWithOverlapAboveTolerance(glycosites, loose_tolerance);
}

void resolve_overlaps::weighted_protein_global_overlap_monte_carlo(GlycosylationSiteVector &glycosites, int max_cycles)
{
    bool accept_change;
    int cycle = 1;
    bool stop = false;
    double previous_chi1;
    double previous_chi2;
    double previous_glycan_overlap, new_glycan_overlap, previous_protein_overlap, new_protein_overlap;
    double lowest_global_overlap = glycoprotein_builder::GetGlobalOverlap(glycosites);
    double new_global_overlap;
    double strict_tolerance = 0.1, loose_tolerance = 1.0;

    GlycosylationSitePointerVector sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance, "total");

    std::cout << "Initial torsions and overlaps:\n";
    glycoprotein_builder::PrintDihedralAnglesAndOverlapOfGlycosites(glycosites);
    while ( (cycle < max_cycles) && (stop == false) )
    {
        ++cycle;
        std::cout << "Cycle " << cycle << " of " << max_cycles << std::endl;
        std::random_shuffle (sites_with_overlaps.begin(), sites_with_overlaps.end());
        for(GlycosylationSitePointerVector::iterator it1 = sites_with_overlaps.begin(); it1 != sites_with_overlaps.end(); ++it1)
        {
            GlycosylationSite *current_glycosite = (*it1);
           // std::cout << "Checking " << current_glycosite->GetResidue()->GetId() << "\n";
            previous_glycan_overlap = current_glycosite->GetGlycanOverlap();
            previous_protein_overlap = current_glycosite->GetProteinOverlap();
            previous_chi1 = current_glycosite->GetChi1Value();
            current_glycosite->SetChi1Value(RandomAngle_360range());
            previous_chi2 = current_glycosite->GetChi2Value();
            current_glycosite->SetChi2Value(RandomAngle_360range());
            new_glycan_overlap = current_glycosite->Calculate_bead_overlaps_noRecord_noSet("glycan");
            new_protein_overlap = current_glycosite->Calculate_bead_overlaps_noRecord_noSet("protein");


            accept_change = monte_carlo::accept_via_metropolis_criterion((new_glycan_overlap + (new_protein_overlap*5)) - (previous_glycan_overlap + (previous_protein_overlap*5)));
            if (!accept_change)
            {
                current_glycosite->SetChi1Value(previous_chi1);
                current_glycosite->SetChi2Value(previous_chi2);
            }
//            else
//            {
//              //  std::cout << "Accepted a change of " << ((new_overlap) - (previous_overlap)) << "\n";
//            }
        }
        //std::cout << "Updating list of sites with overlaps." << std::endl;
        sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance); // Moved glycans may clash with other glycans. Need to check.
        if (sites_with_overlaps.size() == 0)
        {
            std::cout << "Stopping with all overlaps resolved.\n";
            stop = true;
        }

        new_global_overlap = glycoprotein_builder::GetGlobalOverlap(glycosites);
//        std::cout << "Lowest: " << lowest_global_overlap << ", Current: " << new_global_overlap << "\n";
        if ( lowest_global_overlap > new_global_overlap + 1 )
        {
            write_pdb_file(glycosites.at(0).GetGlycoprotein(), cycle, "best", new_global_overlap);
            lowest_global_overlap = new_global_overlap;
        }
    }
//    std::cout << "Global overlap before deleting sites is " << glycoprotein_builder::GetGlobalOverlap(glycosites) << "\n";
//    std::cout << "Finished torsions and overlaps:\n";
//    glycoprotein_builder::PrintDihedralAnglesAndOverlapOfGlycosites(glycosites);
    //DeleteSitesIterativelyWithOverlapAboveTolerance(glycosites, loose_tolerance);
}

void resolve_overlaps::Resolve_Overlaps_Random_Walk_Scaled_To_Overlap(GlycosylationSiteVector &glycosites, std::string type, int max_cycles, double strict_tolerance, double loose_tolerance)
{
    //double strict_tolerance = 0.1, loose_tolerance = 1.0; // Aim for <0.1 when resolving, but keep any less than 1 when culling.
    GlycosylationSitePointerVector sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance, type);
    Overlap_Weighted_Adjust_Torsions_For_X_Cycles(sites_with_overlaps, glycosites, max_cycles, strict_tolerance, type);
    DeleteSitesWithOverlapRecordsAboveTolerance(glycosites, loose_tolerance, type);
    sites_with_overlaps = DetermineSitesWithOverlap(glycosites, strict_tolerance, type);
    SetBestChi1Chi2(sites_with_overlaps, type);
}

void resolve_overlaps::protein_first_random_walk_scaled_to_overlap(GlycosylationSiteVector &glycosites)
{
    // NOTE!!! Upon testing, this algorithm fails with densely clustered glycans. It remembers good spots for individual glycans, but they can be in the same place.

    /* Algorithm overview:
     *  Resolve all protein overlap first, reject sites that cannot be resolved.
     *  Calculate protein overlaps, for each site with overlaps
     *        Change chi1 and chi2 values, record values that reduce overlaps
     *  Once finished delete any sites that could not be resolved
     *  Calculate total (protein+glycan) overlaps, for each site with overlaps
     *        Change chi1 and chi2 values, record values that reduce overlaps
     *  Once finished delete any sites that could not be resolved
     */

//    std::cout << "Initial overlaps for all sites\n";
//    std::cout << "      Site        |  Total | Protein | Glycan \n";
//    for(GlycosylationSiteVector::iterator it1 = glycosites.begin(); it1 != glycosites.end(); ++it1)
//    {
//        GlycosylationSite current_glycosite = *it1;
//        current_glycosite.Calculate_and_print_bead_overlaps();
//    }

     Resolve_Overlaps_Random_Walk_Scaled_To_Overlap(glycosites, "protein");

//    std::cout << "Overlaps for all sites after protein resolution and deletion\n";
//    std::cout << "      Site        |  Total | Protein | Glycan \n";
//    for(GlycosylationSiteVector::iterator it1 = glycosites.begin(); it1 != glycosites.end(); ++it1)
//    {
//        GlycosylationSite current_glycosite = *it1;
//        current_glycosite.Calculate_and_print_bead_overlaps();
//    }

     Resolve_Overlaps_Random_Walk_Scaled_To_Overlap(glycosites, "total");
    // glycoprotein_builder::PrintDihedralAnglesOfGlycosites(glycosites);
    //PrintOverlaps(glycosites);
}


bool resolve_overlaps::dumb_random_walk(GlycosylationSiteVector &glycosites)
{
    /* Algorithm:
     * Determine which sites have overlaps greater than tolerance. Stop if zero sites.
     * For each site with overlaps:
     *        Randomly change all chi1 and chi2 values
     */
    double tolerance = 0.1;
    int cycle = 0, max_cycles = 10;
    GlycosylationSitePointerVector sites_with_overlaps = DetermineSitesWithOverlap(glycosites, tolerance);
    bool resolved = false;

    while ( (cycle < max_cycles) && (resolved == false) )
    {
        ++cycle;
        std::cout << "Cycle " << cycle << " of " << max_cycles << std::endl;
        for(GlycosylationSitePointerVector::iterator it1 = sites_with_overlaps.begin(); it1 != sites_with_overlaps.end(); ++it1)
        {
            GlycosylationSite *current_glycosite = (*it1);
            current_glycosite->SetChi1Value(RandomAngle_360range());
            current_glycosite->SetChi2Value(RandomAngle_360range());
            //double percent_overlap = ((current_glycosite->GetTotalOverlap() / (current_glycosite->GetAttachedGlycan()->GetAllAtomsOfAssembly().size()) ) + 0.01);
            //  new_dihedral_value = Angle_PlusMinusX(current_glycosite->GetChi1Value(), (180 * percent_overlap) ); // scaled to degree of overlap
            //        sites_with_overlaps.erase(std::remove(sites_with_overlaps.begin(), sites_with_overlaps.end(), *it1), sites_with_overlaps.end());
        }
        //std::cout << "Updating list of sites with overlaps." << std::endl;
        sites_with_overlaps = DetermineSitesWithOverlap(glycosites, tolerance); // Moved glycans may clash with other glycans. Need to check.
        if (sites_with_overlaps.size() == 0)
        {
            std::cout << "Stopping with all overlaps resolved.\n";
            resolved = true;
        }
    }
    return resolved;
}


