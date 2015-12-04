// PassObjPtr - change the contents of an object in
//              a function by passing a pointer to the
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

void someFn(Student* pS)
{
    pS->semesterHours = 10;
    pS->gpa           = 3.0;
    cout << "The value of pS->gpa = "
         << pS->gpa << endl;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    Student s;
    s.gpa = 0.0;

    // display the value of s.gpa before calling someFn()
    cout << "The value of s.gpa = " << s.gpa << endl;

    // pass the address of the existing object
    cout << "Calling someFn(Student*)" << endl;
    someFn(&s);
    cout << "Returned from someFn(Student*)" << endl;

    // the value of s.gpa is now 3.0
    cout << "The value of s.gpa = " << s.gpa << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
