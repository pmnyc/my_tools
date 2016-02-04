// MacroConfusion - demonstrate some of the problems with
//         macro definitions and how an inline function
//         has the same effect with no surprises
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// comment out the first macro to expose the next;
// comment out both macros to expose the inline function
#define SQUARE(X) X * X
#ifndef SQUARE
#define SQUARE(X) ((X) * (X))
#ifndef SQUARE
    inline int SQUARE(int X) {return X * X;}
#endif
#endif
int main(int nNumberofArgs, char* pszArgs[])
{
    // try out a simple expression
    int nSQ = SQUARE(2);
    cout << "SQUARE(2) = " << nSQ << endl;

    // here's an error that can be solved with application
    // of parentheses in enough places
    cout << "SQUARE(1 + 2) = " << SQUARE(1 + 2) << endl;

    // here's an error that can't be solved
    int i = 3;
    cout << "i = " << i << endl;
    nSQ = SQUARE(i++);
    cout << "SQUARE(i++) = " << nSQ << endl;
    cout << "now i = " << i << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

