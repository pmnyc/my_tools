// VariableSize - output the size of each type of
//                variable
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    bool        b;
    char        c;
    int         n;
    long        l;
    long long   ll;
    float       f;
    double      d;
    long double ld;

    cout << "sizeof a bool        = " << sizeof b << endl;
    cout << "sizeof a char        = " << sizeof c << endl;
    cout << "sizeof an int        = " << sizeof n << endl;
    cout << "sizeof a long        = " << sizeof l << endl;
    cout << "sizeof a long long   = " << sizeof ll<< endl;
    cout << "sizeof a float       = " << sizeof f << endl;
    cout << "sizeof a double      = " << sizeof d << endl;
    cout << "sizeof a long double = " << sizeof ld<< endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

