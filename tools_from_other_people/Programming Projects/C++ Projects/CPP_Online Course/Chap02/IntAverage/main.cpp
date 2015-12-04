//
//  IntAverage - average 3 numbers using integer arithmetic.
//               First add the sum of each number divided by 3
//               and second divide the sum of the three
//               numbers by 3.
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    int nValue1;
    int nValue2;
    int nValue3;

    // enter three numbers
    cout << "This program averages three numbers using"
         << "integer arithmetic\n\n";
    cout << "Enter three integers:\n";

    cout << "n1 - ";
    cin  >> nValue1;

    cout << "n2 - ";
    cin  >> nValue2;

    cout << "n3 - ";
    cin  >> nValue3;

    // first the sum of three ratios
    cout << "n1/3 + n2/3 + n3/3 = ";
    cout << nValue1/3 + nValue2/3 + nValue3/3;
    cout << "\n";

    // now the ratio of three sums
    cout << "(n1 + n2 + n3)/3   = ";
    cout << (nValue1 + nValue2 + nValue3) / 3;
    cout << "\n";

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
