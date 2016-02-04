// ArrayOfStudents - define an array of student objects
//                   and access an element in it. This
//                   program doesn't do anything
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student
{
  public:
    int  semesterHours;
    float gpa;
    float addCourse(int hours, float grade){return 0.0;}
};

void someFn()
{
    // declare an array of 10 students
    Student s[10];

    // assign the 5th student a gpa of 4.0 (lucky guy)
    s[4].gpa = 4.0;
    s[4].semesterHours = 32;

    // add another course to the 5th student;
    // this time he failed - serves him right
    s[4].addCourse(3, 0.0);
}

int main(int nNumberofArgs, char* pszArgs[])
{
    someFn();
    system("PAUSE");
    return 0;
}

