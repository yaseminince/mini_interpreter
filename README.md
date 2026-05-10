# Mini Programming Language Interpreter

This project is a console based mini programming language interpreter developed in Python for the CS305 Programming Languages course. The main goal of the project is to understand how programming languages work internally by implementing the core stages of an interpreter, including lexical analysis, parsing, abstract syntax tree (AST) generation, and execution.

The interpreter supports arithmetic expressions, variables, string operations, comparison operators, unary operators, exponentiation, and detailed error handling with line and column reporting.

---

# Features

- Integer and floating-point numbers
- Variables and assignments
- Arithmetic operations:
  - `+`
  - `-`
  - `*`
  - `/`
  - `^`
- Unary operators:
  - `+x`
  - `-x`
- Comparison operators:
  - `<`
  - `>`
- String values
- String concatenation
- Print statements
- Parentheses and operator precedence
- Right-associative exponentiation
- Runtime and syntax error handling
- Error reporting with line and column information

---

# Project Structure

Lexer → Parser → AST → Interpreter

## Components

### Lexer
The lexer reads the source code character by character and converts it into tokens.

### Parser
The parser analyzes the token sequence according to grammar rules and generates the abstract syntax tree (AST).

### AST Nodes
AST nodes represent different structures in the language such as numbers, variables, binary operations, unary operations, assignments, and print statements.

### Interpreter
The interpreter traverses the AST and evaluates expressions and statements.

---

# Example Usage

## Variable Assignment

x = 5
y = 2 ^ 3
print(x + y)

Output:

13

---

## String Concatenation

print("Hello " + "World")

Output:

Hello World

---

## Comparison Operations

print(5 > 2)

Output:

True

---

## Runtime Error Example

print(5 / 0)

Output:

Runtime Error: Division by zero at line 1, column 9

---

## String Error Example

print("hello" + 5)

Output:

String Error: Cannot add string and number at line 1, column 15

---

# Technologies Used

- Python 3
- Object Oriented Programming
- Recursive Descent Parsing
- Abstract Syntax Trees (AST)
- Custom Error Handling

---

# What We Learned

During this project, we gained practical experience with:

- Lexical analysis
- Parsing techniques
- Recursive descent parsers
- Abstract syntax trees
- Expression evaluation
- Operator precedence and associativity
- Runtime execution
- Error handling and debugging
- Interpreter architecture

---

# Future Improvements

Possible future improvements include:

- If statements
- While loops
- Functions
- Boolean operators
- Arrays and lists
- File execution support

---
