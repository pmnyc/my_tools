//
//  InheritanceExample - demonstrate an inheritance
//               relationship in which the subclass
//               constructor passes argument information
//               to the constructor in the base class
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;
class Advisor {}; // define an empty class

class Student
{
  public:
    Student(const char *pName = "no name")
       : name(pName), average(0.0), semesterHours(0)
    {
        cout << "Constructing student " << name << endl;
    }

    void addCourse(int hours, float grade)
    {
        cout << "Adding grade to " << name << endl;
        average = semesterHours * average + grade;
        semesterHours += hours;
        average = average / semesterHours;
    }

    int hours( ) { return semesterHours;}
    float gpa( ) { return average;}

  protected:
    string name;
    double average;
    int    semesterHours;
};

class GraduateStudent : public Student
{
  public:
    GraduateStudent(const char *pName, Advisor adv,
                    double qG = 0.0)
        : Student(pName), advisor(adv), qualifierGrade(qG)
    {
        cout << "Constructing graduate student "
             << pName << endl;
    }

    double qualifier( ) { return qualifierGrade; }

  protected:
    Advisor advisor;
    double qualifierGrade;
};

int main(int nNumberofArgs, char* pszArgs[])
{
    // create a dummy advisor to give to GraduateStudent
    Advisor adv;

    // create two Student types
    Student llu("Cy N Sense");
    GraduateStudent gs("Matt Madox", adv, 1.5);

    // now add a grade to their grade point average
    llu.addCourse(3, 2.5);
    gs.addCourse(3, 3.0);

    // display the graduate student's qualifier grade
    cout << "Matt's qualifier grade = "
         << gs.qualifier() << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
