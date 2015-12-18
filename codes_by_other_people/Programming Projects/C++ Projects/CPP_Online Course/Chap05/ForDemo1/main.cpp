// ForDemo1 - input a loop count. Loop while
//           outputting astring arg number of times.
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
    // input the loop count
    int nLoopCount;
    cout << "Enter loop count: ";
    cin  >> nLoopCount;

    // count up to the loop count limit
    for (; nLoopCount > 0;)
    {
        nLoopCount = nLoopCount - 1;
        cout << "Only " << nLoopCount
             << " loops to go" << endl;
    }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

