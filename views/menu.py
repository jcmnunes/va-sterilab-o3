import tkinter as tk
from helpers.colors import *
import graphics

graph = graphics.ImaSettings()

# NOTE: To speed-up development the help button was replaced by the
# reset consumables life. However the name in this file was maintained
# as 'help'.


class Winsettings:
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
        self.ima_changepw = tk.PhotoImage(master=self.master, data=graph.changepw)
        self.ima_changepw_push = tk.PhotoImage(master=self.master, data=graph.changepw_push)
        self.ima_help = tk.PhotoImage(master=self.master, data=graph.resetconsum)
        self.ima_help_push = tk.PhotoImage(master=self.master, data=graph.help_push)
        self.ima_params = tk.PhotoImage(master=self.master, data=graph.params)
        self.ima_params_push = tk.PhotoImage(master=self.master, data=graph.params_push)
        self.ima_pub = tk.PhotoImage(master=self.master, data=graph.pub)
        self.ima_pub_push = tk.PhotoImage(master=self.master, data=graph.pub_push)
        self.ima_resettube = tk.PhotoImage(master=self.master, data=graph.resettube)
        self.ima_resettube_push = tk.PhotoImage(master=self.master, data=graph.resettube_push)
        self.ima_stats = tk.PhotoImage(master=self.master, data=graph.stats)
        self.ima_stats_push = tk.PhotoImage(master=self.master, data=graph.stats_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)
        self.lbl_changepw = tk.Label(self.master, image=self.ima_changepw, bd=0)
        self.lbl_params = tk.Label(self.master, image=self.ima_params, bd=0)
        self.lbl_resettube = tk.Label(self.master, image=self.ima_resettube, bd=0)
        self.lbl_help = tk.Label(self.master, image=self.ima_help, bd=0)
        self.lbl_stats = tk.Label(self.master, image=self.ima_stats, bd=0)
        self.lbl_pub = tk.Label(self.master, image=self.ima_pub, bd=0)

        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)
        self.lbl_changepw.place(x=60, y=180)
        self.lbl_params.place(x=60, y=250)
        self.lbl_resettube.place(x=60, y=320)
        self.lbl_help.place(x=438, y=180)
        self.lbl_stats.place(x=438, y=250)
        self.lbl_pub.place(x=438, y=320)

    def inits(self):
        self.binds()

    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)
        self.lbl_changepw.bind('<Button-1>', self.changepass_call)
        self.lbl_params.bind('<Button-1>', self.params_call)
        self.lbl_resettube.bind('<Button-1>', self.resettube_call)
        self.lbl_help.bind('<Button-1>', self.help_call)
        self.lbl_stats.bind('<Button-1>', self.statistics_call)
        self.lbl_pub.bind('<Button-1>', self.pub_call)

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')
        self.lbl_changepw.unbind('<Button-1>')
        self.lbl_params.unbind('<Button-1>')
        self.lbl_resettube.unbind('<Button-1>')
        self.lbl_help.unbind('<Button-1>')
        self.lbl_stats.unbind('<Button-1>')
        self.lbl_pub.unbind('<Button-1>')


    def back_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'home'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.homepanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.homeapp)
        self.master.after(1200, self.clean_up)

    def changepass_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'changepass'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.changepasspanel, self.master, self.lbl_changepw, self.ima_changepw, self.ima_changepw_push, flag, self.constructor.changepassapp)
        self.master.after(1200, self.clean_up)

    def params_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'params'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.paramspanel, self.master, self.lbl_params, self.ima_params, self.ima_params_push, flag, self.constructor.paramsapp)
        self.master.after(1200, self.clean_up)

    def resettube_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'resettube'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.resettubepanel, self.master, self.lbl_resettube, self.ima_resettube, self.ima_resettube_push, flag, self.constructor.resettubeapp)
        self.master.after(1200, self.clean_up)

    def help_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'resetconsum'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.resetconsumpanel, self.master, self.lbl_help, self.ima_help, self.ima_help_push, flag, self.constructor.resetconsumapp)
        self.master.after(1200, self.clean_up)

    def statistics_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'statistics'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.statisticspanel, self.master, self.lbl_stats, self.ima_stats, self.ima_stats_push, flag, self.constructor.statisticsapp)
        self.master.after(1200, self.clean_up)

    def pub_call(self, event):
        if self.constructor.global_focus != 'settings':
            return
        flag = 'pub'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.pubpanel, self.master, self.lbl_pub, self.ima_pub, self.ima_pub_push, flag, self.constructor.pubapp)
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        pass
