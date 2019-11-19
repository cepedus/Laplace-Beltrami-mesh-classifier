#include <igl/opengl/glfw/Viewer.h>

#ifndef HALFEDGE_DS_HEADER
#define HALFEDGE_DS_HEADER
#include "HalfedgeDS.cpp"
#endif

using namespace Eigen;
using namespace std;

class LaplaceBeltrami
{

public:
	/**
	 * Initialize the data structures
	 **/
	LaplaceBeltrami(MatrixXd& V_in, MatrixXi& F_in, HalfedgeDS& mesh)
	{
		he = &mesh;
		V = &V_in;
		F = &F_in; // NOT NEEDED if using the half-edge data structure

		

		// make vector of face areas, each area propagates to all vertices, then normalize per vertex degree
		int n = V->rows();
		D = VectorXi::Zero(n);
		A_diag = VectorXd::Zero(n);

		W = MatrixXd::Zero(n, n);
		
		std::cout << "Computing degree vector" << std::endl;
		fill_D();

		std::cout << "Computing A matrix" << std::endl;
		fill_A();

		std::cout << "Computing W matrix" << std::endl;
		fill_W();

		std::cout << "Done initializing" << std::endl;

		std::cout << W << std::endl;

	}


	/**
	 * Getters
	 **/
	MatrixXd getVertexCoordinates()
	{
		return *V;
	}

	/**
	 * Return the number of faces
	 **/
	MatrixXi getFaces()
	{
		return *F;
	}

private:

	void fill_D()
	/**
	* Fills vector D of vertices' degrees
	**/
	{
		int n = V->rows();
		for (int i = 0; i < n; i++)
		{
			D(i) = vertexDegree(i);
		}
	}

	void fill_A()
	/**
	* Fills vector A of vertices' areas
	**/
	{
		for (int i = 0; i < F->rows(); i++)
			update_area(i);
	}

	void fill_W()
	/**
	* Fills matrix W of laplacian decomposition
	**/
	{
		int e = he->sizeOfHalfedges();
		int n = V->rows();

		// Step 1: fill W(i, j) = -1/2(cotg(alpha) + cotg(beta)) for i ~ j, with proposed optimization (slide 68, lecture 8)
		for (int e_i = 0; e_i < e; e_i++)
		{
			// get neighboring vertices indexes by looking at halfedges
			int u = he->getTarget(e_i);
			int e_j = he->getOpposite(e_i);
			int v = he->getTarget(e_j);

			if (W(u, v) != 0.0) continue; // discard visited pairs
			
			// get other edges in corresponding faces

			int f1 = he->getFace(e_i);
			int f2 = he->getFace(e_j);

			int e_i2 = he->getNext(e_i);
			int e_i3 = he->getNext(e_i2);
			
			int e_j2 = he->getNext(e_j);
			int e_j3 = he->getNext(e_j2);

			// compute w_ij with area formula instead of cotg
			double w_ij = (len(e_i) * len(e_i) - len(e_i2) * len(e_i2) - len(e_i3) * len(e_i3)) / (8.0 * area(f1));
			w_ij += (len(e_j) * len(e_j) - len(e_j2) * len(e_j2) - len(e_j3) * len(e_j3)) / (8.0 * area(f2));

			W(u, v) = -w_ij;
		}

		// Step 2: fill diagonal W(i, i) = -sum_j W(i, j)
		for (int i = 0; i < n; i++)
		{
			double sum = W.row(i).sum();
			W(i, i) = -sum;
		}
	}

	void update_area(int f)
	/**
	* Updates area matrix of the vertices in face f (needs D degree matrix of all vertices initialized)
	**/
	{
		RowVector3i vertices = F->row(f);

		int v_i1 = vertices(0);
		int v_i2 = vertices(1);
		int v_i3 = vertices(2);

		double a = area(f);

		A_diag(v_i1) += a / D(v_i1);
		A_diag(v_i2) += a / D(v_i2);
		A_diag(v_i3) += a / D(v_i3);

	}

	double len(int e)
	/**
	* Returns length of an edge e
	**/
	{
		int u_i = he->getTarget(e);
		int v_i = he->getTarget(he->getOpposite(e));

		MatrixXd d_uv = V->row(u_i).transpose() - V->row(v_i).transpose();

		return d_uv.norm();		
	}

	double area(int f)
	/**
	* Returns area of a face f by computing the norm of the cross product of 2 of its sides
	**/
	{
		RowVector3i vertices = F->row(f);

		int v_i1 = vertices(0);
		int v_i2 = vertices(1);
		int v_i3 = vertices(2);

		Vector3d v1 = V->row(v_i1).transpose();
		Vector3d v2 = V->row(v_i2).transpose();
		Vector3d v3 = V->row(v_i3).transpose();

		Vector3d cross = (v1 - v2).cross(v1 - v3);

		double a = 0.5 * cross.norm();

		return a;
	}

	int vertexDegree(int v)
	/**
	* Returns degree of vertex v using halfedge traversal
	**/
	{
		int d = 0;
		int e = he->getEdge(v);
		int e_0 = e;

		while (he->getOpposite(he->getNext(e)) != e_0)
		{ 
			d++;
			e = he->getOpposite(he->getNext(e));
		}

		return d;
	}

	/** Half-edge representation of the original input mesh */
	HalfedgeDS* he;
	MatrixXd* V; // vertex coordinates of the original input mesh
	MatrixXi* F; 

	MatrixXd W;
	VectorXd A_diag;
	VectorXi D;
};