// MaxTemplate - create a template max() function
//               that returns the greater of two types
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <typeinfo>

using namespace std;

// simplistic exception class for this example only
template <class T> T maximum(T t1, T t2)
{
    if (t1 > t2)
    {
        return t1;
    }
    return t2;
}

int main(int argc, char* pArgs[])
{
    // find the maximum of two int's;
    // here C++ creates maximum(int, int)
    cout << "The maximum of -1 and 2 is "
         << maximum(-1, 2)
         << endl;

    // repeat for two doubles;
    // in this case, we have to provide T explicitly since
    // the types of the arguments is different
    cout << "The maximum of 1 and 2.5 is "
         << maximum<double>(1, 2.5)
         << endl;

    system("PAUSE");
    return 0;
}
