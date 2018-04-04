// boost_graph.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/topological_sort.hpp>

using namespace boost;
using namespace std;

typedef boost::adjacency_list<listS, vecS, undirectedS> mygraph;

int _tmain(int argc, _TCHAR* argv[])
{
	mygraph g;
	add_edge(0, 1, g);
	add_edge(0, 3, g);
	add_edge(1, 2, g);
	add_edge(2, 3, g);

	mygraph::vertex_iterator vertexIt, vertexEnd;
	mygraph::adjacency_iterator neighbourIt, neighbourEnd;
	tie(vertexIt, vertexEnd) = vertices(g);
	for (; vertexIt != vertexEnd; ++vertexIt)
	{
		cout << *vertexIt << " is connected with ";
		tie(neighbourIt, neighbourEnd) = adjacent_vertices(*vertexIt, g);
		for (; neighbourIt != neighbourEnd; ++neighbourIt)
			cout << *neighbourIt << " ";
		cout << "\n";
	}

	cout << "Number of edges: " << num_edges(g) << "\n";
	cout << "Number of vertices: " << num_vertices(g) << "\n";
	
	return 0;
}

