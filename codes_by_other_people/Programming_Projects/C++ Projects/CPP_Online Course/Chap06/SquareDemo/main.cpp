// SquareDemo - demonstrate the use of a function
//              which processes arguments

#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// square - returns the square of its argument
//          doubleVar - the value to be squared
//          returns - square of doubleVar
double square(double doubleVar)
{
    return doubleVar * doubleVar;
}

// displayExplanation - prompt the user as to the rules
//                      of the game
void displayExplanation(void)
{
    cout << "This program sums the square of multiple\n"
         << "series of numbers. Terminate each sequence\n"
         << "by entering a negative number.\n"
         << "Terminate the series by entering an\n"
         << "empty sequence.\n"
         << endl;
    return;
}


// sumSquareSequence - accumulate the square of the number
//               entered at the keyboard into a sequence
//               until the user enters a negative number
double sumSquareSequence(void)
{
    // loop forever
    double accumulator = 0.0;
    for(;;)
    {
        // fetch another number
        double dValue = 0;
        cout << "Enter next number: ";
        cin  >> dValue;

        // if it's negative...

        if (dValue < 0)
        {
            // ...then exit from the loop
            break;
        }

        // ...otherwise calculate the square
        double value = square(dValue);

        // now add the square to the
        // accumulator
        accumulator += value;
    }

    // return the accumulated value
    return accumulator;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    displayExplanation();

    // Continue to accumulate numbers...
    for(;;)
    {
        // sum a sequence of numbers entered from
        // the keyboard
        cout << "Enter next sequence" << endl;
        double accumulatedValue = sumSquareSequence();

        // terminate if the sequence is zero or negative
        if (accumulatedValue <= 0.0)
        {
            break;
        }

        // now output the accumulated result
        cout << "\nThe total of the values squared is "
             << accumulatedValue
             << "\n"
             << endl;
    }

    cout << "Thank you" << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
