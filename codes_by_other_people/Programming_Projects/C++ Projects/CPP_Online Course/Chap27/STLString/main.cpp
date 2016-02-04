// STLString - demonstrates just a few of the features
//             of the string class which is part of the
//             Standard Template Library
#include <cstdlib>
#include <cstdio>
#include <iostream>
using namespace std;

// removeSpaces - remove any spaces within a string
string removeSpaces(const string& source)
{
    // make a copy of the source string so that we don't
    // modify it
    string s = source;

    // find the offset of the first space;
    // search the string until no more spaces found
    size_t offset;
    while((offset = s.find(" ")) != string::npos)
    {
        // remove the space just discovered
        s.erase(offset, 1);
    }
    return s;
}

// insertPhrase - insert a phrase in the position of
//                <ip> for insertion point
string insertPhrase(const string& source)
{
    string s = source;
    size_t offset = s.find("<ip>");
    if (offset != string::npos)
    {
        s.erase(offset, 4);
        s.insert(offset, "Randall");
    }
    return s;
}


int main(int argc, char* pArgs[])
{
    // create a string that is the sum of two strings
    cout << "string1 + string2 = "
         << (string("string 1") + string("string 2"))
         << endl;

    // create a test string and then remove all spaces
    // from it using simple string methods
    string s2("This is a test string");
    cout << "<" << s2 << "> minus spaces = <"
         << removeSpaces(s2) << ">" << endl;

    // insert a phrase within the middle of an existing
    // sentence (at the location of "<ip>")
    string s3 = "Stephen <ip> Davis";
    cout << s3 + " -> " + insertPhrase(s3) << endl;

    system("PAUSE");
    return 0;
}
