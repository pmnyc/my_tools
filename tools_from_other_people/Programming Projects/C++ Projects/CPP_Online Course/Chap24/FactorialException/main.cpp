//
//  FactorialException - demonstrate exceptions using
//                       a factorial function
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// factorial - compute factorial
int factorial(int n) throw (string)
{
    // you can't handle negative values of n;
    // better check for that condition first
    if (n < 0)
    {
        throw string("Argument for factorial negative");
    }

    // go ahead and calculate factorial
    int accum = 1;
    while(n > 0)
    {
        accum *= n;
        n--;
    }
    return accum;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    try
    {
        // this will work
        cout << "Factorial of 3 is "
             << factorial(3) << endl;

        // this will generate an exception
        cout << "Factorial of -1 is "
             << factorial(-1) << endl;

        // control will never get here
        cout << "Factorial of 5 is "
             << factorial(5) << endl;
    }
    // control passes here
    catch(string error)
    {
        cout << "Error occurred: " << error << endl;
    }
    catch(...)
    {
        cout << "Default catch " << endl;
    }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

