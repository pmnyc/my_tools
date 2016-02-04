//
//  ConstructSeparateID - failed attempt to init data member
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
        cout << "take next student id " << value << endl;
    }

    // int constructor allows user to assign id
    StudentId(int id)
    {
        value = id;
        cout << "assign student id " << value << endl;
    }
    ~StudentId(){cout << "destructing " << value << endl;}
  protected:
    int value;
};

class Student
{
  public:
    Student(const char *pName, int ssId)
    {
        cout << "constructing student " << pName << endl;
        name = pName;
        // don't try this at home kids. It doesn't work
        StudentId id(ssId);    // construct a student id
    }
  protected:
    string    name;
    StudentId id;
};

int main(int argcs, char* pArgs[])
{
    Student s("Chester", 1234);
    cout << "This message from main" << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
