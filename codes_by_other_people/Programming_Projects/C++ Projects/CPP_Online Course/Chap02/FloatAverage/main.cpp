//
//  FloatAverage - average 3 numbers using floating point arithmetic.
//                 Otherwise, same as IntAverage
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    float fValue1;
    float fValue2;
    float fValue3;

    // enter three numbers
    cout << "This program averages three numbers using "
         << "floating point arithmetic\n\n";
    cout << "Enter three integers:\n";

    cout << "f1 - ";
    cin  >> fValue1;

    cout << "f2 - ";
    cin  >> fValue2;

    cout << "f3 - ";
    cin  >> fValue3;

    // first the sum of three ratios
    cout << "n1/3 + n2/3 + n3/3 = ";
    cout << fValue1/3 + fValue2/3 + fValue3/3;
    cout << "\n";

    // now the ratio of three sums
    cout << "(n1 + n2 + n3)/3   = ";
    cout << (fValue1 + fValue2 + fValue3) / 3;
    cout << "\n";

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
