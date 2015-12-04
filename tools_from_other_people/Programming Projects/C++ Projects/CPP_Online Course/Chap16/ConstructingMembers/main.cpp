//
//  ConstructingMembers - a class may pass along arguments
//                        to the members' constructors
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int nextStudentId = 1000; // first legal Student ID
class StudentId
{
  public:
    // default constructor assigns id's sequentially
    StudentId()
    {
        value = nextStudentId++;
        cout << "Take next student id " << value << endl;
    }

    // int constructor allows user to assign id
    StudentId(int id)
    {
        value = id;
        cout << "Assign student id " << value << endl;
    }
  protected:
    int value;
};

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
    string    name;
    int       semesterHours;
    float     gpa;
    StudentId id;
};

int main(int argcs, char* pArgs[])
{
    // create a couple of students
    Student s1("Chester");
    Student s2("Trude");

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
