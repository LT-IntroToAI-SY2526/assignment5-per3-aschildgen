# Assignment 5 Write up

Assignment 5 can be broken up into the following parts:
1. Import the Necessary Modules:
- `copy`: For creating deep copies of objects
- `Stack` and `Queue`: Custom implementations for DFS and BFS operations
2. Utility Functions: 
- `remove_if_exists`: Removes a specified element from a list if it exists, which is used to remove the possibilites from a cell
3. Board Class:
- Represents the Sudoku board
- Consists of functions that will find the most constrained cell, and update the board, which eliminates possible solutions
4. DFS & BFS Functions:
- `DFS`: Uses depth-first search to solve the Sudoku puzzle. It works by trying to fill the most constrained cell with potential values until a solution is found or backtracks if a mistake is made
- `BFS`: Uses breadth-first search to solve the Sudoku puzzle in a similar fashion to DFS but explores nodes level by level
5. Main Execution:
- Defines two different sets of initial moves for Sudoku puzzles
- Uses both DFS and BFS to solve each puzzle and prints the results


After completing the assignment, answer the following reflection questions:

## Reflection Questions

1. What are some things that you learned through this assignment? Think about the concepts of backtracking, constraint satisfaction, and search algorithms. Were there any particular challenges you faced while implementing the Board class methods or the DFS/BFS functions? How did you overcome them?

This assignment helped me understand how backtracking and constraints satisfaction  work together. I learned a lot about how the small details like removing the right values from neighboring cells can be very important to get correct. One challenge was keeping the update method correct—forgetting to remove a value from one of the peers could lead to unsusual or incosistent states that were hard to debug.

2. How can you apply what you learned in this assignment to future programs or projects? Consider other types of problems that involve searching through possibilities, making decisions, and backtracking when those decisions don't work out. Can you think of real-world scenarios where DFS or BFS might be useful? What about other constraint satisfaction problems?

This assignment helped me see how search and constraint-solving ideas show up in a lot of other problems. The way DFS and BFS search can be used for so many things like pathfinding, scheduling, etc. I realized that being able to backtrack and adjust when a decision doesn’t work out is a really important part of many algorithms. For example, DFS can be useful in maze generation or exploring large decision trees, but BFS works well for finding the shortest route or minimum number of steps in a problem. The same concepts could even apply to real-world projects/tasks, like optimizing routes, where you have to test options and eliminate ones that don’t fit.

3. Explain how the Stack and Queue classes work and why they are important for DFS and BFS algorithms. Describe the difference between LIFO (Last In First Out) and FIFO (First In First Out) data structures. How does using a Stack versus a Queue change the way the search algorithm explores possible solutions? Why is one data structure better suited for depth-first search and the other for breadth-first search?

This assignment also helped me understand how using different data structures directly change how an algorithm behaves. A stack works in a last in, first out way, which fits depth-first search better since it keeps diving deeper into one path before going back. A queue works in a different first in, first out way, which is better for breadth first because it explores everything level by level. I learned that choosing between them isnt just about structure, it actually changes the method the program searches for solutions. DFS can reach a valid result faster with less memory, while BFS is more systematic and guarantees the shortest path if that matters at all for what youre doing. 



