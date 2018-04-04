// stl_random.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <random>

using namespace std;

int _tmain(int argc, _TCHAR* argv[])
{
	const int nrolls = 10000; //number of experiments

	default_random_engine generator;
	normal_distribution<double> distribution(5.0, 2.0);

	int p[10] = {};
	for (int i = 0; i < nrolls; ++i)
	{
		double number = distribution(generator);
		if (number >= 0.0 && number <= 10.0) ++p[int(number)];
	}

	cout << "normal distribution(5.0,2.0):" << endl;

	for (int i = 0; i < 10; ++i)
	{
		cout << i << "-" << i + 1 << ": ";
		cout << p[i] << endl;
	}	

	return 0;
}

