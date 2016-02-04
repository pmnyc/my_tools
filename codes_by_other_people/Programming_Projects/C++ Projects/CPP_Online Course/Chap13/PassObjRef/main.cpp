// PassObjRef - change the contents of an object in
//              a function by using a reference
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

// same as before, but this time using references
void someFn(Student& refS)
{
    refS.semesterHours = 10;
    refS.gpa      = 3.0;
    cout << "The value of copyS.gpa = "
         << refS.gpa << endl;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    Student s;
    s.gpa = 0.0;

    // display the value of s.gpa before calling someFn()
    cout << "The value of s.gpa = " << s.gpa  << endl;

    // pass the address of the existing object
    cout << "Calling someFn(Student*)" << endl;
    someFn(s);
    cout << "Returned from someFn(Student&)" << endl;

    // the value of s.gpa is now 3.0
    cout << "The value of s.gpa = " << s.gpa << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
