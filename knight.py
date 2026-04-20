import tkinter as tk
from tkinter import messagebox
import random
import threading

moves = [
    (2,1),(1,2),(-1,2),(-2,1),
    (-2,-1),(-1,-2),(1,-2),(2,-1)
]

# =========================
# Backtracking
# =========================

def count_onward_moves(x, y, board, n):
    count = 0
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0<=nx<n and 0<=ny<n and board[nx][ny]==-1:
            count +=1
    return count

def backtrack_warnsdorff(x, y, move_i, board, n, path):
    if move_i == n*n:
        return True

    next_moves = []
    for dx,dy in moves:
        nx, ny = x+dx, y+dy
        if 0<=nx<n and 0<=ny<n and board[nx][ny]==-1:
            next_moves.append((count_onward_moves(nx, ny, board, n), nx, ny))

    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = move_i
        path.append((nx, ny))
        if backtrack_warnsdorff(nx, ny, move_i+1, board, n, path):
            return True
        board[nx][ny] = -1
        path.pop()
    return False

def solve_backtracking_from(board, path, x, y, n):
    if backtrack_warnsdorff(x, y, len(path), board, n, path):
        return path
    return None

# =========================
# Genetic
# =========================

def generate_individual(n):
    return [random.randint(0,7) for _ in range(n*n)]

def fitness(ind, n):
    x=y=0
    visited={(0,0)}
    for m in ind:
        dx,dy=moves[m]
        x+=dx
        y+=dy
        if not (0<=x<n and 0<=y<n) or (x,y) in visited:
            break
        visited.add((x,y))
    return len(visited)

def crossover(p1,p2):
    point = random.randint(0,len(p1)-1)
    return p1[:point]+p2[point:]

def mutate(ind):
    idx = random.randint(0,len(ind)-1)
    ind[idx] = random.randint(0,7)
    return ind

def genetic_knight(n):
    population=[generate_individual(n) for _ in range(80)]
    for _ in range(200):
        population.sort(key=lambda x:fitness(x,n), reverse=True)
        if fitness(population[0],n)==n*n:
            return population[0]
        new_pop = population[:10]
        while len(new_pop)<80:
            p1,p2 = random.choice(population[:30]), random.choice(population[:30])
            child = crossover(p1,p2)
            if random.random()<0.2:
                child = mutate(child)
            new_pop.append(child)
        population = new_pop
    return population[0]

def genetic_to_path(ind, n, start_x, start_y, visited):
    x, y = start_x, start_y
    path = []

    for m in ind:
        dx, dy = moves[m]
        x += dx
        y += dy
        if not (0 <= x < n and 0 <= y < n) or (x, y) in visited:
            break
        visited.add((x, y))
        path.append((x, y))

    return path

# =========================
# Partial Path 
# =========================

def generate_partial_path(n, k):
    board = [[-1]*n for _ in range(n)]
    x = y = 0
    board[x][y] = 0
    path = [(0,0)]

    for step in range(1, k):
        valid_moves = []
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
                valid_moves.append((nx, ny))

        if not valid_moves:
            break

        valid_moves.sort(key=lambda move: count_onward_moves(move[0], move[1], board, n))
        nx, ny = valid_moves[0]

        board[nx][ny] = step
        path.append((nx, ny))
        x, y = nx, ny

    return board, path, x, y

# =========================
# GUI
# =========================

