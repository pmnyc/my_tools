// STLListStudents - use a list to contain and sort a
//                   user defined class
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <list>

using namespace std;

// Student - some example user defined class
class Student
{
  public:
    Student(const char* pszS, int id)
      : sName(pszS), ssID(id) {}
    string sName;
    int ssID;
};

// the following function is required to support the
// sort operation
bool operator<(const Student& s1, const Student& s2)
{
    return s1.ssID < s2.ssID;
}

// displayStudents - iterate through the list displaying
//                   each element
void displayStudents(list<Student>& students)
{
    // allocate an iterator that points to the first
    // element in the list
    list<Student>::iterator iter = students.begin();

    // continue to loop through the list until the
    // iterator hits the end of the list
    while(iter != students.end())
    {
        // retrieve the Student the iterator points at
        Student& s = *iter;
        cout << s.ssID << " - " << s.sName << endl;

        // now move the iterator over to the next element
        // in the list
        iter++;
    }
}

int main(int argc, char* pArgs[])
{
    // define a collection of students
    list<Student> students;

    // add three student objects to the list
    students.push_back(Student("Marion Haste", 10));
    students.push_back(Student("Dewie Cheatum", 5));
    students.push_back(Student("Stew Dent", 15));

    // display the list
    cout << "The original list:" << endl;
    displayStudents(students);

    // now sort the list and redisplay
    students.sort();
    cout << "\nThe sorted list:" << endl;
    displayStudents(students);

    system("PAUSE");
    return 0;
}
