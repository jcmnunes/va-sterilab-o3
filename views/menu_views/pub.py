import tkinter as tk
import os
from helpers.colors import *
import pickle
import graphics

graph = graphics.ImaPub()

class Winpub:
    def __init__(self, constructor, master, width=848, height=480):

        self.constructor = constructor

        # Attributes
        self.master = master
        self.width = width
        self.height = height

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_back = tk.PhotoImage(master=self.master, data=graph.back)
        self.ima_back_push = tk.PhotoImage(master=self.master, data=graph.back_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)

        self.inits()

    def inits(self):
        pass

    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')

    def back_call(self, event):
        if self.constructor.global_focus != 'pub':
            return
        flag = 'settings'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        pass