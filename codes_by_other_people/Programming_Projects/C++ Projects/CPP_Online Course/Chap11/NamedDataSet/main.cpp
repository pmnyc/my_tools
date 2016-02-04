// NamedDataSet - store associated data in
//                an array of objects
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string.h>
using namespace std;

// NameDataSet - stores name and credit card
//               information
class NameDataSet
{
  public:
    char firstName[128];
    char lastName[128];
    int  creditCard;
};

int main(int nNumberofArgs, char* pszArgs[])
{
    // allocate space for 25 name data sets
    const int MAX = 25;
    NameDataSet nds[MAX];

    // load first names, last names and social
    // security numbers
    cout << "Read name/credit card information\n"
         << "Enter 'exit' to quit" << endl;
    int index = 0;
    for(;index < MAX; index++)
    {
        cout << "\nEnter first name:";
        cin  >> nds[index].firstName;

        // break if the first name entered is "exit"
        if (strcmp(nds[index].firstName, "exit") == 0)
        {
            break;
        }

        cout << "Enter last name:";
        cin  >> nds[index].lastName;

        cout << "Enter credit card number:";
        cin  >>nds[index].creditCard;
    }

    // display the names and numbers entered
    cout << "\nEntries:" << endl;
    for (int i = 0; i < index; i++)
    {
        cout << nds[i].firstName  << " "
             << nds[i].lastName   << "/"
             << nds[i].creditCard << endl;
    }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
