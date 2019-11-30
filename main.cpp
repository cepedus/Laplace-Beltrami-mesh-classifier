#include <igl/opengl/glfw/Viewer.h>
#include <iostream>
#include <ostream>
#include <fstream>
#include <string>
#include <random>
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

// rng from https://stackoverflow.com/questions/5008804/generating-random-integer-from-a-range
std::random_device rd;     // only used once to initialise (seed) engine
std::mt19937 rng(rd());    // random-number engine used (Mersenne-Twister in this case)

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
	// ignore smallest eigenvalue (last of S) and reverse column order in result matrix to have v_1, ..., v_d increasing
	for (int i = 0; i < d - 1; i++)
		result.col(d - 2 - i) = U.col(i) / sqrt(abs(S(i, 0)));

	return result;
}

VectorXd shapeDNA(VectorXd& S)
{
	// get non-zero eigenvalues in increasing order
	return S.topRows(S.rows() - 1).reverse();
}

VectorXd regions(MatrixXd& GPS, int m)
{
	// get corresponding region vector for each row of GPS matrix
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
	string meshName(argv[1]);
	
	cout << "Executing test program: " << meshName << ", m = " << m << " , d = " << d << endl;
	
	// read mesh

	igl::readOBJ("./" + meshName + ".obj", V, F);
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
	cout << "Computing embeddings" << endl;
	MatrixXd gps = GPS(U, S);
	MatrixXd dna = shapeDNA(S);
	cout << "Saving embeddings to results/spectra/" << endl;
	writeMatrix("../results/spectra/" + meshName + "." + to_string(d) + ".GPS.txt", gps);
	writeMatrix("../results/spectra/" + meshName + "." + to_string(d) + ".shapeDNA.txt", dna);

	/*-----------------------------------------------------------------------------------------
	// TODO:
	// - Compute & save embeddings for each shape
	// 
	// Rustamov07:
	//  * for a given m, divide rows of GPS in regions, sample points and compute histograms
	//  * compare histograms
	//
	// Reuter05:
	//  * Clustering on shapeDNA
	//-----------------------------------------------------------------------------------------
	*/

	//std::uniform_int_distribution<int> uni(0, gps.rows() - 1);
	//// while (true) {
	//// 	int i = uni(rng);
	//// 	int j = uni(rng);
	//// 	cout << (gps.row(i) - gps.row(j)).norm() << " / ";
	//// }
	//// regs = regions(gps, m);

	


}
