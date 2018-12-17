#ifndef GLYCOSYLATIONSITE_H
#define GLYCOSYLATIONSITE_H

#include "gmml.hpp"
#include "overlap_record.h"
#include <iomanip> // For setting precision and formating in std::cout 
#include <algorithm> //  std::erase, std::remove

using namespace MolecularModeling;

class GlycosylationSite
{
public:
    //////////////////////////////////////////////////////////
    //                    TYPE DEFINITION                   //
    //////////////////////////////////////////////////////////

    typedef std::vector<GlycosylationSite> GlycosylationSiteVector;
    typedef std::vector<GlycosylationSite*> GlycosylationSitePointerVector;
    typedef std::vector<Overlap_record> OverlapRecordVector;

    //////////////////////////////////////////////////////////
    //                       CONSTRUCTOR                    //
    //////////////////////////////////////////////////////////

    GlycosylationSite();
    GlycosylationSite(std::string glycan_name);
    GlycosylationSite(std::string glycan_name, std::string residue_number);
    //GlycosylationSite(std::string glycan_name, std::string residue_number_, Assembly glycan, Residue* residue);
    ~GlycosylationSite();
    //////////////////////////////////////////////////////////
    //                       ACCESSOR                       //
    //////////////////////////////////////////////////////////

    std::string GetGlycanName();
    std::string GetResidueNumber();
    Residue* GetResidue();
    Assembly* GetAttachedGlycan();
    Assembly* GetGlycoprotein();
    double GetOverlap();
    double GetWeightedOverlap(double glycan_weight, double protein_weight);
    double GetGlycanOverlap();
    double GetProteinOverlap();
    double GetChi1Value();
    double GetChi2Value();
    AtomVector GetSelfGlycanBeads();
    AtomVector GetProteinBeads();
    AtomVector GetOtherGlycanBeads();
    Overlap_record GetBestOverlapRecord(std::string overlap_type = "total");


    //////////////////////////////////////////////////////////
    //                       FUNCTIONS                      //
    //////////////////////////////////////////////////////////
    void AttachGlycan(Assembly glycan, Assembly &glycoprotein);
    double Calculate_bead_overlaps(std::string overlap_type = "total");
    double Calculate_bead_overlaps_noRecord_noSet(std::string overlap_type = "total");
    double Calculate_and_print_bead_overlaps();
    void SetChiAtoms(Residue* residue);

    //////////////////////////////////////////////////////////
    //                       MUTATOR                        //
    //////////////////////////////////////////////////////////

    void SetGlycanName(std::string glycan_name);
    void SetResidueNumber(std::string residue_number);
    void SetResidue(Residue* residue);
    void SetGlycan(Assembly glycan);
    void SetGlycanOverlap(double overlap);
    void SetProteinOverlap(double overlap);
    void SetChi1Value(double angle);
    void SetChi2Value(double angle);
    void SetSelfGlycanBeads(AtomVector *beads);
    void SetProteinBeads(AtomVector *beads);
    void SetOtherGlycanBeads(AtomVector *beads);
    void SetBestOverlapRecord(double overlap, double chi1, double chi2, std::string overlap_type = "total");

    //////////////////////////////////////////////////////////
    //                       DISPLAY FUNCTION               //
    //////////////////////////////////////////////////////////

    void Print_bead_overlaps();

    //////////////////////////////////////////////////////////
    //                       OPERATORS                      //
    //////////////////////////////////////////////////////////

    inline bool operator==(const GlycosylationSite &rhs) const
    {
        return rhs.residue_number_ == residue_number_;
    }

private:

    //////////////////////////////////////////////////////////
    //                       FUNCTIONS                      //
    //////////////////////////////////////////////////////////

    void Prepare_Glycans_For_Superimposition_To_Particular_Residue(std::string amino_acid_name);
    void Superimpose_Glycan_To_Glycosite(Residue *glycosite_residue);
    double CalculateTorsionAngle(AtomVector atoms);
    double Calculate_bead_overlaps(AtomVector &atomsA, AtomVector &atomsB);

    //////////////////////////////////////////////////////////
    //                       ATTRIBUTES                     //
    //////////////////////////////////////////////////////////

    std::string glycan_name_;
    std::string residue_number_;
    Residue* residue_;                                  /*!< A pointer back to the residue for this glycosite >*/
    Assembly glycan_;
    AtomVector superimposition_atoms_;               /*!< The 3 atoms used for superimposition of glycan to sidechain >*/
    double glycan_overlap_;
    double protein_overlap_;
    AtomVector chi1_;
    AtomVector chi2_;
    AtomVector self_glycan_beads_;
    AtomVector other_glycan_beads_;
    AtomVector protein_beads_;
    OverlapRecordVector best_overlap_records_;
    OverlapRecordVector best_protein_overlap_records_;
};

#endif // GLYCOSYLATIONSITE_H
