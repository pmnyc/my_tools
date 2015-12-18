// ConcatenateWide - concatenate two wide strings
//     with a " - " in the middle using library routines
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    // read first string...
    wchar_t wszString1[260];
    cout << "Enter string #1:";
    wcin.getline(wszString1, 128);

    // ...now the second string...
    wchar_t wszString2[128];
    cout << "Enter string #2:";
    wcin.getline(wszString2, 128);

    // now tack the second onto the end of the first
    // with a dash in between
    wcsncat(wszString1, L" - ", 260);
    wcsncat(wszString1, wszString2, 260);

    wcout << L"\n" << wszString1 << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
