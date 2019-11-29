#include <igl/opengl/glfw/Viewer.h>
#include <iostream>
#include <ostream>
#include <fstream>
#include <string>
#include <igl/readOFF.h>
#include <igl/writeOFF.h>
#include <igl/doublearea.h>
#include <igl/massmatrix.h>
#include <igl/invert_diag.h>
#include <igl/barycenter.h>
#include <igl/cotmatrix.h>
#include <igl/grad.h>
#include <igl/jet.h>
#include <igl/eigs.h>
//#include <igl/readDMAT.h>
//#include <igl/repdiag.h>

//#include <igl/gaussian_curvature.h>
//#include <igl/per_vertex_normals.h>
//#include <igl/per_face_normals.h>

//#include "HalfedgeBuilder.cpp"
//#include "LaplaceBeltrami.cpp"


// THIS : https://ensiwiki.ensimag.fr/index.php?title=Descripteur_de_formes_et_mouvements_3D_et_classification_d%27animations

using namespace Eigen; // to use the classes provided by Eigen library
using namespace std;
#define MAXBUFSIZE  ((int) 1e5)

MatrixXd V;
MatrixXi F;
MatrixXd U;
VectorXd S;
VectorXd regs;

// Read-write matrices from file (adapted from https://stackoverflow.com/questions/20786220/eigen-library-initialize-matrix-with-data-from-file-or-existing-stdvector):

MatrixXd readMatrix(const char* filename)
{
	int cols = 0, rows = 0;
	double buff[MAXBUFSIZE];

	// Read numbers from file into buffer.
	ifstream infile;
	infile.open(filename);
	if (!infile)
	{
		cerr << "Error opening" << filename << endl;
		return MatrixXd::Zero(1, 1);
	}

	while (!infile.eof())
	{
		string line;
		getline(infile, line);
		int temp_cols = 0;
		stringstream stream(line);
		while (!stream.eof())
			stream >> buff[cols * rows + temp_cols++];

		if (temp_cols == 0)
			continue;

		if (cols == 0)
			cols = temp_cols;

		rows++;
	}
	infile.close();
	rows--;

	// Populate matrix with numbers.
	MatrixXd result(rows, cols);
	for (int i = 0; i < rows; i++)
		for (int j = 0; j < cols; j++)
			result(i, j) = buff[cols * i + j];

	return result;
}

void writeMatrix(string filename, MatrixXd data)
{
	ofstream file(filename, ios::out | ios::trunc);
	if (file)
	{
		file << data;
		file.close();
	}
	else
		cerr << "Error opening" << filename << endl;
}

MatrixXd GPS(MatrixXd& U, VectorXd& S)
{
	MatrixXd result(U.rows(), U.cols() - 1);
	int d = S.rows();
	for (int i = 1; i < d; i++)
		result.col(i - 1) = U.col(i) / sqrt(abs(S(i, 0)));

	return result;
}

VectorXd shapeDNA(VectorXd& S)
{
	return S.bottomRows(S.rows() - 1);
}

VectorXd regions(MatrixXd& GPS, int m)
{
	VectorXd result = VectorXd::Zero(GPS.rows());
	VectorXd norms = GPS.rowwise().norm();
	double d_max = norms.maxCoeff();
	double delta = d_max / m;

	for (int i = 0; i < GPS.rows(); i++)
		result(i, 0) = floor(norms(i, 0) / delta) + 1;

	return result;
}

// ------------ main program ----------------
int main(int argc, char *argv[])
{
	int m = 4; // number of regions to make histograms
	int d = 15; // depth of spectrum (15 in paper)
	
	cout << "Executing test program: bunny.off, m = " << m << " , d = " << d << endl;

	igl::readOBJ("../models/camel-collapse/camel-collapse-reference.obj", V, F);


	// read mesh
	//igl::readOFF("../data/bunny.off", V, F);

	// compute eigen-decomposition of Laplace-Beltrami operator
	SparseMatrix<double> L, M;
	cout << "Computing Laplacian" << endl;
	igl::cotmatrix(V, F, L); // /!\ MEF cotmatrix seams to be minus what we want
	L = -L;
	// Default is voronoi mass matrix, but we want barytcentric to implement the paper
	igl::massmatrix(V, F, igl::MASSMATRIX_TYPE_BARYCENTRIC, M);
	cout << "Computing Eigen decomposition" << endl;
	igl::eigs(L, M, d + 1, igl::EIGS_TYPE_SM, U, S);

	// build GPS matrix and classify points according to regions
	cout << "Computing GPS embedding" << endl;
	MatrixXd gps = GPS(U, S);
	// std::cout << S.rows()/*gps.rowwise().norm()*/ << std::endl;
	//regs = regions(gps, m);

	writeMatrix("../camel-collapse-reference_15_GPS.txt", gps);
	writeMatrix("../camel-collapse-reference_15_shapeDNA.txt", shapeDNA(S));


}
