// CharDisplay - output a character array to
//               standard output, the MS-DOS window
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// prototype declarations
void displayCharArray(char charArray[],
                      int sizeOfArray);

int main(int nNumberofArgs, char* pszArgs[])
{
    char charMyName[] = {'S', 't', 'e', 'p', 'h', 'e', 'n'};
    displayCharArray(charMyName, 7);
    cout << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// displayCharArray - display an array of characters
//                    by outputing one character at
//                    a time
void displayCharArray(char charArray[],
                      int sizeOfArray)
{
    for(int i = 0; i< sizeOfArray; i++)
    {
        cout << charArray[i];
    }
}

