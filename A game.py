import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

class Puzzle:
    def __init__(self, starting, parent=None):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        inc = 0
        h = 0
        for i in range(3):
            for j in range(3):
                h += abs(inc - self.board[i][j])
                inc += 1
        return h

    def goal(self):
        inc = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != inc:
                    return False
                inc += 1
        return True

    def __eq__(self, other):
        return self.board == other.board

def move_function(curr):
    curr = curr.board
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    if x - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x - 1][y]
        b[x - 1][y] = 0
        succ = Puzzle(b, curr)
        q.append(succ)
    if x + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x + 1][y]
        b[x + 1][y] = 0
        succ = Puzzle(b, curr)
        q.append(succ)
    if y - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x][y - 1]
        b[x][y - 1] = 0
        succ = Puzzle(b, curr)
        q.append(succ)
    if y + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x][y + 1]
        b[x][y + 1] = 0
        succ = Puzzle(b, curr)
        q.append(succ)

    return q

def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if item.f < f:
            f = item.f
            index = i

    return openList[index], index

def AStar(start):
    openList = []
    closedList = []
    openList.append(start)

    while openList:
        current, index = best_fvalue(openList)
        if current.goal():
            return current
        openList.pop(index)
        closedList.append(current)

        X = move_function(current)
        for move in X:
            ok = False   #checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:              #not in closed list
                newG = current.g + 1
                present = False

                #openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    openList.append(move)

    return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")

        self.board_frame = tk.Frame(root)
        self.board_frame.pack()

        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.board_frame, text="", width=5, height=2,
                                               command=lambda x=i, y=j: self.move_button_click(x, y))
                self.buttons[i][j].grid(row=i, column=j)

        self.solve_button = tk.Button(root, text="Solve Puzzle", command=self.solve_puzzle)
        self.solve_button.pack()

        self.reset_button = tk.Button(root, text="Reset Puzzle", command=self.reset_puzzle)
        self.reset_button.pack()

        self.starting_board = [[5, 2, 8], [4, 1, 7], [0, 3, 6]]
        self.current_board = deepcopy(self.starting_board)
        self.update_board()

    def move_button_click(self, x, y):
        if self.current_board[x][y] == 0:
            messagebox.showinfo("Invalid Move", "You cannot move an empty tile.")
        else:
            self.swap_tiles(x, y)

    def swap_tiles(self, x, y):
        empty_x, empty_y = self.find_empty_tile()
        self.current_board[empty_x][empty_y] = self.current_board[x][y]
        self.current_board[x][y] = 0
        self.update_board()

    def find_empty_tile(self):
        for i in range(3):
            for j in range(3):
                if self.current_board[i][j] == 0:
                    return i, j

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.current_board[i][j]))

    def solve_puzzle(self):
        start = Puzzle(self.current_board)
        result = AStar(start)
        if not result:
            messagebox.showinfo("No Solution", "The puzzle has no solution.")
        else:
            self.display_solution(result)

    def display_solution(self, result):
        moves = []
        while result:
            moves.append(result.board)
            result = result.parent

        moves.reverse()

        for move in moves:
            self.current_board = move
            self.update_board()
            self.root.update()
            self.root.after(1000)  # Add a delay (in milliseconds) between moves

    def reset_puzzle(self):
        self.current_board = deepcopy(self.starting_board)
        self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    puzzle_gui = PuzzleGUI(root)
    root.mainloop()
