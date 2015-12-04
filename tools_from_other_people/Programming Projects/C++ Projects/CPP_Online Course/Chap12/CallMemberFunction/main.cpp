//
//  CallMemberFunction - define and invoke a function
//               that's a member of the class Student
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    // add a completed course to the record
    float addCourse(int hours, float grade)
    {
        // calculate the sum of all courses times
        // the average grade
        float weightedGPA;
        weightedGPA = semesterHours * gpa;

        // now add in the new course
        semesterHours += hours;
        weightedGPA += grade * hours;
        gpa = weightedGPA / semesterHours;

        // return the new gpa
        return gpa;
    }

    int  semesterHours;
    float gpa;
};

int main(int nNumberofArgs, char* pszArgs[])
{
    // create a Student object and initialize it
    Student s;
    s.semesterHours = 3;
    s.gpa = 3.0;

    // the values before the call
    cout << "Before: s = (" << s.semesterHours
         << ", "    << s. gpa
         << ")" << endl;

    // the following subjects the data members of the s
    // object to the member function addCourse()
    cout << "Adding 3 hours with a grade of 4.0" << endl;
    s.addCourse(3, 4.0); // call the member function

    // the values are now changed
    cout << "After: s = (" << s.semesterHours
         << ", "    << s. gpa
         << ")"     << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
