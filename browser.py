from URL import *
from HTMLParser import *
from DocumentLayout import *
from PaintTree import *
from Styles import *
from Tab import *
from KillerChrome import *
import socket
import ssl
import tkinter

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.window.bind("<Down>", self.handle_down)
        self.window.bind("<Button-1>", self.handle_click)
        self.window.bind("<Key>", self.handle_key)
        self.window.bind("<Return>", self.handle_enter)

        self.tabs = []
        self.active_tab = None
        self.focus = None
        self.address_bar = ""
        self.killerChrome = KillerChrome(self)

    def draw(self):
        self.canvas.delete("all")
        self.active_tab.draw(self.canvas, self.killerChrome.bottom)
        for cmd in self.killerChrome.paint():
            cmd.execute(0, self.canvas)

    def handle_click(self, e):
        if e.y < self.killerChrome.bottom:
            self.focus = None
            self.killerChrome.click(e.x, e.y)
        else:
            self.focus = "content"
            self.killerChrome.blur()
            tab_y = e.y - self.killerChrome.bottom
            self.active_tab.click(e.x, tab_y)
        self.draw()

    def handle_down(self, e):
        self.active_tab.scrolldown()
        self.draw()

    def handle_key(self, e):
        if len(e.char) == 0: return
        if not (0x20 <= ord(e.char) < 0x7f): return
        if self.killerChrome.keypress(e.char):
            self.draw()
        elif self.focus == "content": 
            self.active_tab.keypress(e.char)
            self.draw()

    def handle_enter(self, e):
        self.killerChrome.enter()
        self.draw()

    def new_tab(self, url):
        new_tab = Tab(HEIGHT - self.killerChrome.bottom)
        new_tab.load(url)
        self.active_tab = new_tab
        self.tabs.append(new_tab)
        self.draw()


if __name__ == "__main__":
    import sys

    Browser().new_tab(URL(sys.argv[1]))
    tkinter.mainloop()