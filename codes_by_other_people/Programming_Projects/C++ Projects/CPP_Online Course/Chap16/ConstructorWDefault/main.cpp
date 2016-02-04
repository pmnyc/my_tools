//
//  ConstructorWDefaults - multiple constructors can often
//                         be combined with the definition
//                         of default arguments
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Student

{
  public:
    Student(const char *pName  = "No Name",
            int xfrHours = 0,
            float xfrGPA = 0.0)
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
