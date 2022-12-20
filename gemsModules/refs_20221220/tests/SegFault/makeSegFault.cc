/* Compile me with:
 *    g++ makeSegFault.cc
 *
 *    From:  https://stackoverflow.com/questions/40317792/handling-segmentation-fault-due-to-a-c-subprocess-spawned-by-python-code
 */
#include <string>
#include <iostream>
int main()
{
int*a;
a=NULL;
std::cout<<*a<<std::endl;
return 0;
}
