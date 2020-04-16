#ifndef OVERLAP_RECORD_H
#define OVERLAP_RECORD_H


class Overlap_record
{
public:
    //////////////////////////////////////////////////////////
    //                       CONSTRUCTOR                    //
    //////////////////////////////////////////////////////////
    Overlap_record();
    Overlap_record(double overlap, double chi1, double chi2);

    double GetOverlap();
    double GetChi1();
    double GetChi2();

    void SetOverlap(double overlap);
    void SetChi1(double chi1);
    void SetChi2(double chi2);

private:
    double overlap_;
    double chi1_;
    double chi2_;
};

#endif // OVERLAP_RECORD_H
