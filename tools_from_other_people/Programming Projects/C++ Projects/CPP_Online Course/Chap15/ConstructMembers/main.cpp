//
//  ConstructMembers - the member objects of a class
//                     are each constructed before the
//                     container class constructor gets
//                     a shot at it
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Course
{
  public:
    Course()
    {
        cout << "constructing course" << endl;
    }
};

class Student
{
  public:
    Student()
    {
        cout << "constructing student" << endl;
        semesterHours = 0;
        gpa = 0.0;
    }
  protected:
    int  semesterHours;
    float gpa;
};
class Teacher
{
  public:
    Teacher()
    {
        cout << "constructing teacher" << endl;
    }
  protected:
    Course c;
};
class TutorPair
{
  public:
    TutorPair()
    {
        cout << "constructing tutorpair" << endl;
        noMeetings = 0;
    }
  protected:
    Student student;
    Teacher teacher;
    int   noMeetings;
};

int main(int nNumberofArgs, char* pszArgs[])
{
    cout << "Creating TutorPair object" << endl;
    TutorPair tp;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
