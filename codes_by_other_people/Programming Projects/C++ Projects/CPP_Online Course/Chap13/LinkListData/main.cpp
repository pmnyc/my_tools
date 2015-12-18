// LinkedListData - store data in a linked list of objects
#include <cstdio>
#include <cstdlib>
#include <iostream>
#define NULLPTR 0   // use nullptr when supported

using namespace std;

// NameDataSet - stores a person's name (these objects
//               could easily store any other information
//               desired).
class NameDataSet
{
  public:
    string sName;

    // the link to the next entry in the list
    NameDataSet* pNext;
};

// the pointer to the first entry in the list
NameDataSet* pHead = NULLPTR;

// add - add a new member to the linked list
void add(NameDataSet* pNDS)
{
    // point the current entry to the beginning of
    // the list
    pNDS->pNext = pHead;

    // point the head pointer to the current entry
    pHead = pNDS;
}

// getData - read a name and social security
//           number; return null if no more to
//           read
NameDataSet* getData()
{
    // read the first name
    string name;
    cout << "Enter name:";
    cin  >> name;

    // if the name entered is 'exit'...
    if (name == "exit")
    {
        // ...return a null to terminate input
        return NULLPTR;
    }

    // get a new entry and fill in values
    NameDataSet* pNDS = new NameDataSet;
    pNDS->sName = name;
    pNDS->pNext = NULLPTR; // zero link

    // return the address of the object created
    return pNDS;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    cout << "Read names of students\n"
         << "Enter 'exit' for first name to exit"
         << endl;

    // create (another) NameDataSet object
    NameDataSet* pNDS;
    while (pNDS = getData())
    {
        // add it to the list of NameDataSet objects
        add(pNDS);
    }

    // to display the objects, iterate through the
    // list (stop when the next address is NULL)
    cout << "\nEntries:" << endl;
    for(NameDataSet *pIter = pHead;
                       pIter; pIter = pIter->pNext)
    {
        // display name of current entry
        cout << pIter->sName << endl;
   }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
