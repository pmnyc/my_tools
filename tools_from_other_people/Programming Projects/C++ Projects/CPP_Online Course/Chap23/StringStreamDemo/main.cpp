// StringStream - read and parse the contents of a file
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iostream>
using namespace std;

// parseAccountInfo - read a passed buffer as if it were
//               an actual file - read the following
//               format:
//                name, account balance
//               return true if all worked well
bool parseString(const char* pString,
                 char* pName, int arraySize,
                 long& accountNum, double& balance)
{
    // associate an istrstream object with the input
    // character string
    istringstream inp(pString);

    // read up to the comma separator
    inp.getline(pName, arraySize, ',');

    // now the account number
    inp >> accountNum;

    // and the balance
    inp >> balance;

    // return the error status
    return !inp.fail();
}

int main(int nNumberofArgs, char* pszArgs[])
{
    // must provide filename
    char szFileName[128];
    cout << "Input name of file to parse:";
    cin.getline(szFileName, 128);

    // get a file stream
    ifstream* pFileStream = new ifstream(szFileName);
    if (!pFileStream->good())
    {
        cerr << "Can't open " << pszArgs[1] << endl;
        return 0;
    }

    // read a line out of file, parse it and display
    // results
    for(int nLineNum = 1;;nLineNum++)
    {
        // read a buffer
        char buffer[256];
        pFileStream->getline(buffer, 256);
        if (pFileStream->fail())
        {
            break;
        }
        cout << nLineNum << ":" << buffer << endl;

        // parse the individual fields
        char name[80];
        long accountNum;
        double balance;
        bool result = parseString(buffer, name, 80,
                                  accountNum, balance);
        if (result == false)
        {
            cerr << "Error parsing string\n" << endl;
            continue;
        }

        // output the fields we parsed out
        cout << "Read the following fields:" << endl;
        cout << "  name = " << name << "\n"
             << "  account = " << accountNum << "\n"
             << "  balance = " << balance << endl;

        // put the fields back together in a different
        // order (inserting the 'ends' makes sure the
        // buffer is null terminated
        ostringstream out;
        out << name << ", "
            << balance << " "
            << accountNum << ends;

        string oString = out.str();
        cout << "Reordered fields: " << oString << endl;
    }

    system("PAUSE");
    return 0;
}
