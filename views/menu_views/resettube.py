import tkinter as tk
from helpers.colors import *
import graphics

graph = graphics.ImaResetTube()

class Winresettube:
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
        self.ima_feed = tk.PhotoImage(master=self.master, data=graph.feed)
        self.ima_feed_push = tk.PhotoImage(master=self.master, data=graph.feed_push)
        self.ima_outlet = tk.PhotoImage(master=self.master, data=graph.outlet)
        self.ima_outlet_push = tk.PhotoImage(master=self.master, data=graph.outlet_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)
        self.lbl_feed = tk.Label(self.master, image=self.ima_feed, bd=0)
        self.lbl_outlet = tk.Label(self.master, image=self.ima_outlet, bd=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)
        self.lbl_feed.place(x=60, y=320)
        self.lbl_outlet.place(x=438, y=320)

    def inits(self):
        self.binds()

    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)
        self.lbl_feed.bind('<Button-1>', self.feed_call)
        self.lbl_outlet.bind('<Button-1>', self.outlet_call)

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')
        self.lbl_feed.unbind('<Button-1>')
        self.lbl_outlet.unbind('<Button-1>')

    def back_call(self, event):
        if self.constructor.global_focus != 'resettube':
            return
        flag = 'settings'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def feed_call(self, event):
        if self.constructor.global_focus != 'resettube':
            return
        self.constructor.anim_pop(event, self.constructor.pop_resettubepanel, self.master, self)
        self.constructor.db['feedpmp_tubelife'][0] = 0
        self.constructor.save_db()

    def outlet_call(self, event):
        if self.constructor.global_focus != 'resettube':
            return
        self.constructor.anim_pop(event, self.constructor.pop_resettubepanelout, self.master, self)
        self.constructor.db['outpmp_tubelife'][0] = 0
        self.constructor.save_db()

    def clean_up(self):
        self.binds()