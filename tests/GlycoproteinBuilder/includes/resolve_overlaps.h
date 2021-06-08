#ifndef RESOLVE_OVERLAPS_H
#define RESOLVE_OVERLAPS_H

#include <iostream>
#include <cstdlib>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <algorithm> // For erase remove and shuffle
#include <iomanip>
#include <cmath>
#include <ctime>
#include <cstring>

#include "bead_residues.h"
#include "glycosylationsite.h"
#include "glycoprotein_builder.h"
#include "metropolis_criterion.h"


namespace resolve_overlaps
{
void weighted_protein_global_overlap_random_descent(GlycosylationSiteVector &glycosites, int max_cycles = 500);
void weighted_protein_global_overlap_monte_carlo(GlycosylationSiteVector &glycosites, int max_cycles = 500);
void Resolve_Overlaps_Random_Walk_Scaled_To_Overlap(GlycosylationSiteVector &glycosites, std::string type = "protein", int max_cycles = 500, double strict_tolerance = 0.1, double loose_tolerance = 1.0);
void protein_first_random_walk_scaled_to_overlap(GlycosylationSiteVector &glycosites);
bool dumb_random_walk(GlycosylationSiteVector &glycosites);
}

#endif // RESOLVE_OVERLAPS_H
