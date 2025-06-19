

Assigned Task Overview:
The assigned task was to develop a Matrix Operation Library in C++ that supports addition, multiplication, and inversion of matrices using dynamic memory allocation and object-oriented programming concepts. The project required the use of pointer arithmetic for direct memory manipulation and implementation of polymorphism through an abstract base class and multiple derived classes.

Completion Strategy:
To complete the task, a dynamic system was implemented where the user inputs the dimensions of two matrices. These matrices are created at runtime using double pointers (`double**`). An abstract base class `MatrixOp` was created to define a virtual `execute()` method, which each derived class overrides. The `AddMatrixOp`, `MulMatrixOp`, and `InverseMatrixOp` classes handle specific matrix operations. Pointer arithmetic is used throughout to manipulate matrix elements efficiently. A pointer-to-object array (`MatrixOp**`) enables dynamic dispatch, demonstrating polymorphism. Memory is managed with careful allocation and deallocation to prevent leaks, and the code is structured modularly for clarity and extensibility.

Matrix Operation Library - Detailed Project Note
Student: Eric Niyigena
Institution: University of Rwanda
Date: June 2025
Project Title: Matrix Operation Library
Objective:
To implement a C++ library that performs matrix operations (Addition, Multiplication, and Inversion) using object-oriented programming principles, dynamic memory management, and pointer arithmetic.
1. Project Overview:
The Matrix Operation Library is a C++ application that enables users to perform various operations on 2D matrices. The system is designed using object-oriented programming (OOP) to allow for flexibility and modularity. It demonstrates the use of abstract classes, inheritance, and polymorphism.
2. Key Functionalities:
- Accepts user-defined dimensions and dynamically allocates two matrices: A and B.
- Performs:
  - Matrix Addition
  - Matrix Multiplication
  - Matrix Inversion (for square matrices)
- All operations are implemented through a common abstract interface (`MatrixOp`).
3. Technical Implementation:
3.1 Dynamic Allocation:
- Used `double**` for matrices.
- Implemented dynamic allocation functions to create 2D arrays based on user input.
3.2 Abstract Class Design:

class MatrixOp {
public:
    virtual double** execute(double**, double**, int, int, int, int) = 0;
    virtual ~MatrixOp() {}
};
3.3 Derived Classes:
- AddMatrixOp – Implements matrix addition.
- MulMatrixOp – Implements matrix multiplication.
- InverseMatrixOp – Implements matrix inversion using Gauss-Jordan elimination.
3.4 Polymorphic Operation Dispatch:
- Used `MatrixOp** ops` to store different operation objects.
- Called `ops[i]->execute(A, B, r1, c1, r2, c2);` to dispatch operations polymorphically.
3.5 Pointer Arithmetic:
- Matrix values accessed using pointer arithmetic like: `*(*(A + i) + j)`.
3.6 Memory Management:
- Implemented proper memory cleanup
 for all allocated matrices and operation objects.
- Avoided memory leaks by deleting all dynamic allocations.
4. Outcomes and Learnings:
- Gained deep understanding of abstract classes and polymorphism.
- Improved proficiency in dynamic memory management and pointer usage.
- Created an extensible architecture for adding more matrix operations.
5. Future Enhancements:
- Add determinant and transpose functionalities.
- Use STL containers like `std::vector` for better memory safety.
- Improve error handling for edge cases.
Conclusion:
This project successfully demonstrates the application of object-oriented programming in solving real-world mathematical problems. It focuses on clean modular code and prepares the base for building more advanced mathematical tool

