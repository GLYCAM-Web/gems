#include "../includes/io.h"

bool fileExists(std::string fileName)
{
    std::ifstream infile(fileName);
    return infile.good();
}

std::string SplitFilename (const std::string& str)
{
  //std::cout << "Splitting: " << str << '\n';
  std::size_t found = str.find_last_of("/\\");
//  std::cout << " path: " << str.substr(0,found) << '\n';
//  std::cout << " file: " << str.substr(found+1) << '\n';
  return str.substr(0,found);
}

std::string Find_Program_Installation_Directory()
{
    // A way to get the program name plus working directory
    char processID[32];
    char pBuffer[256];
    size_t len = sizeof(pBuffer);
    sprintf(processID, "/proc/%d/exe", getpid());
    int bytes = MIN(readlink(processID, pBuffer, len), len - 1);
    if(bytes >= 0)
    {
        pBuffer[bytes] = '\0';
        //std::cout << "processID:" << processID << " pBuffer:" << pBuffer << " bytes:" << bytes << std::endl;
        return SplitFilename (pBuffer);
    }
    else
        return "Error";
}

std::string Find_Program_Working_Directory()
{
    char cCurrentPath[FILENAME_MAX];
    if (!GetCurrentDir(cCurrentPath, sizeof(cCurrentPath)))
        return "Error reading working directory";
    cCurrentPath[sizeof(cCurrentPath) - 1] = '\0'; /* not really required */
    //std::cout << "The current working directory is ""," << cCurrentPath << std::endl;
    return cCurrentPath;
}

std::vector<std::string> split(const std::string &s, char delim) 
{
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}


