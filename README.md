# Sudoku CSP Solver
This is a simple CSP solver written in Python.  
[What is a CSP?](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)  
> NOTE: This solution is not optimized for performance. There are many improvements that could be made. 

### Running
There are two ways you can run this:  
1) To solve all puzzles listed in `puzzles.txt` simply run `python solver.py`.
1) Otherwise, you may specify a specific puzzle: `python solver.py <your sudoku puzzle>`.  
    * Puzzles must be exactly 81 digits long and blanks are `0`. 
    * See `puzzles.txt` for examples.
    
### More Information
> NOTE: Timing data comes from an average of 5 runs on a 9th generation Intel i9900k CPU running at 4.8GHz.  

Most puzzles are solved in under 200ms.  
All 401 puzzles included are typically solved in around 78 seconds.  

It takes around 6 seconds for this CSP implementation to solve the hardest sudoku:
```
8 0 0 0 0 0 0 0 0
0 0 3 6 0 0 0 0 0
0 7 0 0 9 0 2 0 0
0 5 0 0 0 7 0 0 0
0 0 0 0 4 5 7 0 0
0 0 0 1 0 0 0 3 0
0 0 1 0 0 0 0 6 8
0 0 8 5 0 0 0 1 0
0 9 0 0 0 0 4 0 0
```
