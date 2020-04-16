#include "../includes/overlap_record.h"

//////////////////////////////////////////////////////////
//                       CONSTRUCTOR                    //
//////////////////////////////////////////////////////////

Overlap_record::Overlap_record()
{
    SetOverlap(123456789.0);
    SetChi1(0.0);
    SetChi2(0.0);
}

Overlap_record::Overlap_record(double overlap, double chi1, double chi2)
{
    SetOverlap(overlap);
    SetChi1(chi1);
    SetChi2(chi2);
}

//////////////////////////////////////////////////////////
//                       ACCESSOR                       //
//////////////////////////////////////////////////////////

double Overlap_record::GetOverlap()
{
    return overlap_;
}

double Overlap_record::GetChi1()
{
    return chi1_;
}
double Overlap_record::GetChi2()
{
    return chi2_;
}

//////////////////////////////////////////////////////////
//                       MUTATOR                        //
//////////////////////////////////////////////////////////

void Overlap_record::SetOverlap(double overlap)
{
    overlap_ = overlap;
}

void Overlap_record::SetChi1(double chi1)
{
    chi1_ = chi1;
}

void Overlap_record::SetChi2(double chi2)
{
    chi2_ = chi2;
}
