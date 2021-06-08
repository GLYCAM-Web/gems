#ifndef GLYCOPROTEIN_BUILDER_H
#define GLYCOPROTEIN_BUILDER_H

#include <string>
#include <dirent.h>
//#include <unistd.h>
#include <sys/stat.h>
//#include <sys/types.h>
//#include <stdlib.h>     /* getenv */
//#include <fstream>      // std::ifstream
#include "io.h"
#include "glycosylationsite.h"
#include "bead_residues.h"

typedef std::vector<GlycosylationSite> GlycosylationSiteVector;
typedef std::vector<GlycosylationSite*> GlycosylationSitePointerVector;

namespace glycoprotein_builder
{
/*******************************************/
/* Function Declarations                   */
/*******************************************/
void Read_Input_File(GlycosylationSiteVector &glycosites, std::string &proteinPDB, std::string &glycanDirectory, const std::string working_Directory);
void AttachGlycansToGlycosites(MolecularModeling::Assembly &glycoprotein, GlycosylationSiteVector &glycosites, const std::string glycanDirectory);
void PrintDihedralAnglesAndOverlapOfGlycosites(GlycosylationSiteVector &glycosites);
void SetReasonableChi1Chi2Values(GlycosylationSiteVector &glycosites);
void SetRandomChi1Chi2Values(GlycosylationSiteVector &glycosites);
void CalculateOverlaps(GlycosylationSiteVector &glycosites);
double GetGlobalOverlap(GlycosylationSiteVector &glycosites);
double RandomAngle_360range();
double RandomAngle_range(int min, int max);
double RandomAngle_PlusMinusX(double start_point, int max_step_size);
double GetNewAngleScaledToDegreeOfOverlap(double current_angle, double overlap, int number_of_atoms);
void write_pdb_file(Assembly *glycoprotein, int cycle, std::string summary_filename, double score);
void PrintOverlaps(GlycosylationSiteVector &glycosites);
void PrintOverlaps(GlycosylationSitePointerVector &glycosites);
void CalculateAndPrintOverlaps(GlycosylationSiteVector &glycosites);
void SetBestChi1Chi2(GlycosylationSitePointerVector &glycosites, std::string overlap_type = "total");
GlycosylationSitePointerVector DetermineSitesWithOverlap(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type = "total");
GlycosylationSitePointerVector GetSitesWithOverlap(GlycosylationSiteVector &glycosites, double tolerance);
GlycosylationSitePointerVector DeleteSitesWithOverlaps(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type = "total");
void DeleteSitesWithOverlapRecordsAboveTolerance(GlycosylationSiteVector &glycosites, double tolerance, std::string overlap_type = "total");
void DeleteSitesIterativelyWithOverlapAboveTolerance(GlycosylationSiteVector &glycosites, double tolerance);
void Overlap_Weighted_Adjust_Torsions_For_X_Cycles(GlycosylationSitePointerVector &sites, GlycosylationSiteVector &glycosites, int max_cycles, double tolerance, std::string overlap_type);
void Overlap_Weighted_Adjust_Torsions(GlycosylationSitePointerVector &sites);
}

#endif // GLYCOPROTEIN_BUILDER_H
