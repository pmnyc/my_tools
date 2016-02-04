//
//  MultipleInheritance - a single class can inherit from
//                        more than one base class
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

class Bed
{
  public:
    Bed(){}
    void sleep(){ cout << "Sleep" << endl; }
    int weight;
};

class Sofa
{
  public:
    Sofa(){}
    void watchTV(){ cout << "Watch TV" << endl; }
    int weight;
};

// SleeperSofa - is both a Bed and a Sofa
class SleeperSofa : public Bed, public Sofa
{
  public:
    SleeperSofa(){}
    void foldOut(){ cout << "Fold out" << endl; }
};

int main(int nNumberofArgs, char* pszArgs[])
{
    SleeperSofa ss;

    // you can watch TV on a sleeper sofa like a sofa...
    ss.watchTV();     // calls Sofa::watchTV()

    //...and then you can fold it out...
    ss.foldOut();     // calls SleeperSofa::foldOut()

    // ...and sleep on it
    ss.sleep();       // calls Bed::sleep()

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}
