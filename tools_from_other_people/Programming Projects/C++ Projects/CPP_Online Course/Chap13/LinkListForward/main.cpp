// LinkedListForward - a linked list that links new
//                     objects to the end of the list
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string.h>
#define nullptr 0  // required for pre-'09 compilers

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
NameDataSet* pHead = nullptr;

// add - add a new member to the linked list
//       (this version adds new members to the end of
//       the list)
void add(NameDataSet* pNDS)
{
    // make sure that our link pointer is null (since
    // we are about to become the last member)
    pNDS->pNext = nullptr;

    // if the list is empty..
    if (!pHead)
    {
        // ...make us the first (and only guy in
        // the list and call it a day)
        pHead = pNDS;
        return;
    }

    // ...otherwise, link to the last guy in the list
    NameDataSet* pIter = pHead;
    while(pIter->pNext)
    {
        pIter = pIter->pNext;
    }

    // now make that last guy point to us
    pIter->pNext = pNDS;
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
        return nullptr;
    }

    // get a new entry and fill in values
    NameDataSet* pNDS = new NameDataSet;
    pNDS->sName = name;
    pNDS->pNext = nullptr; // zero link

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
