//
//  DestructMembers - this program both constructs and
//                    destructs a set of data members
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Course
{
  public:
    Course()  { cout << "constructing course" << endl; }
    ~Course() { cout << "destructing course" << endl;  }
};

class Student
{
  public:
    Student() { cout << "constructing student" << endl;}
    ~Student() { cout << "destructing student" << endl; }
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
        pC = new Course;
    }
    ~Teacher()
    {
        cout << "destructing teacher" << endl;
        delete pC;
    }
  protected:
    Course* pC;
};
class TutorPair
{
  public:
    TutorPair(){cout << "constructing tutorpair" << endl;}
   ~TutorPair(){cout << "destructing tutorpair" << endl; }
  protected:
    Student student;
    Teacher teacher;
};

TutorPair* fn()
{
    cout << "Creating TutorPair object in function fn()"
         << endl;
    TutorPair tp;

    cout << "Allocating TutorPair off the heap" << endl;
    TutorPair*  pTP = new TutorPair;

    cout << "Returning from fn()" << endl;
    return pTP;
}


int main(int nNumberofArgs, char* pszArgs[])
{
    // call function fn() and then return the
    // TutorPair object returned to the heap
    TutorPair* pTPReturned = fn();
    cout << "Return heap object to the heap" << endl;
    delete pTPReturned;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
