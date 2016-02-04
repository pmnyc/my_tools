//
//  ConstructDataMembers - construct a data member
//                       to a value other than the default
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int nextStudentId = 1000;
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
  protected:
    int value;
};


class Student
{
  public:
    Student(const char *pName, int ssId)
      : name(pName), id(ssId)
    {
        cout << "constructing student " << pName << endl;
    }
  protected:
    string name;
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
