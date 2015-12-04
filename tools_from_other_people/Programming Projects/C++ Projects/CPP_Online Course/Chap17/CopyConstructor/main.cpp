//
//  CopyConstructor - demonstrate a copy constructor
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    // conventional constructor
    Student(const char *pName = "no name", int ssId = 0)
      : name(pName), id(ssId)
    {
        cout << "Constructed "  << name << endl;
    }

    // copy constructor
    Student(Student& s)
      : name("Copy of " + s.name), id(s.id)
    {
        cout << "Constructed "  << name << endl;
    }

    ~Student()
    {
        cout << "Destructing " << name << endl;
    }

  protected:
    string name;
    int  id;
};

// fn - receives its argument by value
void fn(Student copy)
{
    cout << "In function fn()" << endl;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    Student chester("Chester", 1234);
    cout << "Calling fn()" << endl;
    fn(chester);
    cout << "Back in main()" << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
