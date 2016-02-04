// ObjPtr - define and use a pointer to a Student object
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    int  semesterHours;
    float gpa;
    float addCourse(int hours, float grade){return 0.0;};
};

int main(int argc, char* pArgs[])
{
    // create a Student object
    Student s;
    s.gpa = 3.0;

    // now create a pointer pS to a Student object
    Student* pS;

    // make pS point to our Student object
    pS = &s;

    // now ouutput the gpa of the object, once thru
    // the variable name and a second time thru  pS
    cout << "s.gpa   = " << s.gpa   << "\n"
         << "pS->gpa = " << pS->gpa << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
