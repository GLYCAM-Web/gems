#ifndef METROPOLIS_CRITERION_H
#define METROPOLIS_CRITERION_H

#include <cmath>
#include <stdio.h>

namespace monte_carlo
{

inline double get_random_acceptance_probability()
{
    // I did this when testing and calling multiple times, as time wasn't progressing between calls. So Fast!
    srand ((time(NULL) + rand())); // initialise a random seed for rand(). Otherwise it's always the same.
    //std::cout << (rand() % 100) << "rand()\n";
    double r = (rand() % 100); // get a number between 1 and 100
    return (r / 100); // get it between 0 and 1
}

inline bool accept_via_metropolis_criterion(double change_in_overlap)
{
    bool return_value;
    if (change_in_overlap < 0)
    {
        return_value = true;
    }
    else
    {
        double r = get_random_acceptance_probability();
        double p = exp(-change_in_overlap / 10);
        if (p > r)
        {
            std::cout << "ACCEPTED: " << change_in_overlap << " p: " << p << " r: " << r << "\n";
            return_value = true;
        }
        else
        {
            return_value = false;
        }
      //  std::cout << "p:" << p << ", r:" << r << ", accept = " << return_value << "\n";
    }
    return return_value;
}



} // namespace monte_carlo

#endif // METROPOLIS_CRITERION_H
