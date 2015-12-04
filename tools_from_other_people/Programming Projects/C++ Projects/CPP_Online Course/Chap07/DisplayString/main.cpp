// DisplayString - output a character array to
//                 standard output, the MS-DOS window
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// prototype declarations
void displayString(char stringArray[]);

int main(int nNumberofArgs, char* pszArgs[])
{
    char charMyName[] =
              {'S', 't', 'e', 'p', 'h', 'e', 'n', '\0'};
    displayString(charMyName);
    cout << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// displayString - display a character string
//                 one character at a time
void displayString(char stringArray[])
{
    for(int i = 0; stringArray[i] != '\0'; i++)
    {
        cout << stringArray[i];
    }
}

