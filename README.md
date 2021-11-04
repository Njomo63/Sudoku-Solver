# **Sudoku-Solver**
A sudoku solver that approaches sudoku puzzles as exact cover problems and solves them using Donald Knuth's Algorithm X implemented in Python.

## **Introduction**
In order to understand an exact cover problem consider set *X* = {1,2,3,4,5,6} and sets:
* *A* = {1,3,5}
* *B* = {1,5}
* *C* = {2}
* *D* = {2,4}
* *E* = {6}

The subcollection *S* = {A,D,E} is an exact cover since each element of *X* is contained once in the subcollection.
In 9×9 Sudoku there are 4 categories of constraints:
* Each cell contains a number in [1,9]
* Each row contains the numbers 1-9
* Each column contains the numbers 1-9
* Each box contains the numbers 1-9

In total there are 324 constraints for a 9×9 Sudoku puzzle. Each cell of a 9×9 sudoku puzzle will be assigned a value in [1,9]. Since there are 81 cells in the puzzle and they can each contain values in [1,9] there will be 81×9 = 729 possibilities or candidates. Each constraint has a set of possibilities. This results in a 729×324 constraint matrix.
Choosing a value for a cell in the puzzle prohibits that value from being put in the same column, row, box and also another value being placed in that particular cell. This makes Sudoku an exact cover problem.


## **Solving an Exact Cover problem**
Algorithm X finds all solutions to the exact cover problem defined by any given matrix A that consists of 0s and 1s. In order to first use Algorithm X to solve a sudoku exact cover problem, all cells that have 1s are converted to nodes.
The column heads of matrix A need to be represented as doubly linked lists. All nodes in the column also need to be doubly linked. In addition there should be head and tail spacers at the beginning and end of each row. Algorithm X basically loops through the column heads and covers that column by deattaching the column head from the other column heads as well as deattaching nodes in a row.

ALgorithm X is a backtracking program since if a solution isn't found it reattaches the columns and rows that have been deattached (hence the name Dancing Links) and selects another row and repeats the process again. This goes on until a solution is found. 

## **Performance**
My python implementation isn't optimised hence the slow running time on 'hard' puzzles. Future improvements to my implementation will include initially starting looping on the columns with the smallest rows which will reduce the branching factor and make the running time much quicker.

## **Resources**
1. Stanford Lecture: Don Knuth—"Dancing Links" (2018) https://www.youtube.com/watch?v=_cR9zDlvP88
2. https://en.wikipedia.org/wiki/Exact_cover
3. Dancing Links - D. E. Knuth (https://arxiv.org/pdf/cs/0011047v1.pdf)
