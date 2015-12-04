// CascadingException - the following program demonstrates
//              an example of stack unwinding; it also
//              shows how the throw() clause is used in
//              the function declaration
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// prototypes of some functions that we will need later
void f1() throw();
void f2();
void f3() throw(int);

class Obj
{
  public:
    Obj(char c) : label(c)
    { cout << "Constructing object " << label << endl;}
    ~Obj()
    { cout << "Destructing object " << label << endl; }

  protected:
    char label;
};

int main(int nNumberofArgs, char* pszArgs[])
{
    f1();

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// f1 -an empty throw() clause in the declaration of this
//     function means that it does not throw an exception
void f1() throw()
{
    Obj a('a');
    try
    {
        Obj b('b');
        f2();
    }
    catch(float f)
    {
        cout << "Float catch" << endl;
    }
    catch(int i)
    {
        cout << "Int catch" << endl;
    }
    catch(...)
    {
        cout << string("Generic catch") << endl;
    }
}

// f2 - the absence of a throw() clause in the
//      declaration of this function means that it may
//      throw any kind of object
void f2()
{
    try
    {
        Obj c('c');
        f3();
    }
    catch(string msg)
    {
        cout << "String catch" << endl;
    }
}

// f3 - this function may throw an int object
void f3() throw(int)
{
    Obj d('d');
    throw 10;
}
