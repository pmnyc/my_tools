//DemoAssignmentOperator - demonstrate the assignment
//                        operator on a user defined class
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// DArray - a dynamically sized array class used to
//        demonstrate the assignment and copy constructor
//        operators
class DArray
{
  public:
    DArray(int nLengthOfArray = 0)
      : nLength(nLengthOfArray), pArray(0)
    {
        cout << "Creating DArray of length = "
             << nLength << endl;
        if (nLength > 0)
        {
            pArray = new int[nLength];
        }
    }
    DArray(DArray& da)
    {
        cout << "Copying DArray of length = "
             << da.nLength << endl;
        copyDArray(da);
    }
    ~DArray()
    {
        deleteDArray();
    }

    //assignment operator
    DArray& operator=(const DArray& s)
    {
        cout << "Assigning source of length = "
             << s.nLength
             << " to target of length = "
             << this->nLength << endl;

        //delete existing stuff...
        deleteDArray();
        //...before replacing with new stuff
        copyDArray(s);
        //return reference to existing object
        return *this;
    }

    int& operator[](int index)
    {
        return pArray[index];
    }

    int size() { return nLength; }

    void out(const char* pszName)
    {
        cout << pszName << ": ";
        int i = 0;
        while (true)
        {
            cout << pArray[i];
            if (++i >= nLength)
            {
                break;
            }
            cout << ", ";
        }
        cout << endl;
    }

  protected:
    void copyDArray(const DArray& da);
    void deleteDArray();

    int nLength;
    int* pArray;
};

//copyDArray() - create a copy of a dynamic array of ints
void DArray::copyDArray(const DArray& source)
{
    nLength = source.nLength;
    pArray = 0;
    if (nLength > 0)
    {
        pArray = new int[nLength];
        for(int i = 0; i < nLength; i++)
        {
            pArray[i] = source.pArray[i];
        }
    }
}

//deleteDArray() - return heap memory
void DArray::deleteDArray()
{
    nLength = 0;
    delete pArray;
    pArray = 0;
}

int main(int nNumberofArgs, char* pszArgs[])
{
    // a dynamic array and assign it values
    DArray da1(5);
    for (int i = 0; i < da1.size(); i++)
    {
        // uses user defined index operator to access
        // members of the array
        da1[i] = i;
    }
    da1.out("da1");

    // now create a copy of this dynamic array using
    // copy constructor; this is same as da2(da1)
    DArray da2 = da1;
    da2[2] = 20;   // change a value in the copy
    da2.out("da2");

    // overwrite the existing da2 with the original da1
    da2 = da1;
    da2.out("da2");


    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

