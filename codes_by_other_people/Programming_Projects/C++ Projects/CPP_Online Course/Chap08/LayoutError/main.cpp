// LayoutError - demonstrate the results of
//               messing up a pointer
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    int    above = 0;
    int    n     = 0;
    int    below = 0;

    // output the values of the three variables before...
    cout << "The initial values are" << endl;
    cout << "above = " << above << endl;
    cout << "n     = " << n     << endl;
    cout << "below = " << below << endl;

    // now store a double into the space
    // allocated for an int
    cout << "\nStoring 13.33 into the location &n" <<endl;
    double* pD = (double*)&n;
    *pD = 13.33;

    // display the results
    cout << "\nThe final results are:" << endl;
    cout << "above = " << above << endl;
    cout << "n     = " << n     << endl;
    cout << "below = " << below << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
