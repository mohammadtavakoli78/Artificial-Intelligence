import os
import tkinter
import time

window = tkinter.Tk()


class Visualize():
    def __init__(self, level, solution):
        self.level = level
        self.solution = solution
        self.start = False
        self.time = 0
        self.game_len = len(level)
        if 23 < len(level):
            self.game_len = 23
        self.maze = []

        for i in range(2):
            row = []
            for j in range(self.game_len):
                block = tkinter.Button(window)
                block.config(height=63, width=63)
                block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/_.png"))
                block['image'] = block.image
                block.grid(row=i, column=j)
                row.append(block)
            self.maze.append(row)

    def doGame(self, d = 1):
        if self.time >= self.solution.__len__():
            window.quit()
            return
        self.action = self.solution[self.time]

        for i in range(self.game_len):
            block_t = self.maze[0][i]
            block_b = self.maze[1][i]
            try:
                if self.level[i + self.time] == 'L':
                    block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/L.png"))
                    block_t['image'] = block_t.image
                    block_b.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/_.png"))
                    block_b['image'] = block_b.image
                elif self.level[i + self.time] == 'G':
                    block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/_.png"))
                    block_t['image'] = block_t.image
                    block_b.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/G.png"))
                    block_b['image'] = block_b.image
                else:
                    block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/_.png"))
                    block_t['image'] = block_t.image
                    block_b.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/{self.level[i+self.time]}.png"))
                    block_b['image'] = block_b.image
            except:
                pass

        if self.action == '0':
            block_t = self.maze[1][1]
            block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/P.png"))
            block_t['image'] = block_t.image
        elif self.action == '1':
            block_t = self.maze[0][1]
            block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/P.png"))
            block_t['image'] = block_t.image
        elif self.action == '2':
            block_t = self.maze[1][1]
            block_t.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), f"img/P2.png"))
            block_t['image'] = block_t.image

        self.time += 1
        window.after(84, self.doGame)

    def render(self):
        window.bind("<KeyPress>", self.doGame)
        window.mainloop()
