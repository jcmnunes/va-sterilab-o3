import tkinter as tk
from helpers.colors import *
import pickle
import graphics

graph = graphics.ImaStatistics()


class Winstatistics:
    def __init__(self, constructor, master, width=848, height=480):

        self.constructor = constructor

        # Attributes
        self.master = master
        self.width = width
        self.height = height
        self.imadir = 'imastatistics'

        # PhotoImage instances
        self.ima_bg = tk.PhotoImage(master=self.master, data=graph.bg)
        self.ima_back = tk.PhotoImage(master=self.master, data=graph.back)
        self.ima_back_push = tk.PhotoImage(master=self.master, data=graph.back_push)

        # Labels
        self.lbl_bg = tk.Label(self.master, image=self.ima_bg, bd=0)
        self.lbl_back = tk.Label(self.master, image=self.ima_back, bd=0)

        # Textboxes

        # Feed pump total operation time
        self.par1 = tk.Frame(self.master, width=70, height=12)
        self.par1.pack_propagate(0) # Don't shrink
        self.par1.place(x=335, y=184)
        self.par1_lbl = tk.Label(self.par1, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par1_lbl.pack(fill=tk.BOTH, expand=1)

        # Feed pump tube life
        self.par2 = tk.Frame(self.master, width=70, height=12)
        self.par2.pack_propagate(0) # Don't shrink
        self.par2.place(x=335, y=203)
        self.par2_lbl = tk.Label(self.par2, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par2_lbl.pack(fill=tk.BOTH, expand=1)

        # Recir pump total operation time
        self.par3 = tk.Frame(self.master, width=70, height=12)
        self.par3.pack_propagate(0) # Don't shrink
        self.par3.place(x=335, y=237)
        self.par3_lbl = tk.Label(self.par3, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par3_lbl.pack(fill=tk.BOTH, expand=1)

        # Outlet pump total operation time
        self.par4 = tk.Frame(self.master, width=70, height=12)
        self.par4.pack_propagate(0) # Don't shrink
        self.par4.place(x=335, y=272)
        self.par4_lbl = tk.Label(self.par4, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par4_lbl.pack(fill=tk.BOTH, expand=1)

        # Outlet pump tube life
        self.par5 = tk.Frame(self.master, width=70, height=12)
        self.par5.pack_propagate(0) # Don't shrink
        self.par5.place(x=335, y=289)
        self.par5_lbl = tk.Label(self.par5, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par5_lbl.pack(fill=tk.BOTH, expand=1)

        # O3 generator total operation time
        self.par6 = tk.Frame(self.master, width=70, height=12)
        self.par6.pack_propagate(0) # Don't shrink
        self.par6.place(x=335, y=325)
        self.par6_lbl = tk.Label(self.par6, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par6_lbl.pack(fill=tk.BOTH, expand=1)

        # UV lamp total operation time
        self.par7 = tk.Frame(self.master, width=70, height=12)
        self.par7.pack_propagate(0) # Don't shrink
        self.par7.place(x=335, y=369)
        self.par7_lbl = tk.Label(self.par7, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par7_lbl.pack(fill=tk.BOTH, expand=1)

        # O3 destructor total operation time
        self.par8 = tk.Frame(self.master, width=70, height=12)
        self.par8.pack_propagate(0) # Don't shrink
        self.par8.place(x=713, y=193)
        self.par8_lbl = tk.Label(self.par8, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par8_lbl.pack(fill=tk.BOTH, expand=1)

        # Number of sterilization cycles
        self.par9 = tk.Frame(self.master, width=70, height=12)
        self.par9.pack_propagate(0) # Don't shrink
        self.par9.place(x=713, y=237)
        self.par9_lbl = tk.Label(self.par9, bg='white', text='',
                                 bd=0, fg=FG_COLOR, anchor=tk.E,
                                 font=('Roboto', 10, 'bold')) # font=FONT_INFO_KW,
        self.par9_lbl.pack(fill=tk.BOTH, expand=1)
        


        # Place
        self.lbl_bg.place(x=0, y=0)
        self.lbl_back.place(x=299, y=430)

        self.inits()

    def inits(self):
        self.par1_txt = self.constructor.db['feedpmp_op_time'][0]
        self.par2_txt = self.constructor.db['feedpmp_tubelife'][0]
        self.par3_txt = self.constructor.db['recirpmp_op_time'][0]
        self.par4_txt = self.constructor.db['outpmp_op_time'][0]
        self.par5_txt = self.constructor.db['outpmp_tubelife'][0]
        self.par6_txt = self.constructor.db['o3_op_time'][0]
        self.par7_txt = self.constructor.db['uv_op_time'][0]
        self.par8_txt = self.constructor.db['o3_dest_op_time'][0]
        self.par9_txt = self.constructor.db['steri_cycles'][0]

        self.par1_lbl['text'] = format(self.par1_txt, '.1f')
        self.par2_lbl['text'] = format(self.par2_txt, '.1f')
        self.par3_lbl['text'] = format(self.par3_txt, '.1f')
        self.par4_lbl['text'] = format(self.par4_txt, '.1f')
        self.par5_lbl['text'] = format(self.par5_txt, '.1f')
        self.par6_lbl['text'] = format(self.par6_txt, '.1f')
        self.par7_lbl['text'] = format(self.par7_txt, '.1f')
        self.par8_lbl['text'] = format(self.par8_txt, '.1f')
        self.par9_lbl['text'] = format(self.par9_txt, '.1f')

    # Bindings
    def binds(self):
        self.lbl_back.bind('<Button-1>', self.back_call)

    def unbinds(self):
        self.lbl_back.unbind('<Button-1>')

    def back_call(self, event):
        if self.constructor.global_focus != 'statistics':
            return
        flag = 'settings'
        self.unbinds()
        self.constructor.anim_btn(0, self.constructor.settingspanel, self.master, self.lbl_back, self.ima_back, self.ima_back_push, flag, self.constructor.settingsapp)
        self.master.after(1200, self.clean_up)

    def clean_up(self):
        pass