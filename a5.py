import copy  # used for deep copies when branching states
from typing import List, Any, Tuple

# helper imports for search structures
from stack_and_queue import Stack, Queue


def remove_if_exists(lst: Any, elem: Any) -> None:
    """If lst is a list and contains elem, remove the first occurrence.

    Args:
        lst: object expected to be a list of items (or something else)
        elem: item to drop from the list if present
    """
    if isinstance(lst, list) and elem in lst:
        lst.remove(elem)


class Board:
    """A Sudoku board state.

    Unfilled squares store a list of candidate digits [1..9]. Filled squares store
    the integer that was assigned. The class tracks how many cells have been fixed.
    """

    def __init__(self) -> None:
        self.size: int = 9
        self.num_nums_placed: int = 0
        # rows[r][c] is either a list of possibilities or an int assignment
        self.rows: List[List[Any]] = [
            [list(range(1, 10)) for _c in range(self.size)] for _r in range(self.size)
        ]

    def __str__(self) -> str:
        """Return a compact textual snapshot of the board's internal state."""
        lines = [f"num_nums_placed: {self.num_nums_placed}", "board (rows):"]
        for r in self.rows:
            lines.append(str(r))
        return "\n".join(lines)

    def print_pretty(self) -> None:
        """Nicely print only assigned cells; unassigned cells are shown as '*'."""
        out_lines: List[str] = []
        for i, row in enumerate(self.rows):
            if i % 3 == 0:
                out_lines.append(" -------------------------")
            parts: List[str] = []
            for j, cell in enumerate(row):
                sep = " | " if j % 3 == 0 else " "
                parts.append(sep + ("*" if isinstance(cell, list) else str(cell)))
            out_lines.append("".join(parts) + " |")
        out_lines.append(" -------------------------")
        print(f"num_nums_placed: {self.num_nums_placed}\nboard (rows): \n" + "\n".join(out_lines))

    def subgrid_coordinates(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Return coordinates of all cells in the 3x3 box containing (row, col).

        Uses arithmetic to find the top-left of the subgrid, then enumerates the 3x3 block.
        """
        top_r = (row // 3) * 3
        left_c = (col // 3) * 3
        coords: List[Tuple[int, int]] = []
        for dr in range(3):
            for dc in range(3):
                coords.append((top_r + dr, left_c + dc))
        return coords

    def find_most_constrained_cell(self) -> Tuple[int, int]:
        """Return (row, col) for the cell with the fewest candidates.

        If multiple cells tie, the first minimum encountered (scanning rows then columns)
        is returned.
        """
        best_len = 10  # larger than any possible candidate list
        best_r = 0
        best_c = 0
        for r in range(self.size):
            for c in range(self.size):
                cell = self.rows[r][c]
                if isinstance(cell, list):
                    ln = len(cell)
                    if ln < best_len:
                        best_len = ln
                        best_r, best_c = r, c
        return best_r, best_c

    def failure_test(self) -> bool:
        """Return True if any unassigned cell has no candidates (i.e., [])."""
        for row in self.rows:
            for cell in row:
                if cell == []:
                    return True
        return False

    def goal_test(self) -> bool:
        """Return True when the board has been fully assigned."""
        return self.num_nums_placed == self.size * self.size

    def update(self, row: int, column: int, assignment: int) -> None:
        """Place `assignment` at (row, column) and remove it from peers' candidate lists.

        This simplifies a cell to be the integer value and then eliminates that value
        from every other cell in the same row, column and subgrid.
        """
        # set the cell and increment the placed counter
        self.rows[row][column] = assignment
        self.num_nums_placed += 1

        # eliminate from the column
        for r in range(self.size):
            remove_if_exists(self.rows[r][column], assignment)

        # eliminate from the row
        for c in range(self.size):
            remove_if_exists(self.rows[row][c], assignment)

        # eliminate from the subgrid
        for (r, c) in self.subgrid_coordinates(row, column):
            remove_if_exists(self.rows[r][c], assignment)


def DFS(state: Board) -> Board:
    """Depth-first backtracking solver using the most-constrained heuristic."""
    stack = Stack()
    stack.push(state)

    while not stack.is_empty():
        candidate = stack.pop()
        if candidate.goal_test():
            return candidate
        if not candidate.failure_test():
            r, c = candidate.find_most_constrained_cell()
            choices = candidate.rows[r][c]
            # choices will be a list if unassigned; iterate and branch
            for v in choices:
                new_state: Board = copy.deepcopy(candidate)
                new_state.update(r, c, v)
                stack.push(new_state)
    return None


def BFS(state: Board) -> Board:
    """Breadth-first search solver variant (also uses most-constrained branching)."""
    queue = Queue()
    queue.push(state)

    while not queue.is_empty():
        candidate = queue.pop()
        if candidate.goal_test():
            return candidate
        if not candidate.failure_test():
            r, c = candidate.find_most_constrained_cell()
            choices = candidate.rows[r][c]
            for v in choices:
                new_state: Board = copy.deepcopy(candidate)
                new_state.update(r, c, v)
                queue.push(new_state)
    return None


if __name__ == "__main__":
    print("<<<<<<<<<<<<<< Solving Sudoku >>>>>>>>>>>>>>")

    def test_dfs_or_bfs(use_dfs: bool, moves: List[Tuple[int, int, int]]) -> None:
        b = Board()
        for mv in moves:
            b.update(*mv)
        print("<<<<< Initial Board >>>>>")
        b.print_pretty()
        solution = (DFS if use_dfs else BFS)(b)
        print("<<<<< Solved Board >>>>>")
        solution.print_pretty()

    first_moves = [
        (0, 1, 7),
        (0, 7, 1),
        (1, 2, 9),
        (1, 3, 7),
        (1, 5, 4),
        (1, 6, 2),
        (2, 2, 8),
        (2, 3, 9),
        (2, 6, 3),
        (3, 1, 4),
        (3, 2, 3),
        (3, 4, 6),
        (4, 1, 9),
        (4, 3, 1),
        (4, 5, 8),
        (4, 7, 7),
        (5, 4, 2),
        (5, 6, 1),
        (5, 7, 5),
        (6, 2, 4),
        (6, 5, 5),
        (6, 6, 7),
        (7, 2, 7),
        (7, 3, 4),
        (7, 5, 1),
        (7, 6, 9),
        (8, 1, 3),
        (8, 7, 8),
    ]

    second_moves = [
        (0, 1, 2),
        (0, 3, 3),
        (0, 5, 5),
        (0, 7, 4),
        (1, 6, 9),
        (2, 1, 7),
        (2, 4, 4),
        (2, 7, 8),
        (3, 0, 1),
        (3, 2, 7),
        (3, 5, 9),
        (3, 8, 2),
        (4, 1, 9),
        (4, 4, 3),
        (4, 7, 6),
        (5, 0, 6),
        (5, 3, 7),
        (5, 6, 5),
        (5, 8, 8),
        (6, 1, 1),
        (6, 4, 9),
        (6, 7, 2),
        (7, 2, 6),
        (8, 1, 4),
        (8, 3, 8),
        (8, 5, 7),
        (8, 7, 5),
    ]

    # quick tests mirroring the original checks
    b = Board()
    for trip in first_moves:
        b.rows[trip[0]][trip[1]] = trip[2]

    remove_if_exists(b.rows[0][0], 8)
    remove_if_exists(b.rows[0][0], 7)
    remove_if_exists(b.rows[0][0], 3)
    remove_if_exists(b.rows[0][0], 2)
    remove_if_exists(b.rows[4][8], 8)
    remove_if_exists(b.rows[4][8], 1)
    remove_if_exists(b.rows[4][8], 2)
    remove_if_exists(b.rows[4][8], 3)
    remove_if_exists(b.rows[4][8], 4)
    remove_if_exists(b.rows[6][7], 2)
    remove_if_exists(b.rows[6][7], 3)
    remove_if_exists(b.rows[6][7], 5)
    remove_if_exists(b.rows[6][7], 6)

    assert b.find_most_constrained_cell() == (4, 8)
    assert b.failure_test() is False
    assert b.goal_test() is False

    b.rows[4][3] = []
    assert b.find_most_constrained_cell() == (4, 3)
    assert b.failure_test() is True
    print("All part 1 tests passed!")

    g = Board()
    for trip in first_moves:
        g.update(trip[0], trip[1], trip[2])
    g.print_pretty()
    assert g.rows[0][2] == [2, 5, 6]
    assert g.rows[5][5] == [3, 7, 9]
    assert g.num_nums_placed == 28
    assert g.find_most_constrained_cell() == (1, 7)
    assert g.failure_test() is False
    assert g.goal_test() is False
    g.num_nums_placed = 81
    assert g.goal_test() is True
    print("All part 2 tests passed! Testing DFS and BFS next:")

    print("<<<<<<<<<<<<<< Testing DFS on First Game >>>>>>>>>>>>>>")
    test_dfs_or_bfs(True, first_moves)

    print("<<<<<<<<<<<<<< Testing DFS on Second Game >>>>>>>>>>>>>>")
    test_dfs_or_bfs(True, second_moves)

    print("<<<<<<<<<<<<<< Testing BFS on First Game >>>>>>>>>>>>>>")
    test_dfs_or_bfs(False, first_moves)

    print("<<<<<<<<<<<<<< Testing BFS on Second Game >>>>>>>>>>>>>>")
    test_dfs_or_bfs(False, second_moves)