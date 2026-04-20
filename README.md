# Knight-s-tour
🐴 Knight’s Tour Problem Solver  This project solves the classic Knight’s Tour problem in chess, where a knight must visit every square on an n×n chessboard exactly once without repetition
---

##  Problem Description

The Knight’s Tour is a chess puzzle where a knight must visit **every square on an \(n \times n\) chessboard exactly once** without repeating any square.

The knight moves in an **L-shape**:
- 2 squares in one direction
- 1 square perpendicular

The challenge is to construct a complete valid path covering all squares.

---

##  Features

- ✅ User-defined board size (n × n)
- ✅ Backtracking solution (exact search)
- ✅ Genetic Algorithm (for large boards / optimization)
- ✅ Move validation and safe path generation
- ✅ Optional graphical visualization (if GUI included)
- ✅ Efficient move ordering using heuristics

---

##  Algorithms Used

### 1. Backtracking
- Tries all possible moves recursively
- Backtracks when no valid move exists
- Guarantees correct solution (if exists)

### 2. Genetic Algorithm (Optional / Advanced)
- Used for large boards where backtracking becomes slow
- Uses:
  - Population of candidate solutions
  - Fitness function (number of visited squares)
  - Selection, crossover, mutation

---

##  Technologies

- Python 3.x
- Tkinter (if GUI is included)
- Random / threading libraries
- Object-oriented programming (if applied)

---

