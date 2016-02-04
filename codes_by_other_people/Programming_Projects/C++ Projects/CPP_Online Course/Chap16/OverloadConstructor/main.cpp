//
//  OverloadConstructor - provide the class multiple
//                        ways to create objects by
//                        overloading the constructor
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string.h>

using namespace std;
class Student
{
  public:
    Student()
    {
        cout << "constructing student No Name" << endl;
        name = "No Name";
        semesterHours = 0;
        gpa = 0.0;
    }
    Student(const char *pName)
    {
        cout << "constructing student " << pName << endl;
        name = pName;
        semesterHours = 0;
        gpa = 0;
    }
    Student(const char *pName, int xfrHours, float xfrGPA)
    {
        cout << "constructing student " << pName << endl;
        name = pName;
        semesterHours = xfrHours;
        gpa = xfrGPA;
    }

  protected:
    string  name;
    int     semesterHours;
    float   gpa;
};

int main(int argcs, char* pArgs[])
{
    // the following invokes three different constructors
    Student noName;
    Student freshman("Marian Haste");
    Student xferStudent("Pikumup Andropov", 80, 2.5);

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
