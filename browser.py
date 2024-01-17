from URL import *
from HTMLParser import *
from DocumentLayout import *
from PaintTree import *
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
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.display_list = []

    def load(self, url):
        body = url.request()
        self.nodes = HTMLParser(body).parse()
        #print_tree(self.nodes)
        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

    def scrolldown(self, e):
        max_y = max(self.document.height + 2 * VSTEP - HEIGHT, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)
        self.draw()

if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()