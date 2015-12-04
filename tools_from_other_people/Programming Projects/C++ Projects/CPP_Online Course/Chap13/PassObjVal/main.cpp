// PassObjVal - attempts to change the value of an object
//              in a function fail when the object is
//              passed by value
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    int  semesterHours;
    float gpa;
};

void someFn(Student copyS)
{
    copyS.semesterHours = 10;
    copyS.gpa           = 3.0;
    cout << "The value of copyS.gpa = "
         << copyS.gpa << endl;
}

int main(int argc, char* pArgs[])
{
    Student s;
    s.gpa = 0.0;

    // display the value of s.gpa before calling someFn()
    cout << "The value of s.gpa = " << s.gpa << endl;

    // pass the address of the existing object
    cout << "Calling someFn(Student)" << endl;
    someFn(s);
    cout << "Returned from someFn(Student)" << endl;

    // the value of s.gpa remains 0
    cout << "The value of s.gpa = " << s.gpa << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
