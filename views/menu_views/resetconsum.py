import tkinter as tk
import os
from helpers.colors import *
import graphics

graph = graphics.ImaResetConsum()



class Winresetconsum:
    def __init__(self, constructor, master, width=848, height=400):

        self.constructor = constructor

        # Attributes
        self.master = master
        self.width = width
        self.height = height
        self.focus = 0

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_back = tk.PhotoImage(master=self.master, data=graph.back)
        self.ima_back_push = tk.PhotoImage(master=self.master, data=graph.back_push)
        self.ima_uv = tk.PhotoImage(master=self.master, data=graph.uv)
        self.ima_uv_push = tk.PhotoImage(master=self.master, data=graph.uv_push)
        self.ima_o3 = tk.PhotoImage(master=self.master, data=graph.o3)
        self.ima_o3_push = tk.PhotoImage(master=self.master, data=graph.o3_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)
        self.lbl_uv = tk.Label(self.master, image=self.ima_uv, bd=0)
        self.lbl_o3 = tk.Label(self.master, image=self.ima_o3, bd=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)
        self.lbl_uv.place(x=60, y=320)
        self.lbl_o3.place(x=438, y=320)

    def inits(self):
        self.binds()

    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)
        self.lbl_uv.bind('<Button-1>', self.uv_call)
        self.lbl_o3.bind('<Button-1>', self.o3_call)

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')
        self.lbl_uv.unbind('<Button-1>')
        self.lbl_o3.unbind('<Button-1>')

    def back_call(self, event):
        if self.constructor.global_focus != 'resetconsum':
            return
        flag = 'settings'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def uv_call(self, event):
        if self.constructor.global_focus != 'resetconsum':
            return
        self.constructor.anim_pop(event, self.constructor.pop_resetconsumpaneluv, self.master, self)
        self.constructor.db['uv_op_time'][0] = 0
        self.constructor.save_db()

    def o3_call(self, event):
        if self.constructor.global_focus != 'resetconsum':
            return
        self.constructor.anim_pop(event, self.constructor.pop_resetconsumpanelo3, self.master, self)
        self.constructor.db['o3_dest_op_time'][0] = 0
        self.constructor.save_db()

    def clean_up(self):
        self.binds()