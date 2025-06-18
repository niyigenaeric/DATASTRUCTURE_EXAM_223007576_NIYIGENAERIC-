

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
![Screenshot 2025-06-17 220318](https://github.com/user-attachments/assets/6d73b334-3bbf-4a57-a0ff-fecf5fd62d2f)
s in C++.
![Screenshot 2025-06-17 215554](https://github.com/user-attachments/assets/5e3ad459-1c64-4a0d-a80b-e051f12320f2)
![Screenshot 2025-06-17 215636](https://github.com/user-attachments/assets/e93a4434-6f5b-47af-b2c8-c3ea80c788db)
![Screenshot 2025-06-17 213412](https://github.com/user-attachments/assets/75ea37fe-e78b-46e1-9e5d-3e3ffbb41977)
![Screenshot 2025-06-17 214154](https://github.com/user-attachments/assets/5c7f9309-ffe2-42ab-a8bf-3c8f8697b55f)
