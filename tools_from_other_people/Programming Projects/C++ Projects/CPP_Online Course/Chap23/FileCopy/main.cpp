// FileCopy - make backup copies of the files passed
//            to the program
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    // repeat the process for every file passed
    for (int n = 1; n < nNumberofArgs; n++)
    {
        // create a filename and a "Copy of " name
        const char* pszSource = pszArgs[n];
        string target = string(pszSource) + ".backup";
        const char* pszTarget = target.c_str();

        // now open the source for reading and the
        // target for writing
        ifstream input(pszSource,
                       ios_base::in|ios_base::binary);

        ofstream output(pszTarget,
          ios_base::out|ios_base::binary|ios_base::trunc);
        if (input.good() && output.good())
        {
            cout << "Copying " << pszSource << "...";

            // read and write 4k blocks until either an
            // error occurs or the file reaches EOF
            while(!input.eof() && input.good())
            {
                char buffer[4096];
                input.read(buffer, 4096);
                output.write(buffer, input.gcount());
            }
            cout << "finished" << endl;
        }
        else
        {
            cerr << "Couldn't copy " << pszSource << endl;
        }
    }

    system("PAUSE");
    return 0;
}
