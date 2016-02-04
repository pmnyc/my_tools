//
//  CustomExceptionClass - demonstrate the flexibility
//              of the exception mechanism by creating
//              a custom exception class
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
using namespace std;

// MyException - generic exception handling class
class MyException
{
  public:
    MyException(const char* pMsg, int n,
                const char* pFunc,
                const char* pFile, int nLine)
      : msg(pMsg), errorValue(n),
        funcName(pFunc), file(pFile), lineNum(nLine)
    {}

    virtual string display()
    {
        ostringstream out;
        out << "Error <" << msg << ">"
            << " - value is " << errorValue << "\n"
            << "in function " << funcName << "()\n"
            << "in file " << file
            << " line #" << lineNum << ends;
        return out.str();
    }
  protected:
    // error message
    string msg;
    int    errorValue;

    // function name, file name and line number
    // where error occurred
    string funcName;
    string file;
    int lineNum;
};

// factorial - compute factorial
int factorial(int n) throw(MyException)
{
    // you can't handle negative values of n;
    // better check for that condition first
    if (n < 0)
    {
        throw MyException("Negative argument not allowed",
                        n, __func__, __FILE__, __LINE__);
    }

    // go ahead and calculate factorial
    int accum = 1;
    while(n > 0)
    {
        accum *= n;
        n--;
    }
    return accum;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    try
    {
        // this will work
        cout << "Factorial of 3 is "
             << factorial(3) << endl;

        // this will generate an exception
        cout << "Factorial of -1 is "
             << factorial(-1) << endl;

        // control will never get here
        cout << "Factorial of 5 is "
             << factorial(5) << endl;
    }
    // control passes here
    catch(MyException e)
    {
        cout << e.display() << endl;
    }
    catch(...)
    {
        cout << "Default catch " << endl;
    }

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

