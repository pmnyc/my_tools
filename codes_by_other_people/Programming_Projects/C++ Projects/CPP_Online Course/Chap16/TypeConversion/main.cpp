//
//  TypeConversion - demonstrate the implicit conversion
//                   of one type to another
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Complex
{
  public:
    Complex() : dReal(0.0), dImag(0.0)
    { cout << "invoke default constructor" << endl;}
    /*explicit*/ Complex(double _dReal)
      : dReal(_dReal), dImag(0.0)
    { cout << "invoke real constructor " << dReal <<endl;}
    Complex(double _dReal, double _dImag)
      : dReal(_dReal), dImag(_dImag)
    {
        cout << "invoke complex constructor " << dReal
             << ", " << dImag << endl;
    }

    double dReal;
    double dImag;
};

int main(int argcs, char* pArgs[])
{
    Complex c1, c2(1.0), c3(1.0, 1.0);

    // constructor can be used to convert from one type
    // to another
    c1 = Complex(10.0);

    // the following conversions work even if explicit
    // is uncommented
    c1 = (Complex)20.0;
    c1 = static_cast<Complex>(30.0);

    // the following implicit conversions work if the
    // explicit is commented out
    c1 = 40.0;
    c1 = 50;

    system("PAUSE");
    return 0;
}