Here are detailed comments for every block of code:
#include // For input and output
#include // For mathematical functions like abs()
// Abstract base class for matrix operations
class MatrixOp {
public:
virtual ~MatrixOp() {} // Virtual destructor
// Pure virtual function to be implemented by derived classes
virtual double** execute(double** A, double** B, int r1, int c1, int r2, int c2) = 0;
};
// Matrix addition operation class
class AddMatrixOp : public MatrixOp {
public:
double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
// Check for dimension compatibility
if (r1 != r2 || c1 != c2) {
std::cerr << "Error: Addition requires same dimensions\n";
return nullptr;
}
    // Allocate result matrix
    double** result = new double*[r1];
    for (int i = 0; i < r1; i++) {
        result[i] = new double[c1];
        for (int j = 0; j < c1; j++) {
            // Add corresponding elements using pointer arithmetic
            *(*(result + i) + j) = *(*(A + i) + j) + *(*(B + i) + j);
        }
    }
    return result; // Return sum
}
};
// Matrix multiplication operation class
class MulMatrixOp : public MatrixOp {
public:
double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
// Check for dimension compatibility
if (c1 != r2) {
std::cerr << "Error: Multiplication dimension mismatch\n";
return nullptr;
}
    // Allocate result matrix
    double** result = new double*[r1];
    for (int i = 0; i < r1; i++) {
        result[i] = new double[c2]{0}; // Initialize each element to 0

        for (int j = 0; j < c2; j++) {
            for (int k = 0; k < c1; k++) {
                // Multiply and accumulate products using pointer arithmetic
                *(*(result + i) + j) += *(*(A + i) + k) * *(*(B + k) + j);
            }
        }
    }
    return result; // Return product
}
};
// Matrix inversion operation class
class InverseMatrixOp : public MatrixOp {
public:
double** execute(double** A, double** B, int r1, int c1, int r2, int c2) override {
if (r1 != c1) { // Check for square matrix
std::cerr << "Error: Inverse requires square matrix\n";
return nullptr;
}
int n = r1;
    // Create augmented matrix [A|I]
    double** aug = new double*[n];
    for (int i = 0; i < n; i++) {
        aug[i] = new double[2 * n];
        for (int j = 0; j < n; j++) {
            *(*(aug + i) + j) = *(*(A + i) + j); // Copy A
        }
        for (int j = n; j < 2 * n; j++) {
            *(*(aug + i) + j) = (j - n == i) ? 1.0 : 0.0; // Identity matrix
        }
    }

    // Apply Gauss-Jordan elimination
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
            std::swap(aug[i], aug[maxRow]); // Swap rows
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

    // Extract inverse matrix from augmented matrix
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

    return inv; // Return inverse matrix
}
};
// Allocate a dynamic matrix
double** allocateMatrix(int rows, int cols) {
double** matrix = new double*[rows];
for (int i = 0; i < rows; i++) {
matrix[i] = new double[cols];
}
return matrix;
}
// Free a dynamically allocated matrix
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
std::cout << ((matrix + i) + j) << " "; // Print element
}
std::cout << "\n";
}
}
int main() {
int r1, c1, r2, c2;
// Input dimensions and elements for matrix A
std::cout << "Enter dimensions for matrix A (rows columns): ";
std::cin >> r1 >> c1;
double** A = allocateMatrix(r1, c1);
std::cout << "Enter elements for matrix A:\n";
for (int i = 0; i < r1; i++) {
    for (int j = 0; j < c1; j++) {
        std::cin >> *(*(A + i) + j);
    }
}

// Input dimensions and elements for matrix B
std::cout << "Enter dimensions for matrix B (rows columns): ";
std::cin >> r2 >> c2;
double** B = allocateMatrix(r2, c2);
std::cout << "Enter elements for matrix B:\n";
for (int i = 0; i < r2; i++) {
    for (int j = 0; j < c2; j++) {
        std::cin >> *(*(B + i) + j);
    }
}

// Create operation objects using polymorphism
const int NUM_OPS = 3;
MatrixOp* ops[NUM_OPS] = {
    new AddMatrixOp(),
    new MulMatrixOp(),
    new InverseMatrixOp()
};

// Execute each operation and print results
for (int i = 0; i < NUM_OPS; i++) {
    std::cout << "\nOperation " << i+1 << ":\n";
    double** result = ops[i]->execute(A, B, r1, c1, r2, c2);

    if (result) {
        int res_rows, res_cols;

        // Set result dimensions based on operation type
        if (dynamic_cast<AddMatrixOp*>(ops[i])) {
            res_rows = r1;
            res_cols = c1;
        } else if (dynamic_cast<MulMatrixOp*>(ops[i])) {
            res_rows = r1;
            res_cols = c2;
        } else {
            res_rows = r1;
            res_cols = r1; // Square matrix for inverse
        }

        printMatrix(result, res_rows, res_cols); // Display result
        freeMatrix(result, res_rows); // Free result memory
    }
}

// Cleanup original matrices and operations
freeMatrix(A, r1);
freeMatrix(B, r2);
for (int i = 0; i < NUM_OPS; i++) {
    delete ops[i];
}

return 0;
}

SCREENSHOT FOR THE CODE PROVIDED ABOVE
![Screenshot 2025-06-17 220318](https://github.com/user-attachments/assets/6d73b334-3bbf-4a57-a0ff-fecf5fd62d2f)
s in C++.
![Screenshot 2025-06-17 215554](https://github.com/user-attachments/assets/5e3ad459-1c64-4a0d-a80b-e051f12320f2)
![Screenshot 2025-06-17 215636](https://github.com/user-attachments/assets/e93a4434-6f5b-47af-b2c8-c3ea80c788db)
![Screenshot 2025-06-17 213412](https://github.com/user-attachments/assets/75ea37fe-e78b-46e1-9e5d-3e3ffbb41977)
![Screenshot 2025-06-17 214154](https://github.com/user-attachments/assets/5c7f9309-ffe2-42ab-a8bf-3c8f8697b55f)