class KnightGUI:
    def __init__(self, root):
        self.root=root
        root.title("Knight Tour Solver")

        tk.Label(root,text="Board Size (≥5)").pack()
        self.entry=tk.Entry(root)
        self.entry.pack()
        self.entry.insert(0,"8")

        tk.Label(root, text="Pre-moves count").pack()
        self.pre_moves_entry = tk.Entry(root)
        self.pre_moves_entry.pack()
        self.pre_moves_entry.insert(0, "0")

        self.alg=tk.StringVar(value="Backtracking")
        tk.Radiobutton(root,text="Backtracking",
                       variable=self.alg,value="Backtracking").pack()
        tk.Radiobutton(root,text="Genetic",
                       variable=self.alg,value="Genetic").pack()

        tk.Button(root,text="Solve",
                  command=lambda:threading.Thread(target=self.safe_solve).start()).pack(pady=10)

        self.canvas=tk.Canvas(root,width=600,height=600)
        self.canvas.pack()

        self.solving=False
        self.knight=None

    def draw_board(self,n):
        self.canvas.delete("all")
        self.size=600/n
        for i in range(n):
            for j in range(n):
                x1=j*self.size
                y1=i*self.size
                x2=x1+self.size
                y2=y1+self.size
                color="white" if (i+j)%2==0 else "gray"
                self.canvas.create_rectangle(x1,y1,x2,y2,fill=color)

    def draw_pre_moves(self, path):
        for i, (x,y) in enumerate(path):
            self.canvas.create_text(
                y*self.size+self.size/2,
                x*self.size+self.size/2,
                text=str(i+1),
                font=("Arial", int(self.size/3)),
                fill="black"
            )

    def animate_knight(self, path, start_index):
        self.knight_index = start_index
        self.path = path
        self._animate_step()

    def _animate_step(self):
        if self.knight_index >= len(self.path):
            self.solving=False
            return

        x, y = self.path[self.knight_index]

        px = y*self.size+self.size/2
        py = x*self.size+self.size/2

        self.canvas.create_text(
            px, py,
            text=str(self.knight_index+1),
            font=("Arial", int(self.size/3)),
            fill="black"
        )

        if self.knight:
            self.canvas.delete(self.knight)

        self.knight = self.canvas.create_text(
            px, py, text="♞",
            font=("Arial", int(self.size/2)), fill="red"
        )

        self.knight_index += 1
        self.root.after(400, self._animate_step)

    def safe_solve(self):
        if self.solving:
            return
        self.solving=True
        self.solve()

    def solve(self):
        try:
            n = int(self.entry.get())

            k_input = self.pre_moves_entry.get().strip()

            if n > 10:
                n = 10
                messagebox.showinfo(
                    "Limit Applied",
                    "Board size limited to 10 for performance reasons"
                )

            if n < 5:
                raise ValueError("Board size must be ≥ 5")

            max_cells = n * n

            if k_input == "":
                k = random.randint(0, max_cells // 2)

            else:
                k = int(k_input)

                if k < 0:
                    raise ValueError("Pre-moves must be ≥ 0")

                if k >= max_cells:
                    messagebox.showwarning(
                        "Warning",
                        f"Pre-moves too large!\nMax allowed is {max_cells - 1}"
                    )
                    k = max_cells - 1 

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.solving = False
            return

        except:
            messagebox.showerror("Error","Enter valid numbers")
            self.solving=False
            return
        self.draw_board(n)

        board, pre_path, x, y = generate_partial_path(n, k)
        k = len(pre_path) 

        self.draw_pre_moves(pre_path)

        if pre_path:
            x0, y0 = pre_path[-1]
            self.knight = self.canvas.create_text(
                y0*self.size+self.size/2,
                x0*self.size+self.size/2,
                text="♞",
                font=("Arial", int(self.size/2)),
                fill="red"
            )

        if self.alg.get() == "Backtracking":
            if n > 8:
                messagebox.showinfo(
                    "Info",
                    "Backtracking is slow for n > 8\nSwitching to Genetic Algorithm"
                )
                ind = genetic_knight(n)
                visited = set(pre_path)
                visited.add((0,0))
                rest = genetic_to_path(ind, n, x, y, visited)
                full_path = pre_path + rest
            else:
                full_path = solve_backtracking_from(board, pre_path.copy(), x, y, n)

        else:
            ind = genetic_knight(n)
            visited = set(pre_path)
            visited.add((0,0))
            rest = genetic_to_path(ind, n, x, y, visited)
            full_path = pre_path + rest

        if full_path:
            self.animate_knight(full_path, k)  
        else:
            messagebox.showinfo("Result","No solution found")
            self.solving=False


root=tk.Tk()
app=KnightGUI(root)
root.mainloop()