// stl_sort.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <list>
#include <vector>
#include <algorithm>

using namespace std;

int _tmain(int argc, _TCHAR* argv[])
{

	list<int> li; //doubly-linked list

	for (int i = 0; i < 6; i++)
	{
		cout << i << " ";
		li.push_back(i);
	}
	cout << endl;

	// compute min and max
	list<int>::const_iterator it_list;
	it_list = min_element(li.begin(), li.end());
	cout << *it_list << " ";
	it_list = max_element(li.begin(), li.end());
	cout << *it_list << " " << endl;	


	vector<int> vect; //dynamically allocated
	vect.push_back(7);
	vect.push_back(-3);
	vect.push_back(6);
	vect.push_back(2);
	vect.push_back(-5);
	vect.push_back(0);
	vect.push_back(4);

	//sort the list
	sort(vect.begin(), vect.end());

	vector<int>::const_iterator it_vec; //declare an iterator
	for (it_vec = vect.begin(); it_vec != vect.end(); it_vec++)
		cout << *it_vec << " ";
	
	cout << endl;



	return 0;
}

