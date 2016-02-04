// LinkedListClass -linked list example with class methods
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// NameDataSet - stores a person's name (these objects
//               could easily store any other information
//               desired).
class NameDataSet
{
  public:
    NameDataSet(string& refName)
      : sName(refName), pNext(0) {}

    // add self to beginning of list
    void add()
    {
        pNext = pHead;
        pHead = this;
    }

    // access methods
    static NameDataSet* first() { return pHead; }
           NameDataSet* next()  { return pNext; }
          const string& name()  { return sName; }
  protected:
    string sName;

    // the link to the first and next member of list
    static NameDataSet* pHead;
    NameDataSet* pNext;
};

// allocate space for the head pointer
NameDataSet* NameDataSet::pHead = 0;

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
        return 0;
    }

    // otherwise, return an object with that name
    return new NameDataSet(name);
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
        pNDS->add();
    }

    // to display the objects, iterate through the
    // list (stop when the next address is NULL)
    cout << "\nEntries:" << endl;
    for(NameDataSet *pIter = NameDataSet::first();
        pIter;
        pIter = pIter->next())
    {
        // display name of current entry
        cout << pIter->name() << endl;
   }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
