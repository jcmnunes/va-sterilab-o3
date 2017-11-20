import tkinter as tk
from helpers.colors import *
import graphics

graph = graphics.ImaHome()

class Winhome:
    def __init__(self, constructor, master, width=848, height=480):
        
        # Variables
        self.constructor = constructor
        self.master = master
        self.width = width
        self.height = height

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_auto = tk.PhotoImage(master=self.master, data=graph.auto)
        self.ima_auto_push = tk.PhotoImage(master=self.master, data=graph.auto_push)
        self.ima_man = tk.PhotoImage(master=self.master, data=graph.man)
        self.ima_man_push = tk.PhotoImage(master=self.master, data=graph.man_push)
        self.ima_settings = tk.PhotoImage(master=self.master, data=graph.settings)
        self.ima_settings_push = tk.PhotoImage(master=self.master, data=graph.settings_push)
        self.ima_shut = tk.PhotoImage(master=self.master, data=graph.shut)
        self.ima_shut_push = tk.PhotoImage(master=self.master, data=graph.shut_push)
        self.ima_va = tk.PhotoImage(master=self.master, data=graph.va)
        self.ima_steri = tk.PhotoImage(master=self.master, data=graph.steri)
        self.ima_gema = tk.PhotoImage(master=self.master, data=graph.gema)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_auto = tk.Label(self.master, image=self.ima_auto, bd=0)
        self.lbl_man = tk.Label(self.master, image=self.ima_man, bd=0)
        self.lbl_settings = tk.Label(self.master, image=self.ima_settings, bd=0)
        self.lbl_shut = tk.Label(self.master, image=self.ima_shut, bd=0)
        self.lbl_va = tk.Label(self.master, image=self.ima_va, bd=0)
        self.lbl_steri = tk.Label(self.master, image=self.ima_steri, bd=0)
        self.lbl_gema = tk.Label(self.master, image=self.ima_gema, bd=0)

        # Place Labels
        self.lbl_bg.place(x=0, y=0)
        self.lbl_auto.place(x=454, y=150)
        self.lbl_man.place(x=454, y=225)
        self.lbl_settings.place(x=604, y=327)
        self.lbl_shut.place(x=300, y=430)
        self.lbl_steri.place(x=83, y=129)
        self.lbl_va.place(x=246, y=222)
        self.lbl_gema.place(x=108, y=222)

    def inits(self):
        pass

    def binds(self):
        self.constructor.binds()


if __name__ == '__main__':
    root = tk.Tk()
    app = Winhome(root)
    root.mainloop() 