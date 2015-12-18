// NestedDemo - input a series of numbers.
//              Continue to accumulate the sum
//              of these numbers until the user
//              enters a 0. Repeat the process
//              until the sum is 0.
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    // the outer loop
    cout << "This program sums multiple series\n"
         << "of numbers. Terminate each sequence\n"
         << "by entering a negative number.\n"
         << "Terminate the series by entering two\n"
         << "negative numbers in a row\n";

    // continue to accumulate sequences
    int accumulator;
    for(;;)
    {
        // start entering the next sequence
        // of numbers
        accumulator = 0;
        cout << "Start the next sequence\n";

        // loop forever
        for(;;)
        {
            // fetch another number
            int nValue = 0;
            cout << "Enter next number: ";
            cin  >> nValue;

            // if it's negative...
            if (nValue < 0)
            {
                // ...then exit
                break;
            }

            // ...otherwise add the number to the
            // accumulator
            accumulator += nValue;
        }

        // exit the loop if the total accumulated is 0
        if (accumulator == 0)
        {
            break;
        }

        // output the accumulated result and start over
        cout << "The total for this sequence is "
            << accumulator
            << endl << endl;
    }

    // we're about to quit
    cout << "Thank you" << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
