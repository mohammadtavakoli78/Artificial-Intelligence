import tkinter
import time
from build_tree import *

window = tkinter.Tk()


class Visualize():
    def __init__(self, playground, container, path: list):
        self.playground = playground
        self.container = container
        self.path = path
        self.start = False
        self.maze = [[0] * len(playground[0])] * len(playground)

    def doGame(self,e=1):
        if not self.path:
            exit(0)
        self.action = self.path[0]
        del self.path[0]
        self.container = move(self.playground, self.container, self.action)
        for label in window.grid_slaves():
                label.grid_forget()
        for i in range(len(self.playground)):
            for j in range(len(self.playground[0])):
                block = tkinter.Button(window)
                if self.container['robot'][0][0] == i and self.container['robot'][0][1] == j:
                    block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/r.png"))
                elif self.playground[i][j] == 'x':
                    block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/x.png"))
                elif (i, j) in self.container['destination']:
                    block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/g.png"))
                elif (i, j) in self.container['butters']:
                    block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/b.png"))
                else:
                    block.image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/p.png"))
                block['image'] = block.image
                block.config(height=63, width=63)
                block.grid(row=i, column=j)
        window.after(400, self.doGame)
    def render(self):
        window.bind("<KeyPress>", self.doGame)
        window.mainloop()