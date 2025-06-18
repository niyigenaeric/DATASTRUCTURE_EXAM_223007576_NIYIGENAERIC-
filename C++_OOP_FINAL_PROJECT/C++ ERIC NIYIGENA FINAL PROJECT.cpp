#include <iostream>
#include <cmath>

// Abstract base class for matrix operations
class MatrixOp {
public:
    virtual ~MatrixOp() {}
    virtual double** execute(double** A, double** B, int r1, int c1, int r2, int c2) = 0;
};

// Matrix addition operation
class AddMatrixOp : public MatrixOp {
public:
    double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
        if (r1 != r2 || c1 != c2) {
            std::cerr << "Error: Addition requires same dimensions\n";
            return nullptr;
        }

        double** result = new double*[r1];
        for (int i = 0; i < r1; i++) {
            result[i] = new double[c1];
            for (int j = 0; j < c1; j++) {
                // Pointer arithmetic for element access
                *(*(result + i) + j) = *(*(A + i) + j) + *(*(B + i) + j);
            }
        }
        return result;
    }
};

// Matrix multiplication operation
class MulMatrixOp : public MatrixOp {
public:
    double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
        if (c1 != r2) {
            std::cerr << "Error: Multiplication dimension mismatch\n";
            return nullptr;
        }

        double** result = new double*[r1];
        for (int i = 0; i < r1; i++) {
            result[i] = new double[c2]{0}; // Initialize to zero
            
            for (int j = 0; j < c2; j++) {
                for (int k = 0; k < c1; k++) {
                    // Pointer arithmetic for element access
                    *(*(result + i) + j) += *(*(A + i) + k) * *(*(B + k) + j);
                }
            }
        }
        return result;
    }
};

// Matrix inversion operation
class InverseMatrixOp : public MatrixOp {
public:
    double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
        if (r1 != c1) {
            std::cerr << "Error: Inverse requires square matrix\n";
            return nullptr;
        }
        int n = r1;
        
        // Create augmented matrix [A|I]
        double** aug = new double*[n];
        for (int i = 0; i < n; i++) {
            aug[i] = new double[2 * n];
            for (int j = 0; j < n; j++) {
                *(*(aug + i) + j) = *(*(A + i) + j);
            }
            for (int j = n; j < 2 * n; j++) {
                *(*(aug + i) + j) = (j - n == i) ? 1.0 : 0.0;
            }
        }

        // Gauss-Jordan elimination
        for (int i = 0; i < n; i++) {
            // Partial pivoting
            double maxVal = std::abs(*(*(aug + i) + i));
            int maxRow = i;
            for (int k = i + 1; k < n; k++) {
                if (std::abs(*(*(aug + k) + i)) > maxVal) {
                    maxVal = std::abs(*(*(aug + k) + i));
                    maxRow = k;
                }
            }

            if (maxRow != i) {
                std::swap(aug[i], aug[maxRow]);
            }

            double pivot = *(*(aug + i) + i);
            if (std::abs(pivot) < 1e-9) {
                std::cerr << "Error: Matrix is singular\n";
                for (int j = 0; j < n; j++) delete[] aug[j];
                delete[] aug;
                return nullptr;
            }

            // Normalize pivot row
            for (int j = 0; j < 2 * n; j++) {
                *(*(aug + i) + j) /= pivot;
            }

            // Eliminate other rows
            for (int k = 0; k < n; k++) {
                if (k == i) continue;
                double factor = *(*(aug + k) + i);
                for (int j = 0; j < 2 * n; j++) {
                    *(*(aug + k) + j) -= factor * *(*(aug + i) + j);
                }
            }
        }

        // Extract inverse matrix
        double** inv = new double*[n];
        for (int i = 0; i < n; i++) {
            inv[i] = new double[n];
            for (int j = 0; j < n; j++) {
                *(*(inv + i) + j) = *(*(aug + i) + j + n);
            }
        }

        // Cleanup augmented matrix
        for (int i = 0; i < n; i++) delete[] aug[i];
        delete[] aug;

        return inv;
    }
};

// Allocate a matrix dynamically
double** allocateMatrix(int rows, int cols) {
    double** matrix = new double*[rows];
    for (int i = 0; i < rows; i++) {
        matrix[i] = new double[cols];
    }
    return matrix;
}

// Free a matrix
void freeMatrix(double** matrix, int rows) {
    for (int i = 0; i < rows; i++) {
        delete[] matrix[i];
    }
    delete[] matrix;
}

// Print a matrix
void printMatrix(double** matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            std::cout << *(*(matrix + i) + j) << " ";
        }
        std::cout << "\n";
    }
}

int main() {
    int r1, c1, r2, c2;

    // Matrix A input
    std::cout << "Enter dimensions for matrix A (rows columns): ";
    std::cin >> r1 >> c1;
    double** A = allocateMatrix(r1, c1);
    std::cout << "Enter elements for matrix A:\n";
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c1; j++) {
            std::cin >> *(*(A + i) + j);
        }
    }

    // Matrix B input
    std::cout << "Enter dimensions for matrix B (rows columns): ";
    std::cin >> r2 >> c2;
    double** B = allocateMatrix(r2, c2);
    std::cout << "Enter elements for matrix B:\n";
    for (int i = 0; i < r2; i++) {
        for (int j = 0; j < c2; j++) {
            std::cin >> *(*(B + i) + j);
        }
    }

    // Create operations using polymorphism
    const int NUM_OPS = 3;
    MatrixOp* ops[NUM_OPS] = {
        new AddMatrixOp(),
        new MulMatrixOp(),
        new InverseMatrixOp()
    };

    // Execute and show results
    for (int i = 0; i < NUM_OPS; i++) {
        std::cout << "\nOperation " << i+1 << ":\n";
        double** result = ops[i]->execute(A, B, r1, c1, r2, c2);
        
        if (result) {
            // Determine result dimensions
            int res_rows, res_cols;
            if (dynamic_cast<AddMatrixOp*>(ops[i])) {
                res_rows = r1;
                res_cols = c1;
            } else if (dynamic_cast<MulMatrixOp*>(ops[i])) {
                res_rows = r1;
                res_cols = c2;
            } else {
                res_rows = r1;
                res_cols = r1; // Square matrix
            }
            
            printMatrix(result, res_rows, res_cols);
            freeMatrix(result, res_rows);
        }
    }

    // Cleanup
    freeMatrix(A, r1);
    freeMatrix(B, r2);
    for (int i = 0; i < NUM_OPS; i++) {
        delete ops[i];
    }

    return 0;
}