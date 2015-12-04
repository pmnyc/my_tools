//
//  ConstructorWArg - a class may pass along arguments
//                    to the members' constructors
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    Student(const char* pName)
    {
        cout << "constructing Student " << pName << endl;
        name = pName;
        semesterHours = 0;
        gpa = 0.0;
    }

  // ...other public members...
  protected:
    string  name;
    int     semesterHours;
    float   gpa;
};

int main(int argcs, char* pArgs[])
{
    // create a student locally and one off of the heap
    Student s1("Chester");
    Student* pS2 = new Student("Trude");

    // be sure to delete the heap student
    delete pS2;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

