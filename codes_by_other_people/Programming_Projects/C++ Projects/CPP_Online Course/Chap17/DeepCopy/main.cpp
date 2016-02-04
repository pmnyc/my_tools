//
//  DeepCopy  - demonstrate the principle of creating a
//              deep copy by copying each member in the class
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Person
{
  public:
    Person(const char *pN)
    {
        cout << "Constructing " << pN << endl;
        pName = new string(pN);
    }
    Person(Person& person)
    {
        cout << "Copying " << *(person.pName) << endl;
        pName = new string(*person.pName);
    }
    ~Person()
    {
        cout << "Destructing " << pName
             << " (" << *pName << ")" << endl;
        *pName = "already destructed memory";
        // delete pName;
    }
 protected:
    string *pName;
};

void fn()
{
    // create a new object
    Person p1("This_is_a_very_long_name");

    // copy the contents of p1 into p2
    Person p2(p1);
}

int main(int argcs, char* pArgs[])
{
    cout << "Calling fn()" << endl;
    fn();
    cout << "Back in main()" << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
